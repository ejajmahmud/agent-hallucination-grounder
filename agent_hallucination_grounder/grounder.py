"""Core Agent Hallucination Grounder implementation."""
import re
from typing import Set, List, Dict, Any


class GroundingReport:
    def __init__(self, total_claims: int, verified_claims: int, hallucinations: List[str]):
        self.total_claims = total_claims
        self.verified_claims = verified_claims
        self.hallucinations = hallucinations

    @property
    def grounding_score(self) -> float:
        return (self.verified_claims / self.total_claims) if self.total_claims > 0 else 1.0

    def to_dict(self) -> Dict[str, Any]:
        return {
            "total_claims": self.total_claims,
            "verified_claims": self.verified_claims,
            "grounding_score": round(self.grounding_score, 3),
            "hallucinations": self.hallucinations,
            "is_grounded": len(self.hallucinations) == 0
        }


class AgentHallucinationGrounder:
    def __init__(self, known_files: Set[str], known_symbols: Set[str]):
        self.known_files = known_files
        self.known_symbols = known_symbols

    def verify_text(self, text: str) -> GroundingReport:
        # Extract quoted file paths (e.g. "path/to/file.py")
        path_matches = re.findall(r"'([^']+\.[a-zA-Z0-9]+)'", text) + re.findall(r'"([^"]+\.[a-zA-Z0-9]+)"', text)
        # Extract function call patterns (e.g. `some_function()`)
        fn_matches = re.findall(r'`([a-zA-Z0-9_]+)\(\)`', text)

        claims = []
        hallucinations = []
        verified = 0

        for path in path_matches:
            claims.append(path)
            if path in self.known_files:
                verified += 1
            else:
                hallucinations.append(f"Nonexistent file path: '{path}'")

        for fn in fn_matches:
            claims.append(fn)
            if fn in self.known_symbols:
                verified += 1
            else:
                hallucinations.append(f"Nonexistent function symbol: '{fn}'")

        return GroundingReport(len(claims), verified, hallucinations)
