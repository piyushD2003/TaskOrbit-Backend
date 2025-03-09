from typing import Any
from django.db import models
from django.utils import timezone 

# Create your models here.
class Project(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(default='')
    date = models.DateTimeField(default=timezone.now)
    status = models.CharField(max_length=2, choices=[('PR','PROGRESS'),('CO','COMPLETED'),('PA','PAUSED'),('PE','PENDING')])

    def __str__(self):
        return self.name

class Users(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    password = models.CharField(max_length=50)
    
    def __str__(self):
        return self.name
    
class Member(models.Model):
    project = models.ManyToManyField(Project, related_name='members')
    name = models.ForeignKey(Users,on_delete=models.CASCADE)
    Type = models.CharField(max_length=2,choices=[('AD','ADMIN'),('ME','MEMBER'),('VI','VIEWER'),])
    def __str__(self):
        return str(self.name)

class Step(models.Model):
    project = models.ForeignKey(Project,on_delete=models.CASCADE, related_name='steps')
    user = models.ForeignKey(Member, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    description = models.TextField(default='')
    date = models.DateTimeField(default=timezone.now)
    status = models.CharField(max_length=2, choices=[('PR','PROGRESS'),('CO','COMPLETED'),('PA','PAUSED'),('PE','PENDING'),('RE','REJECTED')])
    suggestion = models.TextField(blank=True, null=True)
    resource_used = models.FloatField(default=0)
    time_used = models.FloatField(default=0)
    def __str__(self):
        return self.name

class Resource(models.Model):
    # project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='resources')
    name = models.CharField(max_length=100)
    unit = models.CharField(max_length=20, default="hours")
    total_capacity = models.FloatField()

    def __str__(self):
        return f"{self.name} ({self.total_capacity} {self.unit})"

class ResourceAllocation(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='resource')
    # resource_name = models.CharField(max_length=100)
    # resource = models.ForeignKey(Resource, on_delete=models.CASCADE, related_name='allocation')
    allocated_amount = models.FloatField()
    utilized_amount = models.FloatField(default=0)
    remaining_amount = models.FloatField(blank=True, null=True)

    allocated_time = models.FloatField()
    utilized_time = models.FloatField(default=0)
    remaining_time = models.FloatField(blank=True, null=True)

    # steps = Step.objects.filter(project=project)
    # print("Hello1", steps)
    # utilized_time = sum(step.time_used for step in steps)
    # print("Hello2", utilized_time)
    # remaining_time = allocated_time - utilized_time
    # print("Hello3", remaining_time)

    def update_utilized(self):
        # Sum the resource usage of all steps in the project for this resource
        # print("Hello",Resource.objects.filter(self.project))
        steps = Step.objects.filter(project=self.project)
        print("Hello1", steps)
        self.utilized_amount = sum(step.resource_used for step in steps)
        print("Hello2", self.utilized_amount)
        self.remaining_amount = self.allocated_amount - self.utilized_amount
        print("Hello3", self.remaining_amount)
        print("Hello4")


    def update_time_utilized(self):
        # Sum the resource usage of all steps in the project for this resource
        # print("Hello",Resource.objects.filter(self.project))
        steps = Step.objects.filter(project=self.project)
        print("Hello1", steps)
        self.utilized_time = sum(step.time_used for step in steps)
        print("Hello2", self.utilized_time)
        self.remaining_time = self.allocated_time - self.utilized_time
        print("Hello3", self.remaining_time)
        print("Hello4")

    # def save0(self, *args, **kwargs):
    #     # Automatically calculate the remaining amount
    #     self.remaining_time = self.allocated_time - self.utilized_time
    #     super().save(*args, **kwargs)
    def save0(self, *args, **kwargs):
        # Automatically calculate the remaining amount
        # self.remaining_amount = self.allocated_amount - self.utilized_amount
        self.update_utilized()
        self.update_time_utilized()
        super().save(*args, **kwargs)

    
    def __str__(self):
        return f"{self.allocated_amount} for {self.project.name}"



