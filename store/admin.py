from django.contrib import admin
from store.models import *
# OR

# from store.models import User,Categorymodel,Productmodel

# Register your models here.

admin.site.register(Productmodel)
admin.site.register(Categorymodel)
