import dearpygui.dearpygui as dpg
from client_boilerplate import client as bpclient
import utils

config = utils.load_config()
client = bpclient('manager', apiKey=config['server']['key'], adress=config['server']['ip'])

dpg.create_context()
dpg.create_viewport(title='Task Edit', width=700, height=600)

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
    dpg.show_item('loading')
    print(sender)
    print(app_data)
    print(user_data)
    print(client.post_move_task(user_data[0], user_data[1]))
    update_table()


def set_chunk_todo(sender, app_data, user_data):
    dpg.show_item('loading')
    print(client.post_set_chunk_todo(user_data))
    update_table()


def update_table():
    dpg.show_item('loading')
    task_list = get_tasks()
    dpg.delete_item('display_list')

    with dpg.table(header_row=True, resizable=True, tag='display_list', policy=dpg.mvTable_SizingStretchProp, parent='list_container'):
        if len(task_list) > 0:
            for key in task_list[0]:
                if key == 'uuid':
                    continue
                dpg.add_table_column(label=key)
            dpg.add_table_column(width_fixed=True)

            for task in task_list:
                with dpg.table_row():
                    for info in task:
                        if info == 'uuid':
                            continue
                        elif info == 'chunks':
                            todo = 0
                            running = 0
                            done = 0
                            error = 0
                            for chunk in task[info]:
                                if chunk[1] == 'todo':
                                    todo += 1
                                if chunk[1] == 'running':
                                    running += 1
                                if chunk[1] == 'chunks_done' or chunk[1] == 'done':
                                    done += 1
                                if chunk[1] == 'error':
                                    error += 1
                            dpg.add_text(f'todo: {todo}|running: {running}|done: {done}')

                        elif info == 'errors':
                            dpg.add_text(f'{len(task[info])}')

                        else:
                            dpg.add_text(task[info])

                    with dpg.group(horizontal=True):

                        dpg.add_button(label="Button", arrow=True, direction=dpg.mvDir_Up, callback=move_task, user_data=[task['uuid'], -1])
                        dpg.add_button(label="Button", arrow=True, direction=dpg.mvDir_Down, callback=move_task, user_data=[task['uuid'], +1])
                        dpg.add_button(label='x', user_data=task['uuid'], callback=delete_task)
                        dpg.add_button(label='set_todo', user_data=task['uuid'], callback=set_chunk_todo)
    dpg.delete_item('worker_container', children_only=True)
    workers = client.get_workers()
    frame_count = 0
    for worker in workers:
        frame_count += workers[worker]

    with dpg.group(parent='worker_container'):
        for worker in workers:
            with dpg.group(horizontal=True):
                dpg.add_text(worker)
                if frame_count != 0:
                    dpg.add_progress_bar(default_value=(workers[worker]/frame_count),
                                         overlay=f'{workers[worker]}/{frame_count}')

    dpg.hide_item('loading')


with dpg.window(tag='main'):
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
    with dpg.group(horizontal=True):
        dpg.add_button(label='Post task', callback=upload_task)
        dpg.add_button(label='update', callback=update_table)
        dpg.add_loading_indicator(show=False, style=1, tag='loading', radius=2, color=(230, 230, 230, 255))
    dpg.add_separator()
    with dpg.group(tag='worker_container'):
        pass


if __name__ == '__main__':
    dpg.setup_dearpygui()
    dpg.show_viewport()
    # dpg.show_imgui_demo()
    update_table()
    dpg.set_primary_window("main", True)

    # a substitute to dpg.start_dearpygui() giving more control
    while dpg.is_dearpygui_running():
        jobs = dpg.get_callback_queue()  # retrieves and clears queue
        dpg.run_callbacks(jobs)
        dpg.render_dearpygui_frame()

    dpg.destroy_context()
