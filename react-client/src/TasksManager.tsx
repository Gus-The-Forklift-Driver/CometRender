import ArrowDownwardIcon from "@mui/icons-material/ArrowDownward";
import ArrowUpwardIcon from "@mui/icons-material/ArrowUpward";
import {
  Button,
  CircularProgress,
  Dialog,
  DialogActions,
  DialogContent,
  DialogTitle,
  IconButton,
  Paper,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
} from "@mui/material";
import React, { ReactNode } from "react";
import { API, Task } from "./API";
import { TaskEdit } from "./TaskEdit";

export class TasksManager extends React.Component<
  { token: string },
  { tasks?: Task[]; createDialog: boolean; currTask: Task; v: number }
> {
  constructor(p: any) {
    super(p);

    this.state = { createDialog: false, currTask: {} as any, v: 0 };

    this.load = this.load.bind(this);
    this.closeDialog = this.closeDialog.bind(this);
    this.createTask = this.createTask.bind(this);
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

  closeDialog() {
    this.setState({ createDialog: false });
    this.load();
  }

  async createTask() {
    try {
      await API.CreateTask(this.props.token, this.state.currTask);
      this.setState({ currTask: {} as any, createDialog: false });
      this.load();
      alert("Task created");
    } catch (e) {
      console.error(e);
      alert("Failed to create task");
    }
  }

  render(): ReactNode {
    if (!this.state.tasks) return <CircularProgress />;

    return (
      <>
        <div
          style={{
            display: "flex",
            flexDirection: "row",
            justifyContent: "end",
          }}
        >
          <Button onClick={() => this.setState({ createDialog: true })}>
            New task
          </Button>
        </div>
        <TableContainer component={Paper}>
          <Table sx={{ minWidth: 650 }} aria-label="simple table">
            <TableHead>
              <TableRow>
                <TableCell>Task name</TableCell>
                <TableCell>Blend file</TableCell>
                <TableCell>Engine</TableCell>
                <TableCell>View layer</TableCell>
                <TableCell>Passes</TableCell>
                <TableCell>Frame step</TableCell>
                <TableCell>Output path</TableCell>
                <TableCell>Errors</TableCell>
                <TableCell></TableCell>
              </TableRow>
            </TableHead>
            <TableBody>
              {this.state.tasks.map((t, idx) => (
                <TableRow hover key={t.uuid}>
                  <TableCell component="th" scope="row">
                    {t.name}
                  </TableCell>
                  <TableCell>{t.blend_file}</TableCell>
                  <TableCell>{t.render_engine}</TableCell>
                  <TableCell>{t.view_layer}</TableCell>
                  <TableCell>{t.passes}</TableCell>
                  <TableCell>{t.frame_step}</TableCell>
                  <TableCell>{t.output_path}</TableCell>
                  <TableCell>{JSON.stringify(t.errors)}</TableCell>
                  <TableCell>
                    <IconButton
                      disabled={idx === 0}
                      onClick={() =>
                        API.MoveTask(this.props.token, t, idx + 1)
                          .then(this.load)
                          .catch(handleErr)
                      }
                    >
                      <ArrowUpwardIcon />
                    </IconButton>

                    <IconButton
                      disabled={idx + 1 === this.state.tasks?.length}
                      onClick={() =>
                        API.MoveTask(this.props.token, t, idx - 1)
                          .then(this.load)
                          .catch(handleErr)
                      }
                    >
                      <ArrowDownwardIcon />
                    </IconButton>
                  </TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </TableContainer>

        {/* Create entry dialog */}
        <Dialog open={this.state.createDialog} onClose={this.closeDialog}>
          <DialogTitle>New task</DialogTitle>
          <DialogContent>
            <TaskEdit
              t={this.state.currTask}
              onChange={() => this.setState({ v: this.state.v + 1 })}
            />
          </DialogContent>
          <DialogActions>
            <Button onClick={this.createTask}>Create</Button>
          </DialogActions>
        </Dialog>
      </>
    );
  }
}

function handleErr(e: any) {
  console.error(e);
  alert("Faild to perform operation!");
}
