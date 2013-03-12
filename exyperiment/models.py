from django.db import models
from django.contrib import admin

# Create your models here.
class OnlineStore(models.Model):
    name = models.TextField()

class ProductType(models.Model):
    name = models.TextField()

class Demographics(models.Model):
    opt_in = models.BooleanField(default=False)
    GENDER_CHOICES = (("F", "Female"), ("M", "Male"))
    gender = models.TextField(choices=GENDER_CHOICES)
    birth_year = models.PositiveSmallIntegerField()  # 1900 or later.
    INTERNET_HOURS_CHOICES = (("<2", "Less than 2 hours per week"),
                              ("2-4", "2 hours to 4 hours per week"),
                              ("4-6", "4 hours to 6 hours per week"),
                              ("6-8", "6 hours to 8 hours per week"),
                              (">8", "Greater than 8 hours per week"))
    internet_hours_weekly = models.TextField(choices=INTERNET_HOURS_CHOICES)
    shopped_online = models.BooleanField()
    furniture_online = models.BooleanField()
    SHOP_ONLINE_CHOICES = (("Never", "Never"),
        ("Very Rarely", "Very Rarely"),
        ("Once a month", "Once a month"),
        ("A few times a month", "A few times a month"),
        ("A few times a week", "A few times a week"))
    shop_online_freq = models.TextField(choices=SHOP_ONLINE_CHOICES)
    ONLINE_SPEND_CHOICES = (("$0", "$0"),
        ("$1-$50", "$1-$50"),
        ("$51-$100", "$51-$100"),
        ("$101-$150", "$101-$150"),
        ("$151-$200", "$151-$200"),
        ("$201-$250", "$201-$250"),
        ("$251-$300", "$251-$300"),
        ("Over $300", "Over $300"))
    shop_online_spend = models.TextField(choices=ONLINE_SPEND_CHOICES)
    products_purchased = models.ManyToManyField(ProductType)
    other_product_entry = models.TextField(blank=True)
    online_store = models.ManyToManyField(OnlineStore)
    other_store_entry = models.TextField(blank=True)

class Participant(models.Model):
    NUM_IMAGES_CHOICES = ((2, "Two"), (3, "Three"))
    num_images = models.PositiveSmallIntegerField(choices = NUM_IMAGES_CHOICES, default=2, blank=True)
    demographics = models.ForeignKey(Demographics, blank=True)

class ImageSet(models.Model):
    imageOne = models.FileField(blank=True, upload_to="images/")
    imageTwo = models.FileField(blank=True, upload_to="images/")
    imageThree = models.FileField(blank=True, upload_to="images/")
    DISTANCE_CHOICES = (("N", "Near"), ("M", "Medium"), ("F", "Far"))
    distance = models.TextField(choices = DISTANCE_CHOICES, blank=True)

class Answer(models.Model):
    user = models.ForeignKey(Participant, verbose_name="The Participant who entered this answer.")  # Which User
    imageSet = models.ForeignKey(ImageSet)  # Which image set served, by ID.
    WHICH_CHOICES = (("1 2 3", "1 2 3"), ("1 2", "1 2"), ("2 3", "2 3"), ("1 3", "1 3"))
    which = models.TextField(choices = WHICH_CHOICES)  # Images selected by computer
    value = models.PositiveIntegerField()  # Price input by user

# Put some classes in the admin interface!
admin.site.register(Participant)
admin.site.register(ImageSet)
admin.site.register(ProductType)
admin.site.register(OnlineStore)
admin.site.register(Demographics)