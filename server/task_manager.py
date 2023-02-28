import copy
import os
import uuid
from tabulate import tabulate as taaab
import json
import logging
import coloredlogs

coloredlogs.install(level=logging.INFO)


class TaskManager():

    def __init__(self) -> None:
        logging.info('Task manager initialized')
        self.tasks = []
        # self.load_tasks_from_file()
        pass

    def load_tasks_from_file(self, filepath: str = './task_list.json'):
        try:
            with open(filepath, 'r') as file:
                self.tasks = json.load(file)
            logging.info(f'Successfully loaded {filepath.split("/")[-1]}')
            return
        except Exception as e:
            logging.error('Failed to load tasks', exc_info=True)
            return []

    def save_tasks_to_file(self, filepath: str = './current_status.json'):
        try:
            with open(filepath, 'w') as file:
                json.dump(self.tasks, file)
            logging.info(f'Successfully saved to {os.path.abspath(filepath)}')
            return 0
        except Exception as e:
            logging.error('Failed to save tasks', exc_info=True)
            return None

    def get_next_task(self):
        for task_id in range(len(self.tasks)):
            if len(self.tasks[task_id]["chunks_todo"]) > 0:
                chunk = self.tasks[task_id]["chunks_todo"].pop(0)
                self.tasks[task_id]['chunks_running'].append(chunk)
                logging.info(f'Sending task named : {self.tasks[task_id]["name"]} | {chunk}')
                return self.tasks[task_id], chunk
        # no valid tasks have been found
        return None

    def get_tasks_names(self):
        tasks_names = []
        for task_id in range(len(self.tasks)):
            tasks_names.append(self.tasks[task_id]["name"])
        return tasks_names

    def add_task_by_dict(self, task_info: dict):
        try:
            self.tasks.append(task_info)
            logging.info(f'Added task named : {task_info["task_name"]}')
            return 0
        except Exception as e:
            logging.error('Failed to add task', exc_info=True)
            return None

    def add_task_by_settings(self, task_name, blend_file, frame_range, render_size, render_engine, view_layer, passes, chunks_size):
        task_uuid = str(uuid.uuid4())
        chunks = []
        if chunks_size == -1:
            chunks = {(frame_range[0], frame_range[1]): 'TODO'}
        else:
            # creates chunks from settings
            # this does not take into account for the frame step
            for x in range(frame_range[0], frame_range[1], chunks_size+1):
                a = x
                b = x + chunks_size
                if frame_range[1]-chunks_size < b:
                    b = frame_range[1]
                chunks.append((a, b))

        self.add_task_by_dict({
            "uuid": task_uuid,
            "name": task_name,
            "blend_file": blend_file,
            "render_size": render_size,
            "render_engine": render_engine,
            "view_layer": view_layer,
            "passes": passes,
            "status": {
                "errors": {}},
            "chunks_todo": chunks,
            "chunks_running": [],
            "chunks_done": [], })

    def print_current_status(self):
        display = copy.deepcopy(self.tasks)
        for id in range(len(display)):
            display[id].pop('uuid')

        print(taaab(display, headers="keys"))

    def change_chunk_status(self, uuid, chunk, status):
        for task_id in range(len(self.tasks)):
            if self.tasks[task_id]['uuid'] == uuid:
                try:
                    self.tasks[task_id]['chunks_todo'].remove(chunk)
                except:
                    pass
                try:
                    self.tasks[task_id]['chunks_running'].remove(chunk)
                except:
                    pass
                try:
                    self.tasks[task_id]['chunks_done'].remove(chunk)
                except:
                    pass
                self.tasks[task_id][status].append(chunk)
                logging.info(f'Moved {chunk} to {status} for {self.tasks[task_id]["name"]}')
                return
        logging.info(f'could not find task with uuid : {uuid}')
        return


if __name__ == '__main__':
    # just run some tests
    task = TaskManager()
    task.load_tasks_from_file()
    #a = task.get_next_task()
    # task.add_task_by_dict(a)

    #task.add_task_by_settings('bloop', 'boopsblend', [10, 500, 1], [1024, 2048], 'CYCLES', 'view_layer', 'all', 50)
    #task.add_task_by_settings('test2', 'anotherone', [1, 250, 1], [1920, 1024], 'CYCLES', 'view_layer', 'all', 10)

    task.get_next_task()

    task.change_chunk_status('860dd42e-b012-416f-8a46-965132c40bcf', list(eval('10, 60')), 'chunks_done')

    # print(task.get_tasks_names())
    task.print_current_status()
    # task.save_tasks_to_file('./task_list.json')
    logging.info('===DONE===')
