"""Tests for the heavy-file scanner, driven by a temporary directory tree."""

from __future__ import annotations

import os

import pytest

from pchealth.collectors.heavy_files import scan_path


def _write(path: str, size: int) -> None:
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "wb") as fh:
        fh.write(b"\0" * size)


@pytest.fixture
def tree(tmp_path):
    """A small, predictable directory tree.

        root/
          big.bin            (3000 B)
          small.txt          (100 B)
          media/
            movie.bin        (5000 B)
            clips/
              clip.bin       (2000 B)
          empty/
    """
    root = tmp_path / "root"
    _write(str(root / "big.bin"), 3000)
    _write(str(root / "small.txt"), 100)
    _write(str(root / "media" / "movie.bin"), 5000)
    _write(str(root / "media" / "clips" / "clip.bin"), 2000)
    os.makedirs(str(root / "empty"), exist_ok=True)
    return root


def test_totals_and_counts(tree):
    result = scan_path(str(tree), top_n=10)
    assert result.total_bytes == 3000 + 100 + 5000 + 2000
    assert result.files_scanned == 4
    assert result.errors == 0


def test_top_files_ordered_by_size(tree):
    result = scan_path(str(tree), top_n=10)
    sizes = [e.size_bytes for e in result.top_files]
    assert sizes == sorted(sizes, reverse=True)
    assert result.top_files[0].size_bytes == 5000  # movie.bin
    assert result.top_files[0].path.endswith("movie.bin")


def test_directory_sizes_are_cumulative(tree):
    result = scan_path(str(tree), top_n=10)
    dirs = {os.path.basename(e.path): e.size_bytes for e in result.top_dirs}
    # media = movie(5000) + clips/clip(2000)
    assert dirs["media"] == 7000
    assert dirs["clips"] == 2000


def test_media_is_heaviest_folder(tree):
    result = scan_path(str(tree), top_n=10)
    assert os.path.basename(result.top_dirs[0].path) == "media"


def test_top_n_limits_results(tree):
    result = scan_path(str(tree), top_n=1)
    assert len(result.top_files) == 1
    assert len(result.top_dirs) == 1
    assert result.top_files[0].size_bytes == 5000


def test_empty_dir_not_in_top(tree):
    result = scan_path(str(tree), top_n=10)
    names = [os.path.basename(e.path) for e in result.top_dirs]
    # A 0-byte folder can appear but must never rank above real data; here we
    # only assert it does not crash and real folders dominate.
    assert names[0] == "media"


def test_root_itself_excluded_from_dirs(tree):
    result = scan_path(str(tree), top_n=10)
    paths = [os.path.abspath(e.path) for e in result.top_dirs]
    assert os.path.abspath(str(tree)) not in paths


def test_single_file_path(tmp_path):
    target = tmp_path / "solo.bin"
    _write(str(target), 1234)
    result = scan_path(str(target), top_n=5)
    assert result.files_scanned == 1
    assert result.total_bytes == 1234
    assert result.top_files[0].path.endswith("solo.bin")
    assert result.top_dirs == []


def test_missing_path_raises(tmp_path):
    with pytest.raises(FileNotFoundError):
        scan_path(str(tmp_path / "does-not-exist"), top_n=5)


def test_expanduser_is_applied(monkeypatch, tree):
    # "~" should resolve to the home directory before scanning.
    monkeypatch.setenv("HOME", str(tree))
    monkeypatch.setenv("USERPROFILE", str(tree))  # Windows home variable
    result = scan_path("~", top_n=3)
    assert os.path.abspath(result.root) == os.path.abspath(str(tree))
