import enum
from contextlib import contextmanager
from typing import BinaryIO


class ThumbnailType(enum.IntEnum):
    WINDOWS_VISTA = 0x14
    WINDOWS_7 = 0x15
    WINDOWS_81 = 0x1F
    WINDOWS_10 = 0x20


@contextmanager
def seek_and_return(file: BinaryIO, position: int) -> BinaryIO:
    current_position = file.tell()
    try:
        file.seek(position)
        yield file
    finally:
        file.seek(current_position)
