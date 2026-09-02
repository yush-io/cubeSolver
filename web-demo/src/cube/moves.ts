export type CubeMove =
  | "U"
  | "U'"
  | "U2"
  | "D"
  | "D'"
  | "D2"
  | "L"
  | "L'"
  | "L2"
  | "R"
  | "R'"
  | "R2"
  | "F"
  | "F'"
  | "F2"
  | "B"
  | "B'"
  | "B2";

export const DEFAULT_SOLUTION: CubeMove[] = [
  "R",
  "U",
  "R'",
  "U'",
  "F",
  "R",
  "F'",
  "R'",
];

export function reverseMove(move: string): CubeMove {
  if (move.endsWith("2")) return move as CubeMove;
  if (move.endsWith("'")) return move.slice(0, -1) as CubeMove;
  return `${move}'` as CubeMove;
}

export function solutionToScramble(solution: string[]): CubeMove[] {
  return [...solution].reverse().map(reverseMove);
}

export function normalizeMoves(moves: string[]): CubeMove[] {
  return moves.filter(Boolean).map((move) => move.trim() as CubeMove);
}
