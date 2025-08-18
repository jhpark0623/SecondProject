from django.apps import AppConfig
import sys, os, threading



class SecondConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'second'

    def ready(self):
        if 'runserver' not in sys.argv:
            return  # migrate 등 명령어 방지

            # 2) StatReloader 첫 번째 로딩 방지
        if os.environ.get('RUN_MAIN') != 'true':
            return

        from . import tasks
        threading.Thread(target=tasks.start(), daemon=True).start()
