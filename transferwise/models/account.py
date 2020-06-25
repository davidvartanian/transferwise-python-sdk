import re
from transferwise.models.base import TFModel
from transferwise.utils import snakecase


class Account(TFModel):
    _entity = 'accounts'
    currency = None  # currency code
    type = None  # sort_code, email
    profile = None  # Profile model
    account_holder_name = None
    owned_by_customer = False
    details = {}  # dict of actual recipient details according to country and currency

    def verify(self, account_requirements: list):
        errors = []
        for req in account_requirements:
            if req['type'] != self.type:
                continue
            for field in req['fields']:
                for group in field['group']:
                    self._validate_group(group, errors)
        return errors
