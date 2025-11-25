import os
import traceback
import sys

os.environ.setdefault('DJANGO_SETTINGS_MODULE','sbf.settings')

try:
    print('cwd:', os.getcwd())
    print('sys.path[0]:', sys.path[0])
    print('sys.path sample:', sys.path[:5])
    import django
    # Ensure project root is on sys.path (when running script from scripts/)
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    if project_root not in sys.path:
        sys.path.insert(0, project_root)
        print('inserted project_root into sys.path:', project_root)
    django.setup()
    from main.serializers import CartSerializer
    print('OK')
except Exception:
    traceback.print_exc()
