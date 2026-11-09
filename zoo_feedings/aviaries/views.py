from django.shortcuts import render
from feedings import db
from feedings.views import database_errors
@database_errors
def aviary_list(request):
    return render(request, 'aviaries/aviary_list.html', {'aviaries': db.get_aviaries()})
