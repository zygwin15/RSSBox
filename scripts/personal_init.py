"""Initialize a built image using committed migrations only."""

import os

import django
from django.core.management import call_command
from scripts.init import create_superuser


def main():
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
    django.setup()
    call_command("migrate", interactive=False, verbosity=1)
    call_command("collectstatic", interactive=False, verbosity=0)
    create_superuser()
    call_command("compilemessages", verbosity=0)


if __name__ == "__main__":
    main()
