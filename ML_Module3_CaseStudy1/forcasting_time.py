# Weather forecasting organization wants to show whether is it day or night. So,
# write a program for such an organization to find whether is it dark outside or not.
# Hint: Use the time module

import time

current_hour = time.localtime().tm_hour

if 6 <= current_hour < 18:
    print("It's daytime.")
else:
    print("It's nighttime.")

# Example output:
# If the current time is 10:30 AM, it will print:
# It's daytime.
# If the current time is 9:00 PM, it will print:
# It's nighttime.