import json
import platform
import yaml
import shutil
import dearpygui.dearpygui as dpg
import bpy
import utils

default_config = {
    "client": {
        "blender_bin": "blender not found",
        "name": "worker00",
        "working_dir": "./"
    },
    "server": {
        "ip": "http://127.0.0.1:8000",
        "key": "demo"
    }
}

try:
    config = utils.load_config('./config.yml')
except:
    config = default_config

config['client']['name'] = platform.node()
print(json.dumps(config, indent=4))
# try to detect blender location
if config['client']['blender_bin'] == '' or config['client']['blender_bin'] == 'blender not found':
    config['client']['blender_bin'] = shutil.which("blender")
    if config['client']['blender_bin']:
        print("Found:", config['client']['blender_bin'])
        bpy.app.binary_path = config['client']['blender_bin']
    else:
        config['client']['blender_bin'] = 'blender not found'
        print('blender not found')


dpg.create_context()
dpg.create_viewport(title='WorkerConfig', width=600, height=300)


"""def update_config():
    with open('config.json', 'w') as file:
        json.dump({
            'blender_bin': dpg.get_value('blender_bin'),
            'server_ip': dpg.get_value('server_ip'),
            'api_key': dpg.get_value('api_key'),
            'working_dir': dpg.get_value('working_dir'),
        }, file)
"""

# file dialog


def file_callback(sender, app_data) -> None:
    # print('OK was clicked.')
    # print("Sender: ", sender)
    # print("App Data: ", app_data)
    dpg.set_value('blender_bin', app_data['file_path_name'])


with dpg.file_dialog(
        directory_selector=False, show=False, callback=file_callback, tag="file_dialog_id"):
    dpg.add_file_extension(".exe", color=(0, 255, 0, 255))
    dpg.add_file_extension(".*")
# end of file dialog

# folder dialog


def folder_callback(sender, app_data) -> None:
    # print('OK was clicked.')
    # print("Sender: ", sender)
    # print("App Data: ", app_data)
    dpg.set_value('working_dir', app_data['file_path_name'])


with dpg.file_dialog(
        directory_selector=True, show=False, callback=folder_callback, tag="folder_dialog_id"):
    pass
# end of file dialog


def update_config():
    new_config = {}
    for category in config:
        new_config[category] = {}
        for setting in config[category]:
            new_config[category][setting] = dpg.get_value(category + '/'+setting)
            print(category + '/'+setting)
    utils.save_config(new_config)


with dpg.window(tag='main_window'):
    for category in config:
        dpg.add_text(f'== {category} ==')
        for setting in config[category]:
            with dpg.group(horizontal=True):
                dpg.add_text(setting)
                dpg.add_input_text(default_value=config[category][setting], callback=update_config, tag=category + '/'+setting)
        dpg.add_separator()
    dpg.add_button(label='update_config', callback=update_config)

dpg.setup_dearpygui()
dpg.show_viewport()
dpg.set_primary_window('main_window', True)
dpg.start_dearpygui()
dpg.destroy_context()
