# A website requires a user to input a username and password to register. Write a
# program to check the validity of the password given by the user. Following are the
# criteria for checking password:
# 1. At least 1 letter between [a-z]
# 2. At least 1 number between [0-9]
# 1. At least 1 letter between [A-Z]
# 3. At least 1 character from [$#@]
# 4. Minimum length of transaction password: 6
# 5. Maximum length of transaction password: 12
# Hint: In the case of input data being supplied to the question, it should be assumed to
# be a console input.

# validation_pswd.py
# This script checks the validity of a password based on specified criteria.
import re
password = input("Enter your password: ")
valid = True

if not re.search("[a-z]", password):
    print("Password must contain at least one lowercase letter [a-z].")
    valid = False

if not re.search("[A-Z]", password):
    print("Password must contain at least one uppercase letter [A-Z].")
    valid = False

if not re.search("[0-9]", password):
    print("Password must contain at least one digit [0-9].")
    valid = False

if not re.search("[$#@]", password):
    print("Password must contain at least one special character [$#@].")
    valid = False

if len(password) < 6:
    print("Password must be at least 6 characters long.")
    valid = False

if len(password) > 12:
    print("Password must not be more than 12 characters long.")
    valid = False

# Final result
if valid:
    print("Password is valid!")
else:
    print("Password is invalid. Please try again.")
