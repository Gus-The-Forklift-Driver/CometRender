import json
import logging
import signal
from os import path
from time import sleep

import bpy
import coloredlogs
from client_boilerplate import client as bpclient

# logger.setLevel(logging.DEBUG)
coloredlogs.install()

try:
    logging.info('Loading configuration file')
    with open('config.json', 'r') as file:
        config = json.load(file)
        logging.debug('config file :' + json.dumps(config, indent=4))
except Exception as e:
    logging.error('Failed to load configuration')
    logging.debug('', exc_info=True)
    exit()
client = bpclient(apiKey=config['api_key'], adress=config['server_ip'])

bpy.app.binary_path = config["blender_bin"]

task = None


def main():
    global task
    sleep_times = [5, 10, 15]
    sleep_iteration = 0
    while True:
        # get the next task
        task = client.get_next_task()

        # sleep bc nothing to do
        if task == None:
            logging.info(
                f'No new tasks, sleeping for {sleep_times[sleep_iteration]} seconds')
            sleep(sleep_times[sleep_iteration])
            if sleep_iteration < len(sleep_times)-1:
                sleep_iteration += 1
        else:
            # reset sleep iterations
            sleep_iteration = 0

            task_name = task['task_name']
            task_blend_file = task['blend_file']
            logging.info(f'Starting task : {task_name}')
            logging.debug(f'Task parameters :' + json.dumps(task, indent=4))
            if path.exists(f'{config["working_dir"]}{task_blend_file}.blend'):
                try:
                    bpy.ops.wm.open_mainfile(filepath=f'{config["working_dir"]}{task_blend_file}.blend')
                    # import configuration
                    current_scene = bpy.context.scene
                    # render size
                    current_scene.render.resolution_x = task["render_size"][0]
                    current_scene.render.resolution_y = task["render_size"][1]
                    # frame range
                    current_scene.frame_start = task['frame_range'][0]
                    current_scene.frame_end = task['frame_range'][1]
                    current_scene.frame_step = task['frame_range'][2]
                    # engine
                    current_scene.render.engine = task['render_engine']
                    # view layer
                    bpy.context.window.view_layer = task['view_layer']

                except Exception as e:
                    logging.error('Problem with task settings', exc_info=True)
                    client.post_progress(task_name, 'FAILED')

                try:
                    bpy.ops.render.render(animation=True)
                except Exception as e:
                    logging.error('Problem with render', exc_info=True)
                    client.post_progress(task_name, 'FAILED')

                else:
                    client.post_progress(task_name, 'DONE')
            else:
                logging.error(f"Cannot read file '{config['working_dir']}{task_blend_file}.blend'")
                client.post_progress(task_name, 'FAILED')

    logging.info('this shouldnt print')


def signal_term_handler(signal, frame):
    logging.info('Recieved sigterm')
    logging.info('Posting status')
    client.post_progress(task['task_name'], 'FAILED')


if __name__ == '__main__':
    signal.signal(signal.SIGTERM, signal_term_handler)
    try:
        main()
    except KeyboardInterrupt:
        logging.info('User ended task')
    except Exception as e:
        logging.critical('', exc_info=True)
    logging.info('Posting status')
    client.post_progress(task['task_name'], 'FAILED')
