from django.urls import path, include
# from .views import *
from rest_framework import routers
from api import views

router = routers.DefaultRouter()
router.register(r'projects',views.ProjectView, 'projects')

router1 = routers.DefaultRouter()
router1.register(r'users',views.UserView, 'users')

router2 = routers.DefaultRouter()
router2.register(r'steps',views.StepView, 'steps')

router3 = routers.DefaultRouter()
router3.register(r'members',views.MemberView, 'members')

urlpatterns = [
    path('',include(router.urls)),
    path('',include(router1.urls)),
    path('',include(router2.urls)),
    path('',include(router3.urls)),
    # path('api/user/', include(router1.urls)),
]