import os


os.system("python -Xutf8 manage.py dumpdata catalog_app.Category > fixtures/1_category.json")
os.system("python -Xutf8 manage.py dumpdata catalog_app.Image > fixtures/3_image.json")
os.system("python -Xutf8 manage.py dumpdata taggit.Tag > fixtures/5_tag.json")
os.system("python -Xutf8 manage.py dumpdata taggit.TaggedItem > fixtures/7_taggeditem.json")
os.system("python -Xutf8 manage.py dumpdata catalog_app.Product > fixtures/9_product.json")
