import requests
import json

from os import path


def verify_key(key: str):
    return key == "CHANGEME"
    # f = open('./apiKeys', 'r')
    # for line in f:
    #     if key == line.strip('\n'):
    #         f.close
    #         return True
    # return False
    return True


def notify_status(title: str, message: str = None):
    requests.post("https://ntfy.sh/",
                  data=json.dumps({
                      "topic": "comet_render_beep",
                      "message": message,
                      "title": title,
                      "tags": [],
                      "priority": 3,
                      "attach": "",
                      "filename": "",
                      "click": "",
                      "actions": []
                  })
                  )
    return


if __name__ == '__main__':
    notify_status('This is title', 'beep bop')
