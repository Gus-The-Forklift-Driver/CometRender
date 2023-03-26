let api_url: string = "";

type TaskStatus = "todo" | "running" | "done" | "error";

export interface Task {
  uuid: string;
  name: string;
  blend_file: string;
  render_size: number[];
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
}
