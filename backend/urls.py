from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
# sys import kar ke rasta clear karna
import sys
# Temporary bypass for environment packages mismatch
try:
    from rest_framework.simplejwt.views import TokenObtainPairView, TokenRefreshView
    HAS_JWT = True
except ImportError:
    HAS_JWT = False

urlpatterns = [
    # # 1. Admin Panel
    path('admin/', admin.site.urls),

    # # 2. Users App Routes (Signup wagera ke liye)
    path('api/users/', include('users.urls')),

    # # 5. Zunaira ka AI Notes Generator Route (Ab Connect Ho Gaya!)
    path('api/notes/', include('notes.urls')),
]

# Agar environment mien simplejwt mil jaye toh raste active hon, warna server crash na ho
if HAS_JWT:
    urlpatterns.append(path('api/auth/login/', TokenObtainPairView.as_view(), name='token_obtain_pair'))
    urlpatterns.append(path('api/auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'))
else:
    print("\n[SMARTEDUX WARNING]: SimpleJWT package isolated to prevent crash. AI Notes is fully functional.")