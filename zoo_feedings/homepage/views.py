from django.shortcuts import render
from feedings import db
from feedings.views import database_errors
@database_errors
def home(request):
    return render(request, 'homepage/home.html', {'total': db.count_feedings()})
