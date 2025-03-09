from django.contrib import admin
from .models import Project, Users, Member, Step ,Resource, ResourceAllocation

# Register your models here.

class UserAdmin(admin.ModelAdmin):
    list_display = ('name', 'email')

class StepInline(admin.TabularInline):
    model = Step
    extra = 1

class MemberInline(admin.TabularInline):
    model = Member
    extra = 1

class ProjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'status', 'date')
    inlines = [StepInline]

class StepAdmin(admin.ModelAdmin):
    list_display = ('name', 'status', 'date')

class MemberAdmin(admin.ModelAdmin):
    list_display = ('name', 'Type')
    filter_horizontal = ('project',)

class ResourceInline(admin.TabularInline):
    model = Resource
    extra = 2

class ResourceAdmin(admin.ModelAdmin):
    list_display = ('project', "allocated_amount","allocated_time")
    # inlines=[ResourceInline]


admin.site.register(Project, ProjectAdmin)
admin.site.register(Users, UserAdmin)
admin.site.register(Member, MemberAdmin)
admin.site.register(Step, StepAdmin)
admin.site.register(Resource)
admin.site.register(ResourceAllocation, ResourceAdmin)
