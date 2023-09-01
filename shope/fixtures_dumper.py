import os


data = os.system("python -Xutf8 manage.py dumpdata --exclude auth.permission --exclude contenttypes > fixtures/db.json")
