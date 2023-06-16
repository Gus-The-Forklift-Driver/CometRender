import dearpygui.dearpygui as dpg
from client_boilerplate import client as bpclient
import utils

config = utils.load_config()
client = bpclient('manager', apiKey=config['server']['key'], adress=config['server']['ip'])

dpg.create_context()
dpg.create_viewport(title=' ', width=600, height=600)

# create interface themes
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
    dpg.show_item('loading')
    task = {'task_name': dpg.get_value('task_name'),
            'blend_file': dpg.get_value('blend_file'),
            'frame_start': dpg.get_value('frame_start'),
            'frame_end': dpg.get_value('frame_end'),
            'chunks_size': dpg.get_value('chunks_size')
            }
    print(client.post_task(task))
    update_table()


def delete_task(sender, app_data, user_data):
    dpg.show_item('loading')
    print(client.post_delete_task(user_data))
    update_table()


def move_task(sender, app_data, user_data):
    print(sender)
    print(app_data)
    print(user_data)


def update_table():
    dpg.show_item('loading')
    task_list = get_tasks()
    dpg.delete_item('display_list')

    with dpg.table(header_row=True, resizable=True, tag='display_list', policy=dpg.mvTable_SizingStretchProp, parent='list_container'):
        if len(task_list) > 0:
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

                        dpg.add_button(label="Button", arrow=True, direction=dpg.mvDir_Up, callback=move_task)
                        dpg.add_button(label="Button", arrow=True, direction=dpg.mvDir_Down, callback=move_task)
                        dpg.add_button(label='x', user_data=task['uuid'], callback=delete_task)
    dpg.hide_item('loading')


def update_list_view():
    dpg.show_item('loading_list')
    task_list = get_tasks()
    dpg.delete_item('list_view_container')
    for task in task_list:
        with dpg.table(header_row=False, parent='list_view_container_top'):
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
                    elif task[1] == 'chunk_done':
                        dpg.bind_item_theme(dpg.last_item(), 'done')
                    else:
                        dpg.bind_item_theme(dpg.last_item(), 'error')

    dpg.hide_item('loading_list')


with dpg.window(tag='main'):
    # current task list
    task_list = get_tasks()

    with dpg.tab_bar():
        with dpg.tab(label='manager', tag='manager'):
            with dpg.group(tag='list_container'):
                pass
            dpg.add_separator()
            # New tasks settings
            dpg.add_input_text(label='Task name', tag='task_name')
            dpg.add_input_text(label='Blend file', tag='blend_file')
            with dpg.group(horizontal=True):
                dpg.add_input_int(width=120, tag='frame_start', default_value=1)
                dpg.add_input_int(width=120, tag='frame_end', default_value=250)

                dpg.add_text('frame range')
                _help('frame range : start | end')
            dpg.add_input_int(label='Chunk size', tag='chunks_size', default_value=50)

            dpg.add_button(label='Post task', callback=upload_task)
            with dpg.group(horizontal=True):
                dpg.add_button(label='update', callback=update_table)
                dpg.add_loading_indicator(show=False, style=1, tag='loading', radius=2, color=(230, 230, 230, 255))

# ===================================================
# status tab

        with dpg.tab(label='status'):
            with dpg.group(tag='list_view_container_top'):
                with dpg.group(tag='list_view_container'):
                    pass
            with dpg.group(horizontal=True):
                dpg.add_button(label='update', callback=update_list_view)
                dpg.add_loading_indicator(show=False, style=1, tag='loading_list', radius=2, color=(230, 230, 230, 255))
            dpg.add_separator()
            dpg.add_text('Workers')
            workers = client.get_workers()
            dpg.add_text(workers)

# dpg.configure_app(docking=True)
dpg.setup_dearpygui()
dpg.show_viewport()
# dpg.show_imgui_demo()

dpg.set_primary_window("main", True)

dpg.start_dearpygui()
dpg.destroy_context()
