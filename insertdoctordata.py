# 3

import csv
from datetime import datetime, timezone
import hashlib

# Load the hospital-doctor mapping from the CSV file
hospital_to_doctor_map = {}

with open("hospital_doctors_list.csv", mode="r") as file:
    reader = csv.DictReader(file)
    for row in reader:
        hospital_name = row["Hospital Name"]
        doctor_names = row["Doctors"].split(", ")
        for doctor in doctor_names:
            # Append hospital names to the doctor
            hospital_to_doctor_map.setdefault(doctor, []).append(hospital_name)

# Define doctor specialties
specialties ={
    "Cardiology": [
        "Dr. Aaradhya Sharma",
        "Dr. Adah Desai",
        "Dr. Adhira Patel",
        "Dr. Amoli Jain",
        "Dr. Anaisha Singh",
        "Dr. Ananya Khanna",
        "Dr. Asmee Gupta",
        "Dr. Avni Roy",
        "Dr. Drishti Menon",
        "Dr. Ela Iyer",
        "Dr. Eshika Joshi",
        "Dr. Geetika Singh",
        "Dr. Gulika Shah",
        "Dr. Hiya Agarwal",
        "Dr. Hiral Kumar",
        "Dr. Ira Nair",
        "Dr. Ishita Rao",
        "Dr. Jeevika Sharma",
        "Dr. Kaia Patel",
        "Dr. Kashvi Singh" 
    ],
    "Neurology": [
        "Dr. Keya Khanna",
        "Dr. Kimaya Gupta",
        "Dr. Krisha Roy",
        "Dr. Larisa Menon",
        "Dr. Laasya Iyer",
        "Dr. Mahika Joshi",
        "Dr. Mayra Singh",
        "Dr. Mehar Shah",
        "Dr. Mirai Agarwal",
        "Dr. Mishka Kumar",
        "Dr. Naitee Nair",
        "Dr. Navya Rao",
        "Dr. Nyra Sharma",
        "Dr. Nehrika Patel",
        "Dr. Neysa Singh",
        "Dr. Pavati Khanna",
        "Dr. Prisha Gupta",
        "Dr. Ryka Roy",
        "Dr. Rebecca Menon",
        "Dr. Saanvi Iyer" 
    ],
    "Orthopedics": [
        "Dr. Sahana Joshi",
        "Dr. Sai Singh",
        "Dr. Saisha Shah",
        "Dr. Saira Agarwal",
        "Dr. Saloni Kumar",
        "Dr. Shanaya Nair",
        "Dr. Shrishti Rao",
        "Dr. Sneha Sharma",
        "Dr. Turvi Patel",
        "Dr. Taahira Singh",
        "Dr. Taara Khanna",
        "Dr. Tanvi Gupta",
        "Dr. Viti Roy",
        "Dr. Zara Menon",
        "Dr. Aagya Iyer",
        "Dr. Aaina Joshi",
        "Dr. Aas Singh",
        "Dr. Akaljeet Shah",
        "Dr. Amanroop Agarwal",
        "Dr. Anika Kumar" 
    ],
    "Gynaecology": [
        "Dr. Birva Nair",
        "Dr. Bisanpreet Rao",
        "Dr. Charanpreet Sharma",
        "Dr. Dilreet Patel",
        "Dr. Ekkam Singh",
        "Dr. Faal Khanna",
        "Dr. Gurleen Gupta",
        "Dr. Gurmeet Roy",
        "Dr. Heer Menon",
        "Dr. Harleen Iyer",
        "Dr. Harveen Joshi",
        "Dr. Ikamroop Singh",
        "Dr. Isha Shah",
        "Dr. Ishmeet Agarwal",
        "Dr. Katiya Kumar",
        "Dr. Mehr Nair",
        "Dr. Nihaara Rao",
        "Dr. Paakhi Sharma",
        "Dr. Parminder Patel",
        "Dr. Simrat Singh" 
    ],
    "Dermatology": [
        "Dr. Sukhdeep Khanna",
        "Dr. Sukhleen Gupta",
        "Dr. Shirina Roy",
        "Dr. Tavleen Menon",
        "Dr. Ami Iyer",
        "Dr. Askini Joshi",
        "Dr. Anvi Singh",
        "Dr. Bandhini Shah",
        "Dr. Bansari Agarwal",
        "Dr. Charmi Kumar",
        "Dr. Chavi Nair",
        "Dr. Charul Rao",
        "Dr. Drisna Sharma",
        "Dr. Dhara Patel",
        "Dr. Dhruvi Singh",
        "Dr. Jaisnavi Khanna",
        "Dr. Inika Gupta",
        "Dr. Vaidarbhi Roy",
        "Dr. Ujas Menon",
        "Dr. Urvashi Iyer" 
    ],
    "Pediatrics": [
        "Dr. Unnati Joshi",
        "Dr. Tejshri Singh",
        "Dr. Tapti Shah",
        "Dr. Smita Agarwal",
        "Dr. Shriha Kumar",
        "Dr. Shivanya Nair",
        "Dr. Shivali Rao",
        "Dr. Sharayu Sharma",
        "Dr. Saundarya Patel",
        "Dr. Riya Singh",
        "Dr. Riva Khanna",
        "Dr. Rimjhim Gupta",
        "Dr. Ridhi Roy",
        "Dr. Prachi Menon",
        "Dr. Parina Iyer",
        "Dr. Pallavi Joshi",
        "Dr. Niyati Singh",
        "Dr. Nisha Shah",
        "Dr. Nirali Agarwal",
        "Dr. Navika Kumar" 
    ],
    "ENT": [
        "Dr. Neela Nair",
        "Dr. Mayuri Rao",
        "Dr. Manya Sharma",
        "Dr. Manavi Patel",
        "Dr. Apsara Singh",
        "Dr. Anuja Khanna",
        "Dr. Arohi Gupta",
        "Dr. Bhakti Roy",
        "Dr. Bharati Menon",
        "Dr. Charulata Iyer",
        "Dr. Darshini Joshi",
        "Dr. Dnyanada Singh",
        "Dr. Durga Shah",
        "Dr. Ekata Agarwal",
        "Dr. Falguni Kumar",
        "Dr. Gargi Nair",
        "Dr. Gauri Rao",
        "Dr. Gayatri Sharma",
        "Dr. Grishma Patel",
        "Dr. Harini Singh" 
    ],
    "Psychiatry": [
        "Dr. Ishani Khanna",
        "Dr. Jui Gupta",
        "Dr. Jyotsna Roy",
        "Dr. Kalpana Menon",
        "Dr. Kalyani Iyer",
        "Dr. Kamakshi Joshi",
        "Dr. Kashi Singh",
        "Dr. Kumudini Shah",
        "Dr. Lavanya Agarwal",
        "Dr. Leela Kumar",
        "Dr. Madhavi Nair",
        "Dr. Malini Rao",
        "Dr. Meera Sharma",
        "Dr. Nandini Patel",
        "Dr. Navita Singh",
        "Dr. Nayana Khanna",
        "Dr. Neeta Gupta",
        "Dr. Nirmala Roy",
        "Dr. Oviya Menon",
        "Dr. Padma Iyer" 
    ],
    "General Surgery": [
        "Dr. Pallavi Joshi",
        "Dr. Pratibha Singh",
        "Dr. Prerna Shah",
        "Dr. Purva Agarwal",
        "Dr. Aaliyah Kumar",
        "Dr. Aisha Nair",
        "Dr. Amara Rao",
        "Dr. Farida Sharma",
        "Dr. Fawziya Patel",
        "Dr. Hana Singh",
        "Dr. Inaya Khanna",
        "Dr. Iqra Gupta",
        "Dr. Jasmine Roy",
        "Dr. Laila Menon",
        "Dr. Lina Iyer",
        "Dr. Madiha Joshi",
        "Dr. Maryam Singh",
        "Dr. Nadia Shah",
        "Dr. Naima Agarwal",
        "Dr. Nyla Kumar" 
    ],
    "Urology": [
        "Dr. Rabia Nair",
        "Dr. Rukhsar Rao",
        "Dr. Sahar Sharma",
        "Dr. Saida Patel",
        "Dr. Sana Singh",
        "Dr. Shireen Khanna",
        "Dr. Sofia Gupta",
        "Dr. Tahira Roy",
        "Dr. Yasmin Menon",
        "Dr. Zahira Iyer",
        "Dr. Zainab Joshi",
        "Dr. Zara Singh",
        "Dr. Zoya Shah",
        "Dr. Sumaya Agarwal",
        "Dr. Aaradhya Kumar",
        "Dr. Adah Nair",
        "Dr. Adhira Rao",
        "Dr. Amoli Sharma",
        "Dr. Anaisha Patel",
        "Dr. Ananya Singh" 
    ]
}

