from django.contrib import admin

# Register your models here.

from .models import Post

admin.site.register(Post)


from .models import Article, Category, Publication, Author, Roles
# Register your models here.


from import_export import resources

class ArticleResource(resources.ModelResource):

    class Meta:
        model = Article
        

class CategoryResource(resources.ModelResource):

    class Meta:
        model = Category
        

class AuthorResource(resources.ModelResource):

    class Meta:
        model = Author
        
class PublicationResource(resources.ModelResource):

    class Meta:
        model = Publication
        
class RoleResource(resources.ModelResource):

    class Meta:
        model = Roles
# app/admin.py
from import_export.admin import ImportExportModelAdmin

class ArticleAdmin(ImportExportModelAdmin):
    resource_class = ArticleResource
 
#class ArticleAdmin(admin.ModelAdmin):
    list_display = ("article_title", "article_created")
    prepopulated_fields = {"article_slug": ("article_title",)}
    
admin.site.register(Article, ArticleAdmin)

class RolesInline(admin.TabularInline):
    model = Roles
    extra = 2 # how many rows to show


#class PublicationAdmin(admin.ModelAdmin):



class AuthorAdmin(ImportExportModelAdmin):
    resource_class = AuthorResource

class PublicationAdmin(ImportExportModelAdmin):
    resource_class = PublicationResource
    inlines = (RolesInline,)


class CategoryAdmin(ImportExportModelAdmin):
    resource_class = CategoryResource
    

class RoleAdmin(ImportExportModelAdmin):
    resource_class = RoleResource
admin.site.register(Publication, PublicationAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Roles, RoleAdmin)

admin.site.register(Author, AuthorAdmin)

