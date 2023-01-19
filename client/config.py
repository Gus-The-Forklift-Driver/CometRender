import json
from multiprocessing.sharedctypes import Value
import shutil
import sys
from textwrap import indent
import dearpygui.dearpygui as dpg
import bpy
from matplotlib.font_manager import json_dump


with open('config.json', 'r') as file:
    config = json.load(file)
    print('Loaded_config : ')
    print(json.dumps(config, indent=4))
if config['blender_bin'] == None or config['blender_bin'] == 'blender not found':
    config['blender_bin'] = shutil.which("blender")
    if config['blender_bin']:
        print("Found:", config['blender_bin'])
        bpy.app.binary_path = config['blender_bin']
    else:
        config['blender_bin'] = 'blender not found'
        print('blender not found')


dpg.create_context()
dpg.create_viewport(title='WorkerConfig', width=600, height=300)


def update_config():
    with open('config.json', 'w') as file:
        json.dump({
            'blender_bin': dpg.get_value('blender_bin'),
            'server_ip': dpg.get_value('server_ip'),
            'api_key': dpg.get_value('api_key'),
            'working_dir': dpg.get_value('working_dir'),
        }, file)


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


with dpg.window(tag='main_window'):
    # blender location
    with dpg.group(horizontal=True):
        dpg.add_input_text(tag='blender_bin', default_value=config['blender_bin'], callback=update_config)
        dpg.add_button(label="Blender.exe location", callback=lambda: dpg.show_item("file_dialog_id"))
    dpg.add_separator()
    # server setup
    dpg.add_input_text(label='Server IP', tag='server_ip', callback=update_config, default_value=config['server_ip'])
    dpg.add_input_text(label='Api key', tag='api_key', callback=update_config, default_value=config['api_key'])
    dpg.add_separator()
    # worker setup
    with dpg.group(horizontal=True):
        dpg.add_input_text(tag='working_dir', default_value=config['working_dir'])
        dpg.add_button(label="Working dir location", callback=lambda: dpg.show_item("folder_dialog_id"))
    dpg.add_separator()

dpg.setup_dearpygui()
dpg.show_viewport()
dpg.set_primary_window('main_window', True)
dpg.start_dearpygui()
dpg.destroy_context()
