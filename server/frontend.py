from fastapi import FastAPI
from nicegui import ui


def init(app: FastAPI, task_manager) -> None:
    @ui.page('/show')
    def show():
        test = task_manager.tasks[0]
        ui.label(test)
        with ui.row():
            ui.label(str(test['task_name']))
            ui.label(str(test['blend_file']))
            ui.label(str(test['frame_range']))

    ui.run_with(app)
