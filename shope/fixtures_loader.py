import os

print(sorted(os.listdir('fixtures'), reverse=False))
for fixture in sorted(os.listdir('fixtures'), reverse=False):
    os.system("python manage.py loaddata %s" % fixture)
