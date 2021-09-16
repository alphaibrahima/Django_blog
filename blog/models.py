from django.db import models
from django.db.models.expressions import F
from django.db.models.fields import DateTimeField
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse


# Create your models here.

class Post(models.Model):

    class NewManager(models.Manager):
        def get_queryset(self):
            return super().get_queryset() .filter(status='published')

    options = (
        ('draft', 'Draft'),
        ('published', 'Published'),
    )

    title           = models.CharField(max_length=250)
    slug            = models.SlugField(max_length=250, unique_for_date='publish')
    publish         = models.DateTimeField(default=timezone.now)
    author          = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blog_posts')
    Content         = models.TextField()
    status          = models.CharField(max_length=10, choices=options, default='draft')

    objects         = models.Manager() #default manager
    newmanager      = NewManager() #custom manager

    def get_absolute_url(self):
        return reverse("blog:post_single", args=[self.slug])
    

    class Meta:
        ordering = ('-publish',)

    def __str__(self) :
        return self.title




# model pour les commentaire

class Comment(models.Model):
    post        = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")
    name        = models.CharField(max_length=50)
    email       = models.EmailField()
    content     = models.TextField()
    publish     = DateTimeField(auto_now_add=True)
    status      = models.BooleanField(default=True)

    class Meta:
        ordering = ("publish",)

    def __str__(self):
        return f"Comment by {self.name}"
