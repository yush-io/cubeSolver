import { AnimatePresence, motion } from "motion/react";
import { useEffect, useMemo, useState } from "react";
import { BackendDiagnostics } from "./components/BackendDiagnostics";
import { CameraCapture } from "./components/CameraCapture";
import { SolutionPlayer } from "./components/SolutionPlayer";
import { uploadCubePhotos, type SolverDebug } from "./api/solverClient";
import { CubeScene } from "./cube/CubeScene";
import { DEFAULT_SOLUTION, reverseMove, solutionToScramble, type CubeMove } from "./cube/moves";

type Stage = "intro" | "capture" | "scramble" | "solve" | "done";
const SAMPLE_FACE_URLS = [
  "/sample-faces/face-white.jpg",
  "/sample-faces/face-red.jpg",
  "/sample-faces/face-green.jpg",
  "/sample-faces/face-yellow.jpg",
  "/sample-faces/face-orange.jpg",
  "/sample-faces/face-blue.jpg",
];

export default function App() {
  const [stage, setStage] = useState<Stage>("intro");
  const [solution, setSolution] = useState<CubeMove[]>(DEFAULT_SOLUTION);
  const [solveIndex, setSolveIndex] = useState(0);
  const [isSolving, setIsSolving] = useState(false);
  const [error, setError] = useState("");
  const [backendDebug, setBackendDebug] = useState<SolverDebug | undefined>();
  const [visualMove, setVisualMove] = useState<{ move?: CubeMove; token: number }>({ token: 0 });
  const [cubeResetToken, setCubeResetToken] = useState(0);
  const scramble = useMemo(() => solutionToScramble(solution), [solution]);
  const statusLine = stage === "intro"
    ? "Assembling cube model"
    : stage === "capture"
      ? "Waiting for six calibrated faces"
      : stage === "scramble"
        ? "Reversing solver output into scramble"
        : stage === "solve"
          ? "Solution ready for playback"
          : "Solved state confirmed";

  useEffect(() => {
    const introTimer = window.setTimeout(() => setStage("capture"), 3600);
    return () => window.clearTimeout(introTimer);
  }, []);

  useEffect(() => {
    if (stage !== "scramble") return;

    let moveIndex = 0;
    let nextMoveTimer = 0;
    let cancelled = false;
    const playNextScrambleMove = () => {
      if (cancelled) return;
      const move = scramble[moveIndex];
      if (!move) {
        setStage("solve");
        setSolveIndex(0);
        return;
      }

      setVisualMove((current) => ({ move, token: current.token + 1 }));
      moveIndex += 1;
      nextMoveTimer = window.setTimeout(playNextScrambleMove, move.includes("2") ? 720 : 520);
    };

    nextMoveTimer = window.setTimeout(playNextScrambleMove, 420);
    return () => {
      cancelled = true;
      window.clearTimeout(nextMoveTimer);
    };
  }, [scramble, stage]);

  async function handleSubmit(photos: Blob[]) {
    setIsSolving(true);
    setError("");
    setBackendDebug(undefined);
    try {
      const result = await uploadCubePhotos(photos);
      setSolution(result.moves);
      setBackendDebug(result.debug);
      setSolveIndex(0);
      setVisualMove((current) => ({ token: current.token + 1 }));
      setCubeResetToken((current) => current + 1);
      setStage("scramble");
    } catch (err) {
      setError(err instanceof Error ? err.message : "The solver request failed.");
    } finally {
      setIsSolving(false);
    }
  }

  async function handleSampleSubmit() {
    setIsSolving(true);
    setError("");
    setBackendDebug(undefined);
    try {
      const samplePhotos = await Promise.all(
        SAMPLE_FACE_URLS.map(async (url) => {
          const response = await fetch(url);
          if (!response.ok) throw new Error(`Could not load ${url}`);
          return response.blob();
        }),
      );
      await handleSubmit(samplePhotos);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Could not load the sample scan.");
      setIsSolving(false);
    }
  }

  function nextMove() {
    const move = solution[solveIndex];
    if (move) {
      setVisualMove((current) => ({ move, token: current.token + 1 }));
    }

    setSolveIndex((current) => {
      const next = Math.min(current + 1, solution.length);
      if (next === solution.length) setStage("done");
      return next;
    });
  }

  function previousMove() {
    const previous = solution[solveIndex - 1];
    if (previous) {
      setVisualMove((current) => ({ move: reverseMove(previous), token: current.token + 1 }));
    }

    setStage("solve");
    setSolveIndex((current) => Math.max(current - 1, 0));
  }

  function resetDemo() {
    setSolution(DEFAULT_SOLUTION);
    setSolveIndex(0);
    setVisualMove((current) => ({ token: current.token + 1 }));
    setCubeResetToken((current) => current + 1);
    setStage("intro");
    window.setTimeout(() => setStage("capture"), 3600);
  }

  return (
    <main className={`app-shell stage-${stage}`}>
      <CubeScene
        stage={stage}
        activeMove={visualMove.move}
        moveToken={visualMove.token}
        resetToken={cubeResetToken}
        playbackIndex={solveIndex}
      />

      <div className="grain" />
      <div className="cube-pattern" />
      <div className="light-trails" />
      <div className="system-status">{statusLine}</div>

      <AnimatePresence mode="wait">
        {stage === "intro" && (
          <motion.section
            className="intro-copy"
            initial={{ opacity: 0, y: 16 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: -18 }}
            transition={{ duration: 0.7 }}
          >
            <span>AI Cube Solver</span>
            <h1>Cube Solver</h1>
            <p>Fast scramble, camera scan, clean solve.</p>
          </motion.section>
        )}

        {(stage === "capture" || stage === "scramble") && (
          <motion.div
            className="workspace capture-workspace"
            initial={{ opacity: 0, y: 30, rotateX: -8 }}
            animate={{ opacity: 1, y: 0, rotateX: 0 }}
            exit={{ opacity: 0, y: 24, rotateX: 9, scale: 0.96 }}
            transition={{ duration: 0.55, ease: [0.22, 1, 0.36, 1] }}
          >
            <div className="status-column">
              <span className="mode-label">{stage === "scramble" ? "Replicating scramble" : "Scan faces"}</span>
              <h2>{stage === "scramble" ? "Building the cube state" : "Capture all six centers"}</h2>
              <p>{stage === "scramble" ? scramble.join(" ") : "White, red, green, yellow, orange, then blue."}</p>
              <div className="face-legend" aria-label="Face order">
                {["W", "R", "G", "Y", "O", "B"].map((face) => (
                  <span data-face={face} key={face}>{face}</span>
                ))}
              </div>
              {error && <p className="error-text">{error}</p>}
            </div>
            <div className="right-stack">
              <CameraCapture onSubmit={handleSubmit} onUseSample={handleSampleSubmit} isSolving={isSolving || stage === "scramble"} />
              <BackendDiagnostics debug={backendDebug} isSolving={isSolving} />
            </div>
          </motion.div>
        )}

        {(stage === "solve" || stage === "done") && (
          <motion.div
            className="workspace solve-workspace"
            initial={{ opacity: 0, y: 34, scale: 0.94 }}
            animate={{ opacity: 1, y: 0, scale: 1 }}
            exit={{ opacity: 0, y: 18 }}
            transition={{ duration: 0.6, ease: [0.22, 1, 0.36, 1] }}
          >
            <div className="status-column">
              <span className="mode-label">{stage === "done" ? "Solved" : "Step by step"}</span>
              <h2>{stage === "done" ? "Cube solved" : "Replay the solution"}</h2>
              <p>{solution.join(" ")}</p>
              <p className="scramble-check">Scramble replay: {scramble.join(" ")}</p>
            </div>
            <div className="right-stack compact-stack">
              <SolutionPlayer
                moves={solution}
                index={solveIndex}
                onNext={nextMove}
                onPrevious={previousMove}
                onReset={resetDemo}
              />
              <BackendDiagnostics debug={backendDebug} isSolving={false} />
            </div>
          </motion.div>
        )}
      </AnimatePresence>
    </main>
  );
}
