import { normalizeMoves, type CubeMove } from "../cube/moves";

export type SolverResponse = {
  Solution?: string[];
  solution?: string[];
  debug?: SolverDebug;
};

export type SolverDebug = {
  received_files: number;
  scan_order: string[];
  detection: Array<{
    face_index: number;
    filename?: string;
    attempts: Array<{ attempt: number; stickers_found: number }>;
    detected: number;
    success: boolean;
  }>;
  face_strings: Array<{
    face_index: number;
    expected_center: string;
    stickers: string;
    rows: string[];
  }>;
  raw_cube_string: string;
  final_cube_string: string;
  faces_3x3: Array<{
    name: string;
    rows: string[];
  }>;
  validation: {
    valid: boolean;
    message: string;
  };
};

export type SolverResult = {
  moves: CubeMove[];
  debug?: SolverDebug;
};

const API_BASE_URL =
  import.meta.env.VITE_SOLVER_API_URL?.replace(/\/$/, "") ?? "http://127.0.0.1:8000";

export async function uploadCubePhotos(files: Blob[]): Promise<SolverResult> {
  const form = new FormData();
  files.forEach((file, index) => {
    form.append("files", file, `face_${index + 1}.png`);
  });

  const response = await fetch(`${API_BASE_URL}/upload-photos`, {
    method: "POST",
    body: form,
  });

  if (!response.ok) {
    const message = await response.text();
    let detail = message;
    try {
      const parsed = JSON.parse(message) as { detail?: string };
      detail = parsed.detail ?? message;
    } catch {
      detail = message;
    }
    throw new Error(detail || `Solver request failed with ${response.status}`);
  }

  const data = (await response.json()) as SolverResponse;
  const solution = data.Solution ?? data.solution;
  if (!solution?.length) {
    throw new Error("The solver did not return a solution.");
  }

  return {
    moves: normalizeMoves(solution),
    debug: data.debug,
  };
}
