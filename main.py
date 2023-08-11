import json
import requests

from google.auth.transport.requests import Request as GoogleRequest
from google.oauth2 import service_account


class GoogleIndexingPage:
    def __init__(self, service_account_file):
        self.account_for_indexing = service_account.Credentials.from_service_account_file(
            service_account_file,
            scopes=['https://www.googleapis.com/auth/indexing']
        )

    def listing_index_urls(self, file_name_url):
        with open(file_name_url, 'r') as file:
            urls = file.read().splitlines()

        items = [
            {
                'Content-type': 'application/http',
                'Content-ID': f'response-{index}',
                'body': (
                    f"POST /v3/urlNotifications:publish HTTP/1.1\n"
                    f"Content-Type: application/json\n\n"
                    f"{json.dumps({'url': url, 'type': 'URL_UPDATED'})}"
                )
            }
            for index, url in enumerate(urls)
        ]

        url_batch = 'https://indexing.googleapis.com/batch'
        headers = {'Content-type': 'multipart/related; boundary=BOUNDARY'}

        request_object = GoogleRequest()
        self.account_for_indexing.refresh(request_object)

        boundary = 'BOUNDARY'
        body_parts = [f'--{boundary}\nContent-type: application/http\nContent-ID: {index}\n\n{item["body"]}' for
                      index, item in enumerate(items)]
        body = "\n".join(body_parts) + f'\n--{boundary}--\n'

        options = {
            'headers': {
                'Authorization': f'Bearer {self.account_for_indexing.token}',
                **headers
            },
            'data': body
        }

        response = requests.post(url_batch, **options)
        return response.text


def check_limit_indexing_api(service_account_file):
    credent = service_account.Credentials.from_service_account_file(
        service_account_file,
        scopes=['https://www.googleapis.com/auth/indexing']
    )

    ulr_quota = 'https://indexing.googleapis.com/v3/quota'
    request_quota = GoogleRequest()
    credent.refresh(request_quota)

    access_token = credent.token
    headers = {'Authorization': f'Bearer {access_token}'}

    response = requests.get(ulr_quota, headers=headers)

    if response.status_code == 200:
        data_qouta = response.json()
        max_daily_requests = data_qouta['quota']['maxDailyRequests']
        remaining_daily_requests = data_qouta['quota']['remainingDailyRequests']
        return max_daily_requests, remaining_daily_requests
    else:
        error_msg = f"Ошибка при получении данных о лимитах: {response.status_code} - {response.text}"
        return None, error_msg


if __name__ == "__main__":
    max_daily, remaining_daily = check_limit_indexing_api('service_account.json')

    if max_daily is not None:
        print(f"Количество лимитов Google indexing в сутки: {max_daily}")
        print(f"Оставшиеся количество на сегодня: {remaining_daily}")
    else:
        print({remaining_daily})

    # api = GoogleIndexingPage('service_account.json')
    # result = api.listing_index_urls('urls.txt')
    # print(result)
