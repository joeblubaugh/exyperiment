from django.db import models
from django.contrib import admin

# Create your models here.
class OnlineStore(models.Model):
    name = models.TextField()

    def __unicode__(self):
        return self.name


class ProductType(models.Model):
    name = models.TextField()

    def __unicode__(self):
        return self.name


class Demographics(models.Model):
    BOOL_CHOICES = ((True, "Yes"), (False, "No"))
    GENDER_CHOICES = (("F", "Female"), ("M", "Male"))
    gender = models.CharField(choices=GENDER_CHOICES, verbose_name="Please indicate your gender", max_length=8,
                              blank=False)
    birth_year = models.PositiveSmallIntegerField(verbose_name="Your birth year (e.g.): 1900")  # 1900 or later.
    INTERNET_HOURS_CHOICES = (("<2", "Less than 2 hours per week"),
                              ("2-4", "2 hours to 4 hours per week"),
                              ("4-6", "4 hours to 6 hours per week"),
                              ("6-8", "6 hours to 8 hours per week"),
                              (">8", "Greater than 8 hours per week"))
    internet_hours_weekly = models.CharField(choices=INTERNET_HOURS_CHOICES, max_length=256, blank=False,
                                             verbose_name="How many hours a week do you spend using the internet?")
    shopped_online = models.BooleanField(verbose_name="Have you ever bought any item online?", choices=BOOL_CHOICES)
    furniture_online = models.BooleanField(verbose_name="Have you ever bought furniture online?", choices=BOOL_CHOICES)
    SHOP_ONLINE_CHOICES = (("Never", "Never"),
                           ("Very Rarely", "Very Rarely"),
                           ("Once a month", "Once a month"),
                           ("A few times a month", "A few times a month"),
                           ("A few times a week", "A few times a week"))
    shop_online_freq = models.CharField(choices=SHOP_ONLINE_CHOICES, verbose_name="How often do you shop online?", max_length=256, blank=False)
    ONLINE_SPEND_CHOICES = (("$0", "$0"),
                            ("$1-$50", "$1-$50"),
                            ("$51-$100", "$51-$100"),
                            ("$101-$150", "$101-$150"),
                            ("$151-$200", "$151-$200"),
                            ("$201-$250", "$201-$250"),
                            ("$251-$300", "$251-$300"),
                            ("Over $300", "Over $300"))
    shop_online_spend = models.CharField(choices=ONLINE_SPEND_CHOICES, max_length=256, blank=False,
                          verbose_name="Approximately how much money do you spend shopping online in a month?")
    products_purchased = models.ManyToManyField(ProductType,
                                                verbose_name="What types of products do you purchase on the internet?")
    other_product_entry_one = models.CharField(blank=True, max_length=256, verbose_name="Other")
    other_product_entry_two = models.CharField(blank=True, max_length=256, verbose_name="Other")
    other_product_entry_three = models.CharField(blank=True, max_length=256, verbose_name="Other")
    online_store = models.ManyToManyField(OnlineStore,
                                          verbose_name="Which online stores do you frequently buy from?")
    other_store_entry_one = models.CharField(blank=True, max_length=256, verbose_name="Other")
    other_store_entry_two = models.CharField(blank=True, max_length=256, verbose_name="Other")
    other_store_entry_three = models.CharField(blank=True, max_length=256, verbose_name="Other")


class Participant(models.Model):
    NUM_IMAGES_CHOICES = ((2, "Two"), (3, "Three"))
    num_images = models.PositiveSmallIntegerField(choices=NUM_IMAGES_CHOICES, default=2, blank=True, null=True)
    demographics = models.ForeignKey(Demographics, blank=True, null=True)


class ImageSet(models.Model):
    imageOne = models.FileField(blank=True, upload_to="images/")
    imageTwo = models.FileField(blank=True, upload_to="images/")
    imageThree = models.FileField(blank=True, upload_to="images/")
    DISTANCE_CHOICES = (("N", "Near"), ("M", "Medium"), ("F", "Far"))
    distance = models.TextField(choices=DISTANCE_CHOICES, blank=True)


class Answer(models.Model):
    user = models.ForeignKey(Participant, verbose_name="The Participant who entered this answer.")  # Which User
    imageSet = models.ForeignKey(ImageSet)  # Which image set served, by ID.
    WHICH_CHOICES = (("1 2 3", "1 2 3"), ("1 2", "1 2"), ("2 3", "2 3"), ("1 3", "1 3"))
    which = models.TextField(blank=True, choices=WHICH_CHOICES)  # Images selected by computer
    value = models.PositiveIntegerField()  # Price input by user

# Put some classes in the admin interface!
admin.site.register(Participant)
admin.site.register(ImageSet)
admin.site.register(ProductType)
admin.site.register(OnlineStore)
admin.site.register(Demographics)