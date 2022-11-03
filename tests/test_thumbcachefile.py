from pathlib import Path

import pytest

from dissect.thumbcache.c_thumbcache import c_thumbcache_index
from dissect.thumbcache.exceptions import (
    InvalidSignatureError,
    UnknownThumbnailTypeError,
)
from dissect.thumbcache.thumbcache_file import ThumbcacheFile
from dissect.thumbcache.util import ThumbnailType


@pytest.fixture
def thumbcache_file(path: str) -> ThumbcacheFile:
    current_path = Path(__file__).parent / "data" / path

    with current_path.open("rb") as thumb_file:
        yield ThumbcacheFile(thumb_file)


@pytest.mark.parametrize(
    "path, thumbnail_type",
    [
        ("windows_7/thumbcache_32.db", ThumbnailType.WINDOWS_7),
        ("windows_10/thumbcache_32.db", ThumbnailType.WINDOWS_10),
        ("windows_11/thumbcache_32.db", ThumbnailType.WINDOWS_10),
        ("windows_81/thumbcache_32.db", ThumbnailType.WINDOWS_81),
    ],
)
def test_thumbcache_version(thumbcache_file: ThumbcacheFile, thumbnail_type: ThumbnailType):

    assert thumbcache_file.version == thumbnail_type
    assert thumbcache_file.signature == b"CMMM"


def test_thumbcache_file_failed():
    with pytest.raises(InvalidSignatureError):
        ThumbcacheFile(b"UNKNOWN" + b"\x00" * 20)


def test_unknown_thumbnail_type():
    with pytest.raises(UnknownThumbnailTypeError):
        header = c_thumbcache_index.CACHE_HEADER(Signature=b"CMMM", Version=0xDEADBEEF)
        cache_file = ThumbcacheFile(header.dumps())
        cache_file.version


@pytest.mark.parametrize(
    "path, entries, size",
    [
        ("windows_7/thumbcache_256.db", 0x3, 0x0118),
        ("windows_10/thumbcache_32.db", 0x6, 0),
        ("windows_11/thumbcache_32.db", 0x9, 0),
        ("windows_81/thumbcache_32.db", 0x31, 0),
        ("windows_vista/thumbcache_32.db", 0x12, 0xDDA8),
    ],
)
def test_thumbcache_entries(thumbcache_file: ThumbcacheFile, entries: int, size: int):
    assert len(list(thumbcache_file.entries())) == entries
    assert thumbcache_file.size == size


@pytest.mark.parametrize(
    "path",
    [("windows_7/thumbcache_256.db")],
)
def test_thumbcache_get_entry(thumbcache_file: ThumbcacheFile):
    assert thumbcache_file[0x18].hash == "e84eb8f951bc2409"


@pytest.mark.parametrize(
    "path",
    [("windows_7/thumbcache_256.db")],
)
def test_thumbcache_get_entry_failed(thumbcache_file: ThumbcacheFile):
    with pytest.raises(InvalidSignatureError):
        thumbcache_file[0x42]
