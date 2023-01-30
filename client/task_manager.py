from pydoc import cli
import dearpygui.dearpygui as dpg
from client_boilerplate import client as bpclient

client = bpclient(apiKey='', adress='http://127.0.0.1')

dpg.create_context()
dpg.create_viewport(title='te', width=600, height=600)

task_list = client.get_task_list()


def _help(message):
    last_item = dpg.last_item()
    group = dpg.add_group(horizontal=True)
    dpg.move_item(last_item, parent=group)
    dpg.capture_next_item(lambda s: dpg.move_item(s, parent=group))
    t = dpg.add_text("(?)", color=[0, 255, 0])
    with dpg.tooltip(t):
        dpg.add_text(message)


with dpg.window(tag='main_window'):
    # current task list
    with dpg.table(header_row=True, resizable=True, tag='display_list', policy=dpg.mvTable_SizingStretchProp):
        for key in task_list[0]:
            dpg.add_table_column(label=key)
        dpg.add_table_column()

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


dpg.setup_dearpygui()
dpg.show_viewport()
dpg.set_primary_window('main_window', True)
dpg.start_dearpygui()
dpg.destroy_context()
