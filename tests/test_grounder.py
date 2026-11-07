"""Tests for agent-hallucination-grounder."""
import unittest
from agent_hallucination_grounder.grounder import AgentHallucinationGrounder


class TestHallucinationGrounder(unittest.TestCase):
    def setUp(self):
        self.g = AgentHallucinationGrounder(
            known_files={"app.py", "utils.py"},
            known_symbols={"calculate_tax"}
        )

    def test_verified_output(self):
        rep = self.g.verify_text("Saved to 'app.py' after running `calculate_tax()`.")
        self.assertTrue(rep.to_dict()["is_grounded"])
        self.assertEqual(rep.grounding_score, 1.0)

    def test_catches_hallucinations(self):
        rep = self.g.verify_text("Imported from 'ghost.py' via `fake_call()`.")
        self.assertFalse(rep.to_dict()["is_grounded"])
        self.assertEqual(len(rep.hallucinations), 2)
