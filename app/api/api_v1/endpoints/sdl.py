import json

import yaml
from fastapi import APIRouter
from starlette.responses import JSONResponse

from app.core.akash.models.TxMsgData import CreateCertificate
from app.core.akash.query import get_akash_balance, get_akash_active_certs
from app.core.akash.tx import get_cert_gen_tx_data
from app.core.akash.utils import generate_certificate
from app.core.deployers.deployer import BaseDeployer
from app.core.vault.vault import sample_store, sample_read
from app.models.stack_definition import SDLModel

router = APIRouter()


@router.post("/sdl/teplate/verify", response_model=bool, tags=["sdl"])
async def verify_sdl(
        tag: str,
):
    with open('tests/testdata/simple.yaml', 'r') as file:
        prime_service = yaml.safe_load(file)

    x = json.dumps(prime_service)
    y = SDLModel(**prime_service)

    with open('tests/testdata/simple2.yaml', 'r') as file:
        prime_service = yaml.safe_load(file)

    x = json.dumps(prime_service)
    y = SDLModel(**prime_service)

    with open('tests/testdata/private_service.yaml', 'r') as file:
        prime_service = yaml.safe_load(file)

    x = json.dumps(prime_service)
    y = SDLModel(**prime_service)

    with open('tests/testdata/simple-double-ram.yaml', 'r') as file:
        prime_service = yaml.safe_load(file)

    x = json.dumps(prime_service)
    y = SDLModel(**prime_service)

    with open('tests/testdata/storageClass4.yaml', 'r') as file:
        prime_service = yaml.safe_load(file)

    x = json.dumps(prime_service)
    y = SDLModel(**prime_service)

    with open('tests/testdata/profile-svc-name-mismatch.yaml', 'r') as file:
        prime_service = yaml.safe_load(file)

    x = json.dumps(prime_service)
    #    y = SDLModel(**prime_service)

    with open('tests/testdata/deployment-svc-mismatch.yaml', 'r') as file:
        prime_service = yaml.safe_load(file)

    x = json.dumps(prime_service)
    y = SDLModel(**prime_service)

    print("eeee")
    return True


@router.post("/sdl/dt", tags=["sdl"])
async def run_dp():
    task = BaseDeployer.deploy.apply_async(args=['SampleDeployer', '22'])
    return JSONResponse({"task_id": task.id})


@router.post("/akash/test", tags=["sdl"])
async def run_dp(address: str):
    balance = get_akash_balance(address)
    return JSONResponse({"uakt_balance": str(balance)})


@router.post("/akash/test_cert", tags=["sdl"])
async def run_dp(address: str):
    res = get_akash_active_certs(address)
    return JSONResponse({"certs": res})


@router.post("/akash/test_certgen", response_model=CreateCertificate, tags=["sdl"])
async def run_d_gen(address: str):
    return get_cert_gen_tx_data(address, 'testpass')


@router.post("/vault/test_all", tags=["sdl"])
async def run_d_gen(address: str):
    sample_store()
    sample_read()
    return JSONResponse({"ok": True})

