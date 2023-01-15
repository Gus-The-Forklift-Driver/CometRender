import requests


class client():
    def __init__(self,  apiKey: str, adress: str = 'http://127.0.0.1:8000'):
        self.apiKey = apiKey
        self.adress = adress

    def post_progress(self, task, progress_status):
        requests.post(
            url=f'{self.adress}/progress/{task}?status={progress_status}',
            headers={'key': self.apiKey})

    def get_next_task(self):
        return requests.get(url=f'{self.adress}/next_task').json()

    def ping(self):
        return requests.get(url=f'{self.adress}/ping')
