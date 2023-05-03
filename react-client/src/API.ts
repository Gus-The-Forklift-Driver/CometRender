let api_url: string = "";

type TaskStatus = "todo" | "running" | "done" | "error";

export interface Task {
  uuid: string;
  name: string;
  blend_file: string;
  render_size: [number, number];
  render_engine: string;
  view_layer: string;
  passes: string;
  frame_step: number;
  output_path: string;
  errors: string[];
  chunks: [[number, number], TaskStatus][];
}

export class API {
  static setURL(url: string) {
    api_url = url;
  }

  static async CheckLogin(key: string): Promise<boolean> {
    const req = await fetch(`${api_url}/check_login`, {
      headers: { key: key },
    });

    return (await req.json()) === true;
  }

  static async GetTasksList(key: string): Promise<Task[]> {
    const req = await fetch(`${api_url}/task_list`, {
      headers: { key: key },
    });

    return await req.json();
  }

  static async MoveTask(
    key: string,
    task: Task,
    new_offset: number
  ): Promise<void> {
    const req = await fetch(
      `${api_url}/move_task/${task.uuid}?offset=${new_offset}`,
      {
        method: "POST",
        headers: { key: key },
      }
    );

    return await req.json();
  }

  static async CreateTask(key: string, task: Task): Promise<void> {
    task.uuid = generateUUID();

    const req = await fetch(`${api_url}/new_task`, {
      method: "POST",
      headers: { key: key, "Content-Type": "application/json" },
      body: JSON.stringify(task),
    });

    return await req.json();
  }
}

function generateUUID(): string {
  // Public Domain/MIT
  var d = new Date().getTime(); //Timestamp
  var d2 =
    (typeof performance !== "undefined" &&
      performance.now &&
      performance.now() * 1000) ||
    0; //Time in microseconds since page-load or 0 if unsupported
  return "xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx".replace(/[xy]/g, function (c) {
    var r = Math.random() * 16; //random number between 0 and 16
    if (d > 0) {
      //Use timestamp until depleted
      r = (d + r) % 16 | 0;
      d = Math.floor(d / 16);
    } else {
      //Use microseconds since page-load if supported
      r = (d2 + r) % 16 | 0;
      d2 = Math.floor(d2 / 16);
    }
    return (c === "x" ? r : (r & 0x3) | 0x8).toString(16);
  });
}
