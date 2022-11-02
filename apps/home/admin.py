# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.contrib import admin
from .models import File, Folder
# Register your models here.
@admin.register(Folder)
class Adminfolder(admin.ModelAdmin):
   list_display = ('foldername','folderuser')
   
@admin.register(File)
class Adminfolder(admin.ModelAdmin):
   list_display = ('id','file','filetitle')
# Register your models here.
