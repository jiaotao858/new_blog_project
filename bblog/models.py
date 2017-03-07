# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import AbstractUser
from ckeditor.fields import RichTextField

# Create your models here.

# 用户模式
# 第一种：采用继承方式扩展用户信息（系系统采用）
# 第二种：关联的方式去扩展用户信息

class User(AbstractUser):
    avatar = models.ImageField(upload_to='avatar/%Y/%m',default='avatar/default.png',max_length=200,blank=True,null=True,verbose_name='用户头像')
    qq = models.CharField(max_length=20,blank=True,null=True,verbose_name='QQ号码')
    mobile = models.CharField(max_length=11,blank=True,null=True,unique=True,verbose_name='手机号码')
    url = models.URLField(max_length=100,blank=True,null=True,verbose_name='个人网页地址')

    class Meta:
        verbose_name = '用户'
        verbose_name_plural = verbose_name
        ordering = ['-id']

    def __unicode__(self):
        return self.username


#tag(标签)模型
class Tag(models.Model):
    name = models.CharField(max_length=30,verbose_name='标签名字')

    class Meta:
        verbose_name = '标签'
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.name

#文章分类模型
class Category(models.Model):
    name = models.CharField(max_length=30,verbose_name='文章名称')
    index = models.IntegerField(default=999,verbose_name='文章排序')

    class Meta:
        verbose_name = '分类'
        verbose_name_plural = verbose_name
        ordering = ['index','id']

    def __unicode__(self):
        return self.name

# 自定义一个文章类型管理器
# 1、增加一个数据处理的方法(本系统采用)
# 2、改变原有的queryset
class ArticleManager(models.Manager):
    def distinct_date(self):
        distinct_date_list = []
        date_list = self.values('date_publish')
        for date in date_list:
            date = date['date_publish'].strftime('%Y/%m文章存档')
            if date not in distinct_date_list:
                distinct_date_list.append(date)
        return distinct_date_list

# 文章模型
class Article(models.Model):
    title = models.CharField(max_length=50,verbose_name='文章标题')
    desc = models.CharField(max_length=50,verbose_name='文章描述')
    content = models.TextField(verbose_name='文章内容')
    click_count = models.IntegerField(default=0,verbose_name='点击量')
    is_recommend = models.BooleanField(default=False,verbose_name='是否推荐')
    date_publish = models.DateTimeField(auto_now_add=True,verbose_name='发布时间')
    user = models.ForeignKey(User,verbose_name='作者')
    category = models.ForeignKey(Category,verbose_name='文章分类')
    tag = models.ManyToManyField(Tag,verbose_name='标签')

    objects = ArticleManager()

    class Meta:
        verbose_name = '文章'
        verbose_name_plural = verbose_name
        ordering = ['-date_publish']

    def __unicode__(self):
        return self.title




# 评论模型
class Comment(models.Model):
    context = models.TextField(verbose_name='评论内容')
    username = models.CharField(max_length=30,blank=True,null=True,verbose_name='用户名')
    email = models.EmailField(max_length=50,blank=True,null=True,verbose_name='邮箱地址')
    url = models.URLField(max_length=100,blank=True,null=True,verbose_name='个人网页地址')
    date_publish = models.DateTimeField(auto_now_add=True,verbose_name='评论时间')
    user = models.ForeignKey(User,blank=True,null=True,verbose_name='用户')
    article = models.ForeignKey(Article,blank=True,null=True,verbose_name='文章')
    pid = models.ForeignKey('self',blank=True,null=True,verbose_name='父级评论')



    class Meta:
        verbose_name = '评论'
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.context

# 友情链接模型
class Link(models.Model):
    title = models.CharField(max_length=50,verbose_name='友情链接')
    description = models.CharField(max_length=200,verbose_name='网站描述')
    callback_url = models.URLField(verbose_name='url地址')
    date_publish = models.DateTimeField(auto_now_add=True,verbose_name='发布时间')
    index = models.IntegerField(default=999,verbose_name='排列顺序（从小到大）')

    class Meta:
        verbose_name = '友情链接'
        verbose_name_plural = verbose_name
        ordering = ['index','id']

    def __unicode__(self):
        return self.title

# 定义一个广告类型的管理器
class AdManager(models.Manager):
    def distinct_publish(self):
        distinct_publish_list = []
        date_publish = self.values('date_publish')
        for date in date_publish:
            date = date['date_publish'].strftime('%Y/%m')
            if date not in distinct_publish_list:
                distinct_publish_list.append(date)
        return distinct_publish_list

# 广告模型
class Ad(models.Model):
    title = models.CharField(max_length=50,verbose_name='广告标题')
    description = models.CharField(max_length=200,verbose_name='广告描述')
    image_url = models.ImageField(upload_to='ad/%Y/%m',verbose_name='图片路径')
    date_publish = models.DateTimeField(auto_now_add=True,verbose_name='发布时间')
    index = models.IntegerField(default=999,verbose_name='排列顺序（从小到大）')

    objects = AdManager()

    class Meta:
        verbose_name = '广告'
        verbose_name_plural = verbose_name
        ordering = ['index','id']

    def __unicode__(self):
        return self.title