from pathlib import Path

from dissect.thumbcache.thumbcache import Thumbcache
from dissect.thumbcache.tools.utils import create_argument_parser, write_entry


def dump_entry_data_through_index(path: Path, output_dir: Path):

    cache = Thumbcache(path)
    for location_path, entry in cache.entries():
        file_name = location_path.stem.split("_", 1)[1]
        write_entry(output_dir, entry, file_name)


def main():
    args = create_argument_parser("extract indexed entries")

    path: Path = args.cache_path

    if path.is_dir():
        dump_entry_data_through_index(path, args.output_dir)


if __name__ == "__main__":
    main()
