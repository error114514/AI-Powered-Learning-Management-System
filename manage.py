#!/usr/bin/env python
import os
import sys

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "dj2.settings")
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)

# python  manage.py runserver   --insecure 0.0.0.0:8080  --noreload
#前端：
# http://localhost:8080/dj_intellrnmgmtsystem/front/index.html
#后端：
# http://localhost:8080/dj_intellrnmgmtsystem/admin/dist/index.html#
