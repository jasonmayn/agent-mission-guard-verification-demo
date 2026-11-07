"""Tests of the independent *educational fixture* — NOT AMG tests."""
import io
import sys
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import replay


class FixtureTest(unittest.TestCase):
    def test_allowed(self):
        with redirect_stdout(io.StringIO()):
            r, n, changed, violations = replay.compare(replay.BASE / 'scenarios/01-allowed')
        self.assertEqual((r, n, violations), ('EVIDENCE_PASS', 4, []))
        self.assertEqual(changed, ['site/index.html'])

    def test_out_of_scope(self):
        with redirect_stdout(io.StringIO()):
            r, n, _, violations = replay.compare(replay.BASE / 'scenarios/02-out-of-scope')
        self.assertEqual((r, n, violations), ('VIOLATION', 4, ['notes/unexpected.txt']))

    def test_protected(self):
        with redirect_stdout(io.StringIO()):
            r, n, _, violations = replay.compare(replay.BASE / 'scenarios/03-protected-change')
        self.assertEqual((r, n, violations), ('VIOLATION', 4, ['site/legal.html']))

    def test_missing_requirement(self):
        with redirect_stdout(io.StringIO()):
            r, n, _, violations = replay.compare(replay.BASE / 'scenarios/04-missing-acceptance')
        self.assertEqual((r, n, violations), ('INCOMPLETE', 3, []))

    def test_symlink_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            t = Path(tmp)
            (t / 'escape').symlink_to(Path('/etc/passwd'))
            with self.assertRaises(ValueError):
                replay.contents(t)


if __name__ == '__main__':
    unittest.main()
