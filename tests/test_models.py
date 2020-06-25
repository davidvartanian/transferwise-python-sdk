import random
import unittest
from transferwise.models import Account, Fund, Profile, Quote, Transfer


class AccountTest(unittest.TestCase):
    def setUp(self) -> None:
        self.account = Account()

    def test_account_instance_from_dict(self):
        self.assertIsInstance(Account.create_from_dict({'currency': 'EUR',
                                                        'type': 'BUSINESS'}), Account)

    def test_sync_data_accessible_as_attribute(self):
        self.account._sync['test_attr'] = 'value'
        self.assertEqual(self.account.test_attr, 'value')

    def test_to_json_is_serializable(self):
        self.account.profile = Profile.create_from_dict({'type': 'personal', 'details': {}})
        self.account.profile.id = random.randint(1, 100000)
        obj = self.account.to_json()
        self.assertEqual(obj['profile'], self.account.profile.id)
        self.assertIsInstance(obj, dict)


class FundTest(unittest.TestCase):
    def setUp(self) -> None:
        self.fund = Fund()

    def test_fund_instance_from_dict(self):
        self.assertIsInstance(Fund.create_from_dict({'currency': 'EUR',
                                                     'type': 'BUSINESS'}), Fund)

    def test_sync_data_accessible_as_attribute(self):
        self.fund._sync['test_attr'] = 'value'
        self.assertEqual(self.fund.test_attr, 'value')

    def test_to_json_is_serializable(self):
        self.fund.profile = Profile.create_from_dict({'type': 'personal', 'details': {}})
        self.fund.profile.id = random.randint(1, 100000)
        obj = self.fund.to_json()
        self.assertEqual(obj['profile'], self.fund.profile.id)
        self.assertIsInstance(obj, dict)


class ProfileTest(unittest.TestCase):
    def setUp(self) -> None:
        self.profile = Profile()

    def test_profile_instance_from_dict(self):
        self.assertIsInstance(Profile.create_from_dict({'currency': 'EUR',
                                                        'type': 'BUSINESS'}), Profile)

    def test_sync_data_accessible_as_attribute(self):
        self.profile._sync['test_attr'] = 'value'
        self.assertEqual(self.profile.test_attr, 'value')

    def test_to_json_is_serializable(self):
        obj = self.profile.to_json()
        self.assertIsInstance(obj, dict)


class QuoteTest(unittest.TestCase):
    def setUp(self) -> None:
        self.quote = Quote()

    def test_quote_instance_from_dict(self):
        self.assertIsInstance(Quote.create_from_dict({'currency': 'EUR',
                                                      'type': 'BUSINESS'}), Quote)

    def test_sync_data_accessible_as_attribute(self):
        self.quote._sync['test_attr'] = 'value'
        self.assertEqual(self.quote.test_attr, 'value')

    def test_to_json_is_serializable(self):
        self.quote.profile = Profile.create_from_dict({'type': 'personal', 'details': {}})
        self.quote.profile.id = random.randint(1, 100000)
        obj = self.quote.to_json()
        self.assertEqual(obj['profile'], self.quote.profile.id)
        self.assertIsInstance(obj, dict)


class TransferTest(unittest.TestCase):
    def setUp(self) -> None:
        self.transfer = Transfer()

    def test_transfer_instance_from_dict(self):
        self.assertIsInstance(Transfer.create_from_dict({'currency': 'EUR',
                                                         'type': 'BUSINESS'}), Transfer)

    def test_sync_data_accessible_as_attribute(self):
        self.transfer._sync['test_attr'] = 'value'
        self.assertEqual(self.transfer.test_attr, 'value')

    def test_to_json_is_serializable(self):
        self.transfer.account = Account.create_from_dict({'type': 'personal'})
        self.transfer.account.id = random.randint(1, 100000)
        obj = self.transfer.to_json()
        self.assertEqual(obj['account'], self.transfer.account.id)
        self.assertIsInstance(obj, dict)
