import { ChevronDown } from "lucide-react";
import { AnimatePresence, motion } from "motion/react";
import { useState } from "react";
import type { SolverDebug } from "../api/solverClient";

type BackendDiagnosticsProps = {
  debug?: SolverDebug;
  isSolving: boolean;
};

export function BackendDiagnostics({ debug, isSolving }: BackendDiagnosticsProps) {
  const [isOpen, setIsOpen] = useState(false);
  if (!debug && !isSolving) return null;

  const pipeline = debug
    ? [
        ["Upload", `${debug.received_files} images received`],
        ["Detect", `${debug.detection.filter((face) => face.success).length}/6 faces found 9 stickers`],
        ["Calibrate", `Guided order ${debug.scan_order.join(" ")}`],
        ["Validate", debug.validation.valid ? "Cube state accepted" : debug.validation.message],
        ["Solve", debug.validation.valid ? "Kociemba returned a move sequence" : "Waiting for valid cube"],
      ]
    : [
        ["Upload", "Sending images"],
        ["Detect", "Finding stickers"],
        ["Calibrate", "Mapping colors"],
        ["Validate", "Checking cube state"],
        ["Solve", "Computing solution"],
      ];

  return (
    <section className={`backend-panel ${isOpen ? "is-open" : ""}`} aria-label="Backend diagnostics">
      <button type="button" className="panel-toggle" onClick={() => setIsOpen((current) => !current)}>
        <span>Backend trace</span>
        <strong>{isSolving ? "Running" : "Complete"}</strong>
        <ChevronDown size={17} />
      </button>

      <AnimatePresence initial={false}>
        {isOpen && (
          <motion.div
            className="collapsible-body"
            initial={{ height: 0, opacity: 0 }}
            animate={{ height: "auto", opacity: 1 }}
            exit={{ height: 0, opacity: 0 }}
            transition={{ duration: 0.28, ease: [0.22, 1, 0.36, 1] }}
          >
            <div className="pipeline-list">
              {pipeline.map(([label, value], index) => (
                <div className="pipeline-row" key={label}>
                  <span>{index + 1}</span>
                  <strong>{label}</strong>
                  <p>{value}</p>
                </div>
              ))}
            </div>

            {debug && (
              <>
                <div className="detected-faces">
                  {debug.faces_3x3.map((face) => (
                    <div className="debug-face" key={face.name}>
                      <strong>{face.name}</strong>
                      {face.rows.map((row) => (
                        <code key={row}>{row.split("").join(" ")}</code>
                      ))}
                    </div>
                  ))}
                </div>

                <div className="cube-strings">
                  <p>Raw: <code>{debug.raw_cube_string}</code></p>
                  <p>Kociemba: <code>{debug.final_cube_string}</code></p>
                </div>
              </>
            )}
          </motion.div>
        )}
      </AnimatePresence>
    </section>
  );
}
