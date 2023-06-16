# https://fastapi.tiangolo.com/tutorial/path-params/
import os
from fastapi import Body, FastAPI, HTTPException, Header
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
import utils
import task_manager

data_folder = 'D:/OneDrive - Groupe E.D.H/CometTest/'

app = FastAPI(docs_url=None, redoc_url=None)

origins = [
    "http://localhost",
    "http://localhost:3000",
    "http://localhost:8000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


task_manager = task_manager.TaskManager()

if os.path.exists('./current_status.json'):
    task_manager.load_tasks_from_file('./current_status.json')
else:
    task_manager.load_tasks_from_file('./task_list.json')

# task_manager.load_tasks_from_file('./task_list.json')


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get('/files/{file_path:path}')
async def read_file(file_path: str, key: str | None = Header(default=None)):
    if utils.verify_key(key):
        if os.path.isfile(data_folder + file_path):
            return FileResponse(data_folder + file_path)
        else:
            raise HTTPException(status_code=404, detail="File does not exist")
    else:
        raise HTTPException(status_code=400, detail="Bad request")


@ app.get("/ping")
async def ping():
    return 'pong'


@ app.get("/check_login")
def check_login(key: str | None = Header(default=None)):
    if utils.verify_key(key):
        return key


@ app.get('/next_task')
def next_task(key: str | None = Header(default=None), workername: str | None = Header(default=None)):
    if utils.verify_key(key):
        task_manager.add_worker(workername, 0)
        next_task, chunk = task_manager.get_next_task(workername)
        if next_task != None:
            task_manager.save_tasks_to_file()
        return next_task, chunk
    else:
        raise HTTPException(status_code=400, detail="Bad request")


@ app.post('/progress/{task_uuid}')
def update_progress(task_uuid: str, chunk: str | float, status: str | float, worker_name: str, key: str | None = Header(default=None)):
    if utils.verify_key(key):
        chunk = list(eval(chunk))
        task_manager.change_chunk_status(task_uuid, chunk, status)
        if status == 'chunks_done':
            frames = chunk[1]-chunk[0]
        else:
            frames = 0
        task_manager.add_worker(worker_name, frames)


@ app.post('/error/{task_uuid}')
async def add_error(*, task_uuid: str, data=Body(), key: str | None = Header(default=None)):
    if utils.verify_key(key):
        task_manager.log_error(task_uuid, data)
        task_manager.save_tasks_to_file()
        return


@ app.post('/new_task')
def add_task(data=Body(), key: str | None = Header(default=None)):
    if utils.verify_key(key):
        task_manager.add_task_by_settings(data)
        task_manager.save_tasks_to_file()
    else:
        raise HTTPException(status_code=400, detail="Bad request")


@ app.get('/task_list')
async def task_list():
    return task_manager.tasks


@ app.get('/task_names')
async def task_list():
    return task_manager.get_tasks_names()


@ app.get('/workers')
async def workers():
    return task_manager.workers


@ app.post('/move_task/{task_uuid}')
def move_task(task_uuid: str, offset: int, key: str | None = Header(default=None)):
    if utils.verify_key(key):
        task_manager.move_task(task_uuid, offset)
    return


@ app.post('/clean_workers/{task_uuid}')
def move_task(task_uuid: str, key: str | None = Header(default=None)):
    if utils.verify_key(key):
        task_manager.clean_workers(task_uuid)
    return


@ app.get('/task_status')
async def task_status():
    return task_manager.get_task_status()


@ app.post('/delete_task/{task_uuid}')
def delete_task(task_uuid: str, key: str | None = Header(default=None)):
    if utils.verify_key(key):
        task_manager.delete_task(task_uuid)
        task_manager.save_tasks_to_file()
    else:
        raise HTTPException(status_code=400, detail="Bad request")


if __name__ == '__main__':
    import uvicorn
    uvicorn.run('server:app', reload=True, host='0.0.0.0', port=8000)
