import io
from pathlib import Path
from unittest.mock import Mock

import pytest

from dissect.thumbcache.exceptions import NotAnIndexFileError
from dissect.thumbcache.index import IndexEntry, ThumbnailIndex, ThumbnailType


def test_index():
    ThumbnailIndex(fh=Mock)


@pytest.mark.parametrize(
    "path, expected_type",
    [
        (Path("data/windows_vista/thumbcache_idx.db"), ThumbnailType.WINDOWS_VISTA),
        (Path("data/windows_7/thumbcache_idx.db"), ThumbnailType.WINDOWS_7),
        (Path("data/windows_81/thumbcache_idx.db"), ThumbnailType.WINDOWS_81),
        (Path("data/windows_10/thumbcache_idx.db"), ThumbnailType.WINDOWS_10),
        (Path("data/windows_11/thumbcache_idx.db"), ThumbnailType.WINDOWS_10),
    ],
)
def test_index_type(
    path: Path,
    expected_type: ThumbnailType,
):
    index_path = Path(__file__).parent / path

    with index_path.open("rb") as ifile:
        index = ThumbnailIndex(ifile)
        assert index.type == expected_type


def test_index_unknown():
    with pytest.raises(NotAnIndexFileError):
        index = ThumbnailIndex(io.BytesIO(b"UNKNOWN_DATA"))
        index.header


def test_index_entry():
    index_entry = IndexEntry(io.BytesIO(b"\x00" * 20), ThumbnailType.WINDOWS_VISTA)
    assert not index_entry.in_use()


@pytest.mark.parametrize(
    "path",
    [
        "data/windows_11/thumbcache_idx.db",
        "data/windows_81/thumbcache_idx.db",
        "data/windows_10/thumbcache_idx.db",
        "data/windows_7/thumbcache_idx.db",
        "data/windows_vista/thumbcache_idx.db",
    ],
)
def test_get_index_entries(path: str):
    idx_file = Path(__file__).parent / path
    with idx_file.open("rb") as index_file:
        index = ThumbnailIndex(index_file)
        entries = list(index.entries())
        assert len(entries) == index.used_entries