# Hashing function for password
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# Create doctor list
doctors = []
for specialty, names in specialties.items():
    for name in names:
        first_name, last_name = name.split(" ", 1)
        doctors.append({
            "firstName": first_name,
            "lastName": last_name,
            "email": str(f"{first_name.lower()}.{last_name.lower()}@hospital.com"),
            "phoneNumber": str(f"9{''.join(['{}'.format(i % 10) for i in range(9)])}"),
            "password": hash_password("password123"),
            "specialty": specialty,
            "role": "Doctor",
            "hospital": hospital_to_doctor_map.get(name, []),
            "createdAt": datetime.now(timezone.utc).isoformat(),
            "updatedAt": datetime.now(timezone.utc).isoformat()
        })

# Save to CSV
csv_file = "doctors_with_hospitals.csv"
with open(csv_file, mode="w", newline="") as file:
    writer = csv.DictWriter(file, fieldnames=doctors[0].keys())
    writer.writeheader()
    writer.writerows(doctors)

print(f"CSV file '{csv_file}' has been created with doctor and hospital details.")











#1

# from pymongo import MongoClient

# # Replace with your MongoDB connection string
# client = MongoClient("mongodb+srv://Vishwas:Vishwasgowda@django.zyn54ai.mongodb.net/?retryWrites=true&w=majority")  # Replace with your MongoDB URI
# db = client["clinic"]  # Replace with your database name
# collection = db["bangalore_hospitals"]  # Replace with your collection name

