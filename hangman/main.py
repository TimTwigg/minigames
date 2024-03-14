with open("words.txt", "r") as f:
    words = [w.strip() for w in f.readlines()]

print(f"Words found: {len(words)}")

length = 10

words = [w for w in words if len(w) >= length]

print(f"Words of length {length}+ found: {len(words)}")