from django.urls import path
from . import views

urlpatterns = [
    path('hospitals/', views.get_hospital_list, name='get_hospital_list'),  # List all hospitals
    path('hospital/', views.get_hospital_details, name='get_hospital_details'),  # API for hospital details
    path('department/', views.get_hospital_department, name='get_hospital_department'),  # API for hospital details
    path('booking/', views.book_hospital_appointment, name='book_appointment'),  # Book appointment
    path('doctor_view_appointments/',views.doctor_view_appointments,name="doctor_view_appointments"),
    path('doctor/post_consultation/', views.post_consultation, name='post_consultation'),  # Post consultation notes
    path('user/consultations/', views.get_user_consultations, name='get_patient_consultation_history'),  # Get consultation history for user
    path('doctor/consultations/', views.get_doctor_consultations, name='get_doctor_consultations'),  # Get consultation history for user
    path('doctor/user-consultations', views.get_user_consultations_by_doctor, name='get_user_consultations_by_doctor'),  # Get consultation history for user
]