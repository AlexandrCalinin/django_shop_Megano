import os


os.system("python -Xutf8 manage.py dumpdata catalog_app.Category > fixtures/1_category.json")
os.system("python -Xutf8 manage.py dumpdata catalog_app.Image > fixtures/3_image.json")
os.system("python -Xutf8 manage.py dumpdata taggit.Tag > fixtures/5_tag.json")
os.system("python -Xutf8 manage.py dumpdata taggit.TaggedItem > fixtures/7_taggeditem.json")
os.system("python -Xutf8 manage.py dumpdata catalog_app.Product > fixtures/9_product.json")
os.system("python -Xutf8 manage.py dumpdata auth_app.User > fixtures/10_user.json")
os.system("python -Xutf8 manage.py dumpdata core.Seller > fixtures/11_seller.json")
os.system("python -Xutf8 manage.py dumpdata core.Price > fixtures/12_price.json")
os.system("python -Xutf8 manage.py dumpdata catalog_app.DiscountProduct > fixtures/13_discount_product.json")
os.system("python -Xutf8 manage.py dumpdata catalog_app.DiscountProductGroup > fixtures/15_discount_product_group.json")
os.system("python -Xutf8 manage.py dumpdata catalog_app.CartSale > fixtures/17_cart_sale.json")
