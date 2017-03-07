# coding: utf-8
import logging
from django.shortcuts import render,redirect,HttpResponse
from django.conf import settings  #全局变量设置导入
from bblog.models import *
from django.core.paginator import Paginator,InvalidPage,EmptyPage,PageNotAnInteger
from django.db.models import Count
from forms import *
from django.contrib.auth import login,logout,authenticate  #auth模块中权限管理
from django.contrib.auth.hashers import make_password


# view模块写入日志
logger = logging.getLogger('bblog.views')

# 全局变量设置
def global_setting(request):
    # 文章归档信息
    archive_list = Article.objects.distinct_date()
    # 文章分类信息
    category_list = Category.objects.all()[:6]
    # 广告信息获得
    ad_list = Ad.objects.all()
    #友情连接
    link_list = Link.objects.all()
    #标签云
    tag_list = Tag.objects.all()[:8]
    #浏览排行
    click_count_list =  Article.objects.all().order_by('-click_count')[:5]
    #评论排行
    comment_count_list = Comment.objects.values('article').annotate(comment_count=Count('article')).order_by('-comment_count')
    article_comment_list = [Article.objects.get(pk=comment['article']) for comment in comment_count_list]
    #站长推荐
    recommend_list = Article.objects.all().order_by('-is_recommend')[:5]
    return {
    'ad_list' : ad_list,
    'tag_list' : tag_list,
    'recommend_list' : recommend_list,
    'click_count_list' : click_count_list,
    'link_list' : link_list,
    'article_comment_list' : article_comment_list,
    'archive_list': archive_list,
    'category_list': category_list,
    'SITE_URL' :settings.SITE_URL ,
    'SITE_NAME' : settings.SITE_NAME,
    'SITE_DESC' : settings.SITE_DESC,
    'WEIBO_SINA' : settings.WEIBO_SINA,
    'WEIBO_TENCENT' : settings.WEIBO_TENCENT,
    'PRO_RSS' : settings.PRO_RSS,
    'PRO_EMAIL' : settings.PRO_EMAIL
    }

# Create your views here.
def index(request):
    try:
        #文章信息获取
        article_list = Article.objects.all()
        article_list = getPage(request,article_list)

        #文章归档信息
            # 1、先要去获取到文章中有的 年份-月份  2015/06文章归档
            # 使用values和distinct去掉重复数据（不可行）
            # 直接执行原生sql呢？（不推荐）
            #（推荐方法）自定义文章Manger管理器：


    except Exception as e:
        logger.error(e)
    return render(request, 'index.html', locals())

# 文章归档
def archive(request):
    try:
        # 获取客户端提交信息
        year = request.GET.get('year',None)
        month = request.GET.get('month',None)
        # date_publish__icontains 对发布时间进行（忽略大小写）模糊查询
        article_list = Article.objects.filter(date_publish__icontains=year+'-'+month)
        article_list = getPage(request,article_list)
    except Exception as e:
        logger.error(e)
    return render(request, 'archive.html', locals())

#分页类
def getPage(request,article_list):
    # article_list = Article.objects.all()
    paginator = Paginator(article_list, 3)
    try:
        page = int(request.GET.get('page', 1))
        article_list = paginator.page(page)
    except(InvalidPage, EmptyPage, PageNotAnInteger):
        article_list = paginator.page(1)
    return article_list

# 文章详情
def article(request):
    try:
        # 获取文章id
        id = request.GET.get('id', None)
        try:
            # 获取文章信息
            article = Article.objects.get(pk=id)
        except Article.DoesNotExist:
            return render(request, 'failure.html', {'reason': '没有找到对应的文章'})

        # 获取表单信息,is_authenticated判断是否登陆，初始化一些表单值，如果没有登陆则只初始化article隐藏文本元素
        comment_form = CommentForm({'author': request.user.username,
                                    'email':request.user.email,
                                    'url':request.user.url,
                                    'article':id} if request.user.is_authenticated() else {'article':id})


        #获取评论的信息
        comments = Comment.objects.filter(article=article).order_by('id')
        # print comments
        comment_list = []

        for comment in comments:
            for item in comment_list:
                if not hasattr(item,'children_comment'):
                    setattr(item,'children_comment',[])
                if comment.pid == item:
                    item.children_comment.append(comment)
                    break
            if comment.pid is None:
                comment_list.append(comment)

    except Exception as e:
        print e
        logger.error(e)
    # print comment_list
    return render(request, 'article.html', locals())


# 提交评论，
# is_valid()方法对提交信息，进行服务端验证
def comment_post(request):
    try:
        comment_form =CommentForm(request.POST)
        if comment_form.is_valid():
            comment = Comment.objects.create(username=comment_form.cleaned_data["author"],
                                             ename=comment_form.cleaned_data["email"],
                                             url=comment_form.cleaned_data["url"],
                                             context=comment_form.cleaned_data["comment"],
                                             article_id=comment_form.cleaned_data["article"],
                                             user=request.user if request.user.is_authenticated() else None)
            comment.save()
            print comment
        else:
            return render(request,'failure.html',{'reason': comment_form.errors})
    except Exception as e:
        logger.error(e)
    return redirect(request.META['HTTP_REFERER'])

# 登陆模块
def do_login(request):
    try:
        if request.method == 'POST':  # 如果表单被提交
            login_form = LoginForm(request.POST) #获取Post表单数据
            if login_form.is_valid():
                username = login_form.cleaned_data['username']
                password = login_form.cleaned_data['password']
                user = authenticate(username=username,password=password)
                if user is not None:
                    user.backend = 'django.contrib.auth.backends.ModelBackend' #指定默认登陆方式
                    login(request,user)
                else:
                    return render(request,'failure.html',{'reason': '登录验证失败'})
                return redirect(request.POST.get('source_url'))
            else:
                return render(request,'failure.html', {'reason': login_form.errors})
        else:
            login_form = LoginForm() #如果是get提交则为创建一个表单页
    except Exception as e:
        logger.error(e)
    return render(request,'login.html',locals())

# 注销
def do_logout(request):
    try:
        logout(request)
    except Exception as e:
        print e
        logger.error(e)
    return redirect(request.META['HTTP_REFERER'])

# 注册
def do_reg(request):
    try:
        if request.method == 'POST':
            reg_form = RegForm(request.POST)
            if reg_form.is_valid():
                # 注册
                user = User.objects.create(username=reg_form.cleaned_data["username"],
                                    email=reg_form.cleaned_data["email"],
                                    url=reg_form.cleaned_data["url"],
                                    password=make_password(reg_form.cleaned_data["password"]),)
                user.save()

                # 登录
                user.backend = 'django.contrib.auth.backends.ModelBackend' # 指定默认的登录验证方式
                login(request, user)
                return redirect(request.POST.get('source_url'))
            else:
                return render(request, 'failure.html', {'reason': reg_form.errors})
        else:
            reg_form = RegForm()
    except Exception as e:
        logger.error(e)
    return render(request, 'reg.html', locals())

