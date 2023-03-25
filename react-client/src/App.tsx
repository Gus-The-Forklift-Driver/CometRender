import React from "react";

import "@fontsource/roboto/300.css";
import "@fontsource/roboto/400.css";
import "@fontsource/roboto/500.css";
import "@fontsource/roboto/700.css";
import { Login } from "./Login";
import { Dashboard } from "./Dashboard";

const TOKEN_KEY = "TOKEN";

export class App extends React.Component<{}, { token: string | null }> {
  constructor(p: any) {
    super(p);

    this.state = {
      token: sessionStorage.getItem(TOKEN_KEY),
    };
  }

  render() {
    if (!this.state.token) {
      return (
        <Login
          onLogin={(k) => {
            sessionStorage.setItem(TOKEN_KEY, k);
            this.setState({ token: k });
          }}
        />
      );
    }

    return (
      <Dashboard
        token={this.state.token}
        onLogout={() => {
          sessionStorage.clear();
          this.setState({ token: null });
        }}
      />
    );
  }
}
