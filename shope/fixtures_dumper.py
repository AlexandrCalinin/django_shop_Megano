import os


data1 = os.system("python -Xutf8 manage.py dumpdata catalog_app.Category > fixtures/category.json")
data2 = os.system("python -Xutf8 manage.py dumpdata catalog_app.Product > fixtures/product.json")
data3 = os.system("python -Xutf8 manage.py dumpdata taggit.Tag > fixtures/tag.json")
data4 = os.system("python -Xutf8 manage.py dumpdata taggit.TaggedItem > fixtures/taggeditem.json")
data5 = os.system("python -Xutf8 manage.py dumpdata catalog_app.Image > fixtures/image.json")
