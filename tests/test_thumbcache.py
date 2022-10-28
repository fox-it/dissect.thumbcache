from pathlib import Path

import pytest

from dissect.thumbcache.thumbcache import Thumbcache


@pytest.fixture
def thumbcache(path: str) -> Thumbcache:
    file = Path(__file__).parent / path
    return Thumbcache(file)


def test_thumbcache():
    assert Thumbcache(Path(__file__).parent / "data/windows_7")


@pytest.mark.parametrize(
    "path, expected_mapping",
    [
        ("data/windows_vista", {0: "32", 1: "96", 2: "256", 3: "1024", 4: "sr"}),
        (
            "data/windows_7",
            {0: "32", 1: "96", 2: "256", 3: "1024", 4: "sr"},
        ),
        (
            "data/windows_81",
            {
                0: "16",
                1: "32",
                2: "48",
                3: "96",
                4: "256",
                5: "1024",
                6: "1600",
                7: "sr",
                8: "wide",
                9: "exif",
                10: "wide_alternate",
            },
        ),
        (
            "data/windows_10",
            {
                0: "16",
                1: "32",
                2: "48",
                3: "96",
                4: "256",
                5: "768",
                6: "1280",
                7: "1920",
                8: "2560",
                9: "sr",
                10: "wide",
                11: "exif",
                12: "wide_alternate",
                13: "custom_stream",
            },
        ),
    ],
)
def test_thumbcache_mapping(thumbcache: Thumbcache, expected_mapping: dict):
    for key, value in expected_mapping.items():
        assert value in thumbcache.mapping[key].name


@pytest.mark.parametrize(
    "path, nr_of_entries",
    [
        (
            "data/windows_7",
            1,
        ),
        (
            "data/windows_vista",
            78,
        ),
    ],
)
def test_thumbcache_entries(thumbcache: Thumbcache, nr_of_entries: int):
    assert len(list(thumbcache.entries())) == nr_of_entries


@pytest.mark.parametrize(
    "path, offsets, expected_entries",
    [
        ("data/windows_7", [0xFFFFFFFF, 0xFFFFFFFF, 152, 0xFFFFFFFF, 0xFFFFFFFF], 1),
        ("data/windows_7", [0xFFFFFFFF, 0xFFFFFFFF, 0xFFFFFFFF, 0xFFFFFFFF, 0xFFFFFFFF], 0),
    ],
)
def test_entries_from_offset(thumbcache: Thumbcache, offsets, expected_entries):
    assert len(list(thumbcache._entries_from_offsets(offsets))) == expected_entries
