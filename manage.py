from datetime import datetime

import logging
import os
import sys

# PROJECT_NAME = os.path.dirname(os.path.abspath(__file__)).split("/")[-1]
# WEBSITE_NAME = os.path.dirname(os.path.abspath(__file__)).split("/")[-2]

# Initialize logger
logging.getLogger().setLevel(logging.DEBUG)
logging.basicConfig(datefmt=f"{datetime.now().strftime('%y-%m-%d %H:%M:%S')}",
                    filename=f"{datetime.now().strftime('%Y-%m-%d')}.log",
                    filemode="a",
                    format="%(levelname)s [%(asctime)s] %(message)s")


def main():
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "agence.settings")

    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError("Couldn't import Django. Are you sure it's installed and "
                          "available on your PYTHONPATH environment variable? Did you "
                          "forget to activate a virtual environment?") from exc

    execute_from_command_line(sys.argv)


if __name__ == "__main__":
    main()
