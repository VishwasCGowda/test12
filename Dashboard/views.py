from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from pymongo import MongoClient
from datetime import datetime
from Dashboard.models import Appointment, Consultation
import json
from bson import ObjectId   
# MongoDB Configuration
client = MongoClient("mongodb+srv://Vishwas:Vishwasgowda@django.zyn54ai.mongodb.net/?retryWrites=true&w=majority")  # Replace with your MongoDB connection string
db = client["clinic"]
collection = db["bangalore_hospitals"]

# Get the list of all hospitals
@csrf_exempt
def get_hospital_list(request):
    if request.method == "GET":

        try:
            hospitals = collection.find({}, {"_id": 0, "Hospital_name": 1})  # Retrieve only hospital names
            hospital_list = [hospital["Hospital_name"] for hospital in hospitals]
            return JsonResponse({"hospitals": hospital_list}, safe=False, status=200)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

# Get details of a specific hospital by name
@csrf_exempt
def get_hospital_details(request):
    if request.method == "GET":
        hospital_name = request.GET.get("hospital_name")  # Use GET.get() to retrieve query parameters
        print
        if not hospital_name:
            return JsonResponse({"error": "hospital_name query parameter is required"}, status=400)

        try:
            hospital_detail = collection.find_one({"Hospital_name": hospital_name}, {"_id": 0,"Unnamed":0,"Highlighted_review":0,"Type":0,"No_of_people_rated":0, "Department":0 })  # Adjust field name
            if hospital_detail:
                return JsonResponse({"hospital": hospital_detail}, status=200)
            else:
                return JsonResponse({"error": "Hospital not found"}, status=404)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

@csrf_exempt
def get_hospital_department(request):
    if request.method == "GET":
        hospital_name = request.GET.get("hospital_name",None)  # Use GET.get() to retrieve query parameters
        print
        if not hospital_name:
            return JsonResponse({"error": "hospital name is required"}, status=400)

        try:
            hospital_department = collection.find_one({"Hospital_name": hospital_name}, {"_id": 0,"Unnamed":0,"Highlighted_review":0,"Type":0,"No_of_people_rated":0,"Hospital_name":0,"Rating":0,"Phone_number":0,"Address":0 })  # Adjust field name
            if hospital_department:
                print(hospital_department)
                return JsonResponse({"Department": list(hospital_department["Department"].keys()),"hospital": hospital_department}, status=200)
            else:
                return JsonResponse({"error": "Hospital not found"}, status=404)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

# Book an appointment
@csrf_exempt
def book_hospital_appointment(request):
    if request.method == "POST":
        # Booking appointment logic (as you already have)
        data = json.loads(request.body)
        email = data.get('email')
        hospital_name = data.get("hospital_name")
        department_name = data.get("department")
        doctor_name = data.get("doctor")
        consultation_day = data.get("consultation_day")

        if not all([hospital_name, department_name, doctor_name, consultation_day, email]):
            return JsonResponse({"error": "All fields are required (hospital_name, department, doctor, consultation_day, email)"}, status=400)

        try:
            hospital_department = collection.find_one({"Hospital_name": hospital_name}, {"Department": 1})
            if hospital_department:
                departments = hospital_department["Department"]
                if department_name in departments and doctor_name in departments[department_name]:
                    appointment = {
                        "email": email,
                        "hospital_name": hospital_name,
                        "department": department_name,
                        "doctor": doctor_name,
                        "consultation_day": consultation_day,
                        "appointment_date": datetime.now()
                    }
                    db['appointments'].insert_one(appointment)
                    return JsonResponse({"message": "Appointment booked successfully!"}, status=200)
                else:
                    return JsonResponse({"error": "Invalid department or doctor"}, status=400)
            else:
                return JsonResponse({"error": "Hospital not found"}, status=404)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    elif request.method == "GET":
        # Fetching appointment details
        try:
            # Extract query parameters from the request
            email = request.GET.get('email', None)  # Standard way for query parameters
            hospital_name = request.GET.get('hospital_name', None)
            doctor_name = request.GET.get('doctor_name', None)
            consultation_day = request.GET.get('consultation_day', None)

            # Building query filters based on the parameters provided
            query = {}
            if email:
                query["email"] = email
            if hospital_name:
                query["hospital_name"] = hospital_name
            if doctor_name:
                query["doctor"] = doctor_name
            if consultation_day:
                query["consultation_day"] = consultation_day

            # Fetch appointments from the database based on the filters
            appointments = list(db['appointments'].find(query, {"_id": 0}))

            if appointments:
                return JsonResponse({"appointments": appointments}, status=200)
            else:
                return JsonResponse({"message": "No appointments found for the given filters"}, status=404)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
        
