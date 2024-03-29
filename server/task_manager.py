import copy
import os
import uuid
from tabulate import tabulate as taaab
import json
import logging
import coloredlogs
import utils

coloredlogs.install(level=logging.INFO)

default_light_path = {
    'max': 4,
    'diffuse': 4,
    'glossy': 4,
    'transimission': 4,
    'volume': 0,
    'transparent': 8
}
default_passes = {
    # data
    'Combined': 1,
    'z': 0,
    'mist': 0,
    'position': 0,
    'normal': 0,
    'vector': 0,
    # light
    # diffuse
    'diff_direct': 0,
    'diff_indirect': 0,
    'diff_color': 0,
    # glossy
    'glossy_direct': 0,
    'glossy_indirect': 0,
    'glossy_color': 0,
    # transmission
    'transmission_direct': 0,
    'transmission_indirect': 0,
    'transmission_color': 0,
    # volume
    'volume_direct': 0,
    'volume_indirect': 0,
    'emission': 0,
    'environment': 0,
    'ambient_occlusion': 0,
    'shadow_catcher': 0,
    # cryptomatte
    'object': 0,
    'material': 0,
    'asset': 0,
    'levels': 2,
}
default_cycles_task = {
    'uuid': '',
    'task_name': '',
    'blend_file': '',
    'render_settings': {
        'samples': 1,
        'time_limit': -1,
        'light_paths': default_light_path,
    },
    'output_settings': {
        'resolutionX': 1280,
        'resolutionY': 720,
        'frame_rate': 24,
        'frame_start': 1,
        'frame_end': 100,
        'output_path': '//frame_####.png',
        'denoiser': 0,
        'passes': default_passes,

    }
}


