import os

from databases import DatabaseURL
from starlette.datastructures import CommaSeparatedStrings, Secret

API_V1_STR = "/api"

DEFAULT_MONGO_ENTITY_VER = "0.0.1"

JWT_TOKEN_PREFIX = "Bearer"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24 * 7  # one week

# load_dotenv(".env")

MAX_CONNECTIONS_COUNT = int(os.getenv("MAX_CONNECTIONS_COUNT", 10))
MIN_CONNECTIONS_COUNT = int(os.getenv("MIN_CONNECTIONS_COUNT", 10))
SECRET_KEY = Secret(os.getenv("SECRET_KEY", "secret key for project"))

PROJECT_NAME = os.getenv("backend", "akdep backend apis")
ALLOWED_HOSTS = CommaSeparatedStrings(os.getenv("ALLOWED_HOSTS", ""))

MONGODB_URL = os.getenv("MONGODB_URL", "")  # deploying without docker-compose
if not MONGODB_URL:
    MONGO_HOST = os.getenv("MONGO_HOST", "localhost")
    MONGO_PORT = int(os.getenv("MONGO_PORT", 27017))
    MONGO_USER = os.getenv("MONGO_USER", "admin")
    MONGO_PASS = os.getenv("MONGO_PASSWORD", "admin")
    MONGO_DB = os.getenv("MONGO_DB", "akdep")
    MONGO_AUTH_SRC = os.getenv("MONGO_AUTH_SRC", "admin")

    MONGODB_URL = DatabaseURL(
        f"mongodb://{MONGO_USER}:{MONGO_PASS}@{MONGO_HOST}:{MONGO_PORT}/{MONGO_DB}?authSource={MONGO_AUTH_SRC}"
    )
else:
    MONGODB_URL = DatabaseURL(MONGODB_URL)

database_name = MONGO_DB
# Collection names:
users_collection_name = "users"
categories_collection_name = "categories"
apps_collection_name = "apps"
banners_collection_name = "banners"
sidebars_collection_name = "sidebars"
tags_collection_name = "tags"
dcs_collection_name = "tags"
deployments_collection_name = "tags"
deployment_definitions_collection_name = "tags"
deployment_types_collection_name = "tags"
providers_collection_name = "tags"
regions_collection_name = "tags"
sdl_templates_collection_name = "tags"

# Role String Literals:
# Normal -> default, ipg -> PAID, admin -> MANUAL

# S3 Configs
S3_ACCESS_KEY = os.getenv("S3_KEY", "agHSI34kgkuZy1mT2")
S3_SECRET_KEY = os.getenv("S3_SECRET", "wqSXVo1oK4kZUAMBkADWM8kWk91mq9zE")
S3_ENDPOINT_URL = os.getenv("S3_ENDPOINT", "http://127.0.0.1:9000")
S3_BUCKET_NAME = os.getenv("S3_BUCKET", "ali-dev")

# HashiCorp Wault Config
VAULT_CLIENT_ADDRESS = os.getenv("VAULT_CLIENT_ADDRESS", "https://localhost:8200")
VAULT_UNSEAL_KEY = os.getenv("VAULT_UNSEAL_KEY", "@")
VAULT_ROOT_TOKEN = os.getenv("VAULT_ROOT_TOKEN", "3")