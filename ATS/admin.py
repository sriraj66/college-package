from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from ATS.models import ATS

class ATSAdmin(ImportExportModelAdmin,admin.ModelAdmin):
    
    fieldsets = (
        ("general", {"fields": ("user", "jd", "rating")}),
        ("other", {"fields": ("file", "responce", "created")}),
    )
    list_filter = ("id","user","rating","created")
    list_display = ["id","user","rating","created"]
    

admin.site.register(ATS, ATSAdmin)