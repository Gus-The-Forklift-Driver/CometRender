import json

from matplotlib.font_manager import json_dump
from os import path


def verify_key(key: str):
    # f = open('./apiKeys', 'r')
    # for line in f:
    #     if key == line.strip('\n'):
    #         f.close
    #         return True
    # return False
    return True


class TaskManager:
    def __init__(self) -> None:
        # load previous status if existing
        if path.exists('./current_status.json'):
            print('INFO : loading STATUS from file : ')
            try:
                with open('current_status.json', 'r') as file:
                    current_status = json.load(file)
                    self.tasks = current_status
                    print(current_status)
            except:
                print('WARNING : invalid current status data')
                self.load_tasks_from_file()
        # if previous state doesnt exist
        else:
            self.load_tasks_from_file()

        pass

    def load_tasks_from_file(self, file_path='./task_list.json'):
        print('INFO : loading TASKS form file : ')
        with open(file_path, 'r') as file:
            self.tasks = json.load(file)
        print(self.tasks)

    def get_next_task(self):
        for task in range(len(self.tasks)):
            if self.tasks[task]["status"]["current_status"] == 'TODO':
                self.tasks[task]["status"]["current_status"] = 'RUNNING'
                return self.tasks[task]
        # no valid tasks have been found
        return None

    def mark_task_done(self, task_name):
        for index in range(len(self.tasks)):
            if self.tasks[index]["task_name"] == task_name:
                self.tasks[index]["status"]["current_status"] = 'DONE'
                return 'Done'
        return 'Task does not exist'

    def mark_task_failed(self, task_name):
        for index in range(len(self.tasks)):
            if self.tasks[index]["task_name"] == task_name:
                self.tasks[index]["status"]["current_status"] = 'FAILED'
                return 'Done'
        return 'Task does not exist'

    def save_current_status(self):
        with open('./current_status.json', 'w') as file:
            json.dump(self.tasks, file)
