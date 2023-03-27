import { CircularProgress, Tooltip } from "@mui/material";
import React from "react";
import { ReactNode } from "react";
import { API, Task } from "./API";

export class TasksStatus extends React.Component<
  { token: string },
  { tasks?: Task[] }
> {
  constructor(p: any) {
    super(p);

    this.state = {};
  }

  componentDidMount() {
    this.load();
  }

  async load() {
    try {
      this.setState({ tasks: undefined });
      const tasks = await API.GetTasksList(this.props.token);
      this.setState({ tasks: tasks });
    } catch (e) {
      console.error(e);
      alert("Failed to load tasks list!");
    }
  }

  render(): ReactNode {
    if (!this.state.tasks) return <CircularProgress />;

    return (
      <div>
        {this.state.tasks.map((t) => (
          <div style={{ display: "flex", flexDirection: "row" }} key={t.uuid}>
            <div style={{ width: "150px", fontWeight: "bold" }}>{t.name}</div>
            <div style={{ display: "flex", flex: 1, flexDirection: "row" }}>
              {t.chunks.map((c, num) => (
                <Tooltip title={`${c[0][0]}-${c[0][1]}: ${c[1]}`}>
                  <div
                    key={num}
                    style={{
                      flex: c[0][1] - c[0][0],
                      backgroundColor:
                        c[1] === "error"
                          ? "red"
                          : c[1] === "running"
                          ? "blue"
                          : c[1] === "done"
                          ? "green"
                          : "gray",
                      height: "1em",
                    }}
                  ></div>
                </Tooltip>
              ))}
            </div>
          </div>
        ))}
      </div>
    );
  }
}
