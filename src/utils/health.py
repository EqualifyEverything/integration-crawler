import os
import requests
from utils.watch import logger


def healthcheck():
    return test_proxy()


def test_proxy():
    logger.info("Testing proxy connection...")

    # Set the proxy settings using environment variables
    use_proxy = os.environ.get('USE_PROXY', 'false').lower() == 'true'
    proxy_http = os.environ.get('PROXY_HTTP')
    proxy_https = os.environ.get('PROXY_HTTPS')
    proxies = {'http': proxy_http, 'https': proxy_https} if use_proxy else None

    test_url = 'http://example.com'

    try:
        response = requests.get(test_url, proxies=proxies)
        logger.info(f"Proxy test response status code: {response.status_code}")
        logger.info(f"Proxy test response headers: {response.headers}")
        logger.info(f"Proxy test response content: {response.content}")
        return True
    except Exception as e:
        logger.error(f"Error testing proxy connection: {e}")
        return False


# Queues to test: launch_crawler, landing_crawler, oops_workers, error_crawler

# RABBIT_USERNAME=worker_crawler
# RABBIT_PASSWORD=explore_the_unknown
# RABBIT_HOST=rabbit
# RABBIT_VHOST=gova11y