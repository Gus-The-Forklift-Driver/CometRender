# https://fastapi.tiangolo.com/tutorial/path-params/
from fastapi import FastAPI, Header
import utils
#import frontend

app = FastAPI()

task_manager = utils.TaskManager()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/ping")
async def ping():
    return 'pong'


@app.get('/next_task')
def next_task(key: str | None = Header(default=None)):
    if utils.verify_key(key):
        next_task = task_manager.get_next_task()
        task_manager.save_current_status()
        return next_task


@app.post('/progress/{task_name}')
def update_progress(task_name: str, status: str | float, key: str | None = Header(default=None)):
    if utils.verify_key(key):
        if status == 'DONE':
            internal_status = task_manager.mark_task_done(task_name)
            task_manager.save_current_status()
            return internal_status
        elif status == 'FAILED':
            internal_status = task_manager.mark_task_failed(task_name)
            task_manager.save_current_status()
            return internal_status
        else:
            return 'wtf'


@app.get('/task_list')
def task_list():
    return task_manager.tasks


#frontend.init(app, task_manager)

if __name__ == '__main__':
    import uvicorn
    uvicorn.run('server:app', reload=True, host='0.0.0.0', port=8000)
