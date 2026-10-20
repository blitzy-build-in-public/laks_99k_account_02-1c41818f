"""Read-only checks for the literal data file and the program's exact stdout."""

import subprocess
import sys
import unittest
from pathlib import Path

REPOSITORY_ROOT = Path(__file__).resolve().parents[1]

EXPECTED_LINE = b"Welcome to Blitzy\n"
EXPECTED_LINES = 4000
EXPECTED_BYTES = 72000


class HelloWorldTest(unittest.TestCase):
    """Verify hello_world.txt byte for byte and the stdout of hello_world.py."""

    def test_hello_world_txt_is_literal_line_repeated(self):
        """The data file is the expected line 4000 times, 72000 bytes, no CR."""
        data = (REPOSITORY_ROOT / "hello_world.txt").read_bytes()
        self.assertEqual(data, EXPECTED_LINE * EXPECTED_LINES)
        self.assertEqual(len(data), EXPECTED_BYTES)
        self.assertNotIn(b"\r", data)

    def test_hello_world_py_writes_exact_stdout(self):
        """The program exits 0 and its captured stdout is the one expected line."""
        result = subprocess.run(
            [sys.executable, "hello_world.py"],
            capture_output=True,
            cwd=REPOSITORY_ROOT,
        )
        self.assertEqual(result.returncode, 0)
        self.assertEqual(result.stdout, EXPECTED_LINE)
