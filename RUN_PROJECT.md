# Run RubixCubeSolver

## For development

From the project root:

```bash
./start_backend.command
```

Then open the Unity project and press Play.

## For a Mac build

Build the Unity app into a folder like:

```text
Builds/MacFinal/
```

That folder should contain:

```text
RubixCubeSolver.app
backend/
requirements.txt
start_backend.command
```

Copy those support files into the build folder. Do not move them out of the project root.

The first run may take a while because Python dependencies are installed into `.venv`.

## For Windows

Use the same folder layout, but include:

```text
RubixCubeSolver.exe
backend/
requirements.txt
start_backend.bat
```

Run `start_backend.bat`, then open the Unity app.
