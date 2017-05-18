from django.contrib import admin
from ccblog import models

class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'phone', 'valid', 'loginCount')
    search_fields = ('phone',)
    #fields = ('name', 'age')

class BlogTypeAdmin(admin.ModelAdmin):
    list_display = ('id', 'userId', 'typeName')

class BlogAdmin(admin.ModelAdmin):
    list_display = ('userId', 'title', 'createTime', 'lastModifyTime', 'blogTypeId')


admin.site.register(models.User, UserAdmin)
admin.site.register(models.BlogType, BlogTypeAdmin)
admin.site.register(models.Blog, BlogAdmin)
