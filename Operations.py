from connector import *

def get_accounts_name(headers):

    account_groups = get_data(headers=headers, endp_url="https://api.thousandeyes.com/v6/account-groups.json")

    if 'accountGroups' in account_groups:
        
        accounts = {}

        for acc in account_groups['accountGroups']:

            accounts.update({acc.get('accountGroupName'): acc.get("aid")})

        return accounts
    
    else:

        return False
