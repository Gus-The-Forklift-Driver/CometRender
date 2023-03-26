import ArrowDownwardIcon from "@mui/icons-material/ArrowDownward";
import ArrowUpwardIcon from "@mui/icons-material/ArrowUpward";
import {
  CircularProgress,
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

export class TasksManager extends React.Component<
  { token: string },
  { tasks?: Task[] }
> {
  constructor(p: any) {
    super(p);

    this.state = {};

    this.load = this.load.bind(this);
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
    );
  }
}

function handleErr(e: any) {
  console.error(e);
  alert("Faild to perform operation!");
}
