# https://fastapi.tiangolo.com/tutorial/path-params/
from fastapi import FastAPI, Header
import utils
#import frontend
import task_manager

app = FastAPI()

task_manager = task_manager.TaskManager()


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
        task_manager.save_tasks_to_file()
        return next_task, chunk


@app.post('/progress/{task_uuid}')
def update_progress(task_uuid: str, chunk: str | float, status: str | float, key: str | None = Header(default=None)):
    if utils.verify_key(key):
        chunk = list(eval(chunk))
        task_manager.change_chunk_status(task_uuid, chunk, status)


@app.get('/task_list')
def task_list():
    return task_manager.tasks


@app.get('/task_names')
def task_list():
    return task_manager.get_tasks_names()


#frontend.init(app, task_manager)

if __name__ == '__main__':
    import uvicorn
    uvicorn.run('server:app', reload=True, host='0.0.0.0', port=8000)
