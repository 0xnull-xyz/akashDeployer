import base64

from app.core.akash.models.TxMsgData import CreateCertificate, MSG_CREATE_CERTIFICATE, CreateCertificateValue
from app.core.akash.utils import generate_certificate


def get_cert_gen_tx_data(address: str, password: str) -> CreateCertificate:
    x509_cert, x509_cert_pem, serialized_public, serialized_private = generate_certificate(address, password)

    msg_dict = {
        'typeUrl': MSG_CREATE_CERTIFICATE,
        'value': {
            'owner': address,
            'cert': base64.b64encode(x509_cert_pem).decode('ascii'),
            'pubkey': base64.b64encode(serialized_public).decode('ascii')
        }
    }

    return CreateCertificate(**msg_dict)
