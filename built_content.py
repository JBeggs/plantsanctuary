import sys
import os
import django
import numpy

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "contentserver.settings")
django.setup()

import pandas as pd

from django.core.management.color import no_style
from django.db import connection


from api.models import Content, BlogContent
from products.models import Product, ProductCategory

from users.models import Profile, Address, User

from PIL import Image


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + '/plantsanctuary/'
MEDIA_BASE = BASE_DIR + 'media/'
sys.path.append(BASE_DIR)


def update_base_image(base_image, row):
    if base_image:
        base_image = base_image.replace(" ", "\\ ")
        source = f'{MEDIA_BASE}{base_image}'
        row_image = row["image"].replace(" ", "_")
        destination = f'{MEDIA_BASE}{row_image}'
        print(f'cp -vaR  {source} {destination}')
        dirs = row_image.split('/')
        path = ''
        for directory in dirs:
            path += directory + '/'
            if 'jpg' not in directory and 'jpeg' not in directory and 'png' not in directory:
                os.system(f'mkdir {MEDIA_BASE}{path}')

        os.system(f'cp -vaR {MEDIA_BASE}{base_image} {MEDIA_BASE}{row_image}')
        base_image = f'{row_image}'
        return base_image
    return ''


def delete_old_data():
    for product in Product.objects.all():
        product.delete()

    for cat in ProductCategory.objects.all():
        cat.delete()

    for profile in Profile.objects.all():
        profile.delete()

    delete_users = User.objects.all()
    for user in delete_users:
        user.delete()

    delete_content = Content.objects.all()
    for content in delete_content:
        content.delete()

    sequence_sql = connection.ops.sequence_reset_sql(no_style(), [User, Profile, Product, Content])
    with connection.cursor() as cursor:
        for sql in sequence_sql:
            cursor.execute(sql)


def update_users(df):

    for index, row in df.iterrows():
        user = User(
            id=row["id"],
            password=row["password"],
            is_superuser=row["is_superuser"],
            username=row["username"],
            first_name=row["first_name"],
            last_name=row["last_name"],
            email=row["email"],
            is_staff=row["is_staff"],
            is_active=row["is_active"],

        )
        user.save()
    """
    ,_state,id,password,last_login,is_superuser,username,first_name,last_name,email,is_staff,is_active,date_joined
    """


update_users(
    pd.read_csv(BASE_DIR + '/user.csv').sort_values(by=['id'])
)


def update_profile(df):

    for index, row in df.iterrows():
        profile = Profile()
        user = User.objects.get(id=row["user_id"])
        # profile = Profile.objects.get(user_id=user.id)
        profile.avatar = row["avatar"]
        profile.bio = row["bio"]
        profile.user_id = user.id

        try:
            profile.save()
        except Exception as e:
            print(e)
            exit('profile')
    """
    ,_state,id,user_id,avatar,bio,created_at,updated_at
    """


# update_profile(
#     pd.read_csv(BASE_DIR + '/profile.csv').sort_values(by=['id'])
# )


def update_product_category(df):

    for index, row in df.iterrows():

        category = ProductCategory(
            id=row["id"],
            name=row["name"],
        )
        try:
            category.save()
        except Exception as e:
            print(e)
            exit('productcategory')


update_product_category(
    pd.read_csv(BASE_DIR + '/productcategory.csv').sort_values(by=['id'])
)


def update_content(df):

    for index, row in df.iterrows():
        if not type(row["image"]) == float:
            base_image = 'backup/' + row["image"]
        else:
            base_image = ''

        base_image = update_base_image(base_image, row)

        desc = ''
        if not type(row["desc"]) == float:
            desc = row["desc"]

        content = Content(
            creator_id = row["creator_id"],
            name=row["name"],
            desc=desc,
            active=row["active"],
            image=base_image,
        )

        try:
            content.save()
        except Exception as e:
            print(e)
            exit('content')

    """
    ,_state,id,creator_id,name,desc,image,thumbnail,created_at,updated_at,active
    """


update_content(
    pd.read_csv(BASE_DIR + '/content.csv').sort_values(by=['id'])
)


def update_product_categoy(df):

    for index, row in df.iterrows():
        category = ProductCategory(
            name=row["name"],
        )
        category.save()

    """
    ,_state,id,name,icon,created_at,updated_at
    """


update_product_categoy(
    pd.read_csv(BASE_DIR + 'productcategory.csv').sort_values(by=['id'])
)


def update_product(df):

    for index, row in df.iterrows():

        if not type(row["image"]) == float:

            base_image = 'backup/' + row["image"]
        else:
            base_image = ''

        base_image = update_base_image(base_image, row)

        desc = ''
        if not type(row["desc"]) == float:
            desc = row["desc"]
        category = ProductCategory.objects.get(id=row["category_id"])

        product = Product(
            seller_id = row["seller_id"],
            category_id=category.id,
            name=row["name"],
            desc=desc,
            active=row["active"],
            price=row["price"],
            quantity=row["quantity"],
            barcode=row["barcode"],
            image=base_image,
        )

        try:
            product.save()
        except Exception as e:
            print(e)
            exit('content')

    """
    ,_state,id,seller_id,category_id,name,desc,image,thumbnail,price,quantity,barcode,created_at,updated_at,active
    """


update_product(
    pd.read_csv(BASE_DIR + '/product.csv').sort_values(by=['id'])
)
