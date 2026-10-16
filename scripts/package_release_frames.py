"""Package dataset_final frames into GitHub Release sized ZIP assets.

Run from the publication repository:
    python scripts/package_release_frames.py ../dataset_final release_assets

The archives are stored outside Git. Extract every part into the same directory
to reconstruct ``frames/`` beside ``manifests/`` and ``loaders/``.
"""

import hashlib
import json
import sys
from pathlib import Path
from zipfile import ZIP_STORED, ZipFile


MAX_PAYLOAD_BYTES = 1_700_000_000
MAX_ASSET_BYTES = 2_000_000_000


def sha256(path):
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(8 * 1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def main(source, output):
    source = Path(source).resolve()
    output = Path(output).resolve()
    frame_root = source / "frames"
    if not frame_root.is_dir():
        raise SystemExit(f"Missing frame directory: {frame_root}")
    output.mkdir(parents=True, exist_ok=True)
    if any(output.glob("frames-part-*.zip")):
        raise SystemExit("Remove existing frames-part-*.zip assets before packaging")

    groups = []
    for origin in sorted(frame_root.iterdir()):
        if not origin.is_dir():
            continue
        for sample in sorted(origin.iterdir()):
            if not sample.is_dir():
                continue
            files = sorted(p for p in sample.iterdir() if p.is_file())
            groups.append((files, sum(p.stat().st_size for p in files)))

    assets = []
    archive = None
    payload = 0
    count = 0
    current_path = None

    def close_archive():
        nonlocal archive, current_path, payload, count
        if archive is None:
            return
        publication_root = Path(__file__).resolve().parents[1]
        for notice_name in ("DATA_SOURCES.md", "BDD100K_DATA_LICENSE.rst"):
            notice = publication_root / notice_name
            archive.write(notice, notice_name)
        archive.close()
        size = current_path.stat().st_size
        if size >= MAX_ASSET_BYTES:
            raise RuntimeError(f"Release asset exceeds size target: {current_path}")
        record = {
            "name": current_path.name,
            "bytes": size,
            "sha256": sha256(current_path),
            "frames": count,
        }
        assets.append(record)
        print(json.dumps(record, ensure_ascii=False), flush=True)
        archive = None
        current_path = None
        payload = 0
        count = 0

    for files, group_bytes in groups:
        if group_bytes > MAX_PAYLOAD_BYTES:
            raise RuntimeError(f"Sample group exceeds archive target: {files[0]}")
        if archive is not None and payload + group_bytes > MAX_PAYLOAD_BYTES:
            close_archive()
        if archive is None:
            current_path = output / f"frames-part-{len(assets) + 1:02d}.zip"
            archive = ZipFile(current_path, "w", compression=ZIP_STORED, allowZip64=True)
        for frame in files:
            archive.write(frame, frame.relative_to(source).as_posix())
            count += 1
        payload += group_bytes
    close_archive()

    manifest = {
        "format": "ZIP_STORED; extract all parts into the repository root",
        "source": "dataset_final/frames",
        "assets": assets,
        "total_frames": sum(item["frames"] for item in assets),
        "total_archive_bytes": sum(item["bytes"] for item in assets),
    }
    (output / "release-assets.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print(f"Packaged {manifest['total_frames']} frames in {len(assets)} assets", flush=True)


if __name__ == "__main__":
    if len(sys.argv) != 3:
        raise SystemExit("usage: package_release_frames.py SOURCE_ROOT OUTPUT_DIR")
    main(sys.argv[1], sys.argv[2])
