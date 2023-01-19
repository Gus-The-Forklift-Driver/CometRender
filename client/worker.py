import json
from time import sleep

from retry import retry
from client_boilerplate import client as bpclient
import bpy
import coloredlogs
import logging
from os import path


# logging.debug('This is a debug message')
# logging.info('This is an info message')
# logging.warning('This is a warning message')
# logging.error('This is an error message')
# logging.critical('This is a critical message')

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


@retry(tries=-1, delay=1, backoff=2, max_delay=10)
def wait_until_reconnection():
    client.ping()
    # while True:
    #     try:
    #         r = client.ping()
    #     except:
    #         logging.error(f'Failed to connect to {config["server_ip"]}')
    #         logging.error(f'Sleeping for 10 seconds')
    #         sleep(10)
    #         continue
    #     break


bpy.app.binary_path = config["blender_bin"]
sleep_times = [5, 10, 60]
sleep_iteration = 0
while True:
    # check if we have connection
    wait_until_reconnection()
    # get the next task
    task = client.get_next_task()

    # sleep bc nothing to do
    if task == None:
        logging.info(f'No new tasks, sleeping for {sleep_times[sleep_iteration]} seconds')
        sleep(sleep_times[sleep_iteration])
        if sleep_iteration != len(sleep_times):
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
                bpy.ops.render.render(write_still=True)
            except Exception as e:
                logging.error('Problem with blend file', exc_info=True)
                client.post_progress(task_name, 'FAILED')
            else:
                client.post_progress(task_name, 'DONE')
        else:
            logging.error(f"Cannot read file '{config['working_dir']}{task_blend_file}.blend'")
            client.post_progress(task_name, 'FAILED')

logging.info('this shouldnt print')
