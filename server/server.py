# https://fastapi.tiangolo.com/tutorial/path-params/
from email.policy import default
import json
from pickle import TRUE

from fastapi import Body, FastAPI, Header, Query
from pydantic import BaseModel
import utils
import task_manager

app = FastAPI(docs_url=None, redoc_url=None)

task_manager = task_manager.TaskManager()
task_manager.load_tasks_from_file()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/ping")
async def ping():
    return 'pong'


@app.get('/next_task')
def next_task(key: str | None = Header(default=None)):
    if utils.verify_key(key):
        next_task, chunk = task_manager.get_next_task()
        if next_task != None:
            task_manager.save_tasks_to_file()
        return next_task, chunk


@app.post('/progress/{task_uuid}')
def update_progress(task_uuid: str, chunk: str | float, status: str | float, worker_name: str, key: str | None = Header(default=None)):
    if utils.verify_key(key):
        chunk = list(eval(chunk))
        task_manager.change_chunk_status(task_uuid, chunk, status)
        task_manager.add_worker(worker_name)


@app.post('/error/{task_uuid}')
async def add_error(*, task_uuid: str, data=Body(), key: str | None = Header(default=None)):
    if utils.verify_key(key):
        task_manager.log_error(task_uuid, data)
        return


@app.post('/new_task')
def add_task(data=Body(), key: str | None = Header(default=None)):
    if utils.verify_key(key):
        task_manager.add_task_by_dict(data)
    else:
        return "Invalid auth"


@app.get('/task_list')
async def task_list():
    return task_manager.tasks


@app.get('/task_names')
async def task_list():
    return task_manager.get_tasks_names()


@app.get('/workers')
async def workers():
    return task_manager.workers


@app.post('/move_task/{task_uuid}')
def move_task(task_uuid: str, offset: str, key: str | None = Header(default=None)):
    if utils.verify_key(key):
        task_manager.move_task(task_uuid, offset)
    return


@app.get('task_status')
async def task_status():
    return task_manager.get_task_status()

if __name__ == '__main__':
    import uvicorn
    uvicorn.run('server:app', reload=True, host='0.0.0.0', port=8000)
