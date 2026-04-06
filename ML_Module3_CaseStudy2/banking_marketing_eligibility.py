# banking_marketing_eligibility.py
import csv

unique_jobs = set()
ages = []

with open('bank-data.csv', 'r') as file:
    reader = csv.DictReader(file)
    for row in reader:
        job = row['job'].strip().lower()
        unique_jobs.add(job)

        try:
            ages.append(int(row['age']))
        except ValueError:
            pass 

if ages:
    min_age = min(ages)
    max_age = max(ages)
else:
    min_age = max_age = None


age_criteria = {
    "min_age": min_age,
    "max_age": max_age
}

print("System ready")
print(f"Professions loaded: {len(unique_jobs)} unique professions.")
print(f"Age range in data: {min_age} - {max_age}")


while True:
    profession = input("\nEnter client profession (or type 'END' to quit): ").strip()
    if profession.upper() == "END":
        print("Exiting system. Goodbye!")
        break

   
    if profession.lower() in unique_jobs:
        print(f"Client with profession '{profession}' is ELIGIBLE for marketing campaign.")
    else:
        print(f"Client with profession '{profession}' is NOT eligible.")

    if age_criteria['min_age'] is not None and age_criteria['max_age'] is not None:
        print(f"Age criteria: {age_criteria['min_age']} - {age_criteria['max_age']}")
    else:
        print("Age criteria not available.")    
    print("Please try again with a valid profession.")
    print("Thank you for using the banking marketing eligibility system.")
