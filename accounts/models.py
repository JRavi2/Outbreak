from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.urls import reverse
from multiselectfield import MultiSelectField

userTypes = [('P', 'Patient'), ('H', 'Hospital')]

class UserManager(BaseUserManager):
	def create_user(self, user_id, user_type, password=None):
		if not user_id:
			return ValueError("Please Enter a user_id")
		if not password:
			return ValueError("Please Enter a password")
		
		user = self.model(
			user_id = user_id,
			user_type = user_type
		)
		user.set_password(password)

		user.save(using=self._db)
		return user
	
	def create_superuser(self, user_id, user_type, password=None):
		user = self.create_user(
			user_id = user_id,
			password = password,
			user_type = user_type
		)

		user.is_admin = True
		user.is_superuser = True
		user.is_staff = True

		user.save(using=self._db)
		return user

class User(AbstractBaseUser):
	user_id = 			models.CharField(max_length=100, blank=False, unique=True)
	user_type = 		models.CharField(max_length=2, choices=userTypes, default='Patient')

	# Necessary Fields for Django User Model
	date_joined = 		models.DateTimeField(verbose_name="date-joined", auto_now_add=True)
	last_login = 		models.DateTimeField(verbose_name="last-login", auto_now=True)
	is_admin = 			models.BooleanField(default=False)
	is_active =			models.BooleanField(default=True)
	is_staff = 			models.BooleanField(default=False)
	is_superuser = 		models.BooleanField(default=False)

	USERNAME_FIELD = 'user_id'
	REQUIRED_FIELDS = ['user_type']
	
	objects = UserManager()

	def __str__(self):
		return self.user_id
	
	def has_perm(self, perm, obj=None):
		return self.is_admin

	def has_module_perms(self, app_label):
		return True


class Patient(models.Model):
	user = 				models.OneToOneField(User, on_delete = models.CASCADE)
	name =	 			models.CharField(max_length=250)
	age = 				models.IntegerField(default=None)
	Gender = 			[('Male','M'), ('Female','F'), ('Others','O'),]	#selection of gender
	gender = 			models.CharField(max_length=6, choices=Gender, default='Male')
	contact_no = 		models.IntegerField(unique=True, blank=False)
	Social_Status = 	[('SC','SC'), ('General','Gen'), ('ST','ST'), ('OBC','OBC'),]
	social_status = 	models.CharField(max_length=8, choices=Social_Status, default='Gen')
	prefd_hospital = 	models.CharField(max_length=100)
	tokenNo = 			models.IntegerField(blank=True, null=True)

	def __str__(self):
		return self.name



class Hospital(models.Model):
	user = 					models.OneToOneField(User, on_delete = models.CASCADE)
	name = 					models.CharField(max_length=250)
	address = 				models.CharField(max_length=250)
	latitude = 				models.FloatField()
	longitude = 			models.FloatField()
	bed_capacity = 			models.CharField(max_length=250)
	currently_free = 		models.CharField(max_length=250)
	hasTokenSystem = 		models.BooleanField(default=False)
	linkToTokenWebsite = 	models.URLField(blank=True, null=True)
	department_options =	(("Allergy & Clinical Immunology", "Allergy & Clinical Immunology"), ("Anaesthesia", "Anaesthesia"),("Bariatric & Metabolic Surgery","Bariatric & Metabolic Surgery"),
	 ('Blood Disorders','Blood Disorders'),("Breast Surgery", "Breast Surgery"), ("Cardiac Anaesthesia", "Cardiac Anaesthesia"),("Cardiac Surgery", "Cardiac Surgery"),
	 ("Cardiology","Cardiology"), ("Cardiology - Interventional","Cardiology - Interventional"),("Dental Sciences","Dental Sciences"), ("Dermatology","Dermatology"),
	 ("Diabetes And Endocrinology","Diabetes And Endocrinology"),("Dietetics & Clinical Nutrition","Dietetics & Clinical Nutrition"),("ENT","ENT"),("Geriatric Medicine","Geriatric Medicine"),
	 ("Ophthalmology","Ophthalmology"),("Foetal Medicine","Foetal Medicine"),("Gastroenterology","Gastroenterology"),("General Surgery","General Surgery"),("General and Laparoscopic Surgery","General and Laparoscopic Surgery"),("Gynaecology Oncology","Gynaecology Oncology"),
	 ("Infectious Diseases","Infectious Diseases"),("Infertility Medicine","Infertility Medicine"),("Intensive Care","Intensive Care"),("Internal Medicine","Internal Medicine"),
	 ("Interventional Radiology", "Interventional Radiology"), ("Laparoscopic, Gastro Intestinal, Bariatric & Metabolic Surgery","Laparoscopic, Gastro Intestinal, Bariatric & Metabolic Surgery"),("Liver Transplant / Hepatobiliary Surgery","Liver Transplant / Hepatobiliary Surgery"),
	 ("Medical Oncology","Medical Oncology"),("Medical Oncology, Hematology And BMT","Medical Oncology, Hematology And BMT"),("Mental Health and Behavioural Sciences","Mental Health and Behavioural Sciences"),("Neonatology","Neonatology"),
	 ("Nephrology","Nephrology"),("Neuro & Spine Surgery","Neuro & Spine Surgery"),("Neuro Radiology","Neuro Radiology"),("Neurology","Neurology"),("Non Invasive Cardiology","Non Invasive Cardiology"),("Obstetrics and Gynaecology","Obstetrics and Gynaecology"),
	 ("Onco Sciences","Onco Sciences"),("Oral / Maxillofacial Surgery","Oral / Maxillofacial Surgery"),("Orthopaedics & Spine Surgery","Orthopaedics & Spine Surgery"),("Orthopaedics  Bone & Joint Surgery","Orthopaedics  Bone & Joint Surgery"),("Orthopaedics  Hand & Upper Limb Surgery","Orthopaedics  Hand & Upper Limb Surgery"),
	 ("Paediatric Cardiology","Paediatric Cardiology"), ("Paediatric Endocrinology","Paediatric Endocrinology"),("Paediatric Nephrology","Paediatric Nephrology"),("Paediatric Neurology","Paediatric Neurology"),
	 ("Paediatric Oncology","Paediatric Oncology"),("Paediatric Orthopaedics","Paediatric Orthopaedics"),("Paediatric Pulmonology","Paediatric Pulmonology"),("Paediatric Surgery","Paediatric Surgery"),
	 ("Paediatrics","Paediatrics"),("Pain management","Pain management"),("Physiotherapy and Rehabilitation","Physiotherapy and Rehabilitation"),("Plastic, Cosmetic & Reconstructive Surgery","Plastic, Cosmetic & Reconstructive Surgery"), ("DiabeticFoot Care","Diabetic Foot Care"), ("Pulmonology", "Pulmonology"), ("Radiation Oncology","Radiation Oncology"), ("Radiology","Radiology"), ("Rheumatology","Rheumatology"), ("Arthroscopic Surgery","Arthroscopic Surgery"),
	 ("Surgical Oncology","Surgical Oncology"),("Trauma & Emergency Medicine","Trauma & Emergency Medicine"),("Urology & Andrology","Urology & Andrology"),("Urology, Andrology & Transplant Surgery","Urology, Andrology & Transplant Surgery"),
	 ("Vascular Surgery", "Vascular Surgery"),)
	specialities =			MultiSelectField(choices=department_options, default=None)


	def __str__(self):
		return self.name

class Token(models.Model):
	user = 				models.ForeignKey(User, on_delete = models.CASCADE)
	department = 		models.CharField(max_length=3)
	count = 			models.IntegerField(default=0)