import base64
import unittest
import uuid
from cryptography.hazmat.backends.openssl.rsa import _RSAPrivateKey
from transferwise.client import Client
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding


class ClientTest(unittest.TestCase):
    def setUp(self) -> None:
        self.api_token = uuid.uuid4()
        self.key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=2048,
            backend=default_backend()
        )
        self.private_key = self.key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.TraditionalOpenSSL,
            encryption_algorithm=serialization.NoEncryption()
        )
        self.pubkey = self.key.public_key()
        self.public_key = self.pubkey.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        )

    def test_client_without_private_key(self):
        client = Client(self.api_token)
        self.assertIsInstance(client, Client)

    def test_client_with_private_key(self):
        client = Client(self.api_token, self.private_key)
        self.assertIsInstance(client, Client)
        self.assertIsInstance(client._private_key, _RSAPrivateKey)

    def test_client_signs_approval_token(self):
        client = Client(self.api_token, self.private_key)
        approval_token = uuid.uuid4().bytes
        approval_headers = client.get_approval_headers(approval_token)
        self.assertEqual(approval_headers['x-2fa-approval'], approval_token)
        encoded_signature = approval_headers['X-Signature']
        signature = base64.b64decode(encoded_signature)
        self.pubkey.verify(
            signature,
            approval_token,
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH
            ),
            hashes.SHA256()
        )

    def test_approval_headers_include_api_token(self):
        client = Client(self.api_token, self.private_key)
        approval_token = uuid.uuid4().bytes
        approval_headers = client.get_approval_headers(approval_token)
        self.assertEqual(approval_headers['Authorization'], f'Bearer {self.api_token}')
