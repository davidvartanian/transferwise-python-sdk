# TransferWise Python SDK
An unofficial Python SDK to facilitate the use of the TransferWise API.

[![Build Status](https://travis-ci.org/davidvartanian/transferwise-python-sdk.svg?branch=master)](https://travis-ci.org/davidvartanian/transferwise-python-sdk)

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


api_token = os.environ.get('TRANSFERWISE_API_TOKEN')
private_key = os.environ.get('TRANSFERWISE_PRIVATE_KEY')
client = Client(api_token, private_key, sandbox=True)

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
    'type': 'BALANCE'
})
fund.post(client, profile_id=profile._sync.id, transfer_id=transfer._sync.id)

```

## Model Architecture
Whenever the model is sent to the API as payload, the response populates the `_sync` attribute, which is a dictionary.

Thanks to `__getattribute__` magic method, properties coming from the API are available as instance attributes, e.g.: `obj.id` (where `id` is actually in `obj._sync['id']`). This way reading attributes you get the synced version from the server if exists, otherwise the local attribute is returned. In case you want to access the local attribute easily, there's also an `attr` method.

Models have also a class method `get` with an optional `id` parameter. When `id` isn't specified, a list of object will be returned.

In order to interact with the client, models are able to generate their own API paths through the protected method `_get_path`.

# Client Architecture
The client is very simple. To instance it, it needs your API token.

The `get` and `post` methods accept a path and extra parameters to build and submit a request to the API

Requests are made via the `requests` package using a `Session` instance with a custom `HTTPAdapter`, making possible to add retries if needed.
