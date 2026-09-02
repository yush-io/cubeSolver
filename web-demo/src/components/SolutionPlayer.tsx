import { Check, ChevronDown, ChevronLeft, ChevronRight, RotateCcw } from "lucide-react";
import { AnimatePresence, motion } from "motion/react";
import { useState } from "react";
import type { CubeMove } from "../cube/moves";

type SolutionPlayerProps = {
  moves: CubeMove[];
  index: number;
  onNext: () => void;
  onPrevious: () => void;
  onReset: () => void;
};

export function SolutionPlayer({ moves, index, onNext, onPrevious, onReset }: SolutionPlayerProps) {
  const [showSequence, setShowSequence] = useState(false);
  const done = index >= moves.length;
  const currentMove = done ? "Done" : moves[index] ?? "Ready";

  return (
    <section className={`solution-panel ${showSequence ? "is-open" : ""}`} aria-label="Solution player">
      <div className="move-display">
        <span>Move {Math.min(index + 1, moves.length)} of {moves.length}</span>
        <strong>{currentMove}</strong>
      </div>

      <button type="button" className="panel-toggle sequence-toggle" onClick={() => setShowSequence((current) => !current)}>
        <span>Move sequence</span>
        <strong>{moves.length} moves</strong>
        <ChevronDown size={17} />
      </button>

      <AnimatePresence initial={false}>
        {showSequence && (
          <motion.div
            className="collapsible-body"
            initial={{ height: 0, opacity: 0 }}
            animate={{ height: "auto", opacity: 1 }}
            exit={{ height: 0, opacity: 0 }}
            transition={{ duration: 0.28, ease: [0.22, 1, 0.36, 1] }}
          >
            <div className="move-track">
              {moves.map((move, moveIndex) => (
                <span className={moveIndex < index ? "complete" : moveIndex === index ? "current" : ""} key={`${move}-${moveIndex}`}>
                  {move}
                </span>
              ))}
            </div>
          </motion.div>
        )}
      </AnimatePresence>

      <div className="player-actions">
        <button type="button" className="round-button" onClick={onPrevious} disabled={index <= 0}>
          <ChevronLeft size={21} />
        </button>
        <button type="button" className="round-button" onClick={onReset}>
          <RotateCcw size={19} />
        </button>
        <button type="button" className="round-button primary" onClick={onNext} disabled={done}>
          {done ? <Check size={21} /> : <ChevronRight size={21} />}
        </button>
      </div>
    </section>
  );
}
