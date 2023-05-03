import LockOutlinedIcon from "@mui/icons-material/LockOutlined";
import {
  Avatar,
  Box,
  Button,
  Container,
  CssBaseline,
  TextField,
  Typography,
} from "@mui/material";
import React from "react";
import { API } from "./API";

export function Login(p: {
  onLogin: (key: string) => void;
}): React.ReactElement {
  const [key, setKey] = React.useState("");

  const tryLogin: React.FormEventHandler<HTMLFormElement> = async (e) => {
    e.preventDefault();
    if (!(await API.CheckLogin(key))) alert("Invalid API key!!!");
    else p.onLogin(key);
  };

  return (
    <Container component="main" maxWidth="xs">
      <CssBaseline />
      <Box
        sx={{
          marginTop: 8,
          display: "flex",
          flexDirection: "column",
          alignItems: "center",
        }}
      >
        <Avatar sx={{ m: 1, bgcolor: "secondary.main" }}>
          <LockOutlinedIcon />
        </Avatar>
        <Typography component="h1" variant="h5">
          Sign in
        </Typography>
        <Box component="form" noValidate sx={{ mt: 1 }} onSubmit={tryLogin}>
          <TextField
            margin="normal"
            required
            fullWidth
            label="API key"
            type="text"
            value={key}
            onChange={(event: React.ChangeEvent<HTMLInputElement>) => {
              setKey(event.target.value);
            }}
          />

          <Button
            type="submit"
            fullWidth
            variant="contained"
            disabled={key.length < 3}
            sx={{ mt: 3, mb: 2 }}
          >
            Sign In
          </Button>
        </Box>
      </Box>
    </Container>
  );
}
