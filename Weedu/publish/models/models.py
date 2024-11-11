import os

from django.db import models
from django.core.validators import MaxValueValidator


def image_upload_function(instance, filename):

    model_name = instance.__class__.__name__.lower()

    if model_name == "shop":

        folder_name = "products_images"

    elif model_name == "course":

        folder_name = "courses_images"

    elif model_name == "lesson":

        folder_name = "lessons_images"

    else:
        folder_name = "other_images"

    safe_title = instance.title.replace(" ", "_").replace("/", "_")
    
    return os.path.join(folder_name, safe_title, filename)


class Shop(models.Model):

    """Shop model where user can buy an product"""

    title = models.CharField(max_length=100, null=False, blank=False, unique=True)

    description = models.TextField(null=True, blank=True)

    price = models.IntegerField(blank=False, null=False)

    donation_price = models.IntegerField(blank=True, null=True)

    rating = models.FloatField(blank=False, validators=[MaxValueValidator(5)])

    main_image = models.ImageField(upload_to=image_upload_function, null=True, blank=True)

    image_1 = models.ImageField(upload_to=image_upload_function, null=True, blank=True)

    image_2 = models.ImageField(upload_to=image_upload_function, null=True, blank=True)

    image_3 = models.ImageField(upload_to=image_upload_function, null=True, blank=True)

    image_4 = models.ImageField(upload_to=image_upload_function, null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):

        return self.title


class Purchase(models.Model):

    user_profile = models.ForeignKey('users.Weedu_User', on_delete=models.CASCADE)

    product = models.ForeignKey(Shop, on_delete=models.CASCADE)

    date_purchased = models.DateTimeField(auto_now_add=True)

    quantity = models.PositiveIntegerField(default=1)
    
    def __str__(self):

        return f"Purchase of {self.product.name} by {self.user_profile.user.username}"



class Course(models.Model):

    """Model where defines rows for courses"""

    title = models.CharField(max_length=100, null=False, blank=False, unique=True)

    description = models.TextField(null=True, blank=True)

    rating = models.FloatField(blank=False, validators=[MaxValueValidator(5)])

    main_image = models.ImageField(upload_to=image_upload_function, null=True, blank=True)

    image_1 = models.ImageField(upload_to=image_upload_function, null=True, blank=True)

    image_2 = models.ImageField(upload_to=image_upload_function, null=True, blank=True)

    image_3 = models.ImageField(upload_to=image_upload_function, null=True, blank=True)

    image_4 = models.ImageField(upload_to=image_upload_function, null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):

        return self.title


class Lesson(models.Model):

    """Model where defines rows for lessons"""

    course = models.ForeignKey(Course, related_name='lessons', on_delete=models.CASCADE)

    title = models.CharField(max_length=100, null=False, blank=False, unique=True)

    description = models.TextField(null=True, blank=True)

    rating = models.FloatField(blank=False, validators=[MaxValueValidator(5)])

    content = models.TextField(null=True, blank=True)

    image_1 = models.ImageField(upload_to=image_upload_function, null=True, blank=True)

    image_2 = models.ImageField(upload_to=image_upload_function, null=True, blank=True)

    image_3 = models.ImageField(upload_to=image_upload_function, null=True, blank=True)

    image_4 = models.ImageField(upload_to=image_upload_function, null=True, blank=True)

    image_5 = models.ImageField(upload_to=image_upload_function, null=True, blank=True)


class Progress(models.Model):

    """Model where defines progress of user in course's lesson"""

    user = models.ForeignKey('users.Weedu_User', on_delete=models.CASCADE)

    course = models.ForeignKey(Course, on_delete=models.CASCADE)

    lessons_completed = models.PositiveIntegerField(default=0)

    class Meta:

        unique_together = ('user', 'course')

    def __str__(self):

        return f"{self.user.username} - {self.course.title} ({self.lessons_completed}/{self.course.lessons.count()})"


class Achievement(models.Model):

    class Rarity(models.TextChoices):

        COMMON = 'Common', 'Common'
        RARE = 'Rare', 'Rare'
        EPIC = 'Epic', 'Epic'

    title = models.CharField(max_length=255, null=False, blank=False, unique=True)

    description = models.TextField()

    image = models.ImageField(upload_to='achievement/', null=True, blank=True)

    xp = models.SmallIntegerField(default=0, null=True, blank=True)

    rarity = models.CharField(max_length=10, choices=Rarity.choices, default=Rarity.COMMON)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):

        return self.title


class UserAchievement(models.Model):

    user = models.ForeignKey('users.Weedu_User', on_delete=models.CASCADE)

    achievement = models.ForeignKey(Achievement, on_delete=models.CASCADE)

    achieved_at = models.DateTimeField(auto_now_add=True)

    class Meta:

        unique_together = ('user', 'achievement')

    def __str__(self):

        return f"{self.user.username} - {self.achievement.title}"


class Award(models.Model):

    title = models.CharField(max_length=255, null=False, blank=False, unique=True)

    description = models.TextField()

    image = models.ImageField(upload_to='award/', null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):

        return self.title


class UserAward(models.Model):

    user = models.ForeignKey('users.Weedu_User', on_delete=models.CASCADE)

    award = models.ForeignKey(Award, on_delete=models.CASCADE)

    awarded_at = models.DateTimeField(auto_now_add=True)

    class Meta:

        unique_together = ('user', 'award')

    def __str__(self):

        return f"{self.user.username} - {self.achievement.title}"
