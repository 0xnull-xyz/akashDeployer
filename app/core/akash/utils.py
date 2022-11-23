from datetime import datetime, timedelta

from cryptography import x509
from cryptography.exceptions import InvalidSignature
from cryptography.hazmat._oid import NameOID
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import ec


def generate_key_pair_ec_secp256r1():
    private_key = ec.generate_private_key(ec.SECP256R1(), default_backend())
    public_key = private_key.public_key()
    return private_key, public_key


def generate_certificate(address: str, password: str):
    s_date = datetime.now()
    n2_date = datetime.now()

    # first we generate a key pair
    priv_key, pub_key = generate_key_pair_ec_secp256r1()

    serialized_private = priv_key.private_bytes(encoding=serialization.Encoding.PEM,
                                                format=serialization.PrivateFormat.PKCS8,
                                                encryption_algorithm=serialization.BestAvailableEncryption(
                                                    bytes(password, 'utf-8')))
    serialized_public = pub_key.public_bytes(encoding=serialization.Encoding.PEM,
                                             format=serialization.PublicFormat.SubjectPublicKeyInfo).replace(
        b"PUBLIC KEY", b"EC PUBLIC KEY")

    # Create x509v3 cert
    issuer = x509.Name(
        [x509.NameAttribute(NameOID.COMMON_NAME, address)]
    )
    x509_cert = x509.CertificateBuilder().subject_name(issuer).issuer_name(issuer).public_key(pub_key).serial_number(
        x509.random_serial_number()).not_valid_before(datetime.utcnow()).not_valid_after(
        datetime.utcnow() + timedelta(days=365)).add_extension(
        x509.KeyUsage(False, False, True, True, False, False, False, False, False),
        critical=True
    ).add_extension(
        x509.ExtendedKeyUsage([x509.oid.ExtendedKeyUsageOID.CLIENT_AUTH]), critical=True
    ).add_extension(
        x509.BasicConstraints(True, None), critical=True
    ).sign(
        priv_key,
        hashes.SHA256()  # I suspect this -> SHA256withECDSA?
    )

    x509_cert_pem = x509_cert.public_bytes(encoding=serialization.Encoding.PEM)

    return x509_cert, x509_cert_pem, serialized_public, serialized_private


def ver_key_pair_ec_secp256r1():
    private_value = 0x63bd3b01c5ce749d87f5f7481232a93540acdb0f7b5c014ecd9cd32b041d6f33
    curve = ec.SECP256R1()
    signature_algorithm = ec.ECDSA(hashes.SHA256())

    # Make private and public keys from the private value + curve
    priv_key = ec.derive_private_key(private_value, curve, default_backend())
    pub_key = priv_key.public_key()
    print('Private key: 0x%x' % priv_key.private_numbers().private_value)
    print('Public point (Uncompressed): 0x%s' % pub_key.public_bytes(serialization.Encoding.X962,
                                                                     serialization.PublicFormat.UncompressedPoint).hex())

    # Sign some data
    data = b"this is some data to sign"
    signature = priv_key.sign(data, signature_algorithm)
    print('Signature: 0x%s' % signature.hex())

    # Verify
    try:
        pub_key.verify(signature, data, signature_algorithm)
        print('Verification OK')
    except InvalidSignature:
        print('Verification failed')
