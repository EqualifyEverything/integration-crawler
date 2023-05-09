import os
import time
import json
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from utils.watch import logger
from utils.auth import rabbit


def clean_url(url):
    url = url.split('#')[0]
    url = url.split('?')[0]
    return url


def is_valid_url(url):
    return not (url.startswith('mailto:') or url.startswith('tel:'))


def scrape_url(url_id, url):
    logger.debug(f'🌟 Starting to process: {url}')

    # Set the proxy settings using environment variables
    use_proxy = os.environ.get('USE_PROXY', 'false').lower() == 'true'
    logger.debug(f'USE_PROXY: {use_proxy} ')
    proxy_http = os.environ.get('PROXY_HTTP')
    if proxy_http:
        proxy_http = f'http://{proxy_http}'
    logger.debug(f'PROXY_HTTP: {proxy_http}')
    proxy_https = os.environ.get('PROXY_HTTPS')
    if proxy_https:
        proxy_https = f'https://{proxy_https}'
    logger.debug(f'PROXY_HTTPS: {proxy_https} ')
    proxies = {'http': proxy_http, 'https': proxy_https} if use_proxy else None
    logger.debug(f'Proxies: {proxies} ')

    response = requests.get(url, proxies=proxies)
    soup = BeautifulSoup(response.content, 'html.parser')

    # Extract and clean all URLs from the web page
    raw_links = [a['href'] for a in soup.find_all('a', href=True)]
    cleaned_links = [clean_url(urljoin(url, raw_link)) for raw_link in raw_links if is_valid_url(raw_link)]

    # Deduplicate URLs
    deduplicated_links = list(set(cleaned_links))

    # TODO: Process the urls?

    return deduplicated_links


def send_to_queue(queue_name, message):
    rabbit(queue_name, message)
    logger.info(f'📤 Sent to {queue_name} queue: {message}')


def process_message(channel, method, properties, body):
    url = None
    url_id = None
    try:
        payload = json.loads(body)
        url = payload.get('url')
        url_id = payload.get('url_id')
        logger.debug(f'🔍 Payload received: {payload}')

        deduplicated_links = scrape_url(url_id, url)
        logger.debug(f'🔗 Deduplicated links: {deduplicated_links}')

        # Create a list of dictionaries with source_url_id and url
        deduplicated_links_list = [{"source_url_id": url_id, "url": deduplicated_url} for deduplicated_url in deduplicated_links]

        # Convert the list to a JSON string
        message = json.dumps(deduplicated_links_list)

        # Send the JSON array as a single message to the landing_crawler queue
        send_to_queue("landing_crawler", message)

        channel.basic_ack(delivery_tag=method.delivery_tag)
        logger.debug(f'✅ Successfully processed: {url}')
    except Exception as e:
        error_message = f"❌ Failed to process {url}: {e}"
        logger.error(error_message)
        time.sleep(15)  # Pause for 15 seconds
        channel.basic_nack(delivery_tag=method.delivery_tag)

        # Send a message to the error_crawler queue with url_id, url, and error_message
        error_payload = json.dumps({
            "url_id": url_id,
            "url": url,
            "error_message": error_message
        })
        send_to_queue("error_crawler", error_payload)

