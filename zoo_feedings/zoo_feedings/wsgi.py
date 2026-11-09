import os
from django.core.wsgi import get_wsgi_application
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'zoo_feedings.settings')
application = get_wsgi_application()
