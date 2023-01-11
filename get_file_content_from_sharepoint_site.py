def get_file_content_from_sharepoint_site(azureapp_tenant, azureapp_client,
                                          azureapp_secret, account_login, account_password,
                                          sharepoint_prefix, site_name, file_path):

    """
    :param azureapp_tenant: your azureapp creds tenant
    :param azureapp_client: your azureapp creds client
    :param azureapp_secret: your azureapp creds secret
    :param account_login: your azureapp creds login
    :param account_password: your azureapp creds password
    :param sharepoint_prefix: the begining of your sharepoint site domain
    :param site_name: the name of site where you get the file
    :param file_path: path to file
    :return:
    """

    import requests
    import json
    import pandas as pd
    import io

    # post request to get access token
    r = requests.post(

        url=f"https://login.microsoftonline.com/{azureapp_tenant}/oauth2/v2.0/token",

        headers={
            "Content-Type": "application/x-www-form-urlencoded"
        },

        data={

            "client_id": azureapp_client,
            "client_secret": azureapp_secret,
            "scope": "Files.ReadWrite.All Sites.ReadWrite.All User.Read",
            "grant_type": "password",
            "username": account_login,
            "password": account_password
        },

    )

    # load access token from json
    at = json.loads(r.text)['access_token']

    # request to get site id
    r = requests.get(
        f'https://graph.microsoft.com/v1.0/sites/{sharepoint_prefix}.sharepoint.com:/sites/{site_name}?$select=id ',
        headers={"Authorization": "Bearer " + at, "content-type": "Application/Json"}
    )

    site_id = r.text

    # finally get file content
    r = requests.get(
        f"https://graph.microsoft.com/v1.0/sites/{site_id}/drive/root:{file_path}:/content",
        headers={"Authorization": "Bearer " + at, "content-type": "Application/Json"}
    )

    # get dataframe from json without file download
    print(r.content)

    with io.BytesIO(r.content) as fh:
        df = pd.io.excel.read_excel(fh, engine='openpyxl')

    return df

