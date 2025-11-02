[![Review Assignment Due Date](https://classroom.github.com/assets/deadline-readme-button-22041afd0340ce965d47ae6ef1cefeee28c7c493a6346c4f15d667ab976d596c.svg)](https://classroom.github.com/a/EvxoT0RF)
[![Open in Codespaces](https://classroom.github.com/assets/launch-codespace-2972f46106e565e64193e422d61a12cf1da4916b45550586e14ef0a7c637dd04.svg)](https://classroom.github.com/open-in-codespaces?assignment_repo_id=21191112)
# Rubix Cube Solver
  > Authors: [Evan Lin] https://github.com/Evananlin
            [Aayush Rashinkar]
            [Celso Lopez]
            [Abdullah Kashif]

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
 * FastAPI – to build and serve backend endpoints (/scan, /solve)\
 * cubing.js – for interactive 3D cube visualization and step playback
 * JSON – for communication between frontend and backend
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
 * Interactive 3D Visualization (cubing.js)
 * Displays a 3D model of the cube.
 * Lets users follow each move manually using Next/Prev buttons or auto-play the solution.
### Data Flow
 * Images → YOLOv8 Detection → Color Mapping → Facelet String → Kociemba Solver → Move Sequence → cubing.js Viewer

### Backend Setup
1. Install Miniconda
2. Create the environment:
   ```bash
   conda create -n yolov8 python=3.11
   conda activate yolov8
   pip install -r requirements.txt
   pip install ultralytics opencv-python
   pip install opencv-python-headless
>
>
 > ## Phase II
 > In addition to completing the "User Interface Specification" and "Class Diagram" sections below, you will need to:
 > * Create an "Epic" (note) for each feature. Place these epics in the `Product Backlog` column
 > * Complete your first *sprint planning* meeting to plan out the next 7 days of work.``
 >   * Break down the "Epics" into smaller actionable user stories. Convert them into issues and assign them to team members. Place these in the `Sprint Backlog` column.
 >   * These cards should represent roughly 7 days worth of development time for your team. Then, once the sprint is over you should be repeating these steps to plan a new sprint, taking you until your second scrum meeting with the reader in phase III.
 > * Each team member needs to submit the Peer Evaluation Form on Canvas for this phase. In this form, you need to fill in the names of all team members, the percentage of work contributed by each member for phase  II, and a description of their contributions. Remember that each team member should submit the form individually.
 > * Schedule two check-ins using Calendly. Both time slots should be during your lab on week 6. Your entire team must be present for both check-ins.
 >   * The first check-in needs to be scheduled with your lab TA. During that meeting, you will discuss your project design/class diagram from phase II.
 >   * The second check-in should be scheduled with a reader. During that meeting you will discuss:
 >     * The tasks you are planning for the first sprint
 >     * How work will be divided between the team members
## User Interface Specification
 > Include a navigation diagram for your screens and the layout of each of those screens as desribed below. For all the layouts/diagrams, you can use any tool such as PowerPoint or a drawing program. (Specification requirement is adapted from the User Interface Design Document Template of CMSC 345 at the University of Maryland Global Campus)

### Navigation Diagram
> Draw a diagram illustrating how the user can navigate from one screen to another. Here is an [example](https://creately.com/diagram/example/ikfqudv82/user-navigation-diagram-classic?r=v). Nodes represent the different screens in your program and arrows represent the way to navigate from one screen to another. It can be useful to label each symbol that represents a screen so that you can reference the screens in the next section or the rest of the document if necessary. Give a brief description of what the diagram represents.
 <img width="400" height="600" alt="image" src="https://github.com/user-attachments/assets/195c3363-858b-4221-b08f-72cb573a4651" />


### Screen Layouts
> Include the layout of each of your screens. The layout should describe the screen’s major components such as menus and prompts for user inputs and expected output, or any graphical user interface components if applicable (e.g. buttons, text boxes, etc). Explain what is on the layout, and the purpose of each menu item, button, etc. If many screens share the same layout, start by describing the general layout and then list the screens that will be using that layout and the differences between each of them.

#### Start Screen
* Components
  * Title: "AI Cube Solver"
  * Button: “Start” →navigates to the Scan Screen
  * Background: Simple gradient or cube animation
* Purpose:
  * Introduce the project and start the workflow
#### Scan Screen
* Components
  * Webcam Viewport: Displays the live camera feed
  * Button: “Capture Face” –captures one face and saves it
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
  * Loading Animation / Text: “Computing optimal solution…” animated character running
  * Progress Bar: Visual feedback during backend API call.
* Purpose: 
  * Wait screen while Yolov8 + kociemba backend generates a solution string.
#### 3D Visualization Screen
* Components:
  * 3D Cube Model: Interactive cube rendered in unity
  * Buttons: “Next Move”, “Previous Move” → step through or backwards in the steps
  * Move Display: Shows the current move 
  * Move Counter: “Step # / #” → displays current / total steps
  * Buttons: “Finished” → shows up after current step == total steps
* Purpose:
  * Fun visualizar for the solution sequence in real time
#### Finish Screen
* Components:
  * Message: “Cube Solved!”
  * Button: “Restart” → returns to Start Screen.
  * Button: “Exit” → closes the application
* Purpose:
  * End of workflow or restart option


## Class Diagram
 > Include a **class diagram(s)** for your project and a **description** of the diagram(s). Your class diagram(s) should include all the main classes you plan for the project. This should be in sufficient detail that another group could pick up the project this point and successfully complete it. Use proper UML notation (as discussed in the course slides).
 
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
 
