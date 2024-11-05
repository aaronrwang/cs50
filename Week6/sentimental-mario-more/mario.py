from cs50 import get_int

while True:
    N = get_int("Height: ")
    if N > 0 and N < 9:
        break
for i in range(1, N + 1):
    print(" " * (N - i), end="")
    print("#" * (i), end="")
    print("  ", end="")
    print("#" * (i), end="\n")
