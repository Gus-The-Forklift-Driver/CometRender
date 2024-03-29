import json
import platform

import requests
import dearpygui.dearpygui as dpg
import utils

import os

default_config = {
    "worker": {
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
    print('coudnt load config, default one loaded')
    config = default_config

config['worker']['name'] = platform.node()
print(json.dumps(config, indent=4))

config['worker']['blender_bin'] = utils.locate_blender()

dpg.create_context()
dpg.create_viewport(title='WorkerConfig', width=1000, height=600)


# file dialog
def file_callback(sender, app_data) -> None:
    # print('OK was clicked.')
    # print("Sender: ", sender)
    # print("App Data: ", app_data)
    dpg.set_value('worker/blender_bin', app_data['file_path_name'])
    update_config()


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
    dpg.set_value('worker/working_dir', app_data['file_path_name'])
    update_config()


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
    utils.save_config(new_config)


def ping_server():
    dpg.set_value('ping_status', 'pinging ...')
    try:
        r = requests.get(url=f'{dpg.get_value("server/ip")}/ping', headers={'key': dpg.get_value("server/key")})
        if r.status_code == 200:
            dpg.set_value('ping_status', 'OK')
        else:
            dpg.set_value('ping_status', 'key error ?')
    except:
        dpg.set_value('ping_status', 'error')


def enable_onedrive():
    import pyuac
    import winreg
    if not pyuac.isUserAdmin():
        print("Re-launching as admin!")
        pyuac.runAsAdmin()
    else:
        key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, 'SOFTWARE\Policies\Microsoft\Windows\OneDrive', access=winreg.KEY_READ | winreg.KEY_WOW64_64KEY)
        value = winreg.QueryValueEx(key, 'DisableFileSyncNGSC')
        print(value)
        winreg.SetValueEx(key, 'DisableFileSyncNGSC', 0, 4, 0)
        value = winreg.QueryValueEx(key, 'DisableFileSyncNGSC')
        print(value)


with dpg.window(tag='main_window'):
    for category in config:
        dpg.add_text(f'== {category} ==')
        for setting in config[category]:
            with dpg.group(horizontal=True):
                dpg.add_text(setting)
                dpg.add_input_text(default_value=config[category][setting], callback=update_config, tag=category + '/'+setting)
                if setting == 'blender_bin':
                    dpg.add_button(label='select bin', callback=lambda: dpg.show_item('file_dialog_id'))
                if setting == 'working_dir':
                    dpg.add_button(label='select folder', callback=lambda: dpg.show_item('folder_dialog_id'))
        dpg.add_separator()
    dpg.add_button(label='update_config', callback=update_config)
    with dpg.group(horizontal=True):
        dpg.add_button(label='Ping Server', callback=ping_server)
        dpg.add_text('/', tag='ping_status')
    # dpg.add_button(label='Enable Onedrive', callback=enable_onedrive)

dpg.setup_dearpygui()
dpg.show_viewport()
dpg.set_primary_window('main_window', True)
dpg.start_dearpygui()
dpg.destroy_context()
