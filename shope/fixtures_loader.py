import os


for fixture in os.listdir('fixtures'):
    os.system("python manage.py loaddata %s" % 'fixtures/' + fixture)


os.system("python manage.py loaddata %s" % 'fixtures/12_price.json')