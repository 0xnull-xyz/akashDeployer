from pydantic import BaseModel, Field, validator

networkVersion = 'v1beta2'

MSG_CLOSE_DEPLOYMENT = f'/akash.deployment.{networkVersion}.MsgCloseDeployment'
MSG_CREATE_DEPLOYMENT = f'/akash.deployment.{networkVersion}.MsgCreateDeployment'
MSG_DEPOSIT_DEPLOYMENT = f'/akash.deployment.{networkVersion}.MsgDepositDeployment'
MSG_UPDATE_DEPLOYMENT = f'/akash.deployment.{networkVersion}.MsgUpdateDeployment'
MSG_CREATE_LEASE = f'/akash.market.{networkVersion}.MsgCreateLease'
MSG_REVOKE_CERTIFICATE = f'/akash.cert.{networkVersion}.MsgRevokeCertificate'
MSG_CREATE_CERTIFICATE = f'/akash.cert.{networkVersion}.MsgCreateCertificate'


class BaseTxMsgData(BaseModel):
    class Config:
        allow_population_by_field_name = True


class CreateCertificateValue(BaseModel):
    owner: str
    cert: str
    pubkey: str


class CreateCertificate(BaseTxMsgData):
    type_url: str = Field(alias="typeUrl", default=MSG_CREATE_CERTIFICATE)
    value: CreateCertificateValue
