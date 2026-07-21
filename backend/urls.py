from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    # 1. Admin Panel
    path('admin/', admin.site.urls),

    # 2. Users App Routes
    path('api/users/', include('users.urls')),

    # 3. AI Notes Generator Route
    path('api/notes/', include('notes.urls')),

    # 4. Courses App Routes 
    path('api/', include('courses.urls')),

    # 4. Forced Secure JWT Login Routes (No more yellow screens!)
    path('api/auth/login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]