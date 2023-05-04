import time
import requests

from retry import retry


class client():
    def __init__(self, name: str, apiKey: str, adress: str = 'http://127.0.0.1:8000'):
        self.apiKey = apiKey
        self.adress = adress
        self.name = name

    @retry(tries=-1, delay=1, backoff=2, max_delay=10)
    def post_progress(self, task_uuid, chunk, status):
        requests.post(
            url=f'{self.adress}/progress/{task_uuid}?chunk={chunk[0]},{chunk[1]}&status={status}&worker_name={self.name}',
            headers={'key': self.apiKey})

    @retry(tries=-1, delay=1, backoff=2, max_delay=10)
    def post_error(self,  error_type, error_info, task_uuid, chunk=None):
        error_msg = {
            'worker_name': self.name,
            'time': str(time.time()),
            'chunk': chunk,
            'type': error_type,
            'info': error_info
        }
        requests.post(
            url=f'{self.adress}/error/{task_uuid}',
            json=error_msg,
            headers={'key': self.apiKey}
        )

    @retry(tries=-1, delay=1, backoff=2, max_delay=10)
    def get_next_task(self):
        result = requests.get(url=f'{self.adress}/next_task',
                                  headers={'key': self.apiKey,
                                           'workername': self.name})
        result.raise_for_status()
        return result.json()

    @retry(tries=-1, delay=1, backoff=2, max_delay=10)
    def ping(self):
        return requests.get(url=f'{self.adress}/ping')

    @retry(tries=-1, delay=1, backoff=2, max_delay=10)
    def get_task_list(self):
        return requests.get(url=f'{self.adress}/task_list', headers={'key': self.apiKey}).json()

    @retry(tries=-1, delay=1, backoff=2, max_delay=10)
    def get_workers(self):
        return requests.get(url=f'{self.adress}/workers',
                            headers={'key': self.apiKey}).json()

    @retry(tries=-1, delay=1, backoff=2, max_delay=10)
    def get_task_status(self):
        return requests.get(url=f'{self.adress}/task_status',
                            headers={'key': self.apiKey}).json()

    def post_task(self, task):
        return requests.post(url=f'{self.adress}/new_task',
                             headers={'key': self.apiKey},
                             json=task)
