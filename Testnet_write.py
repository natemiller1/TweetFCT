from factom import Factomd, FactomWalletd

# Default settings
factomd = Factomd()
walletd = FactomWalletd()

# You can also specify default fct and ec addresses, change host, or specify RPC credentials, for example:
fct_address = 'FA2jK2HcLnRdS94dEcU27rF3meoJfpUcZPSinpb7AwQvPRY6RL1Q'
ec_address = 'EC2jhmCtabeTXGtuLi3AaPzvwSuqksdVsjfxXMXV5gPmipXc4GjC'

factomd = Factomd(
    host='http://someotherhost:8088',
    fct_address=fct_address,
    ec_address=ec_address,
    username='rpc_username',
    password='rpc_password'
)
