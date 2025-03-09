# Create your views here.
# from rest_framework.views import APIView
# from rest_framework.response import Response
from rest_framework import status,viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from django.contrib.auth.hashers import check_password
from itsdangerous import URLSafeSerializer
from .serializer import ProjectSerializer, User_Serializer, Member_Serializer, Step_Serializer
from .models import Project, Users, Member, Step ,Resource, ResourceAllocation
from .middleware import MiddleWare
Secret_key = "I am a good boy"

class ProjectView(viewsets.ModelViewSet):
    serializer_class = ProjectSerializer
    queryset = Project.objects.all()
    # permission_classes = [IsAuthenticated]

    @action(detail=False, methods=['post'])
    def Create(self, request, *args, **kwargs):
        
        auth = MiddleWare().fetchuser(request)
        if auth.data.get('detail') is not True:
            return Response(auth.data)
        
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=True, methods=['delete'],url_path='Delete')
    def Delete(self, request, pk=None):
        auth = MiddleWare().fetchuser(request)
        if auth.data.get('detail') is not True:
            return Response(auth.data)
        
        try:
            project = Project.objects.get(pk=pk)
            project.delete()
            return Response({"detail": "Project deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
        except Project.DoesNotExist:
            return Response({"detail": "Project not found"}, status=status.HTTP_404_NOT_FOUND)
    
    @action(detail=True, methods=['post'], url_path="AllocateResource")
    def AllocateResource(self,request,pk=None):
        auth = MiddleWare().fetchuser(request)
        if auth.data.get('detail') is not True:
            return Response(auth.data)
        print(request, pk)
        try:

            project = Project.objects.get(pk=pk)
            allocation = ResourceAllocation.objects.filter(project=project).first()
            StepExist = Step.objects.filter(project = project).first()
            print(StepExist)
            if Project.objects.filter(pk=pk).exists():
                if allocation and StepExist is None:
                    allocation.allocated_amount=allocation.remaining_amount = request.data.get("allocated_amount", allocation.allocated_amount)
                    allocation.allocated_time= allocation.remaining_time = request.data.get("allocated_time", allocation.allocated_time)
                    allocation.utilized_amount = allocation.utilized_time = 0
                    # allocation.remaining_amount = request.data.get("allocated_amount", allocation.allocated_amount)
                    # allocation.remaining_time = request.data.get("allocated_time", allocation.allocated_time)
                    allocation.save()
                    return Response({"detail": "Project Resource updated successfully"}, status=status.HTTP_200_OK)
                elif allocation is None:
                    ResourceAllocation.objects.create(
                        project=project,
                        allocated_amount=request.data.get("allocated_amount"),
                        allocated_time=request.data.get("allocated_time"),
                        remaining_amount = request.data.get("allocated_amount"),
                        remaining_time = request.data.get("allocated_time")
                        
                    )
                    return Response({"detail": "Project Resource allocated successfully"}, status=status.HTTP_201_CREATED)
                else:
                    return Response({"detail": "Project Resource already allocated and distritubed"}, status=status.HTTP_201_CREATED)
        except Project.DoesNotExist:
            return Response({"detail": "Project not found or Resource already assigned"}, status=status.HTTP_404_NOT_FOUND)
        

class UserView(viewsets.ModelViewSet):
    serializer_class = User_Serializer
    queryset = Users.objects.all()

    @action(detail=False, methods=['post'])
    def Create(self, request):
        print(request.data)
        userexist = Users.objects.filter(email=request.data.get("email")).exists()
        serializer = User_Serializer(data=request.data)
        if serializer.is_valid() and not userexist:
            serializer.save()

            user = Users.objects.get(email=request.data.get("email"))
            s = URLSafeSerializer(Secret_key)
            token = s.dumps({"user_id":user.id}, salt="activate")
            return Response(
                {
                    "token": token,
                    "detail":serializer.data,
                },
                status=status.HTTP_201_CREATED
            )
        return Response(
                {
                "detail":"User already exist"
                },
                status = status.HTTP_208_ALREADY_REPORTED
            )
    
    @action(detail=False, methods=['post'])
    def login(self, request):
        print(request.data)
        email = request.data.get("email")
        password = request.data.get("password")

        try:
            user = Users.objects.get(email=email)
            print(user.id)
            if check_password(password, user.password):  # Use hashed password check with Django's methods in real scenarios
                s = URLSafeSerializer(Secret_key)
                token = s.dumps({"user_id":user.id}, salt="activate")
                print(token)

                return Response(
                    {
                    "detail": "Login successful",
                    "token": token,
                    "user": {"id": user.id, "name": user.name, "email": user.email},
                },
                    status=status.HTTP_200_OK,
                )
            return Response({"detail": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)
        except Users.DoesNotExist:
            return Response({"detail": "User not found"}, status=status.HTTP_404_NOT_FOUND)
        
    @action(detail=False, methods=['post'])
    def logout(self, request):
        pass

class MemberView(viewsets.ModelViewSet):

    serializer_class = Member_Serializer
    queryset = Member.objects.all()

    @action(detail=False, methods=['post'], url_path='Create/(?P<userid>[0-9]+)/(?P<projectid>[0-9]+)')
    def Create(self, request, userid = None, projectid = None):
        auth = MiddleWare().fetchuser(request)
        if auth.data.get('detail') is not True:
            return Response(auth.data)
        project = Project.objects.get(pk = projectid)
        name = Users.objects.get(pk = userid)
        memberExist = Member.objects.filter(name= name, project= project).exists()
        if memberExist:
            return Response({"detail": "Member already created"}, status=201)
        else:
            member = Member.objects.create(
                name = name,
                Type = request.data.get("Type")
            )
            member.project.set([project])
            return Response({"detail": "Member created successfully", "member_id": member.id}, status=201)
        


class StepView(viewsets.ModelViewSet):

    serializer_class = Step_Serializer
    queryset = Step.objects.all()
    
    @action(detail=False, methods=['post'], url_path='Create/(?P<memberid>[0-9]+)/(?P<projectid>[0-9]+)')
    def Create(self, request, memberid = None, projectid = None):
        auth = MiddleWare().fetchuser(request)
        if auth.data.get('detail') is not True:
            return Response(auth.data)
        try:
            project = Project.objects.get(pk = projectid)
            member = Member.objects.get(pk = memberid)
            print(project, member)
            print(request.data)
            print(projectid, memberid)
            step = Step.objects.create(
                project = project,
                user = member,
                name = request.data.get("name"),
                description = request.data.get("description"),
                status = request.data.get("status"),
                resource_used = request.data.get("resource_used"),
                time_used = request.data.get("time_used"),

            )
            
            ReAllo = ResourceAllocation.objects.filter(project=project).first()  # Assume only one allocation per project
            if ReAllo:
                ReAllo.remaining_amount =ReAllo.remaining_amount- step.resource_used
                ReAllo.remaining_time = ReAllo.remaining_time - step.time_used
                ReAllo.utilized_amount += step.resource_used
                ReAllo.utilized_time += step.time_used
                ReAllo.save()

            return Response({"detail": "Step created Successfully"}, status=status.HTTP_200_OK)
        except:
            return Response({"detail": "Internal Server Error"}, status=status.HTTP_404_NOT_FOUND)
    
    @action(detail=False, methods=['post'],url_path='Suggestion/(?P<memberid>[0-9]+)/(?P<projectid>[0-9]+)/(?P<stepid>[0-9]+)')
    def Suggestion(self, request, memberid = None, projectid = None, stepid=None):
        print("AAAAAAAAAAAAAAAAAAAa")
        auth = MiddleWare().fetchuser(request)
        if auth.data.get('detail') is not True:
            return Response(auth.data)
        print("AAAAAAAAAAAAAAAAAAA0a")
        print(projectid, memberid, request.data)
        project = Project.objects.get(pk = projectid)
        memberExist = Step.objects.filter(pk = stepid, project = project).exists()
        print(memberExist)
        if memberExist:
            member = Member.objects.get(pk = memberid)
            if member.Type == "AD" or member.Type == "VI":
                return Response({"detail":"This is a admin or viewer"})
            else:
                return Response({"detail":"This is not admin or viewer"})
        else:
                return Response({"detail":"Member not Exist"})


        
        
        
        



    
# class ApiView(APIView):
#     def get(self, request):
#         data = {"project":f"{Project.objects.all()}"}
#         return Response(data, status=status.HTTP_200_OK)

# class ExampleView(APIView):   
#     def get(self, request):
#         data = {"message": "Hello, World api/example!"}
#         return Response(data, status=status.HTTP_200_OK)

# class ProjectDetail(APIView):
#     def get(self, request):
#         project = get_list_or_404(Project)

# class CreateUser(APIView):
#     def get(self, request):
#         pass



