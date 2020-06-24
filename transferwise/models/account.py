import re
from transferwise.models.base import TFModel


class Account(TFModel):
    _entity = 'accounts'
    currency = None  # currency code
    type = None  # sort_code, email
    profile = None  # Profile model
    account_holder_name = None
    legal_type = None  # PRIVATE, BUSINESS
    owned_by_customer = False
    details = {}  # dict of actual recipient details according to country and currency

    def verify(self, account_requirements: list):
        errors = []
        for req in account_requirements:
            if req['type'] != self.type:
                continue
            for field in req['fields']:
                for group in field['group']:
                    value = self.details.get(group['key'], None)
                    if group['required'] and not value:
                        errors.append(group)
                    elif not group['required'] and not value:
                        continue
                    if group['validationRegexp']:
                        match = re.match(r'^[A-Z]{2}[a-zA-Z0-9 ]{12,40}$', value)
                        if not match:
                            errors.append(group)
                    if group['minLength'] and len(value) < group['minLength']:
                        errors.append(group)
                    if group['maxLength'] and len(value) > group['maxLength']:
                        errors.append(group)
                    if group['valuesAllowed']:
                        if value not in [v['key'] for v in group['valuesAllowed']]:
                            errors.append(group)
        return errors
