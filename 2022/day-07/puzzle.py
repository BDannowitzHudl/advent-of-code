"""Day 7, 2022 Advent of Code puzzle solution.

This is a solution to the puzzle found at:
https://adventofcode.com/2022/day/7

"""
from typing import Optional, List, Union


class Directory:
    def __init__(self, name: str, parent: Optional["Directory"] = None):
        self.name: str = name
        self.parent: Optional[Directory] = parent
        self.children: List[Union[File, Directory]] = []

    def __repr__(self):
        return f"dir {self.name} (size: {self.size})"

    @property
    def size(self) -> int:
        return 0 if not self.children else sum(child.size for child in self.children)
    
    def add_directory(self, name: str) -> None:
        self.children.append(Directory(name=name, parent=self))

    def add_file(self, name: str, size: int) -> None:
        self.children.append(File(name=name, size=size, parent=self))

    def cd(self, name: str) -> "Directory":
        for child in self.children:
            if child.name == name and type(child) == Directory:
                return child

    def ls(self) -> None:
        for child in self.children:
            print(child)

    def __contains__(self, name: str) -> bool:
        return name in [child.name for child in self.children]


class File:
    def __init__(self, name: str, size: int, parent: Directory):
        self.name: str = name
        self.size: int = size
        self.parent: Directory = parent

    def __repr__(self):
        return f"{self.size} {self.name}"


def create_filesystem(data_file: str) -> Directory:
    with open(data_file, 'r') as f:
        lines = f.read().splitlines()
    
    filesystem = Directory(name="/", parent=None)
    current_dir = filesystem
    
    n = 0
    while n < len(lines):
        if lines[n] == "$ cd /":
            current_dir = filesystem
            n += 1
        elif lines[n] == "$ cd ..":
            if current_dir != filesystem:
                current_dir = current_dir.parent
            else:
                raise ValueError("Cannot go up from root directory")
            n += 1
        elif lines[n].startswith("$ cd"):
            dir_name = lines[n].split(" ")[2]
            if dir_name not in current_dir:
                raise ValueError(f"Directory '{dir_name}' does not exist")
            else:
                current_dir = current_dir.cd(dir_name)
            n += 1
        elif lines[n].startswith("$ ls"):
            n += 1
            while n < len(lines) and not lines[n].startswith("$"):
                if lines[n].startswith("dir"):
                    dir_name = lines[n].split(" ")[1]
                    current_dir.add_directory(name=dir_name)
                else:
                    filesize = int(lines[n].split(" ")[0])
                    filename = lines[n].split(" ")[1]
                    current_dir.add_file(name=filename, size=filesize)
                n += 1
    
    return filesystem


def add_up_dir_sizes(dir: Directory, limit: int = 100_000) -> int:
    """If a directory is of size limit or less, add up all the directory sizes.
    Repeat this for all subdirectories.
    """
    size = 0
    for child in dir.children:
        if isinstance(child, Directory):
            if child.size < limit:
                size += child.size
            size += add_up_dir_sizes(child)
    return size

def find_smallest_directory(dir: Directory, limit: int) -> Directory:
    """Find the smallest directory that is larger than limit."""
    smallest_dir = None
    for child in dir.children:
        if isinstance(child, Directory):
            if child.size > limit:
                if smallest_dir is None:
                    smallest_dir = child
                elif child.size < smallest_dir.size:
                    smallest_dir = child
                # If this child directory has children directories that satisfy, consider them
                smallest_child_dir = find_smallest_directory(child, limit)
                if smallest_child_dir is not None and smallest_child_dir.size <= smallest_dir.size:
                    smallest_dir = smallest_child_dir
    return smallest_dir


def main(data_file: str) -> None:
    SYSTEM_SIZE = 70_000_000
    REQUIRED_SIZE = 30_000_000
    
    filesystem = create_filesystem(data_file)
    size = add_up_dir_sizes(filesystem, limit=100_000) 
    print(f"Part 1: {size} bytes\n")
    
    print(f"Filesystem usage: {filesystem.size} bytes")
    free_space = SYSTEM_SIZE - filesystem.size
    print(f"Free space: {free_space} bytes")
    space_needed = REQUIRED_SIZE - free_space
    print(f"Space needed: {space_needed} bytes\n")

    smallest_dir = find_smallest_directory(filesystem, limit=space_needed)
    print(f"Part 2: Smallest directory is {smallest_dir.name} with size {smallest_dir.size} bytes")

    return None
    
if __name__ == '__main__':
    main("puzzle_data.csv")