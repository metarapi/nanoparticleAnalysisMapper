import os
from django.conf import settings

os.makedirs(settings.FILE_UPLOAD_TEMP_DIR, exist_ok=True)