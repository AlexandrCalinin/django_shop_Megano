import os


for fixture in os.listdir('fixtures'):
    os.system("python manage.py loaddata %s" % fixture)
