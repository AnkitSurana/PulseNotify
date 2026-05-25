import os
import dotenv
from django.core.asgi import get_asgi_application

dotenv.load_dotenv()
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "pulsenotify.settings.local")

application = get_asgi_application()
