from django.db import models
from django.core.validators import MinLengthValidator
from django.contrib.auth.models import User
from django.conf import settings
from taggit.managers import TaggableManager


class Ads(models.Model):

    title = models.CharField(
        max_length = 200,
        validators = [MinLengthValidator(limit_value=2, message="Title must be atleast 2 or more characters.")]
    )
    price = models.DecimalField(max_digits=7, decimal_places=2, null=True)
    tags = TaggableManager(blank=True)
    text = models.TextField()
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='ad_owner')
    picture = models.BinaryField(null=True, editable=True)
    content_type = models.CharField(max_length=256, null=True, help_text='The MIMEType of the file')
    comments = models.ManyToManyField(settings.AUTH_USER_MODEL, through='Comment', related_name='ads_comments')
    favorites = models.ManyToManyField(settings.AUTH_USER_MODEL, through='Favorite', related_name='favorite_ads')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def __str__(self) -> str:
        return self.title

class Favorite(models.Model):
    ads = models.ForeignKey(Ads, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('ads', 'user')

    def __str__(self):
        return '%s likes %s'%(self.user.username, self.ads.title[:10])


class Comment(models.Model):

    text = models.TextField(
        validators = [MinLengthValidator(5, 'Your text must be greater than 5 characters')]
    )

    ad = models.ForeignKey(Ads, on_delete=models.CASCADE)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        if len(self.text) < 15:
             return self.text
        return self.text[:11] + ' ...'



