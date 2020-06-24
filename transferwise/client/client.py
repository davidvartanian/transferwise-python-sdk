import base64

import requests
from Crypto.Hash import SHA256
from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_v1_5
from requests.adapters import HTTPAdapter
from requests.exceptions import ConnectionError
from transferwise.client import config
import logging


class Client:
    def __init__(self, access_token, private_key, sandbox=True):
        self._access_token = access_token
        self._private_key = private_key
        self.api_base_url = config.API_SANDBOX_URL if sandbox else config.API_PRODUCTION_URL
        self.api_version = config.API_VERSION
        self.session = requests.Session()
        self._transferwise_adapter = HTTPAdapter(max_retries=3)
        self.session.mount(self.api_base_url, self._transferwise_adapter)
        self.logger = logging.getLogger(__name__)

    def get_url(self, path):
        return f'{self.api_base_url}/{path}'

    def get_headers(self):
        return {'Content-Type': 'application/json',
                'Authorization': f'Bearer {self._access_token}'}

    def get_approval_headers(self, approval_token):
        headers = self.get_headers()
        headers.update({
            'x-2fa-approval': approval_token,
            'X-Signature': self._get_approval_signature(approval_token)
        })
        return headers

    def _get_approval_signature(self, approval_token: str):
        h = SHA256.new(approval_token.encode())
        pkey = RSA.importKey(self._private_key)
        signature = PKCS1_v1_5.new(pkey).sign(h)
        return base64.b64encode(signature).decode()

    def _request(self, url, method, headers, params=None, payload: dict = None, try_again=True):
        try:
            response = self.session.request(method, url, params=params, json=payload, headers=headers)
            if response.status_code == 403 and response.headers.get('x-2fa-approval-result', None) == 'REJECTED':
                if not try_again:
                    return response
                approval_token = response.headers.get('x-2fa-approval')
                approval_headers = self.get_approval_headers(approval_token)
                return self._request(url, method, approval_headers, params, payload, try_again=False)
            return response.json()
        except ConnectionError as e:
            self.logger.warning(e)

    def get(self, path):
        api_url = self.get_url(path)
        headers = self.get_headers()
        return self._request(api_url, 'GET', headers)

    def post(self, path, payload: dict):
        api_url = self.get_url(path)
        headers = self.get_headers()
        return self._request(api_url, 'POST', headers, payload=payload)
