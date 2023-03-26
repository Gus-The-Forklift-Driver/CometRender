import { TabContext, TabList, TabPanel } from "@mui/lab";
import {
  AppBar,
  Toolbar,
  IconButton,
  Typography,
  Button,
  Box,
  Tab,
} from "@mui/material";
import React from "react";
import { TasksManager } from "./TasksManager";
import { TasksStatus } from "./TasksStatus";

export class Dashboard extends React.Component<
  {
    token: string;
    onLogout: () => any;
  },
  { tab: "status" | "task-manager" }
> {
  constructor(p: any) {
    super(p);
    this.state = { tab: "status" };
  }

  render(): React.ReactNode {
    return (
      <>
        <AppBar position="static">
          <Toolbar>
            <Typography variant="h6" component="div" sx={{ flexGrow: 1 }}>
              CometRender
            </Typography>
            <Button color="inherit" onClick={this.props.onLogout}>
              Sign out
            </Button>
          </Toolbar>
        </AppBar>
        <TabContext value={this.state.tab}>
          <Box sx={{ borderBottom: 1, borderColor: "divider" }}>
            <TabList
              onChange={(_ev, v) => {
                this.setState({ tab: v });
              }}
            >
              <Tab label="Status" value="status" />
              <Tab label="Tasks manager" value="task-manager" />
            </TabList>
          </Box>
          <TabPanel value="status">
            <TasksStatus token={this.props.token} />
          </TabPanel>
          <TabPanel value="task-manager">
            <TasksManager token={this.props.token} />
          </TabPanel>
        </TabContext>
      </>
    );
  }
}