@csrf_exempt
def doctor_view_appointments(request):
    if request.method == "GET":
        try:
            doctor_name = request.GET.get('doctor', None)
            if not doctor_name:
                return JsonResponse({"error": "Doctor name is required"}, status=400)

            # Query to find all appointments for the given doctor
            appointments = list(db['appointments'].find({"doctor": doctor_name}))

            if appointments:
                # Convert ObjectId to string to make it JSON serializable
                for appointment in appointments:
                    appointment["_id"] = str(appointment["_id"])

                return JsonResponse({"appointments": appointments}, status=200)
            else:
                return JsonResponse({"message": "No appointments found for the given doctor"}, status=404)

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
# Get consultation history for the user
@csrf_exempt
def get_user_consultations(request):
    if request.method == "GET":
        try:
            # Extract email from query parameters
            email = request.GET.get("email")
            if not email:
                return JsonResponse({"error": "Email is required as a query parameter"}, status=400)

            # Fetch consultations for the user
            consultations = db['consultations'].find({"email": email})
            consultations_list = []

            for consultation in consultations:
                consultations_list.append({
                    "hospital_name": consultation.get("hospital_name"),
                    "entries": consultation.get("entries", []),
                    "created_at": consultation.get("created_at"),
                    "last_updated": consultation.get("last_updated"),
                })

            if not consultations_list:
                return JsonResponse({"message": "No consultations found for the user"}, status=404)

            return JsonResponse({"email": email, "consultations": consultations_list}, status=200)

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    else:
        return JsonResponse({"message": "Method not allowed. Only GET requests are allowed."}, status=405)

# Post a consultation record by doctor
@csrf_exempt
def post_consultation(request):
    if request.method == "POST":
        try:
            # Parse the JSON data
            data = json.loads(request.body)

            # Extract required fields
            doctor_name = data.get('doctor_name')
            consultation_notes = data.get('consultation_notes')
            prescription_text = data.get('prescription_text')  # Stringified JSON
            appointment_id = data.get('appointment_id')
            print(data)
            # Check if all fields are present
            if not all([doctor_name, consultation_notes, prescription_text, appointment_id]):
                return JsonResponse({"error": "All fields (appointment_id, doctor_name, consultation_notes, prescription_text) are required"}, status=400)

            # Convert appointment_id to ObjectId and fetch the appointment
            appointment = db['appointments'].find_one({"_id": ObjectId(appointment_id)})
            if not appointment:
                return JsonResponse({"error": "Appointment not found"}, status=404)

            # Fetch user email and hospital name
            patient_email = appointment.get("email")
            hospital_name = appointment.get("hospital_name")

            if not all([patient_email, hospital_name]):
                return JsonResponse({"error": "Invalid appointment data"}, status=400)

            # Build the new consultation entry
            new_entry = {
                "doctor_name": doctor_name,
                "consultation_notes": consultation_notes,
                "prescription_text": json.loads(prescription_text),  # Convert back to JSON object
                "last_visit": datetime.now(),
                "created_at": datetime.now(),
                "last_updated": datetime.now()
            }

            # Check if a record already exists for this user and hospital
            existing_record = db['consultations'].find_one({
                "email": patient_email,
                "hospital_name": hospital_name
            })

            if existing_record:
                # Append the new entry to the existing document
                db['consultations'].update_one(
                    {"_id": existing_record["_id"]},
                    {"$push": {"entries": new_entry}, "$set": {"last_updated": datetime.now()}}
                )
                message = "New consultation entry added to existing record"
                consultation_id = str(existing_record["_id"])
            else:
                # Create a new document with the first entry in the "entries" array
                new_document = {
                    "email": patient_email,
                    "hospital_name": hospital_name,
                    "entries": [new_entry],  # Create an array with the new entry
                    "created_at": datetime.now(),
                    "last_updated": datetime.now()
                }
                result = db['consultations'].insert_one(new_document)
                message = "New consultation document created"
                consultation_id = str(result.inserted_id)

            # Add the consultation ID to the appointment document
            db['appointments'].update_one(
                {"_id": ObjectId(appointment_id)},
                {"$set": {"consultation_id": consultation_id}}
            )

            return JsonResponse({
                "message": message,
                "consultation_id": consultation_id
            }, status=200)

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    else:
        return JsonResponse({"message": "Method not allowed. Only POST requests are allowed."}, status=405)


