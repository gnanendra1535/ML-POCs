from cryptography.fernet import Fernet
import re

# Generate a key 
key = Fernet.generate_key()
cipher = Fernet(key)

# Read input from user
reference_id = input("Enter your Reference ID (12 characters - letters/numbers allowed): ")

# Validate Reference ID
if not re.fullmatch(r"[A-Za-z0-9]{12}", reference_id):
    print("Invalid Reference ID! It must be exactly 12 letters/numbers.")
    exit()

#Encrypt the Reference ID
encrypted_id = cipher.encrypt(reference_id.encode())

print("\n Reference ID encrypted successfully!")
print("Encrypted ID:", encrypted_id.decode())

#Optional Decryption
choice = input("\nDo you want to decrypt the Reference ID? (yes/no): ").strip().lower()
if choice == "yes":
    decrypted_id = cipher.decrypt(encrypted_id).decode()
    print("Decrypted Reference ID:", decrypted_id)

# Show the secret key
print("\n[DEBUG] Secret Key (keep it safe!):", key.decode())

# output example
# Enter your Reference ID (12 characters - letters/numbers allowed): ABC123XYZ789

# Reference ID encrypted successfully!
# Encrypted ID: gAAAAABn...

# Do you want to decrypt the Reference ID? (yes/no): yes
# Decrypted Reference ID: ABC123XYZ789

