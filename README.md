# A11yCrawler Adventure 🌐🐾
Welcome to the A11yCrawler Adventure! This repo focuses on web scraping, crawling, and processing. It extracts links from web pages and sends them to the RabbitMQ for further processing within the EqualifyApp ecosystem.
[![🏗️📤 Build and publish 🐳 images](https://github.com/EqualifyApp/integration-crawler/actions/workflows/containerize.yml/badge.svg)](https://github.com/EqualifyApp/integration-crawler/actions/workflows/containerize.yml)


## How It Works

This repo contains a scraper that extracts links from websites and sends these links to dedicated RabbitMQ queues, waiting for further processing. Links to be crawled are read from the `launch_crawler` RabbitMQ queue.

## Getting Started

To start your A11yCrawler Adventure, jump right in by deploying the container! 🎉

| Env Var | Default | Options | Notes |
|-----------|-----------|-----------|-----------|
| APP_PORT     | 8083     | Any port number     | Doesn't need to be exposed if not using api endpoint     |

### Deploy the Let's Go Stack
The ecosystem can be deployed via a simple docker compose - more info here https://github.com/EqualifyApp/lets-go

### Deploy Stand Alone Container 🐳

Get the standalone container from Docker Hub and unleash the power of the A11yCrawler!

```bash
docker pull equalifyapp/a11y-crawler-adventure:latest
docker run --name a11y-crawler-adventure -p 8086:8086 equalifyapp/a11y-crawler-adventure:latest
```

## Repo Summary
This quick guide will walk you through some of the core components of the A11yCrawler Adventure repo:

- **Dockerfile:** The recipe that dictates how the Docker image is prepared 🍲
- **src:** The source folder, where our crawling story unfolds 📚
    - **main.py:** The main script that coordinates the crawling escapade 🎬
    - **utils:** A utility folder containing helpful scripts and tools 🛠️
        - **auth.py:** Handles RabbitMQ communication and message processing 🐇
        - **scrape.py:** Manages web scraping and link processing 🔗
        - **watch.py:** Configures and manages logging 🪵

### A File-by-File Breakdown

#### Dockerfile 🍲
This Dockerfile sets up the Python image, installs essential tools such as `wget` and `curl`, configures the working directory, and installs necessary packages from the [requirements.txt](requirements.txt) file. Then, it defines the `APP_PORT` environment variable and sets a health check. Finally, it runs [src/main.py](src/main.py) to kick off the action.

#### src/main.py 🎬
This main script listens to RabbitMQ messages in the `launch_crawler` queue and processes incoming messages using the `check_queue` function. It calls the `process_message` function found in [src/utils/scrape.py](src/utils/scrape.py).

#### src/utils/auth.py 🔐
This file helps our noble crawler communicate with RabbitMQ. It contains two primary functions, rabbit for sending messages to RabbitMQ and `catch_rabbits` for consuming messages from the queue.

#### src/utils/scrape.py 🔍
Our fearless web scraper tackles the real challenge here! This file has a set of functions for web scraping, link processing, and RabbitMQ message handling. The process_message function reads a message, then scrapes and processes links, sending the results to the `landing_crawler` and `error_crawler` queues.

#### src/utils/watch.py 🪵
`watch.py` configures the logger for the entire adventure. It provides a unified logging system for A11yCrawler Adventure, keeping an eye on everything that happens behind the scenes!


### License
This repo is under the GPL-3.0 License. In a nutshell, this means you're free to use, modify, and distribute this software as long as you follow the requirements specified in the LICENSE file. You can find it here: [LICENSE](LICENSE)

## Happy A11yCrawler Adventuring! 🌐🐾🎉