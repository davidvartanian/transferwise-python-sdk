import base64
import requests
from requests.adapters import HTTPAdapter
from requests.exceptions import ConnectionError
from transferwise.client import config
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
import logging


class Client:
    def __init__(self, api_token, private_key=None, sandbox=True):
        self._api_token = api_token
        if private_key:
            self._private_key = serialization.load_pem_private_key(
                private_key,
                password=None,
                backend=default_backend()
            )
        self._transferwise_adapter = HTTPAdapter(max_retries=5)
        self.api_base_url = config.API_SANDBOX_URL if sandbox else config.API_PRODUCTION_URL
        self.api_version = config.API_VERSION
        self.session = requests.Session()
        self.session.mount(self.api_base_url, self._transferwise_adapter)
        self.logger = logging.getLogger(__name__)

    def get_url(self, path):
        return f'{self.api_base_url}/{path}'

    def get_headers(self):
        return {'Content-Type': 'application/json',
                'Authorization': f'Bearer {self._api_token}'}

    def get_approval_headers(self, approval_token):
        headers = self.get_headers()
        headers.update({
            'x-2fa-approval': approval_token,
            'X-Signature': self._get_approval_signature(approval_token)
        })
        return headers

    def _get_approval_signature(self, approval_token: str):
        signature = self._private_key.sign(
            approval_token,
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH
            ),
            hashes.SHA256()
        )
        return base64.b64encode(signature).decode()

    def _request(self, url, method, headers, params=None, payload: dict = None, try_again=True):
        try:
            response = self.session.request(method, url, params=params, json=payload, headers=headers)
            approval_rejected = response.headers.get('x-2fa-approval-result', None) == 'REJECTED'
            if self._private_key and not response.ok and approval_rejected:
                if not try_again:
                    self.logger.warning(response.json())
                    return response.json()
                approval_token = response.headers.get('x-2fa-approval')
                approval_headers = self.get_approval_headers(approval_token)
                return self._request(url, method, approval_headers, params, payload, try_again=False)
            if not response.ok:
                self.logger.warning(response.json())
            return response.json()
        except ConnectionError as e:
            self.logger.warning(e)

    def get(self, path, additional_headers=None):
        api_url = self.get_url(path)
        headers = self.get_headers()
        if additional_headers:
            headers.update(additional_headers)
        return self._request(api_url, 'GET', headers)

    def post(self, path, payload: dict):
        api_url = self.get_url(path)
        headers = self.get_headers()
        return self._request(api_url, 'POST', headers, payload=payload)
