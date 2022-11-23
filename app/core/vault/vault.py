import hvac

from app.core.configs.config import VAULT_ROOT_TOKEN, VAULT_CLIENT_ADDRESS, VAULT_UNSEAL_KEY


def sample_store():
    create_response = get_hvac_client().secrets.kv.v2.create_or_update_secret(
        path='foo',
        secret=dict(baz='bar'), )
    print('xexue#$yiub')


def sample_read():
    read_response = get_hvac_client().secrets.kv.read_secret_version(path='foo')
    print('xexue#$yiub')


def get_hvac_client():
    client = hvac.Client(url=VAULT_CLIENT_ADDRESS, token=VAULT_ROOT_TOKEN)
    if client.sys.is_sealed():
        unseal_response1 = client.sys.submit_unseal_key(VAULT_UNSEAL_KEY)
    return client
