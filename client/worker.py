import json
import logging
import signal
from os import path
from time import sleep
import utils
import bpy
import coloredlogs
from client_boilerplate import client as bpclient
import platform


# coloredlogs.install(level=logging.DEBUG)
coloredlogs.install(level=logging.INFO)


try:
    logging.info('Loading configuration file')
    config = utils.load_config()
    logging.debug('config file :' + json.dumps(config, indent=4))
except Exception as e:
    logging.error('Failed to load configuration')
    logging.debug('', exc_info=True)
    exit()
client = bpclient(name=config['worker']['name'], apiKey=config['server']['key'], adress=config['server']['ip'])

bpy.app.binary_path = config['worker']["blender_bin"]


def main():
    sleep(1)
    global task
    sleep_times = [5, 10, 15]
    sleep_iteration = 0
    while True:

        # get the next task
        task, chunk = client.get_next_task()

        # sleep bc nothing to do
        if task == None:
            logging.info(
                f'No new tasks, sleeping for {sleep_times[sleep_iteration]} seconds')
            sleep(sleep_times[sleep_iteration])
            if sleep_iteration < len(sleep_times)-1:
                sleep_iteration += 1

        else:
            # reset sleep time
            sleep_iteration = 0

            task_name = task['name']
            task_blend_file = task['blend_file']
            logging.info(f'Starting task : {task_name} | {chunk}')

            logging.debug(f'Task parameters :' + json.dumps(task, indent=4))
            blend_file_path = utils.locate_blend_file(task_blend_file, config['worker']["working_dir"])
            if blend_file_path != None:
                # load blendfile this shouldn't raise any error but incase of...
                try:
                    bpy.ops.wm.open_mainfile(filepath=blend_file_path)
                except Exception as e:
                    logging.error('Problem with loading .blend file', exc_info=True)
                    client.post_error(task['uuid'], 'pb_blendfile', str(e))
                else:
                    missing_files = utils.check_external_files()
                    if len(missing_files) > 0:
                        logging.error(f'Missing external files : ')
                        for file in missing_files:
                            logging.error(file)
                        client.post_error(task['uuid'], 'pb_settings', missing_files)

                    try:
                        # import configuration
                        current_scene = bpy.context.scene
                        # render size
                        current_scene.render.resolution_x = task["render_size"][0]
                        current_scene.render.resolution_y = task["render_size"][1]
                        # frame range
                        current_scene.frame_start = chunk[0]
                        current_scene.frame_end = chunk[1]
                        current_scene.frame_step = task['frame_step']
                        # engine
                        current_scene.render.engine = task['render_engine']
                        # view layer
                        bpy.context.window.view_layer.name = task['view_layer']

                    except Exception as e:
                        logging.error('Problem with task settings', exc_info=True)
                        client.post_error(task['uuid'], 'pb_settings', str(e))
                    else:
                        try:
                            bpy.ops.render.render(animation=True)
                        except Exception as e:
                            logging.error('Problem with render', exc_info=True)
                            client.post_error(task['uuid'], 'pb_render', str(e))
                        else:
                            client.post_progress(task_uuid=task['uuid'], chunk=chunk, status="chunks_done")
            else:
                logging.error(f"File doesn't exist : '{config['worker']['working_dir']}{task_blend_file}.blend'")
                logging.info(f"file should be here {config['worker']['working_dir']}{task_blend_file}.blend")
                client.post_error(task['uuid'], 'pb_blendfile_missing',
                                  f'Looked in {config["worker"]["working_dir"]}')

        task = None
        chunk = None
    logging.info('this shouldnt print')


def signal_term_handler(signal, frame):
    logging.info('Recieved sigterm')
    if task != None:
        logging.info('Posting status')
        client.post_error(task['uuid'], 'pb_canceled', 'canceled by user')


if __name__ == '__main__':
    signal.signal(signal.SIGTERM, signal_term_handler)
    try:
        main()
    except KeyboardInterrupt:
        logging.info('User ended workder')
    except Exception as e:
        logging.critical('', exc_info=True)
    if task != None:
        logging.info('Posting status')
        client.post_error(task['uuid'], 'pb_canceled', 'canceled by user')
