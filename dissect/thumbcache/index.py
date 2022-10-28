from __future__ import annotations

from datetime import datetime
from typing import BinaryIO, Iterator

from dissect.cstruct import Structure
from dissect.util import ts

from dissect.thumbcache.c_thumbcache import c_thumbcache_index
from dissect.thumbcache.exceptions import NotAnIndexFileError
from dissect.thumbcache.util import ThumbnailType

INDEX_ENTRIES = {
    ThumbnailType.WINDOWS_7: 5,
    ThumbnailType.WINDOWS_81: 11,
    ThumbnailType.WINDOWS_10: 14,
    ThumbnailType.WINDOWS_VISTA: 5,
}

MAX_IMM_OFFSET = 4
BYTES_IN_NUMBER = 4
IDENTIFIER_BYTES = 8


class ThumbnailIndex:
    _signature = b"IMMM"

    def __init__(self, file: BinaryIO) -> None:
        self.file = file
        self._header = None

    @property
    def header(self) -> Structure:
        if self._header is None:
            self._header = self._find_header(self.file)
        return self._header

    def _find_header(self, file: BinaryIO) -> Structure:
        """Searches for the header signature, and puts ``file`` at the correct position.

        From Windows 8.1 onward, the two fields seem to use a 64-bit format field
        inside the header with the value ``0C 00 30 20``.

        Args:
            file: The file to read the header and indexes from.

        Returns:
            A c_thumbcache_index.INDEX_HEADER structure.

        Raises:
            NotAThumbnailIndexFileError: If the ``IMMM`` signature could not be found.
        """
        position = file.tell()
        buffer = file.read(len(c_thumbcache_index.INDEX_HEADER_V1))
        offset = buffer.find(self._signature)

        if offset == MAX_IMM_OFFSET:
            file.seek(position)

            header = c_thumbcache_index.INDEX_HEADER_V2(file)
            # From looking at the index files, it has a specific amount of information.
            # It is alligned in the follwing way:
            #   INDEX_HEADER_V2
            #   length of an INDEX_ENTRY of a specific type including the cache_offsets
            # After that point, there are only zero bytes, which seem to have the following relation:
            #   length of the same INDEX_ENTRY - length of the length of INDEX_HEADER_V2
            #
            # TODO: see if it the data contains any useful information.

            # Read one index entry from the file till only zero bytes
            entry = IndexEntry(file, header.version)
            entry.header
            entry.cache_offsets

            # Read offset to first entry
            zero_bytes = len(entry.header) + INDEX_ENTRIES.get(header.version) * BYTES_IN_NUMBER - len(header)
            file.read(zero_bytes)
            return header
        elif offset == 0:
            return c_thumbcache_index.INDEX_HEADER_V1(buffer)
        else:
            raise NotAnIndexFileError(
                f"The index file signature {self._signature!r} could not be found at the expected location."
            )

    @property
    def version(self) -> int:
        return self.header.version

    @property
    def type(self) -> ThumbnailType:
        return ThumbnailType(self.version)

    @property
    def total_entries(self) -> int:
        return self.header.total_entries

    @property
    def used_entries(self) -> int:
        return self.header.used_entries

    def entries(self) -> Iterator[IndexEntry]:
        """Returns all index entries that are actually used."""
        for _ in range(self.total_entries):
            entry = IndexEntry(self.file, self.type)
            entry.header
            entry.cache_offsets

            if entry.in_use():
                yield entry


class IndexEntry:
    def __init__(self, file: BinaryIO, type: ThumbnailType, data=[]) -> None:
        self.file = file
        self.type = type
        self._header = None
        self._data = None

    @property
    def header(self) -> Structure:
        if not self._header:
            self._header = self._select_header()
        return self._header

    def _select_header(self) -> Structure:
        """Selects header version according to the thumbnailtype."""
        if self.type == ThumbnailType.WINDOWS_VISTA:
            return c_thumbcache_index.VISTA_ENTRY(self.file)
        elif self.type == ThumbnailType.WINDOWS_7:
            return c_thumbcache_index.WINDOWS7_ENTRY(self.file)
        else:
            return c_thumbcache_index.WINDOWS8_ENTRY(self.file)

    def in_use(self) -> bool:
        return self.identifier != b"\x00" * IDENTIFIER_BYTES

    @property
    def identifier(self) -> bytes:
        return self.header.hash

    @property
    def flags(self) -> int:
        return self.header.flags

    @property
    def cache_offsets(self) -> list[int]:
        """Retrieves the index data entries.

        These are offsets into the thumbcache files, where the order specifies in which of the files.
        More information about the order can be found in :class:`Thumbcache`.

        """
        if not self._data:
            size = INDEX_ENTRIES.get(self.type)
            self._data = c_thumbcache_index.uint32[size](self.file)
            if self.type > ThumbnailType.WINDOWS_7:
                # Alignment step
                self.file.read((size % 2) * BYTES_IN_NUMBER)
        return self._data

    @property
    def last_modified(self) -> datetime:
        if self.type == ThumbnailType.WINDOWS_VISTA:
            return ts.wintimestamp(self._header.last_modified)
        return None

    def __repr__(self) -> str:
        return (
            f"identifier={self.identifier.hex()} flags={hex(self.flags)} "
            f"cache_offsets={[hex(x) for x in self.cache_offsets]}"
        )
