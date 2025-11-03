import os


class GetLogsDetails:
    def __call__(self, log_name):
        current_dir = os.path.dirname(os.path.abspath(__file__))
        base_dir = os.path.abspath(
            os.path.join(current_dir, "..", "..", "assets", "router_logs")
        )
        file_path = os.path.join(base_dir, log_name)

        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Log file not found: {file_path}")

        with open(file_path, "r", encoding="utf-8") as file:
            data = [line.strip() for line in file.readlines()]

        return data[1:] if len(data) > 1 else data
