from werkzeug.security import generate_password_hash

password = 'ss123'  # Replace with the actual password
hashed_password = generate_password_hash(password)
print(hashed_password)
