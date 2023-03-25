import { AppBar, Toolbar, IconButton, Typography, Button } from "@mui/material";
import React from "react";

export class Dashboard extends React.Component<{
  token: string;
  onLogout: () => any;
}> {
  constructor(p: any) {
    super(p);
  }

  render(): React.ReactNode {
    return (
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
    );
  }
}
