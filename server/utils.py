import json

from matplotlib.font_manager import json_dump
from os import path


def verify_key(key: str):
    f = open('./apiKeys', 'r')
    for line in f:
        if key == line.strip('\n'):
            f.close
            return True
    return False


class TaskManager:
    def __init__(self) -> None:
        # load previous status if existing
        if path.exists('./current_status.json'):
            print('INFO : loading STATUS from file : ')
            try:
                with open('current_status.json', 'r') as file:
                    current_status = json.load(file)
                    self.tasks = current_status["task_list"]
                    self.current_tasks = current_status["current_tasks"]
                    self.done_tasks = current_status["done_tasks"]
                    print(current_status)
            except:
                print('WARNING : invalid current status data')
                self.tasks = {}
                self.current_tasks = {}
                self.done_tasks = {}
                self.load_tasks_from_file()
        # if previous state doesnt exist
        else:
            self.tasks = {}
            self.current_tasks = {}
            self.done_tasks = {}
            self.load_tasks_from_file()

        pass

    def load_tasks_from_file(self, file_path='./task_list.json'):
        print('INFO : loading TASKS form file : ')
        with open(file_path, 'r') as file:
            self.tasks = json.load(file)
        print(self.tasks)

    def get_next_task(self):
        if len(self.tasks) == 0:
            return None
        else:
            task_name = list(self.tasks.keys())[0]
            next_task = self.tasks.pop(task_name)
            self.current_tasks[task_name] = next_task
            print(self.current_tasks)
            return {'task_name': task_name, 'task': next_task}

    def mark_task_done(self, task_name):
        try:
            self.done_tasks[task_name] = self.current_tasks.pop(task_name)
        except KeyError:
            return 'Task does not exist'
        return 'Done'

    def mark_task_failed(self, task_name):
        try:
            self.tasks[task_name] = self.current_tasks.pop(task_name)
        except KeyError:
            return 'Task does not exist'
        return 'Done'

    def save_current_status(self):
        with open('./current_status.json', 'w') as file:
            current_status = {}
            current_status["task_list"] = self.tasks
            current_status["current_tasks"] = self.current_tasks
            current_status["done_tasks"] = self.done_tasks

            json.dump(current_status, file)
