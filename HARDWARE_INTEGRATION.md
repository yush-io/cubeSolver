# Hardware Integration Handoff

This branch is for continuing the Rubix Cube Solver as a real physical machine. The existing project already handles the computer science side:

- Capturing six cube-face images through the Unity frontend.
- Sending those images to a local FastAPI backend.
- Detecting the 9 stickers on each face.
- Mapping sticker colors into a valid cube state.
- Solving the cube with Kociemba.
- Returning a move sequence such as `R U R' U'`.

The mechanical/electrical system does not need to reimplement computer vision or cube solving unless the team intentionally chooses to. The clean integration point is the final solution sequence.

## Current System Overview

The project has two main parts:

```text
Unity frontend
  - Camera UI
  - Takes six photos in guided order
  - Sends photos to backend
  - Receives solution sequence
  - Visualizes moves on a 3D cube

Python FastAPI backend
  - Receives six uploaded images
  - Runs YOLOv8 sticker detection
  - Maps sticker colors
  - Builds Kociemba cube string
  - Validates cube state
  - Returns solution moves
```

Main data flow:

```text
Physical cube
  -> Unity camera capture
  -> POST /upload-photos
  -> YOLOv8 sticker detection
  -> color mapping
  -> Kociemba solver
  -> JSON solution response
  -> Unity SolutionStore.LatestSolution
  -> 3D move visualization
  -> future hardware controller
```

## Important Files

Frontend:

- `Assets/PhotoManager.cs`
  - Controls the scan flow.
  - Prompts the user for the six required cube faces.
  - Calls the backend through `APIClient`.
  - Stores the returned solution in `SolutionStore.LatestSolution`.

- `Assets/Scripts/APIClient.cs`
  - Sends the six captured images to the backend endpoint.
  - Expects a JSON response containing a solution array.

- `Assets/Scripts/SolutionStore.cs`
  - Holds the latest solution sequence:

```csharp
public static string[] LatestSolution;
```

- `Assets/Scripts/cubeRotater.cs`
  - Reads `SolutionStore.LatestSolution`.
  - Applies the solution moves to the Unity cube visualization.

Backend:

- `backend/main_API.py`
  - Defines the main endpoint: `POST /upload-photos`.
  - Receives six files named `files`.
  - Returns a JSON solution.

- `backend/StickerDetector.py`
  - Runs sticker detection.

- `backend/ColorMapper.py`
  - Converts sticker image crops into cube color labels.

- `backend/cube_validator.py`
  - Validates that the cube state is physically possible.

- `backend/KociembaSolver.py`
  - Calls the Kociemba solver and returns the move sequence.

Deployment helpers:

- `start_backend.command`
  - Mac backend startup script.

- `start_backend.bat`
  - Windows backend startup script.

- `requirements.txt`
  - Python dependencies.

## Current Backend API Contract

### Endpoint

```http
POST http://127.0.0.1:8000/upload-photos
```

### Request

The request must contain exactly six uploaded image files using the repeated form field name `files`.

Conceptually:

```text
files = face_0.png
files = face_1.png
files = face_2.png
files = face_3.png
files = face_4.png
files = face_5.png
```

### Required Face Order

The current scan order is fixed and important:

```text
1. WHITE center
2. RED center
3. GREEN center
4. YELLOW center
5. ORANGE center
6. BLUE center
```

This order maps to the solver orientation:

```text
W = Up
R = Right
G = Front
Y = Down
O = Left
B = Back
```

The backend assumes this guided order when constructing the cube state.

### Successful Response

The backend currently returns:

```json
{
  "Solution": ["R", "U", "R'", "U'"]
}
```

Unity also accepts the lowercase form:

```json
{
  "solution": ["R", "U", "R'", "U'"]
}
```

The hardware team should treat the solution as an ordered list of moves.

### Error Responses

Common failure cases:

- Fewer or more than six photos were uploaded.
- The backend detected fewer than 9 stickers on one face.
- The colors did not form a valid cube state.
- Kociemba could not solve the generated cube state.

Example sticker detection error:

```json
{
  "status": "error",
  "reason": "detected fewer than 9 stickers",
  "detected": 7,
  "face_index": 2
}
```

## Move Notation

The solution uses standard 3x3 Rubik's cube notation.

Basic face moves:

```text
U = Up face clockwise
D = Down face clockwise
R = Right face clockwise
L = Left face clockwise
F = Front face clockwise
B = Back face clockwise
```

Prime moves:

```text
U' = Up face counterclockwise
R' = Right face counterclockwise
F' = Front face counterclockwise
```

Double moves:

```text
U2 = Up face 180 degrees
R2 = Right face 180 degrees
F2 = Front face 180 degrees
```

Important mechanical convention:

Clockwise and counterclockwise are defined as if you are looking directly at that face from outside the cube. For example, `R` means rotate the right face clockwise as viewed from the right side of the cube.

## What The Hardware Team Needs To Decide

