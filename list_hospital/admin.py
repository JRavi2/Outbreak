from django.contrib import admin
import sys
sys.path.insert(0, '')
from accounts.models import Hospital, Patient


admin.site.register(Hospital)

admin.site.register(Patient)

# Register your models here.
