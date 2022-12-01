if __name__ == "__main__":
	data = []
	with open("data/day1_input.txt") as d:
		elf = 0
		for line in d.readlines():
			value = line.replace("\n", "")
			if not value:
				data.append(elf)
				elf = 0
			else:
				elf += int(value)

	print(f"challenge 1: {max(data)}")
	print(f"challenge 2: {sum(sorted(data, reverse=True)[:3])}")

