from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    # 1. Admin Panel
    path('admin/', admin.site.urls),
    
    # 2. Users App Routes (Signup wagera ke liye)
    path('api/users/', include('users.urls')), 
    
    # 3. JWT Login (Is URL se Token milega)
    path('api/auth/login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    
    # 4. Token Refresh (Jab access token expire ho jaye)
    path('api/auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    # 5. Courses
    path('api/courses/', include('courses.urls')),  
]