#!/usr/bin/env python3
"""Stack explicitly ordered detail-page images without changing their pixels."""

from __future__ import annotations

import argparse
import os
import sys
import tempfile
from pathlib import Path

try:
    from PIL import Image
except ImportError as exc:  # pragma: no cover - environment guidance
    raise SystemExit(
        "Pillow is required. Use the Codex bundled Python runtime or install Pillow."
    ) from exc


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Vertically concatenate detail-page images in the exact order supplied. "
            "No resize, crop, gap, padding, filter, or color conversion is applied."
        )
    )
    parser.add_argument("pages", nargs="+", type=Path, help="Page files in final order")
    parser.add_argument("--output", required=True, type=Path, help="Output PNG path")
    parser.add_argument(
        "--overwrite",
        action="store_true",
        help="Replace an existing output file explicitly",
    )
    return parser.parse_args()


def fail(message: str) -> None:
    raise ValueError(message)


def stitch(pages: list[Path], output: Path, overwrite: bool = False) -> tuple[int, int]:
    if len(pages) < 2:
        fail("at least two page images are required")

    resolved_pages = [page.expanduser().resolve() for page in pages]
    resolved_output = output.expanduser().resolve()
    if len(set(resolved_pages)) != len(resolved_pages):
        fail("page list contains duplicate input paths")
    if resolved_output in resolved_pages:
        fail("output path cannot also be an input page")
    missing = [str(page) for page in resolved_pages if not page.is_file()]
    if missing:
        fail("missing page image(s): " + ", ".join(missing))
    if resolved_output.suffix.lower() != ".png":
        fail("output must use the .png extension for lossless delivery")
    if resolved_output.exists() and not overwrite:
        fail(f"output already exists: {resolved_output}; pass --overwrite to replace it")

    images: list[Image.Image] = []
    temp_path: Path | None = None
    try:
        for page in resolved_pages:
            image = Image.open(page)
            image.load()
            images.append(image)

        first = images[0]
        expected_width = first.width
        expected_mode = first.mode
        if any(image.width != expected_width for image in images):
            fail(
                "all pages must have the same width; refusing to resize: "
                + ", ".join(f"{path.name}={image.width}" for path, image in zip(resolved_pages, images))
            )
        if any(image.mode != expected_mode for image in images):
            fail(
                "all pages must have the same color mode; refusing to convert: "
                + ", ".join(f"{path.name}={image.mode}" for path, image in zip(resolved_pages, images))
            )

        total_height = sum(image.height for image in images)
        combined = Image.new(expected_mode, (expected_width, total_height))
        y = 0
        for image in images:
            combined.paste(image, (0, y))
            y += image.height

        resolved_output.parent.mkdir(parents=True, exist_ok=True)
        with tempfile.NamedTemporaryFile(
            prefix=f".{resolved_output.stem}.",
            suffix=".png",
            dir=resolved_output.parent,
            delete=False,
        ) as temp_file:
            temp_path = Path(temp_file.name)
        combined.save(temp_path, format="PNG", optimize=False)

        with Image.open(temp_path) as reopened:
            reopened.load()
            if reopened.size != (expected_width, total_height):
                fail(f"saved long image has unexpected dimensions: {reopened.size}")
            if reopened.mode != expected_mode:
                fail(f"saved long image changed color mode: {expected_mode} -> {reopened.mode}")
            y = 0
            for index, source in enumerate(images, start=1):
                segment = reopened.crop((0, y, expected_width, y + source.height))
                if segment.tobytes() != source.tobytes():
                    fail(f"pixel verification failed at page {index}")
                y += source.height

        if overwrite:
            os.replace(temp_path, resolved_output)
        else:
            try:
                os.link(temp_path, resolved_output)
            except FileExistsError:
                fail(f"output already exists: {resolved_output}; pass --overwrite to replace it")
            temp_path.unlink()
        temp_path = None

        print(f"CREATED={resolved_output}")
        print(f"PAGES={len(images)}")
        print(f"SIZE={expected_width}x{total_height}")
        print("ORDER=" + ">".join(str(index) for index in range(1, len(images) + 1)))
        print(f"PIXEL_MATCH={len(images)}/{len(images)}")
        return expected_width, total_height
    finally:
        for image in images:
            image.close()
        if temp_path is not None:
            temp_path.unlink(missing_ok=True)


def main() -> int:
    args = parse_args()
    try:
        stitch(args.pages, args.output, args.overwrite)
    except (OSError, ValueError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
