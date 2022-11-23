from decimal import Decimal

import requests

from app.core.akash.models.TxMsgData import networkVersion
from app.core.configs.akash import ACTIVE_NODE_API


def get_akash_balance(address: str):
    r = requests.get(f'{ACTIVE_NODE_API}/cosmos/bank/v1beta1/balances/{address}')
    response = r.json()
    akt_amount = next(filter(lambda b: b['denom']=='uakt', response['balances']))['amount']
    return Decimal(akt_amount)


def get_akash_active_certs(address: str):
    r = requests.get(
        f'{ACTIVE_NODE_API}/akash/cert/{networkVersion}/certificates/list?filter.state=valid&filter.owner={address}'
    )
    response = r.json()
    valid_certs = list(filter(lambda cert: cert['certificate']['state'].lower()=='valid', response['certificates']))
    return valid_certs
