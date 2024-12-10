"""
api.py will have :
- APIClient class
- get method
- post method
- get_with_auth method

this module is needed for:
- making http requests
- handling http errors
- handling http retries
- handling http timeouts
- handling http caching
- handling http authentication
- handling http headers

"""

import requests
import logging
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from cachetools import cached, TTLCache

logger = logging.getLogger(__name__)


class APIClient:
    def __init__(self, base_url, headers=None):
        self.base_url = base_url
        self.headers = headers
        self.session = requests.Session()
        self.session.headers.update(headers or {})
        retries = Retry(total=5, backoff_factor=1, status_forcelist=[504, 500, 502, 429, 503])
        self.session.mount('http://', HTTPAdapter(max_retries=retries))
        self.session.mount('https://', HTTPAdapter(max_retries=retries))
        self.cache = TTLCache(maxsize=100, ttl=300)
        self.cache_enabled = True
        
        
    @cached(cache=lambda self: self.cache)
    def get(self, endpoint, params=None):
        url = f"{self.base_url}{endpoint}"
        logger.info(f"making GET request to {url}")
        try:
            response = self.session.get(url, params=params)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.HTTPError as e:
            logger.error(f"HTTP error occurred: {e}")
            raise
    def post(self, endpoint, data=None):
        url = f"{self.base_url}{endpoint}"
        logger.info(f"making POST request to {url}")
        try:
            response = self.session.post(url, json=data)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.HTTPError as e:
            logger.error(f"Post request failed: {e}")
            raise
        
    def get_with_auth(self, endpoint, token, params=None):
        headers = {
            "Authorization": f"Bearer {token}"
            }
        self.session.headers.update(headers)
        return self.get(endpoint, params=params)
    