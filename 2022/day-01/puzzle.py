from collections import OrderedDict


def main(data_csv: str) -> None:

    # Read data
    data: list[str] = []
    with open(data_csv, "r") as f:
        data = f.read().splitlines()

    # Compile calories per elf
    elf_calories: OrderedDict[int, int] = {}
    elf_id = 1
    elf_calories[elf_id] = 0
    for line in data:
        if line != "":
            elf_calories[elf_id] += int(line)
        else:
            elf_id += 1
            elf_calories[elf_id] = 0
    
    # Find the elf with the most calories for part 1
    max_elf_id = max(elf_calories, key=elf_calories.get)
    print(f"Elf #{max_elf_id} with the most calories {elf_calories[max_elf_id]}\n")

    # Sort the whole thing
    sorted_elf_calories = OrderedDict(
        sorted(elf_calories.items(), key=lambda x: x[1], reverse=True)
    )

    # Find the three elves with the most calories for part 2
    top_calories: int = 0
    for elf, cal in list(sorted_elf_calories.items())[:3]:
        print(f"Elf #{elf} with {cal} calories")
        top_calories += cal
    print(f"Total Calories: {top_calories}")
    
    return None


if __name__ == "__main__":
    main("puzzle_data.csv")
    