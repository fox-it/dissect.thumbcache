#!/bin/python3

from pathlib import Path

from dissect.thumbcache.exceptions import Error
from dissect.thumbcache.thumbcache_file import ThumbcacheFile
from dissect.thumbcache.tools.utils import create_argument_parser, write_entry


def dump_entry_data(path: Path, output_dir: Path):
    with path.open("rb") as file:
        try:
            cache_file = ThumbcacheFile(file)

            for entry in cache_file.entries():
                write_entry(output_dir, entry, path.name.split("_", 1)[1])
        except Error as e:
            print(e)


def main():
    args = create_argument_parser("extract raw thumbcache entries").parse_args()
    path: Path = args.cache_path

    if path.name.endswith("idx.db"):
        print("Please provide a file other than the idx file.")
        exit(1)

    if path.is_dir():
        for file in path.iterdir():
            if file.name.endswith("idx.db"):
                continue
            dump_entry_data(file, args.output_dir)
    else:
        dump_entry_data(path, args.output_dir)


if __name__ == "__main__":
    main()
