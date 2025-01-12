# import pandas as pd
# from pymongo import MongoClient
# import requests
# import io

# # Step 1: Download the CSV from the URL
# url = "https://storage.googleapis.com/kagglesdsdata/datasets/5030014/8442627/hospital_data_bangalore.csv?X-Goog-Algorithm=GOOG4-RSA-SHA256&X-Goog-Credential=gcp-kaggle-com%40kaggle-161607.iam.gserviceaccount.com%2F20250111%2Fauto%2Fstorage%2Fgoog4_request&X-Goog-Date=20250111T072430Z&X-Goog-Expires=259200&X-Goog-SignedHeaders=host&X-Goog-Signature=3c4b001e4f32d6c5e1c45c59d5b791e4d964114e4f6f9f80e33c0dc106fb88b5490c894414940907334f2e5fffa0532b975f2668a10a019bf20a48bfd9f941bb29704d44f15ee112d4788e3bfc0de6d0d71d2894555508a5fe266c48d0b75ddde17087b7b57e6a82a7cdc8e32a333a90da5dd1387f9ca1337dbe388a66e44fb8e721fca7a9c21359e8eeba7db95711b3536c58abe38beea698bcda525d2098b90bb25b5719ad9b55cd5e0b4281cf22da61dfff5085090d35eb31c586d90eb2e9a6a2bb67613545f3e0a011275b24e68bf1b22dcab92de5a87507e774fbca8622a8ebf08d405081e20d20ae0ddac0387c71a43977cfecf6ece67a228f3fe64f54"

# response = requests.get(url)
# response.raise_for_status()  # Raise an error if the request fails

# # Step 2: Read the CSV into a Pandas DataFrame
# data = pd.read_csv(io.StringIO(response.text))

# # Step 3: Convert DataFrame to JSON
# data_json = data.to_dict(orient="records")

# # Step 4: Insert JSON data into MongoDB
# client = MongoClient("mongodb+srv://Vishwas:Vishwasgowda@django.zyn54ai.mongodb.net/?retryWrites=true&w=majority")  # Replace with your MongoDB connection string
# db = client["clinic"]  # Database name
# collection = db["bangalore_hospitals"]  # Collection name

# # Insert data
# collection.insert_many(data_json)

# print("Data inserted successfully!")

import pandas as pd
import random
from pymongo import MongoClient
from collections import defaultdict

# MongoDB connection
client = MongoClient("mongodb+srv://Vishwas:Vishwasgowda@django.zyn54ai.mongodb.net/?retryWrites=true&w=majority")
db = client['clinic']
collection = db['bangalore_hospitals']

# Departments and their doctors
departments = {
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

# Tracking the count of doctors assigned to hospitals to ensure no doctor appears in more than 2 hospitals
doctor_assignment_count = defaultdict(int)

# Function to add department and doctors to each hospital
def add_department_and_doctor(data):
    department_doctors = {}

    # Get 5 random departments for the hospital
    selected_departments = random.sample(list(departments.keys()), 5)

    for department in selected_departments:
        # Get available doctors from the department that are not assigned to more than 2 hospitals
        available_doctors = [doctor for doctor in departments[department] if doctor_assignment_count[doctor] < 2]

        # If not enough doctors are available, skip this department
        if len(available_doctors) < 2:
            continue

        # If there are fewer than 4 available doctors, take all available doctors (max available)
        num_doctors_to_select = min(4, len(available_doctors))

        # Select the doctors
        selected_doctors = random.sample(available_doctors, num_doctors_to_select)

        # Assign the selected doctors to the department
        department_doctors[department] = selected_doctors
        
        # Update the doctor assignment count for each selected doctor
        for doctor in selected_doctors:
            doctor_assignment_count[doctor] += 1

    # If no doctors were assigned to any department, ensure there is at least one doctor
    for department, doctors in department_doctors.items():
        if not doctors:  # If the department has no doctors, add at least one doctor
            available_doctors = [doctor for doctor in departments[department] if doctor_assignment_count[doctor] < 2]
            selected_doctor = random.choice(available_doctors)
            department_doctors[department] = [selected_doctor]
            doctor_assignment_count[selected_doctor] += 1

    # Add the department and doctor information to the data
    data["Department"] = department_doctors
    return data


# Read the dataset from the URL
url = "https://storage.googleapis.com/kagglesdsdata/datasets/5030014/8442627/hospital_data_bangalore.csv?X-Goog-Algorithm=GOOG4-RSA-SHA256&X-Goog-Credential=gcp-kaggle-com%40kaggle-161607.iam.gserviceaccount.com%2F20250111%2Fauto%2Fstorage%2Fgoog4_request&X-Goog-Date=20250111T072430Z&X-Goog-Expires=259200&X-Goog-SignedHeaders=host&X-Goog-Signature=3c4b001e4f32d6c5e1c45c59d5b791e4d964114e4f6f9f80e33c0dc106fb88b5490c894414940907334f2e5fffa0532b975f2668a10a019bf20a48bfd9f941bb29704d44f15ee112d4788e3bfc0de6d0d71d2894555508a5fe266c48d0b75ddde17087b7b57e6a82a7cdc8e32a333a90da5dd1387f9ca1337dbe388a66e44fb8e721fca7a9c21359e8eeba7db95711b3536c58abe38beea698bcda525d2098b90bb25b5719ad9b55cd5e0b4281cf22da61dfff5085090d35eb31c586d90eb2e9a6a2bb67613545f3e0a011275b24e68bf1b22dcab92de5a87507e774fbca8622a8ebf08d405081e20d20ae0ddac0387c71a43977cfecf6ece67a228f3fe64f54"
df = pd.read_csv(url)

# Iterate over each row in the dataset
for index, row in df.iterrows():
    # Prepare the data in the required format
    hospital_data = row.to_dict()
    hospital_data.pop('Unnamed', None)
    hospital_data.pop('Highlighted_review', None)
    hospital_data.pop('Type', None)
    hospital_data.pop('No_of_people_rated', None)
    
    # Add department and doctor details
    prepared_data = add_department_and_doctor(hospital_data)

    # Insert the data into MongoDB
    collection.insert_one(prepared_data)

print("Data insertion complete.")

