 [![Review Assignment Due Date](https://classroom.github.com/assets/deadline-readme-button-22041afd0340ce965d47ae6ef1cefeee28c7c493a6346c4f15d667ab976d596c.svg)](https://classroom.github.com/a/EvxoT0RF)
[![Open in Codespaces](https://classroom.github.com/assets/launch-codespace-2972f46106e565e64193e422d61a12cf1da4916b45550586e14ef0a7c637dd04.svg)](https://classroom.github.com/open-in-codespaces?assignment_repo_id=21191112)
# Rubix Cube Solver
Authors: [Evan Lin] https://github.com/Evananlin
            [Aayush Rashinkar] https://github.com/AayushRashinkar
            [Celso Lopez] https://github.com/CelsoSLopez
            [Abdullah Kashif] https://github.com/abdullah0432

## Project Description
### Personal Importance:
 * Using the integration of an AI based image recognition technology (yolov8) with algorithmic problem solving (kociemba) to solve a globally respected puzzle sounds interesting. It uses multiple aspects of CS including computer vision, backend (python), and  frontend 3D graphics. It connects the gap between the physical world and digital problem solving. Aayush likes 3x3 cubes. 
### Languages:
 * Python (backend logic, image processing, API)
 * Unity, C# (frontend UI)
### Frameworks / Libraries / Tools:
 * YOLOv8 (Ultralytics) – for object detection of cube stickers
 * OpenCV – for image processing and color extraction 
 * scikit-image – for LAB color space comparison
 * Kociemba Algorithm (Python Library) – for optimal cube solving
 * Unity – for interactive 3D cube visualization and step playback
 * FastAPI - communication structure between frontend and backend
 * JSON – data format for frontend/backend communication
### Input:
 * 6 images of each face of the scrambled 3x3 cube.
### Output:
 * Output of optimal solution in standard 3x3 notation (ex: R U R’ U R U2 R’ U)
 * 3D cube on a webpage visualizing the solution with (next, previous, maybe play/plause)
### Features and Complexity:
 * Cube Detection (YOLOv8 + OpenCV)
 * Automatically identifies and labels the 9 stickers on each cube face.
 * Detects colors under different lighting conditions using LAB color distance.
 * State Construction and Validation
 * Builds a valid cube state (URFDLB facelet string) using nearest-color matching.
 * Validates the input to ensure it represents a possible cube configuration.
 * Algorithmic Solver (Kociemba)
 * Computes an optimal (or near-optimal) sequence of moves to solve the cube.
 * Returns both the full move string and total move count.
 * Interactive 3D Visualization (Unity)
 * Displays a 3D model of the cube.
 * Lets users follow each move manually using Next/Prev buttons or auto-play the solution.
### Data Flow
 * Images → YOLOv8 Detection → Color Mapping → Facelet String → Kociemba Solver → Move Sequence → Unity Viewer

### Backend Setup
1. Install Miniconda
2. Create the environment:
   ```bash
   conda create -n yolov8 python=3.11
   conda activate yolov8
   pip install -r requirements.txt
   pip install ultralytics opencv-python
   pip install opencv-python-headless
## User Interface Specification
### Navigation Diagram
<img width="737" height="1059" alt="image" src="https://github.com/user-attachments/assets/b50424ca-8ab7-40ea-b23f-29e25b5e48bd" />


Description: The user interface will consist of a sequence of interactive screens in Unity that guide the user through the entire process: from scanning their physical cube to visualizing the solution. Each screen would be connected through navigation buttons (except for the loading screen), allowing users to capture cube images, review and confirm scans, trigger the solving process, and visualize each step that leads to the final solution. This design ensures a an interative and step-by-step experience.

### Screen Layouts

#### Start Screen
* Components
  * Title: "AI Cube Solver"
  * Button: “Start” → navigates to the Scan Screen
  * Background: Simple gradient or cube animation
* Purpose:
  * Introduce the project and start the workflow
#### Scan Screen
* Components
  * Webcam Viewport: Displays the live camera feed
  * Button: “Capture Face” → captures one face and saves it
  * Indicator: Shows which cube face is being scanned.
  * Button: “Submit” → goes to Review Screen after all 6 faces are captured.
* Purpose:
  * Gather 6 inputs images for the cube
#### 3D Visualization Screen
* Components:
  * 3D Cube Model: Interactive cube rendered in unity
  * Buttons: “Next Move”, “Previous Move” → tep forward or backward through the solution steps.
  * Move Display: Shows the current move 
  * Move Counter: “Step # / #” → displays current / total steps
  * Buttons: “Finished” → shows up after current step == total steps
  * Buttons: "Restart" → sends the user back to the start screen.
* Purpose:
  * Fun visualizer for the solution sequence in real time, has interactive buttons to show next and previous steps.
#### Finish Screen
* Components:
  * Message: “Cube Solved!”
  * Button: “Restart” → returns to Start Screen.
  * Button: “Exit” → closes the application
* Purpose:
  * End of workflow or restart option



## Class Diagram
<img width="1181" height="684" alt="cs100finaldiagram-Page-2 drawio" src="https://github.com/user-attachments/assets/b3d04d24-4140-4ce2-ad84-345829ece855" />
Description: The class diagram above represents the overall architecture of the Rubik’s Cube Solver project, illustrating how both the backend logic (Python) and frontend interface (Unity, C#) interact to process cube images, compute the solution, and visualize it in 3D. The design separates responsibilities into clear functional modules — image processing, cube solving, and user interaction — while maintaining communication through a unified API interface.
 
### Updated Class Diagram with SOLID principles

<img width="1424" height="1206" alt="image" src="https://github.com/user-attachments/assets/9caf044a-4362-4c86-9cc1-cf5fd0c36812" />


### Explaning Class Diagram Changes

Breaking Down the Cube Scanner
 * **SOLID Principle Applied:** Single Responsibility Principle
 * **How we applied it:** The original CubeScanner was split into two dedicated classes: StickerDetector (responsible only for running the Yolov8/OpenCV model) and ColorMapper (responsible only for converting detected colors to the cube state string). We also remnoved the backend Capture_image() method, recognizing it as a frontend responsibility.
 * **How this change helps write better code:** The code is now modular. If we want to upgrade the model from YOLOv8 to YOLOv9, we would only need to edit the StickerDetector class. Each class is not smaller, easier to test, and most importantly independent.

Implementing interfaces for Solvers and Dectors
 * **SOLID Principle Applied:** Inversion Principle
 * **How we applied it:** We introduce the ISolver, IColorMapper, and IDetector interfaces, making sure that Kociembasolver and the new classes we implemented (StickerDetector and ColorMapper) implement them. The high-level FastAPI_API now depends on these abstract interfaces instead of the concrete classes.
 * **How this change helps write better code:** This change makes the design flexible, testable, and pluggable. We can now substitue the real solver with a simple mock object during unit testing to ensuring the high-level logic is correct without needing to execute time-consuming code.

Refining the MoveSequence Logic
 * **SOLID Principle Applied:** Single Responsibility Principle
 * **How we applied it:** The parse_solution() method was moved from the simple data container MoveSequence into the KociembaSolver class.
 * **How this change helps write better code:** The KociembaSolver is now responsible for providing a complete, usable solution (including any necessary parsing or formatting), while the MoveSequence class remains a simple, clean, struct. This clarifies the role of each component and simplifies the data container.

Adjustment to Client-Server Relationship
 * **SOLID Principle Applied:** Single Responsibility Principle
 * **How we applied it:** We removed the direct "uses" relationship between the CubeController (Frontend) and the FastAPI_API (backend). this implies that the communication logic will be handled by a dedicated, abstract class in the Unity environment, separate from low-level code.
 * **How this change helps write better code:** The CubeController now maintains a single responsibility: managing the 3D cube model and applying rotations. This separation makes the frontend logic cleaner and allows the system to change its network protocol without modifying the cube's core behavior.


 
 > ## Final deliverable
 > All group members will give a demo to the reader during lab time. ou should schedule your demo on Calendly with the same reader who took your second scrum meeting. The reader will check the demo and the project GitHub repository and ask a few questions to all the team members. 
 > Before the demo, you should do the following:
 > * Complete the sections below (i.e. Screenshots, Installation/Usage, Testing)
 > * Plan one more sprint (that you will not necessarily complete before the end of the quarter). Your In-progress and In-testing columns should be empty (you are not doing more work currently) but your TODO column should have a full sprint plan in it as you have done before. This should include any known bugs (there should be some) or new features you would like to add. These should appear as issues/cards on your Project board.
 > * Make sure your README file and Project board are up-to-date reflecting the current status of your project (e.g. any changes that you have made during the project such as changes to your class diagram). Previous versions should still be visible through your commit history.
>  * Each team member should also submit the Peer Evaluation Form on Canvas for this final phase. In this form, you need to fill in the names of all team members, the percentage of work contributed by each member for the final phase, and a description of their contributions. Remember that each team member should submit the form individually.
 
 ## Screenshots
 > Screenshots of the input/output after running your application
 ## Installation/Usage
 > Instructions on installing and running your application
 ## Testing
 > How was your project tested/validated? If you used CI, you should have a "build passing" badge in this README.
 
