class Error(Exception):
    """A generic exception for the thumbcache module."""

    pass


class NotAnIndexFileError(Error):
    """Raises if a thumbnail index signature could not be found."""

    pass


class InvalidSignatureError(Error):
    """Raises if the signature does not match the expected value."""

    pass


class UnknownThumbnailTypeError(Error):
    """Raises if an unknown thumbnail type was found."""

    pass