The CS solver outputs abstract cube moves. The physical machine needs a lower-level translation layer.

The hardware team should define:

- How the cube is physically held.
- Which cube face is considered front in the machine.
- Which motors control which faces or grippers.
- Whether the machine rotates faces directly or reorients the whole cube between moves.
- How one abstract move maps to one or more motor commands.
- How to detect that a move finished successfully.
- What to do if a motor stalls or the cube slips.

Recommended architecture:

```text
Solver output:
  ["R", "U", "R'", "U'"]

Hardware planner:
  Converts cube notation into machine actions.

Motor controller:
  Runs timed or sensor-confirmed motor commands.

Physical cube:
  Executes the solve.
```

## Recommended Hardware Interface

The cleanest next software step is to add a small hardware-facing output contract. Do not make the hardware team scrape Unity logs.

Recommended endpoint to add later:

```http
GET /latest-solution
```

Suggested response:

```json
{
  "solution": ["R", "U", "R'", "U'"],
  "move_count": 4,
  "notation": "standard_3x3",
  "ready": true
}
```

Alternative file-based contract:

```text
solutions/latest_solution.json
```

Suggested file contents:

```json
{
  "solution": ["R", "U", "R'", "U'"],
  "move_count": 4,
  "generated_at": "2026-07-08T22:00:00",
  "source": "camera_scan"
}
```

Endpoint-based communication is better if the hardware controller is another program running on the same computer. File-based communication is simpler if the hardware side is a script that polls for new output.

## Recommended Development Plan

### Phase 1: Keep Hardware Simulated

Before connecting motors, create a small script that receives a hardcoded solution:

```python
solution = ["R", "U", "R'", "U'"]
```

Then print the planned motor actions:

```text
R  -> right motor clockwise 90
U  -> top motor clockwise 90
R' -> right motor counterclockwise 90
U' -> top motor counterclockwise 90
```

This proves the notation translator works before dealing with hardware timing.

### Phase 2: Add A Hardware Adapter

Create one module whose only job is converting solver moves into machine commands.

Example conceptual interface:

```python
def convert_move_to_motor_commands(move: str) -> list[dict]:
    ...
```

Example output:

```json
[
  {
    "motor": "right_face",
    "direction": "clockwise",
    "degrees": 90
  }
]
```

### Phase 3: Connect To Real Motors

Once the translation works, connect it to the actual motor driver, microcontroller, or serial interface.

Possible communication methods:

- USB serial to Arduino, ESP32, or similar controller.
- HTTP endpoint from a Raspberry Pi.
- Local Python script using a motor-control library.
- Direct GPIO control if the backend runs on a Raspberry Pi.

### Phase 4: Add Feedback

A real machine should eventually know whether a move actually happened.

Possible feedback:

- Limit switches.
- Rotary encoders.
- Stepper motor position tracking.
- Camera verification after some number of moves.
- Manual emergency stop.

## Running The Current Project

### Backend manually

From the project root:

Mac:

```bash
./start_backend.command
```

Windows:

```bat
start_backend.bat
```

Backend URL:

```text
http://127.0.0.1:8000/docs
```

### Unity

Open the project in Unity, then run the normal app flow:

```text
Start screen -> Camera scan -> Submit -> 3D solution viewer
```

## Deployment Notes

The packaged builds expect the backend files beside the app.

Mac build folder:

```text
RubixCubeSolver.app
backend/
requirements.txt
start_backend.command
```

Windows build folder:

```text
RubixCubeSolver/
  rubixCube.exe
  rubixCube_Data/
backend/
requirements.txt
start_backend.bat
```

Do not commit or distribute these generated folders unless intentionally making a release artifact:

```text
.venv/
__pycache__/
backend_launcher.log
*_BurstDebugInformation_DoNotShip/
.DS_Store
```

## Known Risks

- The camera pipeline depends on lighting and image clarity.
- The backend assumes six images in the guided face order.
- If one face has fewer than 9 detected stickers, solving stops.
- The current system returns the solution but does not yet expose a dedicated hardware endpoint.
- The current Unity visualizer is separate from any real motor control.
- Auto-starting the backend works best after the Python virtual environment has already been created once.

## Recommended Next Code Change

The next code change should be small and intentional:

1. Store the latest solution on the backend after `/upload-photos` succeeds.
2. Add `GET /latest-solution`.
3. Document the exact JSON response.
4. Let the hardware controller call that endpoint.

Do not put motor-control logic inside `main_API.py`. Keep the solver and hardware control separated so both teams can work independently.

## Summary For ME/EE Team

You do not need to understand the full Unity UI to start.

The important output is:

```json
{
  "Solution": ["R", "U", "R'", "U'"]
}
```

Your job is to define how each move maps to the physical machine:

```text
abstract cube move -> machine command -> motor action -> verified physical move
```

Once that mapping is stable, the CS side can expose the solution sequence through a small endpoint or JSON file for the hardware controller to consume.
