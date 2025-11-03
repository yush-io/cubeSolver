[![Review Assignment Due Date](https://classroom.github.com/assets/deadline-readme-button-22041afd0340ce965d47ae6ef1cefeee28c7c493a6346c4f15d667ab976d596c.svg)](https://classroom.github.com/a/EvxoT0RF)
[![Open in Codespaces](https://classroom.github.com/assets/launch-codespace-2972f46106e565e64193e422d61a12cf1da4916b45550586e14ef0a7c637dd04.svg)](https://classroom.github.com/open-in-codespaces?assignment_repo_id=21191112)
# Rubix Cube Solver
  > Authors: [Evan Lin] https://github.com/Evananlin
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
<img width="400" height="600" alt="image" src="https://github.com/user-attachments/assets/3e825c1e-3a94-408d-8d23-3527af0250d9" />

Description: The user interface will consist of a sequence of interactive screens in Unity that guide the user from scanning their physical cube to visualizing the solution.

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
  * Button: “Next” → move to the next cube face.
  * Button: “Submit” → goes to Review Screen after all 6 faces are captured.
* Purpose:
  * Gather 6 inputs images for the cube
#### Review Screen
* Components:
  * Thumbnails: 6 captured images labeled by face (U, R, F, D, L, B)
  * Button: “Retake” goes back to Scan Screen
  * Button: “Confirm” → proceeds to solving screen
* Purpose:
  * Let users confirm their captures before processing
#### Solving Screen
* Components:
  * Loading Animation/Text: “Computing optimal solution…”; animated character running
  * Progress Bar: Visual feedback during backend API call.
* Purpose: 
  * Wait screen while Yolov8 + kociemba backend generates a solution string.
#### 3D Visualization Screen
* Components:
  * 3D Cube Model: Interactive cube rendered in unity
  * Buttons: “Next Move”, “Previous Move” → tep forward or backward through the solution steps.
  * Move Display: Shows the current move 
  * Move Counter: “Step # / #” → displays current / total steps
  * Buttons: “Finished” → shows up after current step == total steps
* Purpose:
  * Fun visualizer for the solution sequence in real time
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
 
 > ## Phase III
 > You will need to schedule a check-in for the second scrum meeting with the same reader you had your first scrum meeting with (using Calendly). Your entire team must be present. This meeting will occur on week 8 during lab time.
 
 > BEFORE the meeting you should do the following:
 > * Update your class diagram from Phase II to include any feedback you received from your TA/grader.
 > * Considering the SOLID design principles, reflect back on your class diagram and think about how you can use the SOLID principles to improve your design. You should then update the README.md file by adding the following:
 >   * A new class diagram incorporating your changes after considering the SOLID principles.
 >   * For each update in your class diagram, you must explain in 3-4 sentences:
 >     * What SOLID principle(s) did you apply?
 >     * How did you apply it? i.e. describe the change.
 >     * How did this change help you write better code?
 > * Perform a new sprint plan like you did in Phase II.
 > * Make sure that your README file (and Project board) are up-to-date reflecting the current status of your project and the most recent class diagram. Previous versions of the README file should still be visible through your commit history.
>  * Each team member should also submit the Peer Evaluation Form on Canvas for phase III. In this form, you need to fill in the names of all team members, the percentage of work contributed by each member for phase III, and a description of their contributions. Remember that each team member should submit the form individually.
 
> During the meeting with your reader you will discuss: 
 > * How effective your last sprint was (each member should talk about what they did)
 > * Any tasks that did not get completed last sprint, and how you took them into consideration for this sprint
 > * Any bugs you've identified and created issues for during the sprint. Do you plan on fixing them in the next sprint or are they lower priority?
 > * What tasks you are planning for this next sprint.

 
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
 
