from transferwise.models.base import TFModel


class Account(TFModel):
    _entity = 'accounts'
    currency = None  # currency code
    type = None  # sort_code, email
    profile = None  # Profile model
    account_holder_name = None
    legal_type = None  # PRIVATE, BUSINESS
    details = None  # dict of actual recipient details according to country and currency
