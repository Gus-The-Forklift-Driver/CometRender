import json
import logging
import signal
from os import path
from time import sleep
import utils
import bpy
import coloredlogs
from client_boilerplate import client as bpclient

task = None
chunk = None

# coloredlogs.install(level=logging.DEBUG)
coloredlogs.install(level=logging.INFO)

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
    sleep_times = [5, 10, 15, 30, 30, 30, 30, 60, 120]
    sleep_iteration = 0
    while True:

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
            blend_file_path = utils.locate_blend_file(task_blend_file, config['worker']["working_dir"])
            if blend_file_path != None:
                # load blendfile this shouldn't raise any error but incase of...
                try:
                    bpy.ops.wm.open_mainfile(filepath=blend_file_path)
                except Exception as e:
                    logging.error('Problem with loading .blend file', exc_info=True)
                    client.post_error('pb_blendfile', str(e), task['uuid'])
                else:
                    # diabled file checking for now
                    '''
                    missing_files = utils.check_external_files(config['worker']["working_dir"])
                    if len(missing_files) > 0:
                        logging.error(f'Missing external files : ')
                        for file in missing_files:
                            logging.error(file)
                        client.post_error('pb_local_files', missing_files, task['uuid'])
                    '''
                    try:
                        utils.set_settings(task, chunk)

                    except Exception as e:
                        logging.error('Problem with task settings', exc_info=True)
                        client.post_error('pb_settings', str(e), task['uuid'])
                    else:
                        try:
                            logging.info(f'beep boop computing {task["name"]}')
                            bpy.ops.render.render(animation=True)
                        except Exception as e:
                            logging.error('Problem with render', exc_info=True)
                            client.post_error('pb_render', str(e), task['uuid'], chunk)
                        else:
                            client.post_progress(task_uuid=task['uuid'], chunk=chunk, status="done")
            else:
                logging.error(f"File doesn't exist : '{config['worker']['working_dir']}{task_blend_file}.blend'")
                logging.info(f"file should be here {config['worker']['working_dir']}{task_blend_file}.blend")
                client.post_error('pb_blendfile_missing',
                                  f'Looked in {config["worker"]["working_dir"]}', task['uuid'], chunk=chunk)

        task = None
        chunk = None


def signal_term_handler(signal, frame):
    logging.info('Recieved sigterm')
    if task != None:
        logging.info('Posting status')
        client.post_error('pb_canceled', 'canceled by user', task['uuid'], chunk)


if __name__ == '__main__':

    signal.signal(signal.SIGTERM, signal_term_handler)
    try:
        main()
    except KeyboardInterrupt:
        logging.info('User ended worker')
    except Exception as e:
        logging.critical('', exc_info=True)
    if task != None:
        logging.info('Posting status')
        client.post_error('pb_canceled', 'canceled by user', task['uuid'], chunk)
