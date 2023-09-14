import os

print(os.listdir('fixtures'))
for fixture in os.listdir('fixtures'):
    os.system("python manage.py loaddata %s" % fixture)
