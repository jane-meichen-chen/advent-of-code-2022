if __name__ == "__main__":
    with open("data/day6_input.txt") as d:
        buffer = d.readline().split("\n")[0]

    for i in range(4, len(buffer)):
        marker = buffer[i-4:i]
        if len(set(marker)) == 4:
            print(f"Challenge 1: {i}")
            break

    for j in range(14, len(buffer)):
        message = buffer[j-14:j]
        if len(set(message)) == 14:
            print(f"Challenge 2: {j}")
            break
