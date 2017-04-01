from django.db import models
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill
# Create your models here.
from django.utils import timezone
from ckeditor.fields import RichTextField

class Category(models.Model):
    category_name = models.CharField(max_length=200)
    
    def __str__(self):
        return self.category_name

class Publication(models.Model):
    publication_name = models.CharField(max_length=200)
    
    def __str__(self):
        return self.publication_name
class Author(models.Model):
    pre = models.CharField(max_length=30, null=True, blank=True)
    first_name = models.CharField(max_length=30, null=True, blank=True)
    last_name = models.CharField(max_length=40, null=True, blank=True)
    suf = models.CharField(max_length=30, null=True, blank=True)
    title = models.CharField(max_length=60, null=True, blank=True)
    other_name = models.CharField(max_length=40, null=True, blank=True)
    publication = models.ManyToManyField('Publication', through='Roles')
    email = models.CharField(max_length=40, null=True, blank=True)
    twitter = models.CharField(max_length=40, null=True, blank=True)
    def __str__(self):
        return '%s %s %s' % (self.first_name, self.last_name, self.other_name)

class PublishedArticlesManager(models.Manager):  
    def get_query_set(self):
        return super(PublishedArticlesManager, self).filter(article_publish=True)
            

        
class Roles(models.Model):
    author = models.ForeignKey(Author, related_name='affiliation')
    publication = models.ForeignKey(Publication, related_name='affiliation')
    role_name = models.CharField(max_length=100)
    
    def __str__(self):
        return "%s %s (as %s)" % (self.author, self.publication, self.role_name)
class Post(models.Model):
    author = models.ForeignKey('auth.User')
    title = models.CharField(max_length=200)
    text = models.TextField()
    created_date = models.DateTimeField(
            default=timezone.now)
    published_date = models.DateTimeField(
            blank=True, null=True)
    
    url = models.URLField("URL", max_length=250, blank=True)
    category_name = models.ForeignKey(Category, on_delete=models.CASCADE)
    
    article_coverurl = models.URLField(max_length=250, blank=True)
    article_publication_name = models.ForeignKey(Publication, on_delete=models.CASCADE, blank=True)
    article_authors = models.ManyToManyField(Author, blank=True, null=True)
    
    article_authorsroles = models.ManyToManyField(Roles, blank=True, null=True)
    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return self.title
        
        
class Article(models.Model):
    article_category_name = models.ForeignKey(Category, on_delete=models.CASCADE)
    article_title = models.CharField(max_length=200)
    article_body = RichTextField()
    article_slug = models.SlugField(max_length=200, unique=True)
    article_publish = models.BooleanField(default=False)
    article_created = models.DateTimeField(auto_now_add=True)
    article_modified = models.DateTimeField(auto_now=True)
    article_url = models.URLField("URL", max_length=250, blank=True)
    article_coverurl = models.URLField(max_length=250, blank=True)
    article_publication_name = models.ForeignKey(Publication, on_delete=models.CASCADE, blank=True)
    article_authors = models.ManyToManyField(Author, blank=True, null=True)
    article_date = models.DateTimeField(blank=True, null=True)
    def __str__(self):
        return self.article_title
    objects = models.Manager()
    published_articles = PublishedArticlesManager()
 
    article_authorsroles = models.ManyToManyField(Roles, blank=True, null=True)

    class Meta:
        verbose_name = "Blog Entry"
        verbose_name_plural = "Blog Entries"
        ordering = ["-article_created"]