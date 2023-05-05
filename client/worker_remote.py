import json
import logging
import os
import sys
from time import sleep
import utils
import bpy
import coloredlogs
from client_boilerplate import client as bpclient

task = None
chunk = None

# coloredlogs.install(level=logging.DEBUG)
# coloredlogs.install(level=logging.INFO)
logFormatter = logging.Formatter("%(asctime)s [%(levelname)s] : %(message)s")
coloredLogFormatter = logging.Formatter("\033[1;32m%(asctime)s \033[1;34m[%(levelname)s] \033[0m %(message)s")
rootLogger = logging.getLogger()
rootLogger.setLevel(logging.INFO)

fileHandler = logging.FileHandler("{0}/{1}".format('./', 'log'))
fileHandler.setFormatter(logFormatter)
rootLogger.addHandler(fileHandler)
consoleHandler = logging.StreamHandler(sys.stdout)
consoleHandler = logging.StreamHandler()
consoleHandler.setFormatter(coloredLogFormatter)
rootLogger.addHandler(consoleHandler)


# load worker config
try:
    logging.info('Loading configuration file')
    config = utils.load_config()
    logging.debug('config file :' + json.dumps(config, indent=4))
except Exception as e:
    logging.error('Failed to load configuration')
    logging.debug('', exc_info=True)
    exit()
# setup client boilerplate
client = bpclient(name=config['worker']['name'], apiKey=config['server']['key'], adress=config['server']['ip'])

bpy.app.binary_path = config['worker']["blender_bin"]


def main():
    sleep_times = [5, 10, 15]
    sleep_iteration = 0
    while True:
        try:
            # get the next task
            task, chunk = client.get_next_task()

            # wait until new task
            if task == None:
                logging.info(
                    f'No new tasks, sleeping for {sleep_times[sleep_iteration]} seconds')
                sleep(sleep_times[sleep_iteration])
                if sleep_iteration < len(sleep_times)-1:
                    sleep_iteration += 1

            else:
                # reset sleep time
                sleep_iteration = 0

                # start task
                task_name = task['name']
                task_blend_file = task['blend_file']
                logging.info(f'Starting task : {task_name} | {chunk}')
                logging.debug(f'Task parameters :' + json.dumps(task, indent=4))

                # load blendfile
                if os.path.exists(os.path.join(config['worker']['working_dir'], task_blend_file)):
                    logging.info(f'blend file already exists : {task_blend_file}')
                else:
                    logging.info(f'downloading blend file : {task_blend_file}')
                    client.get_file(task_blend_file, config['worker']['working_dir'])
                bpy.ops.wm.open_mainfile(filepath=os.path.join(config['worker']['working_dir'], task_blend_file))

                # get external files
                missing_files = utils.check_external_files(config['worker']['working_dir'])
                for file in missing_files:
                    if os.path.exists(os.path.join(config['worker']['working_dir'], file)):
                        logging.info(f'file already exists : {file}')
                    else:
                        logging.info(f'downloading file : {file}')
                        client.get_file(file, config['worker']['working_dir'])
        except:
            print('an unknown error occured')
        logging.info('done')
        break


main()
