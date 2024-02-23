---
title: "Upload files from GCP to Azure without SAS/AccessKey"
date: 2024-02-24
classes: wide
---

![image](https://github.com/rtree/pages/assets/1018794/5891e09b-69e8-47e2-af3e-778883314b52)

Credential is like plutonium.

One concerns recently on me is that User account for human-kinds are secured by MFA, but what about workload identities / Service accounts?
They are used within scripts stored securely, but once they are exfiltrated, they can be utilized from anywhere basically, this is the issue.

While looking around the cloud trends, recent years, we can use:
- Service accounts without keys within GCP
- User assigned managed identities within Azure

How it would be nice if we can do above in cross-cloud scenario! and there is the way for it.
I have tried cross cloud for uploading files from GCP to Azure Data Lake Gen2, and access them from PowerBI Desktop.

## How it is made of

Just a few steps:
- Prepare accounts in each cloud: user-assigned managed-identities in Azure, service account in GCP
- Connect above 2 by setting federated identitiy into user-assigned managed-identities in Azure
- Get token from GCP, pass it to Azure for returning back of token of Azure
- Upload files to Azure Data Lake Gen2 using the returned token of Azure

The steps above is well documented in following:
- <https://learn.microsoft.com/en-us/entra/workload-id/workload-identity-federation>
- <https://blog.identitydigest.com/azuread-federate-gcp/>

Well documented, but it was a little bit hard to grab overview and small how-to-s for actual implementation.
That's why I have introduced what I did in this article.

## What I did

### Procedure

#### [Configure in GCP]

- 1) Create service account
- 2) Assign it as Service Account of CloudFunctions
- 3) Refer cloudFunctions part

#### [Configure in Azure]

- 1) Create user-assigned managed identity
- 2) Set federated credentials to it
	- Federated credential scenario: OpenID Connect								
	- Issuer URL: https://accounts.google.com								
	- Subject identifier: Unique ID of the GCP service account								
	- Name: (Assign as you like)								
	- Audience: api://AzureADTokenExchange								
- 3) Make storageAccount with hierarcy enabled (to be accessed as Azure Data Lake Gen2)									
- 4) Assign Storage Data Contributer of storageAccount to user-assigned managed identity

#### [Place scripts into CloudFunctions]

refer following

### main.py

```python
import functions_framework
from google.cloud import storage
from google.cloud import firestore
import json
import os
from google.cloud.firestore import SERVER_TIMESTAMP
from datetime import datetime
import requests
from azure.storage.filedatalake import DataLakeServiceClient
from azure.identity import ClientAssertionCredential
import logging
BUCKET_NAME = os.getenv("BUCKET_NAME")
FOLDER_NAME = os.getenv("FOLDER_NAME")
AZURE_TENANT_ID      = os.getenv("AZURE_TENANT_ID")
AZURE_CLIENT_ID      = os.getenv("AZURE_CLIENT_ID")
AZURE_DATALAKE_URL   = os.getenv("AZURE_DATALAKE_URL")
AZURE_CONTAINER_NAME = os.getenv("AZURE_CONTAINER_NAME")
@functions_framework.http
def hello_http(request):
    """HTTP Cloud Function.
    Args:
        request (flask.Request): The request object.
        <https://flask.palletsprojects.com/en/1.1.x/api/#incoming-request-data>
    Returns:
        The response text, or any set of values that can be turned into a
        Response object using `make_response`
        <https://flask.palletsprojects.com/en/1.1.x/api/#flask.make_response>.
    """
    request_json = request.get_json(silent=True)
    request_args = request.args
    if request_json and 'name' in request_json:
        name = request_json['name']
    elif request_args and 'name' in request_args:
        name = request_args['name']
    else:
        name = 'World'
    save_to_bucket(BUCKET_NAME, FOLDER_NAME, "_log_launch")
    return 'Hello {}!'.format(name)
def mask_field(field_value):
    # TODO: Add your masking logic here
    # This is just an example that replaces the field value with asterisks
    masked = field_value
    return masked
def to_serializable(val):
    """
    Convert Firestore data types to JSON serializable objects
    """
    if isinstance(val, datetime):
        return val.isoformat()
    elif isinstance(val, SERVER_TIMESTAMP):
        return None
    else:
        return val
def dump_to_blob(filename, str_to_dump):
    db = firestore.Client()
    storage_client = storage.Client()
    bucket = storage_client.bucket(BUCKET_NAME)
    blob = bucket.blob(filename + "dump.txt")
    blob.upload_from_string(str_to_dump)
def save_to_adls_sdk(credential):
    service_client = DataLakeServiceClient(account_url=AZURE_DATALAKE_URL,
                                           credential =credential)
    file_system_client = service_client.get_file_system_client(file_system=AZURE_CONTAINER_NAME)
    file_name = "example.txt"
    file_contents = "Hello, Azure AD and GCP Federation!"
    file_client = file_system_client.get_file_client(file_name)
    file_client.upload_data(file_contents, overwrite=True)
    print(f"Uploaded {file_name} to Azure Data Lake Storage Gen2")
def get_azure_ad_token_sdk():
    credential = ClientAssertionCredential(
        AZURE_TENANT_ID,
        AZURE_CLIENT_ID,
        func=get_google_id_token,
    )
    return credential
def get_google_id_token():
    metadata_url = "http://metadata.google.internal/computeMetadata/v1/instance/service-accounts/default/identity"
    params = {
        "audience": "api://AzureADTokenExchange"
    }
    headers = {
        "Metadata-Flavor": "Google"
    }
    response = requests.get(metadata_url, params=params, headers=headers)
    if response.status_code == 200:
      return response.text
    else:
        raise Exception("Failed to obtain Google ID token")
def save_to_bucket(bucket_name, folder_name, collection_name):
    acred = get_azure_ad_token_sdk()
    logging.basicConfig(level=logging.DEBUG)
    save_to_adls_sdk(acred)
```

### requirements.txt
```python
functions-framework==3.*
google-cloud-firestore
google-cloud-storage
requests
azure-storage-file-datalake
azure-identity
```

### variables
```bash
AZURE_TENANT_ID      Entra->Identity->Overview->Tenant ID						
AZURE_CLIENT_ID      Managed Identities-> (the identity created)->overview->Client ID						
AZURE_DATALAKE_URL      https://<your-storage-account>.dfs.core.windows.net/						
AZURE_CONTAINER_NAME      Your Container Name
```

## Conclusion

Enjoy! and if you have questions, please DM on <https://twitter.com/rtree>.

