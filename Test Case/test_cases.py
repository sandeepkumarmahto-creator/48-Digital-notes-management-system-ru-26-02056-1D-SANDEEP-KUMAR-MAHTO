"""Test cases for Digital Notes Management System (one.py)

Run with:  python test_cases.py
"""

import io
import os
import sys
import tempfile
import unittest
from contextlib import redirect_stdout
from unittest.mock import patch

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import one


def run_program(notes_content, inputs):
    """Run one.main() in a temp folder with fake keyboard input.
    Returns (console_output, notes_file_text_or_None)."""
    old_cwd = os.getcwd()
    with tempfile.TemporaryDirectory() as tmp:
        os.chdir(tmp)
        try:
            if notes_content is not None:
                with open("notes.txt", "w", encoding="utf-8") as f:
                    f.write(notes_content)
            buf = io.StringIO()
            with patch("builtins.input", side_effect=inputs + ["6"]), \
                    redirect_stdout(buf):
                one.main()
            saved = None
            if os.path.exists("notes.txt"):
                with open("notes.txt", encoding="utf-8") as f:
                    saved = f.read()
            return buf.getvalue(), saved
        finally:
            os.chdir(old_cwd)


TWO_NOTES = "N1|Python|Learn loops\nN2|Maths|Revise algebra\n"


class TestNotesManagement(unittest.TestCase):

    def test_case_1_normal_input_add(self):
        out, saved = run_program(None, ["1", "Python", "Learn loops"])
        self.assertIn("Note saved. ID: N1 | Python", out)
        self.assertEqual(saved, "N1|Python|Learn loops\n")

    def test_case_2_boundary_empty_file(self):
        out, saved = run_program("", ["2"])
        self.assertIn("No notes found.", out)

    def test_case_3_invalid_empty_title(self):
        out, saved = run_program(None, ["1", "", "Buy books"])
        self.assertIn("Title cannot be empty. Note not saved.", out)
        self.assertIsNone(saved)

    def test_case_4a_search(self):
        out, saved = run_program(TWO_NOTES, ["3", "python"])
        self.assertIn("N1 | Python | Learn loops", out)
        self.assertNotIn("N2 | Maths", out)

    def test_case_4b_edit(self):
        out, saved = run_program(TWO_NOTES, ["4", "N2", "Revise calculus"])
        self.assertIn("Note N2 updated.", out)
        self.assertIn("N2|Maths|Revise calculus", saved)

    def test_case_4c_delete(self):
        out, saved = run_program(TWO_NOTES, ["5", "N1"])
        self.assertIn("Note N1 deleted. Notes left: 1", out)
        self.assertEqual(saved, "N2|Maths|Revise algebra\n")

    def test_note_id_does_not_exist(self):
        out, saved = run_program(TWO_NOTES, ["5", "N9"])
        self.assertIn("Note N9 does not exist.", out)
        self.assertEqual(saved, TWO_NOTES)


if __name__ == "__main__":
    unittest.main(verbosity=2)
