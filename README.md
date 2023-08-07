Script for bulk indexing of URL addresses through Google API indexing.
The script uses these credentials for authentication and sending requests to the Google API Indexing.
- Create, file data service_account.json: It is a file containing credentials for a service account in Google Cloud Platform.
- Format file:
{
 "type": "service_account",
 "project_id": "{name project service account in Google Cloud Platform}",
 "private_key_id":{generate key in Google Cloud Platform},
 "private_key":{}
 "client_email"{}
 "client_id":{}
 "auth_uri":{}
 "token_uri":{}
 "auth_provider_x509_cert_url":{}
 "client_x509_cert_url":{}
 "universe_domain":{} 
}
- Create file named urls,txt to load string data (URLs)

1. To install the following libraries:
pip install requests, google 
2. To perform an update
python.exe -m pip install --upgrade pip - if using pip version
pip install --upgrade google-cloud-storage - In case of encountering errors
