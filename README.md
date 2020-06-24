# TransferWise Python SDK
An unofficial Python SDK to facilitate the use of the TransferWise API.

## Installation
```bash
$ pip install transferwise-python-sdk
```

## Usage
```python
import os
import uuid
from decimal import Decimal
from transferwise.client import Client
from transferwise.models import (
    Account,
    Profile,
    Quote,
    Transfer,
    TransferRequirements,
    Fund
)


access_token = os.environ.get('TRANSFERWISE_ACCESS_TOKEN')
private_key = os.environ.get('TRANSFERWISE_PRIVATE_KEY')
client = Client(access_token, private_key, sandbox=True)

# get profile
profile = Profile.get(client)

# create quote
quote = Quote.create_from_dict({
    'profile': profile,
    'source': 'EUR',
    'target': 'EUR',
    'target_amount': Decimal('1000')
})

# quote is updated with server response
quote.post(client)  

# validate account requirements
account_requirements = quote.get_account_requirements(client)

# create account
account = Account.create_from_dict({
    'currency': 'EUR',
    'type': 'sort_code',
    'profile': profile,
    'account_holder_name': 'The Dude Inc.',
    'legal_type': 'BUSINESS',
    'details': {
        'legalType': 'BUSINESS',
        'iban': 'DE51700111106050000891'
    }
})

# verify recipient account
account.verify(account_requirements)  # proceed if there are no errors

# account is updated with server response
account.post(client)

# create transfer
transaction_id = uuid.uuid4()  # required for request idempotency
transfer_reference = 'Order XXX reference'
source_of_funds = 'verification.source.of.funds.other'
transfer = Transfer.create_from_dict({
    'target_account': account,
    'quote': quote,
    'customer_transaction_id': transaction_id,
    'details': {
        'reference': transfer_reference,
        'transfer_purpose': 'verification.transfers.purpose.pay.bills',
        'source_of_funds': source_of_funds
    }
})

# transfer requirements
transfer_requirements = TransferRequirements.create_from_dict({
    'target_account': account,
    'quote': quote,
    'details': {
        'reference': transfer_reference,
        'source_of_funds': source_of_funds,
        'source_of_funds_other': 'Trust funds'
    },
    'customer_transaction_id': transaction_id
})

transfer_requirements.post(client)
transfer.verify(transfer_requirements)
transfer.post(client)

# fund transfer
fund = Fund.create_from_dict({
    'profile': profile,
    'transfer': transfer,
    'type': 'BALANCE'
})
fund.post(client)

```
