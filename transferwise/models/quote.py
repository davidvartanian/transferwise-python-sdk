from decimal import Decimal

from transferwise.models.base import TFModel


class Quote(TFModel):
    _entity = 'quotes'
    profile = None  # Profile model
    source = None  # currency code
    target = None  # currency code
    rate_type = 'FIXED'
    target_amount = Decimal('0')
    type = None  # BALANCE_PAYOUT, BALANCE_CONVERSION

    def get_account_requirements(self, client):
        return client.get(f'{self._get_path(self.id)}/account-requirements',
                          additional_headers={'Accept-Minor-Version': '1'})