# # Delete documents where "Department" is an empty object (effectively null)
# result = collection.delete_many({"Department": {}})

# # Print the number of deleted documents
# print(f"Deleted {result.deleted_count} documents.")
















# 2

# import csv
# from pymongo import MongoClient

# # Connect to MongoDB
# client = MongoClient("mongodb+srv://Vishwas:Vishwasgowda@django.zyn54ai.mongodb.net/?retryWrites=true&w=majority")  # Replace with your MongoDB URI
# db = client["clinic"]  # Replace with your database name
# collection = db["bangalore_hospitals"]  # Replace with your collection name

# # Query the database
# hospitals = collection.find()

# # Prepare data for CSV
# csv_data = [["Hospital Name", "Doctors"]]  # CSV header

# # Extract hospital names and doctors (irrespective of department)
# for hospital in hospitals:
#     hospital_name = hospital.get("Hospital_name", "Unknown Hospital")
#     department_data = hospital.get("Department", {})
    
#     # Combine all doctors into a single list
#     all_doctors = []
#     for doctors in department_data.values():
#         all_doctors.extend(doctors)
    
#     # Add data to CSV (aggregate doctors for each hospital)
#     csv_data.append([hospital_name, ", ".join(set(all_doctors))])  # Remove duplicates with `set`

# # Write data to CSV
# csv_filename = "hospital_doctors_list.csv"
# with open(csv_filename, mode="w", newline="", encoding="utf-8") as file:
#     writer = csv.writer(file)
#     writer.writerows(csv_data)

# print(f"Data has been successfully written to {csv_filename}")
