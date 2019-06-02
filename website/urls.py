from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("", include("home.urls", namespace="home")),
    path("accounts/", include("oauth.urls")),
    path("admin/", admin.site.urls),
    path("blog/", include("guides.urls", namespace="blog")),
    path("profile/", include("profiles.urls", namespace="profiles")),
    path("stats/", include("stats.urls", namespace="stats")),
]
