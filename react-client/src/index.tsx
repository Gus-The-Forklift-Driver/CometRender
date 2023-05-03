import { createTheme, CssBaseline, ThemeProvider } from "@mui/material";
import React from "react";
import ReactDOM from "react-dom/client";
import { API } from "./API";
import { App } from "./App";
import "./index.css";
import reportWebVitals from "./reportWebVitals";

async function init() {
  try {
    // First, load config
    const req = await fetch("/config.json");
    if (req.status !== 200) throw new Error("Could not load config!");
    const serverURL = (await req.json()).server;
    API.setURL(serverURL);

    const root = ReactDOM.createRoot(
      document.getElementById("root") as HTMLElement
    );

    const darkTheme = createTheme({
      palette: {
        mode: "dark",
      },
    });

    root.render(
      <React.StrictMode>
        <ThemeProvider theme={darkTheme}>
          <CssBaseline />
          <App />
        </ThemeProvider>
      </React.StrictMode>
    );

    // If you want to start measuring performance in your app, pass a function
    // to log results (for example: reportWebVitals(console.log))
    // or send to an analytics endpoint. Learn more: https://bit.ly/CRA-vitals
    reportWebVitals();
  } catch (e) {
    console.error(e);
    alert("Failed to init app!");
  }
}

init();
