from django.urls import include, path
urlpatterns = [path('', include('homepage.urls')), path('aviaries/', include('aviaries.urls')),
               path('feedings/', include('feedings.urls'))]
handler404 = 'feedings.views.page_not_found'
