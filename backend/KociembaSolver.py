from abc import ABC, abstractmethod
import kociemba
from typing import List

class ISolver(ABC):
    @abstractmethod
    def solve(self, state_string: str) -> str:
        pass


class KociembaSolver(ISolver):
    # solves the cube state using the kociemba algorithm
    def solve(self, state_string: str) -> str:
        try:
            solution = kociemba.solve(state_string)
            return solution
        except Exception as e:
            # For future, certain errors can be raised if we want to
            raise ValueError(f"Kociemba solver failed: {e}")