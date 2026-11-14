"""The template must produce a repository whose own tests pass. Run: python3 -m unittest discover -s tests"""
from __future__ import annotations

import os
import re
import subprocess
import sys
import tempfile
import unittest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class Init(unittest.TestCase):
    def test_init_creates_a_green_repo(self):
        with tempfile.TemporaryDirectory() as tmp:
            dest = os.path.join(tmp, "acme-skills")
            r = subprocess.run([sys.executable, os.path.join(ROOT, "init.py"), "--product", "Acme IAM", "--prefix",
                                "acme", "--dest", dest, "--skill", "workflows"], capture_output=True, text=True)
            self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
            self.assertTrue(os.path.isdir(os.path.join(dest, "skills", "acme-workflows")))
            for base, _, files in os.walk(dest):
                for f in files:
                    with open(os.path.join(base, f), encoding="utf-8", errors="ignore") as fh:
                        self.assertIsNone(re.search(r"__(PRODUCT|PREFIX|REPO|AUTHOR|GITHUB|YEAR|DATE)__", fh.read()), f)

    def test_refuses_non_empty_destination(self):
        with tempfile.TemporaryDirectory() as tmp:
            open(os.path.join(tmp, "x"), "w").close()
            r = subprocess.run([sys.executable, os.path.join(ROOT, "init.py"), "--product", "A", "--prefix", "a1",
                                "--dest", tmp, "--no-test"], capture_output=True, text=True)
            self.assertEqual(r.returncode, 2)

    def test_eval_scripts_roundtrip(self):
        ev = os.path.join(ROOT, "template", "evals")
        with tempfile.TemporaryDirectory() as tmp:
            q = os.path.join(tmp, "q.jsonl")
            b = os.path.join(tmp, "b.jsonl")
            s = os.path.join(tmp, "s.jsonl")
            open(q, "w").write('{"id":"x-1","skill":"x","q":"?","must":["m"],"must_not":[],"source":""}\n')
            open(b, "w").write('{"id":"x-1","answer":"no"}\n')
            open(s, "w").write('{"id":"x-1","answer":"yes"}\n')
            subprocess.run([sys.executable, os.path.join(ev, "blind.py"), q, b, s, "--out", tmp], check=True,
                           capture_output=True)
            import json
            m = json.load(open(os.path.join(tmp, "blind_map.json")))
            g = {"id": "x-1", "A": {"score": 2 if m["x-1"]["A"] == "skills" else 0},
                 "B": {"score": 2 if m["x-1"]["B"] == "skills" else 0}}
            open(os.path.join(tmp, "grades.jsonl"), "w").write(json.dumps(g) + "\n")
            out = subprocess.run([sys.executable, os.path.join(ev, "score.py"), os.path.join(tmp, "grades.jsonl"),
                                  os.path.join(tmp, "blind_map.json"), q], capture_output=True, text=True).stdout
            self.assertIn("**0/2 (0%)**", out)
            self.assertIn("**2/2 (100%)**", out)


if __name__ == "__main__":
    unittest.main()
