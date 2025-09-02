from django.contrib import admin
from .models import LeaveRequest

@admin.register(LeaveRequest)
class LeaveRequestAdmin(admin.ModelAdmin):
    list_display = ("employee", "reason_short", "status", "created_at")  
    list_filter = ("status", "created_at")
    search_fields = ("employee__username", "reason")     
    ordering = ("-created_at",)                            

    def reason_short(self, obj):
        return (obj.reason[:50] + "...") if len(obj.reason) > 50 else obj.reason
    reason_short.short_description = "Reason"