class TaskManager():

    def __init__(self) -> None:
        logging.info('Task manager initialized')
        self.tasks = []
        self.workers = {}
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

    def get_next_task(self, worker_name):
        for task in self.tasks:
            dirty = False
            for error in task['errors']:
                if error['worker_name'] == worker_name:
                    dirty = True
            if dirty:
                logging.info(f'Worker {worker_name} is dirty, skipping task')
                continue
            for chunk in task['chunks']:
                if chunk[1] == 'todo':
                    chunk[1] = 'running'
                    logging.info(f'Sending task named : {task["name"]} | {chunk[0]} to {worker_name}')
                    return task, chunk[0]

        # no valid tasks have been found
        # logging.info(f'No task to send for {worker_name}')
        return None, None

    def get_tasks_names(self):
        tasks_names = []
        for task in self.tasks:
            tasks_names.append(task["name"])
        return tasks_names

    def add_task_by_settings(self, task_settings):
        task_uuid = str(uuid.uuid4())
        chunks = []
        if task_settings['chunks_size'] == -1:
            chunks.append([(task_settings['frame_start'], task_settings['frame_end']), 'todo'])
        else:
            # creates chunks from settings
            # this does not take into account for the frame step
            for x in range(task_settings['frame_start'], task_settings['frame_end'], task_settings['chunks_size']+1):
                a = x
                b = x + task_settings['chunks_size']
                if task_settings['frame_end']-task_settings['chunks_size'] < b:
                    b = task_settings['frame_end']
                chunks.append([(a, b), 'todo'])

        # add task to task list
        try:
            self.tasks.append({
                "uuid": task_uuid,
                "name": task_settings['task_name'],
                "blend_file": task_settings['blend_file'],
                "frame_start": task_settings['frame_start'],
                "frame_end": task_settings['frame_end'],
                "errors": [],
                "chunks": chunks, })
            logging.info(f'Added task named : {task_settings["task_name"]}')
            return 0
        except Exception as e:
            logging.error('Failed to add task', exc_info=True)
            return None

    def print_current_status(self):
        display = copy.deepcopy(self.tasks)
        for id in range(len(display)):
            display[id].pop('uuid')
            display[id].pop('chunks')

        print(taaab(display, headers="keys"))

    def change_chunk_status(self, uuid, chunk_in, status):
        for task in self.tasks:
            if task['uuid'] == uuid:
                # logging.critical('=============CHUNK DEBUG===========')
                # logging.critical(f'uuid : {uuid} | chunk_in : {chunk_in} | status : {status}')
                # logging.critical(f'type : {type(chunk_in)} | 0 : {chunk_in[0]} | 1 : {chunk_in[1]}')
                for chunk in task['chunks']:
                    if chunk[0][0] == chunk_in[0] and chunk[0][1] == chunk_in[1]:
                        chunk[1] = status
                        logging.info(f'Moved {chunk_in} to {status} for {task["name"]}')
                        if self.check_if_complete(uuid):
                            utils.notify_status(f'Task : {task["name"]} complete', 'task_complete')

                        return
                logging.info(f'Could not find chunk : {chunk_in} for {task["name"]}')
                return
        logging.info(f'Could not find task with uuid : {uuid}')
        return

    def log_error(self, task_uuid, data):
        for task_id in range(len(self.tasks)):
            if self.tasks[task_id]['uuid'] == task_uuid:
                self.tasks[task_id]['errors'].append(data)
                logging.info(f'Added new error for {self.tasks[task_id]["name"]} : {data}')
                return
        logging.error(f'Failed to log error for task with : {task_uuid} uuid')
        return

    def move_task(self, task_uuid: str, offset: int):
        # find the place of the task in the task array
        for task_id in range(len(self.tasks)):
            if self.tasks[task_id]['uuid'] == task_uuid:
                break

        # clamp the offset
        new_index = max(0, min(task_id + offset, len(self.tasks)-1))
        # move task
        logging.info(f'Original index : {task_id} | new index : {new_index} | offset : {offset}')
        self.tasks.insert(new_index, self.tasks.pop(task_id))
        return

    def delete_task(self, task_uuid: str):
        for task_id in range(len(self.tasks)):
            if self.tasks[task_id]['uuid'] == task_uuid:
                logging.info(f'Deleting task {self.tasks[task_id]["name"]}')
                self.tasks.pop(task_id)
                return
        logging.error(f'Failed to delete task with : {task_uuid} uuid')

    def add_worker(self, name: str, frame_count):
        # logs workers and completed tasks
        if name in self.workers:
            self.workers[name] += frame_count
        else:
            self.workers[name] = frame_count

    def clean_workers(self, task_uuid):
        for task_id in range(len(self.tasks)):
            if self.tasks[task_id]['uuid'] == task_uuid:
                logging.info(f'Cleaning workers for : {self.tasks[task_id]["name"]}')
                for error in self.tasks[task_id]['errors']:
                    error['worker_name'] += 'cleaned'
                return
        logging.error(f'Failed to clean task with : {task_uuid} uuid')

    def check_if_complete(self, task_uuid):
        for task_id in range(len(self.tasks)):
            if self.tasks[task_id]['uuid'] == task_uuid:
                chunk_count = len(self.tasks[task_id]['chunks'])
                complete = 0
                for chunk in self.tasks[task_id]['chunks']:
                    if chunk[1] == 'done' or chunk[1] == 'chunks_done':
                        complete += 1

                if chunk_count == complete:
                    return True
                else:
                    return False
        return False

    def set_chunks_todo(self, task_uuid):
        for task_id in range(len(self.tasks)):
            if self.tasks[task_id]['uuid'] == task_uuid:
                for chunk in self.tasks[task_id]['chunks']:
                    if chunk[1] == 'running':
                        self.tasks[task_id][chunk][1] = 'todo'


if __name__ == '__main__':
    # just run some tests
    task = TaskManager()

    task.add_task_by_settings({'task_name': 'test',
                               'blend_file': 'render',
                               'scene': 'main',
                               'frame_start': 1,
                               'frame_end': 250,
                               'chunks_size': 50,
                               })

    task.save_tasks_to_file('./task_list.json')
    logging.info('===DONE===')