@csrf_exempt
def get_doctor_consultations(request):
    if request.method == "GET":
        try:
            # Extract doctor_name and optional email from query parameters
            doctor_name = request.GET.get("doctor_name")
            user_email = request.GET.get("email")  # Optional parameter to filter by user

            if not doctor_name:
                return JsonResponse({"error": "Doctor name is required as a query parameter"}, status=400)

            # Query based on the filters
            query = {"entries.doctor_name": doctor_name}
            if user_email:
                query["email"] = user_email

            # Fetch consultations
            consultations = db['consultations'].find(query)
            consultations_list = []

            for consultation in consultations:
                filtered_entries = [
                    entry for entry in consultation.get("entries", [])
                    if entry.get("doctor_name") == doctor_name
                ]

                consultations_list.append({
                    "email": consultation.get("email"),
                    "hospital_name": consultation.get("hospital_name"),
                    "entries": filtered_entries,
                    "created_at": consultation.get("created_at"),
                    "last_updated": consultation.get("last_updated"),
                })

            if not consultations_list:
                return JsonResponse({"message": "No consultations found"}, status=404)

            return JsonResponse({"doctor_name": doctor_name, "consultations": consultations_list}, status=200)

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    else:
        return JsonResponse({"message": "Method not allowed. Only GET requests are allowed."}, status=405)
    
@csrf_exempt
def get_user_consultations_by_doctor(request):
    if request.method == "GET":
        try:
            # Extract doctor_name and email from query parameters
            doctor_name = request.GET.get("doctor_name")
            user_email = request.GET.get("email")  # Required parameter to filter consultations by user

            if not doctor_name:
                return JsonResponse({"error": "Doctor name is required as a query parameter"}, status=400)
            
            if not user_email:
                return JsonResponse({"error": "Email is required as a query parameter"}, status=400)

            # Query based on doctor and email to filter consultations for a particular user
            query = {"email": user_email, "entries.doctor_name": doctor_name}

            # Fetch consultations for the specific user and doctor
            consultations = db['consultations'].find(query)
            consultations_list = []

            for consultation in consultations:
                filtered_entries = [
                    entry for entry in consultation.get("entries", [])
                    if entry.get("doctor_name") == doctor_name
                ]
                consultations_list.append({
                    "hospital_name": consultation.get("hospital_name"),
                    "entries": filtered_entries,
                    "created_at": consultation.get("created_at"),
                    "last_updated": consultation.get("last_updated"),
                })

            if not consultations_list:
                return JsonResponse({"message": "No consultations found for this user with the specified doctor."}, status=404)

            return JsonResponse({"doctor_name": doctor_name, "user_email": user_email, "consultations": consultations_list}, status=200)

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    else:
        return JsonResponse({"message": "Method not allowed. Only GET requests are allowed."}, status=405)