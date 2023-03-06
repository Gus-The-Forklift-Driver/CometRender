from re import T
import dearpygui.dearpygui as dpg
from client_boilerplate import client as bpclient

client = bpclient('manager', apiKey='', adress='http://127.0.0.1:8000')

dpg.create_context()
dpg.create_viewport(title=' ', width=600, height=600)

task_list = client.get_task_list()


def get_tasks(prettify: bool = True):
    tasks = client.get_task_list()
    if prettify:
        for id in range(len(tasks)):
            tasks[id].pop('uuid')
            tasks[id].pop('chunks_todo')
            tasks[id].pop('chunks_running')
            tasks[id].pop('chunks_done')
            tasks[id].pop('chunks_error')
    return tasks


def _help(message):
    last_item = dpg.last_item()
    group = dpg.add_group(horizontal=True)
    dpg.move_item(last_item, parent=group)
    dpg.capture_next_item(lambda s: dpg.move_item(s, parent=group))
    t = dpg.add_text("(?)", color=[0, 255, 0])
    with dpg.tooltip(t):
        dpg.add_text(message)


with dpg.window(tag='manager'):
    # current task list
    task_list = get_tasks()
    with dpg.table(header_row=True, resizable=True, tag='display_list', policy=dpg.mvTable_SizingStretchProp):
        for key in task_list[0]:
            dpg.add_table_column(label=key)
        dpg.add_table_column(width_fixed=True)

        for task in task_list:
            with dpg.table_row():
                for info in task:
                    dpg.add_text(task[info])
                with dpg.group(horizontal=True):

                    dpg.add_button(label="Button", arrow=True, direction=dpg.mvDir_Up)
                    dpg.add_button(label="Button", arrow=True, direction=dpg.mvDir_Down)
                    dpg.add_button(label='x')
    dpg.add_separator()
    dpg.add_input_text(label='Task name')
    dpg.add_input_text(label='Blend file')
    dpg.add_input_text(label='View layer')
    with dpg.group(horizontal=True,):
        dpg.add_input_int(width=120)
        dpg.add_input_int(width=120)
        dpg.add_input_int(width=120)
        dpg.add_text('frame range')
        _help('1 : start\n'
              '2 : end\n'
              '3 : step\n')
    dpg.add_combo(('CYCLES', 'BLENDER_EEVEE', 'BLENDER_WORKBENCH'), label='Render engine', default_value='CYCLES')
# status window

with dpg.theme(tag='todo'):
    with dpg.theme_component(dpg.mvButton):
        dpg.add_theme_color(dpg.mvThemeCol_Button, (120, 184, 221))

with dpg.theme(tag='running'):
    with dpg.theme_component(dpg.mvButton):
        dpg.add_theme_color(dpg.mvThemeCol_Button, (220, 220, 170))

with dpg.theme(tag='done'):
    with dpg.theme_component(dpg.mvButton):
        dpg.add_theme_color(dpg.mvThemeCol_Button, (50, 149, 131))

with dpg.window(tag='status'):
    task_list = get_tasks(False)
    for task in task_list:
        with dpg.table(header_row=False):
            row_count = len(task['chunks_todo'])+len(task['chunks_running'])+len(task['chunks_done'])+1
            for x in range(row_count):
                dpg.add_table_column()
            with dpg.table_row():
                dpg.add_text(default_value=task['name'])
                for todo in task['chunks_todo']:
                    dpg.add_button(label=todo, width=-1)
                    dpg.bind_item_theme(dpg.last_item(), 'todo')
                for running in task['chunks_running']:
                    dpg.add_button(label=running, width=-1)
                    dpg.bind_item_theme(dpg.last_item(), 'running')
                for running in task['chunks_done']:
                    dpg.add_button(label=running, width=-1)
                    dpg.bind_item_theme(dpg.last_item(), 'done')
        dpg.add_separator()

dpg.setup_dearpygui()
dpg.show_viewport()
# dpg.set_primary_window('manager', True)
dpg.start_dearpygui()
dpg.destroy_context()
