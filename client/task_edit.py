import dearpygui.dearpygui as dpg
from client_boilerplate import client as bpclient
import utils

config = utils.load_config()
client = bpclient('manager', apiKey=config['server']['key'], adress=config['server']['ip'])

dpg.create_context()
dpg.create_viewport(title=' ', width=600, height=600)

with dpg.theme(tag='todo'):
    with dpg.theme_component(dpg.mvButton):
        dpg.add_theme_color(dpg.mvThemeCol_Button, (15, 86, 135))
with dpg.theme(tag='running'):
    with dpg.theme_component(dpg.mvButton):
        dpg.add_theme_color(dpg.mvThemeCol_Button, (220, 220, 170))
with dpg.theme(tag='done'):
    with dpg.theme_component(dpg.mvButton):
        dpg.add_theme_color(dpg.mvThemeCol_Button, (50, 149, 131))
with dpg.theme(tag='error'):
    with dpg.theme_component(dpg.mvButton):
        dpg.add_theme_color(dpg.mvThemeCol_Button, (230, 20, 20))


# task_list = client.get_task_list()


def get_tasks(prettify: bool = False):
    tasks = client.get_task_list()
    if prettify:
        for id in range(len(tasks)):
            tasks[id].pop('uuid')
            tasks[id].pop('chunks')
    return tasks


def _help(message):
    last_item = dpg.last_item()
    group = dpg.add_group(horizontal=True)
    dpg.move_item(last_item, parent=group)
    dpg.capture_next_item(lambda s: dpg.move_item(s, parent=group))
    t = dpg.add_text("(?)", color=[0, 255, 0])
    with dpg.tooltip(t):
        dpg.add_text(message)


def upload_task():
    task = {'task_name': dpg.get_value('task_name'),
            'blend_file': dpg.get_value('blend_file'),
            'resolution_x': dpg.get_value('resolution_x'),
            'resolution_y': dpg.get_value('resolution_y'),
            'render_engine': dpg.get_value('render_engine'),
            'scene': dpg.get_value('scene'),
            'output_path': dpg.get_value('output_path'),
            'frame_start': dpg.get_value('frame_start'),
            'frame_end': dpg.get_value('frame_end'),
            'frame_step': dpg.get_value('frame_step'),
            'chunks_size': dpg.get_value('chunks_size')
            }
    print(client.post_task(task))


def delete_task(sender, app_data, user_data):
    print(client.post_delete_task(user_data))


with dpg.window(tag='main'):
    # current task list
    task_list = get_tasks()

    with dpg.tab_bar():
        with dpg.tab(label='manager'):

            with dpg.table(header_row=True, resizable=True, tag='display_list', policy=dpg.mvTable_SizingStretchProp):
                for key in task_list[0]:
                    if key == 'uuid' or key == 'chunks' or key == 'errors':
                        continue
                    dpg.add_table_column(label=key)
                dpg.add_table_column(width_fixed=True)

                for task in task_list:
                    with dpg.table_row():
                        for info in task:
                            if info == 'uuid' or info == 'chunks' or info == 'errors':
                                continue
                            dpg.add_text(task[info])
                        with dpg.group(horizontal=True):

                            dpg.add_button(label="Button", arrow=True, direction=dpg.mvDir_Up)
                            dpg.add_button(label="Button", arrow=True, direction=dpg.mvDir_Down)
                            dpg.add_button(label='x', user_data=task['uuid'], callback=delete_task)
            dpg.add_separator()
            # New tasks settings
            dpg.add_input_text(label='Task name', tag='task_name')
            dpg.add_input_text(label='Blend file', tag='blend_file')
            dpg.add_input_text(label='Scene', tag='scene')
            dpg.add_input_text(label='Output path', tag='output_path')
            with dpg.group(horizontal=True):
                dpg.add_input_int(width=120, tag='resolution_x', default_value=1920)
                dpg.add_input_int(width=120, tag='resolution_y', default_value=1080)
                dpg.add_text('resolution')
                _help('resolution x/y')
            with dpg.group(horizontal=True):
                dpg.add_input_int(width=120, tag='frame_start', default_value=1)
                dpg.add_input_int(width=120, tag='frame_end', default_value=250)
                dpg.add_input_int(width=120, tag='frame_step', default_value=1)
                dpg.add_text('frame range')
                _help('frame range : start | end | step')
            dpg.add_input_int(label='Chunk size', tag='chunks_size', default_value=50)
            dpg.add_combo(('CYCLES', 'BLENDER_EEVEE', 'BLENDER_WORKBENCH'), label='Render engine', default_value='CYCLES', tag='render_engine')
            dpg.add_button(label='Post task', callback=upload_task)

# ===================================================
# status tab
        with dpg.tab(label='status'):
            task_list = get_tasks(False)
            for task in task_list:
                with dpg.table(header_row=False):
                    row_count = len(task['chunks'])+1
                    for x in range(row_count):
                        dpg.add_table_column()
                    with dpg.table_row():
                        dpg.add_text(default_value=task['name'])
                        for task in task['chunks']:
                            dpg.add_button(label=task[0], width=-1)
                            if task[1] == 'todo':
                                dpg.bind_item_theme(dpg.last_item(), 'todo')
                            elif task[1] == 'running':
                                dpg.bind_item_theme(dpg.last_item(), 'running')
                            elif task[1] == 'done':
                                dpg.bind_item_theme(dpg.last_item(), 'done')
                            else:
                                dpg.bind_item_theme(dpg.last_item(), 'error')

            dpg.add_separator()
            dpg.add_text('Workers')
            workers = client.get_workers()
            dpg.add_text(workers)

# dpg.configure_app(docking=True)
dpg.setup_dearpygui()
dpg.show_viewport()

dpg.set_primary_window("main", True)
dpg.start_dearpygui()
dpg.destroy_context()
