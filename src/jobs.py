from fireblocks_sdk import FireblocksSDK, VAULT_ACCOUNT, ONE_TIME_ADDRESS, PagedVaultAccountsRequestFilters, GetAssetWalletsFilters, TransferPeerPath, DestinationTransferPeerPath
from src.config import settings


# ASSET = "ETH_TEST"


def get_fireblock():
    api_secret = open('key/sandbox_fireblocks_secret.key', 'r').read()
    api_key = settings.FIREBLOCK_API_KEY
    api_url = settings.FIREBLOCK_API_URL
    return FireblocksSDK(api_secret, api_key, api_base_url=api_url)

def sweep_accounts() -> dict:
   """
   :param treasury_vault_id: The vault that will receive all the funds.
   :return: A dictionary of accounts swept with the values being the amount transferred.
   """
   fireblocks = get_fireblock()
   
   vault_dict = {}
   vault_accounts = fireblocks.get_vault_accounts_with_page_info(PagedVaultAccountsRequestFilters(name_prefix=settings.USER_NAME_PREFIX))
   for vault in vault_accounts['accounts']:
        print("- Vault = ", vault)
        for asset in vault['assets']:
            if asset['id'] in settings.ASSET_LIST and float(asset['balance']) >= settings.MIN_SWEEPING_THRESHOLD:
                fireblocks.create_transaction(
                    asset_id=asset['id'],  
                    amount=asset['balance'],
                    source=TransferPeerPath(
                        peer_type=VAULT_ACCOUNT,
                        peer_id=vault['id']
                    ),
                    destination=DestinationTransferPeerPath(
                        peer_type=VAULT_ACCOUNT,
                        peer_id=settings.TREASURY_ID
                    )
                )
                vault_dict[vault['name']] = asset['balance']
              
   return vault_accounts

