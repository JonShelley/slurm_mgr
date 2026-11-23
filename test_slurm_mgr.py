import contextlib
import io
from pathlib import Path
import runpy
import subprocess
import unittest
from unittest.mock import patch


slurm_mgr = runpy.run_path(str(Path(__file__).with_name("slurm_mgr")))


class InfoTests(unittest.TestCase):
    def test_full_multiline_reasons_and_grouped_nodes(self):
        output = (
            "USER TIMESTAMP NODELIST REASON\x1e\n"
            "root 2026-11-23T14:15:56 node-[1,5-8] Healthcheck:: Multiple failures\n"
            "GPU unavailable\n\nlink down\x1e\n"
            "root 2026-11-23T14:15:58 node-2 Other reason\x1e\n"
        )
        result = subprocess.CompletedProcess([], 0, stdout=output)
        with patch("subprocess.run", return_value=result) as run:
            with contextlib.redirect_stdout(io.StringIO()) as stdout:
                self.assertEqual(slurm_mgr["main"](["info", "-R"]), 0)
        self.assertEqual(stdout.getvalue(), (
            "USER TIMESTAMP NODELIST REASON\n"
            "root 2026-11-23T14:15:56 node-[1,5-8] Healthcheck:: Multiple failures;"
            "GPU unavailable;;link down\n"
            "root 2026-11-23T14:15:58 node-2 Other reason\n"
        ))
        self.assertEqual(run.call_args.args[0], [
            "sinfo", "-R", "-o", "%9u %19H %60N %E\x1e",
        ])

    def test_sinfo_failure_preserves_exit_status(self):
        result = subprocess.CompletedProcess([], 1, stdout="partial output")
        with patch("subprocess.run", return_value=result):
            with contextlib.redirect_stdout(io.StringIO()) as stdout:
                self.assertEqual(slurm_mgr["main"](["info", "-R"]), 1)
        self.assertEqual(stdout.getvalue(), "")

    def test_missing_sinfo_explains_requirement(self):
        with patch("subprocess.run", side_effect=FileNotFoundError):
            with contextlib.redirect_stderr(io.StringIO()) as stderr:
                self.assertEqual(slurm_mgr["main"](["info", "-R"]), 127)
        self.assertIn("sinfo was not found", stderr.getvalue())


if __name__ == "__main__":
    unittest.main()
