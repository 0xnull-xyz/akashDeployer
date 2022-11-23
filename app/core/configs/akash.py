MAINNET_NODE_ID = "akash.c29r3.xyz"
MAINNET_NODE_API = "https://akash.c29r3.xyz:443/api"
MAINNET_NODE_RPC = "http://akash.c29r3.xyz:80/rpc"

TESTNET_NODE_ID = "testnet-1.ewr1.aksh.pw"
TESTNET_NODE_API = "http://api.testnet-1.ewr1.aksh.pw:1317"
TESTNET_NODE_RPC = "http://rpc.testnet-1.ewr1.aksh.pw:26657"

MAINNET = True

ACTIVE_NODE_ID = MAINNET_NODE_ID if MAINNET else TESTNET_NODE_ID
ACTIVE_NODE_API = MAINNET_NODE_API if MAINNET else TESTNET_NODE_API
ACTIVE_NODE_RPC = MAINNET_NODE_RPC if MAINNET else TESTNET_NODE_RPC
