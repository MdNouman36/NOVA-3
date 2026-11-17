"""
test_smoke.py — Smoke and safety net tests for OILS-3.

Runs with:
    python -m unittest discover -s For_Developers/tests
"""

import ast
import os
import re
import shutil
import subprocess
import sys
import tempfile
import unittest

# Ensure For_Developers is in sys.path
TEST_DIR = os.path.dirname(os.path.abspath(__file__))
FOR_DEV_DIR = os.path.dirname(TEST_DIR)
REPO_ROOT = os.path.dirname(FOR_DEV_DIR)

if FOR_DEV_DIR not in sys.path:
    sys.path.insert(0, FOR_DEV_DIR)

from arcade.dsa.experiments_data import DSA_EXPERIMENTS
from arcade.java.experiments_data import JAVA_EXPERIMENTS
from arcade.git.experiments_data import GIT_EXPERIMENTS
from arcade.session import (
    _BADGES,
    _VISUALIZERS,
    _SESSION,
    _mark_experiment_done,
    _record_visualizer_explored,
)
from arcade.viva_bank import VIVA_PRACTICE_SETS


class TestOILS3Smoke(unittest.TestCase):

    def test_experiment_files_exist(self):
        """1. Every file path in DSA_EXPERIMENTS, JAVA_EXPERIMENTS, and GIT_EXPERIMENTS exists on disk."""
        self.assertEqual(len(DSA_EXPERIMENTS), 12, "Should have 12 DSA experiments")
        self.assertEqual(len(JAVA_EXPERIMENTS), 10, "Should have 10 Java experiments")
        self.assertEqual(len(GIT_EXPERIMENTS), 12, "Should have 12 Git experiments")

        for exp_list, name in [
            (DSA_EXPERIMENTS, "DSA"),
            (JAVA_EXPERIMENTS, "Java"),
            (GIT_EXPERIMENTS, "Git"),
        ]:
            for exp in exp_list:
                if "file" in exp:
                    full_path = os.path.join(FOR_DEV_DIR, exp["file"])
                    self.assertTrue(
                        os.path.isfile(full_path),
                        f"{name} Exp {exp.get('num')} file missing: {full_path}",
                    )

    def test_trophy_ids_registered(self):
        """2. Every trophy ID passed to _unlock_badge / _unlock_trophy anywhere in arcade/ exists in _BADGES."""
        arcade_dir = os.path.join(FOR_DEV_DIR, "arcade")
        pattern = re.compile(r'_unlock_(?:badge|trophy)\(\s*["\']([^"\']+)["\']\s*\)')

        found_calls = []
        for root, _, files in os.walk(arcade_dir):
            for file in files:
                if file.endswith(".py"):
                    file_path = os.path.join(root, file)
                    with open(file_path, "r", encoding="utf-8") as f:
                        content = f.read()
                    matches = pattern.findall(content)
                    for m in matches:
                        found_calls.append((file, m))

        self.assertGreater(len(found_calls), 0, "Should find unlock calls in arcade/")
        for filename, trophy_id in found_calls:
            self.assertIn(
                trophy_id,
                _BADGES,
                f"Trophy ID '{trophy_id}' unlocked in {filename} is not registered in _BADGES!",
            )

    def test_milestone_badge_ids(self):
        """3. Every ID referenced in _check_milestone_badges() is either a valid experiment ID or a registered visualizer ID."""
        session_file = os.path.join(FOR_DEV_DIR, "arcade", "session.py")
        with open(session_file, "r", encoding="utf-8") as f:
            tree = ast.parse(f.read(), filename=session_file)

        # Extract string constants within _check_milestone_badges
        func_node = None
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef) and node.name == "_check_milestone_badges":
                func_node = node
                break

        self.assertIsNotNone(func_node, "Function _check_milestone_badges not found in session.py")

        valid_exp_ids = set(
            [f"DSA-{i}" for i in range(1, 13)]
            + [f"JAVA-{i}" for i in range(1, 11)]
            + [f"GIT-{i}" for i in range(1, 13)]
        )
        valid_vis_ids = set(_VISUALIZERS.keys())
        all_valid_ids = valid_exp_ids | valid_vis_ids

        id_pattern = re.compile(r'^(DSA|JAVA|GIT)-[A-Z0-9]+$')
        referenced_ids = set()
        for node in ast.walk(func_node):
            if isinstance(node, ast.Constant) and isinstance(node.value, str):
                val = node.value
                if id_pattern.match(val):
                    referenced_ids.add(val)

        for rid in referenced_ids:
            self.assertIn(
                rid,
                all_valid_ids,
                f"ID '{rid}' in _check_milestone_badges() is neither a valid experiment ID nor a registered visualizer ID!",
            )

    def test_vault_paths_exist(self):
        """4. Every vault path used by _show_code_vault() exists."""
        dsa_dir = os.path.join(FOR_DEV_DIR, "dsa-lab", "programs")
        java_dir = os.path.join(FOR_DEV_DIR, "java-lab", "programs")
        doc1 = os.path.join(FOR_DEV_DIR, "docs", "GIT_REFERENCE.md")
        doc2 = os.path.join(FOR_DEV_DIR, "docs", "GIT_COMMANDS.md")

        self.assertTrue(os.path.isdir(dsa_dir), f"DSA dir missing: {dsa_dir}")
        dsa_files = [f for f in os.listdir(dsa_dir) if f.endswith(".c")]
        self.assertEqual(len(dsa_files), 12, "Should have 12 DSA C programs in vault")

        self.assertTrue(os.path.isdir(java_dir), f"Java dir missing: {java_dir}")
        java_files = [f for f in os.listdir(java_dir) if f.endswith(".java")]
        self.assertEqual(len(java_files), 10, "Should have 10 Java programs in vault")

        self.assertTrue(os.path.isfile(doc1), f"DOC1 missing: {doc1}")
        self.assertTrue(os.path.isfile(doc2), f"DOC2 missing: {doc2}")

    def test_viva_practice_sets_count(self):
        """5. VIVA_PRACTICE_SETS has exactly 3 subjects x 2 sets x 15 questions = 90."""
        self.assertEqual(len(VIVA_PRACTICE_SETS), 3, "Should have 3 subjects (git, dsa, java)")
        total_q = 0
        for sub, data in VIVA_PRACTICE_SETS.items():
            sets = data.get("sets", {})
            self.assertEqual(len(sets), 2, f"Subject {sub} should have 2 sets")
            for set_id, set_data in sets.items():
                q_list = set_data.get("questions", [])
                self.assertEqual(
                    len(q_list),
                    15,
                    f"Subject {sub} Set {set_id} should have 15 questions, found {len(q_list)}",
                )
                total_q += len(q_list)
        self.assertEqual(total_q, 90, f"Expected 90 total viva questions, got {total_q}")

    def test_c_programs_compile(self):
        """6a. If gcc is on PATH, all 12 C programs compile with -Wall."""
        gcc = shutil.which("gcc")
        if not gcc:
            self.skipTest("gcc not found on PATH; skipping C compilation smoke test")

        dsa_dir = os.path.join(FOR_DEV_DIR, "dsa-lab", "programs")
        c_files = sorted([f for f in os.listdir(dsa_dir) if f.endswith(".c")])
        self.assertEqual(len(c_files), 12)

        with tempfile.TemporaryDirectory() as tmpdir:
            for c_file in c_files:
                src = os.path.join(dsa_dir, c_file)
                obj = os.path.join(tmpdir, f"{c_file}.o")
                cmd = [gcc, "-Wall", "-Werror", "-c", src, "-o", obj]
                proc = subprocess.run(cmd, capture_output=True, text=True)
                self.assertEqual(
                    proc.returncode,
                    0,
                    f"gcc compilation failed for {c_file}:\nSTDOUT: {proc.stdout}\nSTDERR: {proc.stderr}",
                )

    def test_java_programs_compile(self):
        """6b. If javac is on PATH, all 10 Java programs compile (including mypack)."""
        javac = shutil.which("javac")
        if not javac:
            self.skipTest("javac not found on PATH; skipping Java compilation smoke test")

        java_dir = os.path.join(FOR_DEV_DIR, "java-lab", "programs")
        java_files = sorted(
            [os.path.join(java_dir, f) for f in os.listdir(java_dir) if f.endswith(".java")]
        )
        self.assertEqual(len(java_files), 10)

        mypack_file = os.path.join(java_dir, "mypack", "MyPackageClass.java")
        self.assertTrue(os.path.isfile(mypack_file), "mypack/MyPackageClass.java missing")

        with tempfile.TemporaryDirectory() as tmpdir:
            cmd = [javac, "-encoding", "UTF-8", "-d", tmpdir] + java_files + [mypack_file]
            proc = subprocess.run(cmd, capture_output=True, text=True)
            self.assertEqual(
                proc.returncode,
                0,
                f"javac compilation failed:\nSTDOUT: {proc.stdout}\nSTDERR: {proc.stderr}",
            )

    def test_mark_experiment_done_milestone_unlock(self):
        """Test milestone unlock when all 12 DSA experiments are completed."""
        _SESSION["experiments_done"] = []
        _SESSION["trophies"] = []
        _SESSION["badges"] = []

        for i in range(1, 13):
            _mark_experiment_done(f"DSA-{i}")

        self.assertIn(
            "dsa_lab_complete",
            _SESSION["trophies"],
            "Completing 12 DSA experiments must unlock 'dsa_lab_complete'",
        )

    def test_visualizer_explored_tracking(self):
        """Test that _record_visualizer_explored adds to visualizers_explored."""
        _SESSION["visualizers_explored"] = []
        _record_visualizer_explored("DSA-V1")
        self.assertIn("DSA-V1", _SESSION["visualizers_explored"])


if __name__ == "__main__":
    unittest.main()
