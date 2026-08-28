import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from PIL import Image


SKILL_ROOT = Path(__file__).resolve().parents[1]
SCRIPT = SKILL_ROOT / "scripts" / "stitch_long_page.py"


class StitchLongPageTests(unittest.TestCase):
    def run_script(self, *args: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [sys.executable, str(SCRIPT), *args],
            text=True,
            capture_output=True,
            check=False,
        )

    def test_stitches_explicit_order_without_pixel_changes(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            first = root / "page-1.png"
            second = root / "page-2.png"
            output = root / "long.png"
            Image.new("RGB", (4, 2), (244, 180, 120)).save(first)
            Image.new("RGB", (4, 3), (95, 70, 45)).save(second)

            result = self.run_script(
                "--output", str(output), str(first), str(second)
            )

            self.assertEqual(result.returncode, 0, result.stderr)
            with Image.open(output) as combined:
                self.assertEqual(combined.size, (4, 5))
                self.assertEqual(
                    combined.crop((0, 0, 4, 2)).tobytes(),
                    Image.open(first).tobytes(),
                )
                self.assertEqual(
                    combined.crop((0, 2, 4, 5)).tobytes(),
                    Image.open(second).tobytes(),
                )
            self.assertIn("PIXEL_MATCH=2/2", result.stdout)

    def test_rejects_mismatched_widths_instead_of_resizing(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            first = root / "page-1.png"
            second = root / "page-2.png"
            output = root / "long.png"
            Image.new("RGB", (4, 2), "white").save(first)
            Image.new("RGB", (5, 2), "white").save(second)

            result = self.run_script(
                "--output", str(output), str(first), str(second)
            )

            self.assertNotEqual(result.returncode, 0)
            self.assertIn("same width", result.stderr)
            self.assertFalse(output.exists())

    def test_refuses_to_overwrite_without_explicit_flag(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            first = root / "page-1.png"
            second = root / "page-2.png"
            output = root / "long.png"
            Image.new("RGB", (4, 2), "white").save(first)
            Image.new("RGB", (4, 2), "black").save(second)
            output.write_bytes(b"existing")

            result = self.run_script(
                "--output", str(output), str(first), str(second)
            )

            self.assertNotEqual(result.returncode, 0)
            self.assertIn("already exists", result.stderr)
            self.assertEqual(output.read_bytes(), b"existing")


if __name__ == "__main__":
    unittest.main()
