import uuid
from tabulate import tabulate as taaab
import json
import logging
import coloredlogs
from more_itertools import tabulate
coloredlogs.install(level=logging.INFO)


class TaskManager():
    def __init__(self) -> None:
        self.tasks = []
        pass

    def load_tasks_from_file(self, filepath: str = './task_list.json'):
        try:
            with open(filepath, 'r') as file:
                self.tasks = json.load(file)
            logging.info(f'Successfully loaded {filepath.split("/")[-1]}')
            return 0
        except Exception as e:
            logging.error('Failed to load configuration', exc_info=True)
            return None

    def save_tasks_to_file(self, filepath: str = './current_status.json'):
        try:
            with open('./current_status.json', 'w') as file:
                json.dump(self.tasks, file)
            logging.info(f'Successfully saved {filepath.split("/")[-1]}')
            return 0
        except Exception as e:
            logging.error('Failed to save configuration', exc_info=True)
            return None

    def get_next_task(self):
        for task_id in range(len(self.tasks)):
            if self.tasks[task_id]["status"]["current_status"] == 'TODO':
                self.tasks[task_id]["status"]["current_status"] = 'RUNNING'
                logging.info(f'Sending task named : {self.tasks[task_id]["name"]}')
                return self.tasks[task_id]
        # no valid tasks have been found
        return None

    def get_tasks_names(self):
        tasks_names = []
        for task_id in range(len(self.tasks)):
            tasks_names.append(self.tasks[task_id]["name"])
        return tasks_names

    # def add_task_by_dict(self, task_info: dict):
        try:
            self.tasks.append(task_info)
            logging.info(f'Added task named : {task_info["task_name"]}')
            return 0
        except Exception as e:
            logging.error('Failed to add task', exc_info=True)
            return None

    def add_task_by_settings(self, task_name, blend_file, frame_range, render_size, render_engine, view_layer, passes, chunks_size):
        task_uuid = uuid.uuid4()
        chunks = []
        if chunks_size == -1:
            chunks = {(frame_range[0], frame_range[1]): 'TODO'}
        else:
            for x in range(frame_range[0], frame_range[1], chunks_size+1):
                a = x
                b = x + chunks_size
                if frame_range[1]-chunks_size < b:
                    b = frame_range[1]
                chunks.append({(a, b): 'TODO'})

        self.tasks.append({
            "uuid": task_uuid,
            "name": task_name,
            "blend_file": blend_file,
            "render_size": render_size,
            "render_engine": render_engine,
            "view_layer": view_layer,
            "passes": passes,
            "status": {
                "errors": {},
                "chunks": chunks, }})

    def print_current_status(self):
        print(taaab(self.tasks, headers="keys"))


task = TaskManager()
task.load_tasks_from_file()
a = task.get_next_task()
# task.add_task_by_dict(a)

task.add_task_by_settings('bloop', 'boopsblend', [10, 500, 1], [1024, 2048], 'CYCLES', 'view_layer', 'all', 50)
print(task.get_tasks_names())
task.print_current_status()
logging.info('===DONE===')
