from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from pymongo import MongoClient
from collections import defaultdict
from helpers.authReghelper import AuthRegHelper
from .models import Register
from django.core.exceptions import ObjectDoesNotExist

client = MongoClient("mongodb+srv://Vishwas:Vishwasgowda@django.zyn54ai.mongodb.net/?retryWrites=true&w=majority")  # Replace with your MongoDB URI
db = client["clinic"]  # Replace with your database name
@csrf_exempt
def register(request):
    if request.method == 'POST':
        try:
            userDetails = json.loads(request.body)
            
            existing_user = Register.objects.filter(email=userDetails.get("email")
            ).first() or Register.objects.filter(
                phoneNumber=userDetails.get("phoneNumber")
            ).first()

            if existing_user:
                # Checking if both email and phone number match
                if existing_user.email == userDetails.get("email") and existing_user.phoneNumber == userDetails.get("phoneNumber"):
                    return JsonResponse({"message": "User with both email and phone number is already registered."})
                # Checking if only email matches
                elif existing_user.email == userDetails.get("email"):
                    return JsonResponse({"message": "User with this email is already registered."})
                # Checking if only phone number matches
                elif existing_user.phoneNumber == userDetails.get("phoneNumber"):
                    return JsonResponse({"message": "User with this phone number is already registered."})
                    
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON format"}, status=400)

        # Validate user details
        validationResult = AuthRegHelper.validate_user_details(userDetails)
        if not validationResult['success']:
            return JsonResponse({"errors": validationResult['errors']}, status=400)

        # Encrypt password
        encryptedPassword = AuthRegHelper.encrypt_password(userDetails['password'])

        # Save the new user to MongoDB
        try:
            Register.objects.create(
                email=userDetails['email'],
                firstName=userDetails['firstName'],
                lastName=userDetails['lastName'],
                phoneNumber=userDetails['phoneNumber'],
                role=userDetails['role'],
                password=encryptedPassword,
            )
        except Exception as e:
            print(str(e))
            return JsonResponse({"error": f"Failed to register user: {str(e)}"}, status=500)
        print("hi")
        return JsonResponse({"message": "User registered successfully"}, status=200)

    elif request.method == 'PATCH':
        # Handle User Details Update
        try:
            userDetails = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON format"}, status=400)

        # Validate user details
        validationResult = AuthRegHelper.validate_user_details(userDetails)
        if not validationResult['success']:
            return JsonResponse({"errors": validationResult['errors']}, status=400)

        # Encrypt password
        encryptedPassword = AuthRegHelper.encrypt_password(userDetails['password'])

        # Update user details in MongoDB
        try:
            user = Register.objects.get(email=userDetails['email'])
            user.firstName = userDetails.get('firstName', user.firstName)
            user.lastName = userDetails.get('lastName', user.lastName)
            user.phoneNumber = userDetails.get('phoneNumber', user.phoneNumber)
            user.role = userDetails.get('role', user.role)
            if encryptedPassword:
                user.password = encryptedPassword
            user.save()
        except ObjectDoesNotExist:
            return JsonResponse({"error": "User not found"}, status=404)

        return JsonResponse({"message": "User details updated successfully"}, status=200)

    elif request.method == 'DELETE':
        # Handle User Deletion
        try:
            userDetails = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON format"}, status=400)

        # Ensure email is provided for deletion
        email = userDetails.get('email')
        if not email:
            return JsonResponse({"error": "Email is required for deletion"}, status=400)

        try:
            user = Register.objects.get(email=email)
            user.delete()
            return JsonResponse({"message": "User deleted successfully"}, status=200)
        except ObjectDoesNotExist:
            return JsonResponse({"error": "User not found"}, status=404)

    return JsonResponse({"error": "Method not allowed"}, status=405)


@csrf_exempt
def login(request):
    if request.method == 'POST':
        # Handle User Login
        try:
            loginDetails = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON format"}, status=400)

        email = loginDetails.get('email')
        password = loginDetails.get('password')

        if not email or not password:
            return JsonResponse({"error": "Email and password are required"}, status=400)

        # Authenticate user
        user = db['Auth_register'].find_one({"email":email},{"_id": 0})
        print(type(user))
        if user and AuthRegHelper.check_password(password, user.get("password")):
            # Here you can generate a token or session for user login if required
            if user.get("role") == "User":
                return JsonResponse({"message": "Login successful", "data": {'name': f'{user.get("firstName")} {user.get("lastName")}', 'email': f'{user.get("email")}', 'role': f'{user.get("role")}'}}, status=200)
            elif user.get("role") == "Admin":
                pass
            elif user.get("role") == "Doctor":
                return JsonResponse({"message": "Login successful", "data": {'name': f'{user.get("firstName")} {user.get("lastName")}', 'email': f'{user.get("email")}', 'role': f'{user.get("role")}',"specialty":user.get("specialty"),"hospitals":f'{user.get("hospital")}'}}, status=200)
        else:
            return JsonResponse({"error": "Invalid credentials"}, status=401)

    return JsonResponse({"error": "Method not allowed"}, status=405)


@csrf_exempt
def user_details(request):
    if request.method == 'GET':
        # Get user details
        email = request.GET.get('email')
        if not email:
            return JsonResponse({"error": "Email is required"}, status=400)

        try:
            user = Register.objects.get(email=email)
            user_data = {
                "email": user.email,
                "firstName": user.firstName,
                "lastName": user.lastName,
                "phoneNumber": user.phoneNumber,
                "role": user.role,
            }
            return JsonResponse({"user": user_data}, status=200)
        except ObjectDoesNotExist:
            return JsonResponse({"error": "User not found"}, status=404)

    return JsonResponse({"error": "Method not allowed"}, status=405)
