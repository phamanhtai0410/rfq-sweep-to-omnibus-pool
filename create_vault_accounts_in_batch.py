from fireblocks_sdk import FireblocksSDK, VAULT_ACCOUNT, ONE_TIME_ADDRESS, PagedVaultAccountsRequestFilters, GetAssetWalletsFilters, TransferPeerPath, DestinationTransferPeerPath
import os
os.path.join('.')

from src.config import settings
ASSET = "ETH_TEST3"
api_secret = open('key/sandbox_fireblocks_secret.key', 'r').read()
api_key = settings.FIREBLOCK_API_KEY
api_url = settings.FIREBLOCK_API_URL
fireblocks = FireblocksSDK(api_secret, api_key, api_base_url=api_url)

def create_vault_accounts(amount: int, fireblocks=fireblocks) -> dict:
    """
    :param amount: Amount of vault accounts to create (one, per end user).
    :return: A dictionary where keys are the vault names and IDs are the co-responding values.
    """    
    vault_dict = {}
    counter = 1

    while counter <= amount:
        vault_name = f"End-User {counter} Vault"
        vault_id = fireblocks.create_vault_account(name=vault_name, hiddenOnUI=True)['id']
        fireblocks.create_vault_asset(vault_id, ASSET)
        vault_dict[vault_name] = vault_id
        counter += 1
    else:
        vault_name = "Treasury"
        vault_id = fireblocks.create_vault_account(name=vault_name)['id']
        fireblocks.create_vault_asset(vault_id, ASSET)
        vault_dict[vault_name] = vault_id

    return vault_dict

# _batch = create_vault_accounts(10)
# print("Batch = ", _batch)

# Batch =  {'End-User 1 Vault': '64', 'End-User 2 Vault': '65', 'End-User 3 Vault': '66', 'End-User 4 Vault': '67', 'End-User 5 Vault': '68', 'End-User 6 Vault': '69', 'End-User 7 Vault': '70', 'End-User 8 Vault': '71', 'End-User 9 Vault': '72', 'End-User 10 Vault': '73', 'Treasury': '74'}

print("List vault accounts = ", fireblocks.get_vault_accounts_with_page_info(PagedVaultAccountsRequestFilters(name_prefix="End-User")))

# for i in range(64, 74):
#     _data = fireblocks.get_deposit_addresses(i, "ETH_TEST3")[0]['address']
#     print(f"* TEST_{i} is {_data}")