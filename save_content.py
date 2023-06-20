import sys
import os
import django

import pandas as pd

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
print(BASE_DIR)
sys.path.append(BASE_DIR)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "contentserver.settings")
django.setup()

from api.models import Content, BlogContent
from products.models import Product, ProductCategory

from users.models import Profile, Address, User

from cms.models import Page


df = pd.DataFrame(o.__dict__ for o in Content.objects.all())
df.to_csv(BASE_DIR + "/content.csv")

df = pd.DataFrame(o.__dict__ for o in BlogContent.objects.all())
df.to_csv(BASE_DIR + "/blogcontent.csv")

df = pd.DataFrame(o.__dict__ for o in Product.objects.all())
df.to_csv(BASE_DIR + "/product.csv")

df = pd.DataFrame(o.__dict__ for o in ProductCategory.objects.all())
df.to_csv(BASE_DIR + "/productcategory.csv")

df = pd.DataFrame(o.__dict__ for o in Profile.objects.all())
df.to_csv(BASE_DIR + "/profile.csv")

df = pd.DataFrame(o.__dict__ for o in Address.objects.all())
df.to_csv(BASE_DIR + "/address.csv")

df = pd.DataFrame(o.__dict__ for o in Page.objects.all())
df.to_csv(BASE_DIR + "/page.csv")

df = pd.DataFrame(o.__dict__ for o in User.objects.all())
df.to_csv(BASE_DIR + "/user.csv")
