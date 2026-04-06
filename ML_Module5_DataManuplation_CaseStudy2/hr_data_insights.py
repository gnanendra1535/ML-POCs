# HR Data Insights Analysis
import pandas as pd

# Load dataset
file_path = "Salaries.csv" 
salaries_df = pd.read_csv(file_path)

# Convert numeric columns
for col in ['BasePay','OvertimePay','OtherPay','Benefits','TotalPay','TotalPayBenefits']:
    salaries_df[col] = pd.to_numeric(salaries_df[col], errors='coerce')


# 1. Increase in total salary cost (2011 → 2014)

salary_2011 = salaries_df[salaries_df['Year'] == 2011]['TotalPayBenefits'].sum()
salary_2014 = salaries_df[salaries_df['Year'] == 2014]['TotalPayBenefits'].sum()
increase_salary_cost = salary_2014 - salary_2011
print("1. Increase in Total Salary Cost (2011 → 2014):", increase_salary_cost)

# 2. Job Title in 2014 with highest mean salary

job_2014 = salaries_df[salaries_df['Year'] == 2014]
highest_mean_job_2014 = job_2014.groupby('JobTitle')['TotalPayBenefits'].mean().idxmax()
highest_mean_salary = job_2014.groupby('JobTitle')['TotalPayBenefits'].mean().max()
print("\n2. Highest Mean Salary Job (2014):", highest_mean_job_2014, "→", highest_mean_salary)

# 3. Money saved in 2014 by stopping OvertimePay

saved_overtime_2014 = job_2014['OvertimePay'].sum()
print("\n3. Money saved by stopping OvertimePay (2014):", saved_overtime_2014)

# 4. Top 5 common jobs in 2014 and their cost

top5_jobs = job_2014['JobTitle'].value_counts().head(5).index
top5_cost = job_2014[job_2014['JobTitle'].isin(top5_jobs)].groupby('JobTitle')['TotalPayBenefits'].sum()
print("\n4. Top 5 common jobs in 2014 and cost:\n", top5_cost)

# 5. Top earning employee across all years

top_earner = salaries_df.loc[salaries_df['TotalPayBenefits'].idxmax(), ['EmployeeName','TotalPayBenefits']]
print("\n5. Top earning employee across all years:\n", top_earner)

# Enhancements
# Last 5 common jobs in 2014 and cost
last5_jobs = job_2014['JobTitle'].value_counts().tail(5).index
last5_cost = job_2014[job_2014['JobTitle'].isin(last5_jobs)].groupby('JobTitle')['TotalPayBenefits'].sum()
print("\n6. Last 5 common jobs in 2014 and cost:\n", last5_cost)

# OvertimePay % of TotalPayBenefits in 2011
job_2011 = salaries_df[salaries_df['Year'] == 2011]
overtime_pct_2011 = (job_2011['OvertimePay'].sum() / job_2011['TotalPayBenefits'].sum()) * 100
print("\n7. Overtime % of TotalPayBenefits in 2011:", overtime_pct_2011)

# Job Title in 2014 with lowest mean salary
lowest_mean_job_2014 = job_2014.groupby('JobTitle')['TotalPayBenefits'].mean().idxmin()
lowest_mean_salary = job_2014.groupby('JobTitle')['TotalPayBenefits'].mean().min()
print("\n8. Lowest Mean Salary Job (2014):", lowest_mean_job_2014, "→", lowest_mean_salary)

# 1. Increase in total salary cost (2011 → 2014):
#  $1,227,752,749.88 increase

# 2. Job Title in 2014 with highest mean salary:
#  Chief Investment Officer → Avg Salary ≈ $436,224.36

# 3. Money that could be saved in 2014 by stopping OverTimePay:
#  $205,918,599.27

# 4. Top 5 common jobs in 2014 and their total cost:

# Transit Operator → $214,976,400

# Registered Nurse → $187,216,500

# Firefighter → $144,827,000

# Special Nurse → $53,443,100

# Public Svc Aide-Public Works → $9,806,300

# 5. Top earning employee across all years:
#  NATHANIEL FORD → $567,595.43

# 6. Last 5 common jobs in 2014 and their cost:

# Asst Dir, Log Cabin Rnch → $138,807.52

# Chf Prob Ofc, Juv Court → $246,877.14

# Claims Process Clerk → $89,163.42

# Electric Motor Repair Sprv 1 → $141,254.20

# Media Production Specialist → $101,110.75

# 7. Overtime Pay as % of TotalPayBenefits in 2011:
#  6.32%

# 8. Job Title in 2014 with lowest mean salary:
#  BdComm Mbr, Grp2,M=$25/Mtg → Avg Salary ≈ $345.42
