import sys

with open('1_input.txt', 'r') as f:
    # Redirecting input from input.txt
    sys.stdin = f
    name = input("Enter the coordinates: \n")
    input_string = input()  # reads the first line of input from input.txt
    print(input_string)  # prints the first line of input



