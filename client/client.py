from time import sleep
from client_boilerplate import client as bpclient
import bpy

client = bpclient(apiKey='DEMO')

while True:
    try:
        r = client.ping()
    except:
        # Maybe set up for a retry, or continue in a retry loop
        print('failed to connect, retring in 10 secs')
        sleep(10)
        continue
    break

while True:
    next_task = client.get_next_task()
    if next_task == None:
        break
    else:
        task_name = next_task['task_name']
        print(f'starting {next_task}')

        try:
            bpy.ops.wm.open_mainfile(filepath=f'./test/{task_name}.blend')
            bpy.ops.render.render(write_still=True)
        except:
            client.post_progress(task_name, 'FAILED')
        else:
            client.post_progress(task_name, 'DONE')

print('==DONE==')
