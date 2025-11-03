import subprocess
import time
import re
import os

from pprint import pprint


def run_ansible_playbook(playbook, router_info):
    extra_vars = (
        f"router_ip={router_info['host']} "
        f"router_user={router_info['username']} "
        f"router_pass={router_info['password']} "
        f"file_name={router_info['name']}-{time.strftime('%Y%m%d-%H%M%S')}.log"
    )

    command = [
        "ansible-playbook",
        "--ssh-common-args",
        "-o KexAlgorithms=+diffie-hellman-group14-sha1",
        "--extra-vars",
        extra_vars,
        f"./playbooks/{playbook}",
    ]

    result = subprocess.run(command, capture_output=True, text=True, cwd="./ansible")
    result = result.stdout

    return result


def get_log(host, username, password, router_name):
    router_info = {
        "host": host,
        "username": username,
        "password": password,
        "name": router_name,
    }
    output = run_ansible_playbook("query_log.yml", router_info)

    if not ("failed=0" in output):
        raise Exception("Failed to get performance data")

    filename = re.findall('"msg": "(.*)"', output)

    with open(f"./router_logs/{filename[0]}", "r") as file:
        log_content = file.read().splitlines()
        if len(log_content) == 3:
            os.remove(f"./router_logs/{filename[0]}")
            return ""

    return filename[0]


def get_interface(host, username, password, router_name):
    router_info = {
        "host": host,
        "username": username,
        "password": password,
        "name": router_name,
    }
    output = run_ansible_playbook("query_interface.yml", router_info)

    if not ("failed=0" in output):
        raise Exception("Failed to get performance data")

    content = re.findall('"msg": "(.*)"', output)[0]
    content = content.split("\\n")[1:]

    regex = r"^(\S+)\s+(\S+)\s+(\S+)\s+(\S+)\s+(.*?)\s+(\S+)$"
    interface = []
    for line in content:
        line = line.strip()
        match = re.match(regex, line)
        if match:
            interface.append(
                {
                    "interface": match.group(1),
                    "ip_address": match.group(2),
                    "ok?": match.group(3),
                    "method": match.group(4),
                    "status": match.group(5),
                    "protocol": match.group(6),
                }
            )

    return interface


def get_performance(host, username, password, router_name):
    router_info = {
        "host": host,
        "username": username,
        "password": password,
        "name": router_name,
    }
    output = run_ansible_playbook("query_performance.yml", router_info)

    if not ("failed=0" in output):
        raise Exception("Failed to get performance data")

    content = re.findall('"msg": "(.*)"', output)
    cpu = content[0]
    memory = content[1].split("\\n")

    cpu_percent = re.findall(r"(\d+%)", cpu)
    cpu = {"total": cpu_percent[0], "interrupt": cpu_percent[1]}

    mem = {}
    for line in memory:
        line = line.strip()
        mem_percent = re.match(
            r"(.+) Pool Total:\s+(\d+) Used:\s+(\d+) Free:\s+(\d+)", line
        )
        if mem_percent:
            mem[mem_percent.group(1)] = {
                "total": mem_percent.group(2),
                "used": mem_percent.group(3),
                "free": mem_percent.group(4),
            }

    performance = {"cpu": cpu, "memory": mem}
    return performance


if __name__ == "__main__":
    pprint(get_performance("10.2.17.21", "admin", "cisco", "Router1"))
