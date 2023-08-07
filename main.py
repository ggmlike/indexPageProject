import json
import requests

from google.auth.transport.requests import Request as GoogleRequest
from google.oauth2 import service_account

indexing_account = service_account.Credentials.from_service_account_file('service_account.json', scopes=['https://www'
                                                                                                         '.googleapis'
                                                                                                         '.com/auth'
                                                                                                         '/indexing'])



with open('urls.txt', 'r') as file:
    bathc = file.read().splitlines()

items = [
    {
        'Content-type': 'application/http',
        'Content-ID': '',
        'body': (
            f"POST /v3/urlNotifications:publish HTTP/1.1\n"
            f"Content-Type: application/json\n\n"
            f"{json.dumps({'url': line, 'type': 'URL_UPDATED'})}"
        )
    }
    for line in bathc
]

urlRequest = 'https://indexing.googleapis.com/batch'
headers = {'Content-type': 'multipart/related; boundary=BOUNDARY'}

request_object = GoogleRequest()
indexing_account.refresh(request_object)

boundary = 'BOUNDARY'
body_parts = [f'--{boundary}\nContent-type: application/http\nContent-ID: {index}\n\n{item["body"]}' for index, item in enumerate(items)]
body = "\n".join(body_parts) + f'\n--{boundary}--\n'

options = {
    'headers': {
        'Authorization': f'Bearer {indexing_account.token}',
        **headers
    },
    'data': body
}

response = requests.post(urlRequest, **options)
print(response.text)
