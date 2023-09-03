import os


data1 = os.system("python manage.py loaddata category.json")
data5 = os.system("python manage.py loaddata image.json")
data3 = os.system("python manage.py loaddata tag.json")
data4 = os.system("python manage.py loaddata taggeditem.json")
data2 = os.system("python manage.py loaddata product.json")
