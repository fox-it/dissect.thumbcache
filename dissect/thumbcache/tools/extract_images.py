#!/bin/python3

from pathlib import Path

from dissect.thumbcache.thumbcache_file import ThumbcacheFile
from dissect.thumbcache.tools.utils import create_argument_parser, write_entry


def dump_entry_data(path: Path, output_dir: Path):
    with path.open("rb") as file:
        cache_file = ThumbcacheFile(file)

        for entry in cache_file.entries():
            write_entry(output_dir, entry, path.name.split("_", 1)[1])


def main():
    args = create_argument_parser("extract raw thumbcache entries")
    path: Path = args.cache_path

    if path.is_dir():
        for file in path.iterdir():
            if file.name.endswith("idx.db"):
                continue
            dump_entry_data(file, args.output_dir)
    else:
        dump_entry_data(path, args.output_dir)


if __name__ == "__main__":
    main()
