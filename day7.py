import re
from dataclasses import dataclass
from typing import Optional, List, Union


@dataclass
class Directory:
    name: str
    parent: Optional["Directory"]
    contains: List[Union["Directory", "File"]]

    @property
    def size(self) -> int:
        return sum(c.size for c in self.contains)


@dataclass
class File:
    name: str
    size: int


if __name__ == "__main__":
    root = Directory(name="/", parent=None, contains=[])
    current_directory = root
    with open("data/day7_input.txt") as d:
        for line in d.readlines():
            if line.startswith("$"):
                if line.startswith("$ cd"):
                    cd = re.match(r"\$ cd (?P<target>[./a-z]+)\n", line)
                    if cd.group("target") == "..":
                        current_directory = current_directory.parent
                    elif cd.group("target") == "/":
                        while current_directory.name != "/":
                            current_directory = current_directory.parent
                    else:
                        current_directory = [
                            d for d in current_directory.contains
                            if isinstance(d, Directory) and d.name == cd.group("target")
                        ][0]

            else:
                ls_output = re.match(r"(?P<size>[0-9]+) (?P<file_name>[\.a-z]+)|dir (?P<nested_dir>[a-z]+)", line)
                if ls_output.group("file_name"):
                    item = File(ls_output.group("file_name"), int(ls_output.group("size")))
                else:
                    item = Directory(name=ls_output.group("nested_dir"), parent=current_directory, contains=[])
                current_directory.contains.append(item)

    def extract_directories(parent_directory):
        _directories = []
        for directory in parent_directory.contains:
            if isinstance(directory, Directory):
                _directories.append(directory)
                _directories += extract_directories(directory)
        return _directories

    directories = extract_directories(root)
    print(f"Challenge 1: {sum(d.size for d in directories if d.size <= 100000)}")

    required_space = 30_000_000
    currently_available = 70_000_000 - root.size
    minimum_free_up = required_space - currently_available
    to_be_deleted = list(sorted([d for d in directories if d.size >= minimum_free_up], key=lambda _d: _d.size))[0]
    print(f"Challenge 2: {to_be_deleted.size}")
