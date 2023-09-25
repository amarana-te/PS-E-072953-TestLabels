from connector import *
from openpyxl import load_workbook
from Operations import get_accounts_name

# EXCEL
wb = load_workbook("Templates/PWC.xlsx")
wb.active = wb["Report"] #para movernos a una pagina en específico
ws = wb.active


def get_labels(test_details) -> list:

    
    if "groups" in test_details["test"][0]:

        labels = []
        for label in test_details["test"][0]["groups"]:

            labels.append(label["name"])

        return labels

    else:

        labels = []

        return labels


def get_tests_info(headers):

    aid_accounts = get_accounts_name(headers) #{"Dani's sandbox":1234,"Switching team":1231231}

    for each_account in aid_accounts:

        #list of tests
        tests_endpoint = "https://api.thousandeyes.com/v6/tests.json?aid=%s" % aid_accounts[each_account]
        tests_list = get_data(headers, endp_url=tests_endpoint)

        if "error" not in tests_list and "test" in tests_list:

            aid_account = each_account

            for test in tests_list["test"]:

                if test["liveShare"] == 0 and test["savedEvent"] == 0: #if the test belongs to the parent

                    details_endpoint = "https://api.thousandeyes.com/v6/tests/%s.json?aid=%s" % (test["testId"], aid_accounts[each_account])

                    test_details = get_data(headers, endp_url=details_endpoint)

                    labels = get_labels(test_details)


                    if len(test_details["test"][0]["sharedWithAccounts"]) > 1:

                        accounts = []
                        for account in test_details["test"][0]["sharedWithAccounts"]:
                            
                            if account["name"] != aid_account:
                                
                                accounts.append(account["name"])
                        
                        #group_assign.append({"Test":test_details["testName"],"Assigned account":aid_account,"Shared with":", ".join(accounts)})

                        test_entry = ["PWC", 
                                    aid_account, 
                                    test["type"], 
                                    test["testName"],
                                    test["testId"],
                                    "TRUE" if test["enabled"] == 1 else "FALSE",
                                    ", ".join(accounts),
                                    ", ".join(labels)]

                        ws.append(test_entry)


    file_name = timestamp().replace("/", "-").replace(":", "") + '-pwc.xlsx' # que a cada rato se cree uno nuevo? -- se le tendría que pedir al usuario que modifique en el main el nombre del file
    wb.save(filename=file_name)
    print("Template has been created on this folder with the following name: " + file_name)


