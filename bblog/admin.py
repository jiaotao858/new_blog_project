# -*- coding:utf-8 -*-
from django.contrib import admin
from models import *
from . import models
# Register your models here.

#设置显示内容
class UserAdmin(admin.ModelAdmin):
    pass

class ArticleAdmin(admin.ModelAdmin):
    pass

class TagAdmin(admin.ModelAdmin):
    pass

class CategoryAdmin(admin.ModelAdmin):
    pass

class ArticleAdmin(admin.ModelAdmin):
    # fields 内容页面设置显示内容
    # fields = ('title','content','click_count')

    # exclude 除了该内容不显示，其余内容都显示
    # exclude = ('click_count',)

    # list_display目录页需显示内容
    list_display = ('title','desc','date_publish','click_count')

    # list_display_links可以点击的内容
    list_display_links = ('title','desc',)

    # list_editable可以编辑的内容
    list_editable = ('click_count',)

    # list_filter右侧边显示筛选项
    list_filter = ('desc',)

    search_fields = ('title',)
    # fieldsets折叠内容设置
    fieldsets = (
        ('基本内容', {
            'fields': ('title', 'desc', 'content','user','category','tag')
        }),
        ('选填内容', {
            'classes': ('collapse',),
            'fields': ('click_count', 'is_recommend')
        }),
     )

    # 副文本编辑器的模型
    class Media:
        js = (
            '/static/js/kindeditor-4.1.10/kindeditor-min.js',
            '/static/js/kindeditor-4.1.10/lang/zh_CN.js',
            '/static/js/kindeditor-4.1.10/config.js',
        )
class CommentAdmin(admin.ModelAdmin):
    pass

class LinkAdmin(admin.ModelAdmin):
    pass

class LinkAdmin(admin.ModelAdmin):
    pass

#将模型注册到admin中
admin.site.register(User)
admin.site.register(Tag)
admin.site.register(Category)
admin.site.register(Article,ArticleAdmin)
admin.site.register(Comment)
admin.site.register(Link)
admin.site.register(Ad)



