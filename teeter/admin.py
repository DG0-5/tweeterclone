from django.contrib import admin
from django.contrib.auth.models import Group, User
from .models import Profile, Teep

# Unregistered Groups(Removing groups from  the admin interface)
admin.site.unregister(Group)

# Link Profile with user section
class ProfileInline(admin.StackedInline):
    model = Profile

#  Registering Users to be edited in the UserAdmin
class UserAdmin(admin.ModelAdmin):
    model = User
    fields = ['username']
    inlines = [ProfileInline]

admin.site.unregister(User)
admin.site.register(User, UserAdmin)
admin.site.register(Teep)
