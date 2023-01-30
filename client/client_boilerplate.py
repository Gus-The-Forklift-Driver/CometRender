from time import sleep
from matplotlib.pyplot import bar_label
import requests

from retry import retry


class client():
    def __init__(self,  apiKey: str, adress: str = 'http://127.0.0.1'):
        self.apiKey = apiKey
        self.adress = adress

    @retry(tries=-1, delay=1, backoff=2, max_delay=10)
    def post_progress(self, task, progress_status):

        requests.post(
            url=f'{self.adress}/progress/{task}?status={progress_status}',
            headers={'key': self.apiKey})

    @retry(tries=-1, delay=1, backoff=2, max_delay=10)
    def get_next_task(self):
        return requests.get(url=f'{self.adress}/next_task').json()

    @retry(tries=-1, delay=1, backoff=2, max_delay=10)
    def ping(self):
        return requests.get(url=f'{self.adress}/ping')

    @retry(tries=-1, delay=1, backoff=2, max_delay=10)
    def get_task_list(self):
        return requests.get(url=f'{self.adress}/task_list').json()
