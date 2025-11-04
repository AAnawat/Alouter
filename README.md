# Alouter

A distributed network router monitoring and management system for the IPA2025 project. Alouter provides real-time monitoring of router interfaces, performance metrics, and log collection through a microservices architecture.

## Project Documentation

📋 **[IPA Project 2025 - Notion Documentation](https://www.notion.so/IPA-Project-2025-29af4ff1255280b4b4f4d20d2602fd7a?source=copy_link)**

## Features

-   **Real-time Router Monitoring**: Automated collection of interface status and performance data
-   **Log Management**: Centralized router log collection and storage
-   **Web Dashboard**: Flask-based interface for viewing router metrics and data
-   **Scalable Architecture**: Microservices design with Docker containerization
-   **Message Queue Processing**: Asynchronous task handling with RabbitMQ
-   **Persistent Storage**: MongoDB for router credentials and collected data

## Architecture

The system consists of three main services:

-   **Website**: Flask web application providing the user interface and API
-   **Scheduler**: Periodic task scheduler that triggers data collection jobs
-   **Worker**: Background service that connects to routers via Ansible to collect data

## Quick Start

### Prerequisites

-   Docker and Docker Compose
-   Git

### Installation

1. Clone the repository:

```bash
git clone <repository-url>
cd alouter
```

2. Set up environment variables:

```bash
cp .env.example .env
# Edit .env with your MongoDB and RabbitMQ credentials
```

3. Start all services:

```bash
docker-compose up -d
```

4. Access the web interface at `http://localhost:8080`

### Service URLs

-   **Web Interface**: http://localhost:8080
-   **RabbitMQ Management**: http://localhost:15672
-   **MongoDB**: localhost:27017

## Development

### Project Structure

```
alouter/
├── website/              # Flask web application
├── scheduler/            # Task scheduling service
├── worker/              # Background processing service
├── manifests/           # Kubernetes deployment files
├── nfs/                 # Shared storage for router logs
└── docker-compose.yaml  # Service orchestration
```

### Running Individual Services

```bash
# Start specific service
docker-compose up website

# Build and start with logs
docker-compose up --build scheduler

# View service logs
docker-compose logs -f worker
```

## Configuration

### Environment Variables

Create `.env` file in the root directory:

```env
MONGO_INITDB_ROOT_USERNAME=your_mongo_user
MONGO_INITDB_ROOT_PASSWORD=your_mongo_password
RABBITMQ_DEFAULT_USER=your_rabbitmq_user
RABBITMQ_DEFAULT_PASS=your_rabbitmq_password
```

Each service also has its own `.env` file for service-specific configuration.

### Router Credentials

Router credentials are stored in the MongoDB `credential` collection. Add router information through the web interface or directly in the database.

## Data Collection

The system collects three types of data from routers:

1. **Interface Data**: Network interface status and configuration
2. **Performance Metrics**: Router performance statistics
3. **Log Files**: Router system and application logs

Data collection frequency:

-   Interface and Performance: Every 30 seconds
-   Logs: Every 2 minutes (every 4th cycle)
