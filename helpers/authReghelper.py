import re
import hashlib

class AuthRegHelper:

    @staticmethod
    def validate_user_details(userDetails):
        """
        Validates user details.
        Returns a dictionary with success status and error messages if validation fails.
        """
        errors = []

        # Check if all required fields are present
        requiredFields = ['email', 'firstName', 'lastName', 'confirmPassword', 'password', 'phoneNumber', 'role']
        missingFields = [field for field in requiredFields if not userDetails.get(field)]
        available_role = ("User","Doctor","Admin")
        if missingFields:
            errors.append(f"Missing fields: {', '.join(missingFields)}")

        # Validate email
        email = userDetails.get('email')
        if email and not re.match(r'^[\w\.-]+@[\w\.-]+\.\w{2,4}$', email):
            errors.append("Invalid email format")

        # Validate phone number
        phoneNumber = userDetails.get('phoneNumber')
        if phoneNumber and len(phoneNumber) != 10:
            errors.append("Phone number must be 10 digits long")

        # Validate password
        if userDetails.get('password') != userDetails.get('confirmPassword'):
            errors.append("Passwords do not match")

        if userDetails.get('role') not in available_role:
            errors.append("Role not specified.")
        return {'success': len(errors) == 0, 'errors': errors}

    @staticmethod
    def encrypt_password(password):
        """
        Encrypts the password using SHA256.
        """
        return hashlib.sha256(password.encode()).hexdigest()

    @staticmethod
    def check_password(plain_password, hashed_password):
        """
        Compares the plain password with the hashed password.
        Returns True if the passwords match, otherwise False.
        """
        return AuthRegHelper.encrypt_password(plain_password) == hashed_password
