# A Robot moves in a Plane starting from the origin point (0,0). The robot can move
# UP, DOWN, LEFT, or RIGHT. The trace of Robot movement is as given following:
# UP 5
# DOWN 3
# LEFT 3
# RIGHT 2
# The numbers after directions are steps. Write a program to compute the
# distance current position after a sequence of movements.
# Hint: Use the math module.

import math

# Initialize starting position
x, y = 0, 0

print("Enter movements (e.g., UP 5). Type 'STOP' to end:")

while True:
    move = input().strip()
    if move.upper() == "STOP":
        break
    if not move:
        continue

    direction, steps = move.split()
    steps = int(steps)

    if direction.upper() == "UP":
        y += steps
    elif direction.upper() == "DOWN":
        y -= steps
    elif direction.upper() == "LEFT":
        x -= steps
    elif direction.upper() == "RIGHT":
        x += steps

# Calculate distance from origin
distance = math.sqrt(x**2 + y**2)

print(f"Current position: ({x}, {y})")
print(f"Distance from origin: {distance:.2f}")

# Example input:
# Enter movements (e.g., UP 5). Type 'STOP' to end:
# UP 5
# DOWN 3
# LEFT 3
# RIGHT 2
# STOP
# Current position: (-1, 2)
# Distance from origin: 2.24

