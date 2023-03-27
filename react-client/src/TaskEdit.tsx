import { MenuItem, Select, TextField } from "@mui/material";
import { Task } from "./API";

export function TaskEdit(p: {
  t: Task;
  onChange: () => void;
}): React.ReactElement {
  if (!p.t.render_size) p.t.render_size = [0, 0];
  if (!p.t.render_engine) p.t.render_engine = "CYCLES";
  if (!p.t.frame_step) p.t.frame_step = 1;
  if (!p.t.errors) p.t.errors = [];
  if (!p.t.chunks) {
    p.t.chunks = [];
    for (let index = 0; index < 10; index++) {
      p.t.chunks.push([[index * 10 + 1, (index + 1) * 10 + 1], "todo"]);
    }
  }

  return (
    <div
      style={{
        display: "flex",
        flexDirection: "column",
        minHeight: "300px",
        justifyContent: "space-around",
      }}
    >
      <TextField disabled label="UUID" variant="outlined" value={p.t.uuid} />

      <TextField
        label="Name"
        variant="outlined"
        value={p.t.name ?? ""}
        onChange={(e) => {
          p.t.name = e.target.value;
          p.onChange();
        }}
      />

      <TextField
        label="Blend file"
        variant="outlined"
        value={p.t.blend_file ?? ""}
        onChange={(e) => {
          p.t.blend_file = e.target.value;
          p.onChange();
        }}
      />

      <div>
        <TextField
          label="Render width"
          variant="outlined"
          value={p.t.render_size[0].toString()}
          onChange={(e) => {
            p.t.render_size[0] = Number(e.target.value);
            p.onChange();
          }}
        />

        <TextField
          label="Render height"
          variant="outlined"
          value={p.t.render_size[1].toString()}
          onChange={(e) => {
            p.t.render_size[1] = Number(e.target.value);
            p.onChange();
          }}
        />
      </div>

      <Select
        value={p.t.render_engine}
        label="Render engine"
        onChange={(e) => {
          p.t.render_engine = e.target.value;
          p.onChange();
        }}
      >
        <MenuItem value={"CYCLES"}>CYCLES</MenuItem>
        <MenuItem value={"BLENDER_EEVEE"}>BLENDER_EEVEE</MenuItem>
        <MenuItem value={"BLENDER_WORKBENCH"}>BLENDER_WORKBENCH</MenuItem>
      </Select>

      <TextField
        label="View layer"
        variant="outlined"
        value={p.t.view_layer ?? ""}
        onChange={(e) => {
          p.t.view_layer = e.target.value;
          p.onChange();
        }}
      />

      <TextField
        label="Passes"
        variant="outlined"
        value={p.t.passes ?? ""}
        onChange={(e) => {
          p.t.passes = e.target.value;
          p.onChange();
        }}
      />

      <TextField
        label="Frame step"
        variant="outlined"
        value={p.t.frame_step}
        onChange={(e) => {
          p.t.frame_step = Number(e.target.value);
          p.onChange();
        }}
      />

      <TextField
        label="Output path"
        variant="outlined"
        value={p.t.output_path}
        onChange={(e) => {
          p.t.output_path = e.target.value;
          p.onChange();
        }}
      />

      <TextField
        label="Chunks"
        variant="outlined"
        value={JSON.stringify(p.t.chunks)}
        onChange={(e) => {
          try {
            p.t.chunks = JSON.parse(e.target.value);
            p.onChange();
          } catch (e) {
            console.error(e);
          }
        }}
      />
    </div>
  );
}
