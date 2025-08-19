from django.contrib import admin
from django import forms


# Register your models here.
from .models import Category, Post, Heading, PostAnalytics

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'title', 'parent', 'slug')
    search_fields = ('name', 'title', 'description', 'slug')
    prepopulated_fields = {'slug': ('name',)}
    list_filter = ('parent',)
    ordering = ('name',)
    readonly_fields = ('id',)
    list_editable = ('title',)

class HeadingInline(admin.TabularInline):
    model = Heading
    extra = 1 #Esto hace que si queremos agregar otro heading, nos añade +1 abajo
    fields = ('title', 'level', 'order', 'slug')
    prepopulated_fields = {'slug': ('title',)}
    ordering = ('order',)

@admin.register(Post) #Recordar que en el metodo post es slugs, se me fue una "s" en ese modelo xd
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'status', 'category', 'created_at', 'updated_at')
    search_fields = ('title', 'description', 'content', 'keywords', 'slug')
    prepopulated_fields = {'slug': ('title',)} #Error mío, solo el "slugs" funciona aquí, en los demás campos es sin la "s"
    list_filter =('status', 'category', 'updated_at',)
    ordering = ('-created_at',) #el negativo aqui nos funciona para señalizar desde el más nuevo al mas viejo
    readonly_fields = ('id', 'created_at', 'updated_at',)
    fieldsets = (
        ('General Information', {
            'fields' : ('title', 'description', 'content','thumbnail', 'keywords', 'slug', 'category' )
        }),
        ('Status & Dates', {
            'fields' : ('status', 'created_at', 'updated_at')
        }),
    )
    inlines = [HeadingInline]


#Definir el administrador de los headings 
#@admin.register(Heading)
#class HeadingAdmin(admin.ModelAdmin):
#    list_display = ('title', 'post', 'level', 'order')
 #   search_fields = ('title', 'post__title') # Ese post__title, significa que es el título que hace referencia al post
  #  list_filter = ('level', 'post')
   # ordering = ('post', 'order')
    #prepopulated_fields = {'slug': ('title',)}

#Esto será el admin de las analiticas 
@admin.register(PostAnalytics)
class PostAnalyticsAdmin(admin.ModelAdmin):
    list_display = ('post_title','views',
                        'impressions',
                        'clicks',
                        'click_through_rate',
                        'avg_time_on_page')
    search_fields = ( 'post__title',)

    readonly_fields = (   'post_title','views',
                        'impressions',
                        'clicks',
                        'click_through_rate',
                        'avg_time_on_page')
   
    def post_title(self, obj):
        return obj.post.title
    
    post_title.short_description = 'Post Title'