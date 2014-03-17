# coding: utf-8

import re
import hashlib
import datetime
import string
from django.db.models import Q
from django.core.context_processors import csrf
from django.shortcuts import render_to_response
from django.http.response import HttpResponseRedirect
from django.http import HttpResponse
from main.models import *

phupload = 'D:/University/Program/chemical_school_website/chem/chem/main'

def getip(request):
    if request.META.has_key('HTTP_X_FORWARDED_FOR'):  
        return request.META['HTTP_X_FORWARDED_FOR']  
    else:  
        return request.META['REMOTE_ADDR']

def login(request):
    uname = request.POST.get('uname')
    passwd = hashlib.md5(request.POST.get('passwd')).hexdigest().upper()
    
    ip = getip(request)

    try:
        user = User.objects.get(name = uname)
    except:
        log("用户名错误",ip)
        return HttpResponse("用户名或密码错误")
        
    if passwd != user.password:
        log("密码错误", ip, user.id)
        return HttpResponse("用户名或密码错误")

    log("用户登录成功", ip, user.id)

    request.session['id'] = user.id
    request.session['ip'] = ip

    return HttpResponse("OK")


def logout(request):
    if 'id' in request.session:
        del request.session['id']
        del request.session['ip']

    return HttpResponseRedirect('/')

def cms(request, method = None, id = None):
    ip = getip(request)
    if not 'id' in request.session:
        return HttpResponseRedirect('/')
    try:
        user = User.objects.get(id = request.session['id'])
    except:
        log("越权访问cms",ip)
        return HttpResponseRedirect('/')

    if method == "chpwd":
        user.password = hashlib.md5(request.POST.get('passwd')).hexdigest().upper()
        user.save()
        log("管理员修改密码", ip, user.id)
        del request.session['id']
        return HttpResponse("OK")

    if method == "news":

        bls = []#用户可管理的板块
        bids = []#用户可管理的板块的id
        block = Block.objects.all();
        for bl in block:
            if str(bl.id) in user.type:
                bids.append(bl.id)
                bls.append(bl)
        if id != None:
                id = string.atoi(id)

        if request.POST.get('add'):
            if id != None:
                try:
                    block = Block.objects.get(id = id)
                    bname = u'%s - 发布消息' % block.name
                    c = locals()
                    c.update(csrf(request))
                    return render_to_response('main/cms_addart.html', c)
                except:
                    hint = "不存在要发布消息的板块"
                    log("请求不存在的板块id", ip, user.id)

        if request.POST.get('modify'):
            if id != None:
                try:
                    art = Article.objects.get(id = request.POST.get('aid'))
                    if art.bid != id:
                        log("!!非正常请求修改文章!!", ip, user.id)
                        return HttpResponseRedirect('news.html')
                    bname = '修改消息'
                    c = locals()
                    c.update(csrf(request))
                    return render_to_response('main/cms_modart.html', c)
                except:
                    hint = "不存在要修改的文章"
                    log("修改不存在的文章", ip, user.id)

        if request.POST.get('delete'):
            if id != None:
                try:
                    article = Article.objects.get(id = request.POST.get('aid'))
                    if article.bid != id:
                        log("!!非正常请求删除文章!!", ip, user.id)
                        return HttpResponseRedirect('news.html')
                    article.delete()
                    log("删除一篇文章", ip, user.id)
                    hint = "删除成功"
                except:
                    hint = "不存在要删除的文章"
                    log("删除不存在的文章", ip, user.id)

        if request.POST.get('add_art'):
            if id != None:
                if id == 4:
                    type = request.POST.get('type')
                else:
                    type = ''
                try:
                    block = Block.objects.get(id = id)
                    Article(bid = id, \
                            title = request.POST.get('title'), \
                            author = user.name, \
                            content = request.POST.get('content'), \
                            time = datetime.datetime.now(), \
                            type = type).save()
                    log("发布一条消息", ip, user.id)
                    bname = '消息管理'
                    hint = "发布成功"
                except:
                    hint = "不存在要发布消息的板块"
                    log("!!请求不存在的板块id1!!", ip, user.id)

        if request.POST.get('mod_art'):
            if id != None:
                if id == 4:
                    type = request.POST.get('type')
                else:
                    type = ''
                try:
                    article = Article.objects.get(id = request.POST.get('aid'))
                    if article.bid != id:
                        log("!!非正常请求修改文章!!", ip, user.id)
                        return HttpResponseRedirect('news.html')
                    article.title = request.POST.get('title')
                    article.author = user.name
                    article.content = request.POST.get('content')
                    article.time = datetime.datetime.now()
                    article.type = type
                    article.save()
                    log("修改一条消息", ip, user.id)
                    bname = '消息管理'
                    hint = "修改成功"
                except:
                    hint = "不存在要修改消息的板块"
                    log("!!请求不存在的板块id2!!", ip, user.id)

        bname = '消息管理'
        if id == None:
            q = Q()
            for bid in bids:
                q = q | Q(bid = bid)
            article = Article.objects.filter(q).order_by('-id')
        else:
            if id in bids:
                article = Article.objects.filter(bid = id).order_by('-id')
            else:
                return HttpResponseRedirect('/cms/news.html')
        c = locals()
        c.update( csrf(request))
        return render_to_response('main/cms_news.html', c)

    if method == "pics":
        bname = '图片管理'
        filehd = request.FILES.get('pic', None)
        if filehd:
            if filehd.size > 1000000:
                hint = '照片文件超过1MB'
            else:
                m = re.match(r'^.+\.(jpg|gif|png)$', filehd.name.lower())
                if m == None:
                    hint = '请上传一个图片文件'
                else:
                    photo_url = '/static/main/upload/%s.%s' % (datetime.datetime.now().strftime("%Y%m%d%H%M%S"), m.group(1))
                    target = open(phupload + photo_url,'wb+')
                    target.write(filehd.read())
                    target.close()
                    Pic(title = request.POST.get('title'), link = request.POST.get('link'), src = photo_url).save()
                    log("上传首页大图", ip, user.id)

        if request.POST.get('delete'):
            try:
                pic = Pic.objects.get(id = request.POST.get('delete'))
                pic.delete()
                log("删除一张图片", ip, user.id)
            except:
                log("删除的图片Id不存在", ip, user.id)
                hint = '不存在要删除的图片'

        pics = Pic.objects.all().order_by('-id')
        c = locals()
        c.update(csrf(request))
        return render_to_response('main/cms_pics.html', c)


    if method == "teas":
        bname = '教师管理'
        
        #添加研究所
        if request.POST.get('labs'):
            try:
                Lab.objects.get(name = request.POST.get('labs'))
                hint = "该研究所已存在"
            except:
                Lab(name = request.POST.get('labs')).save()
                log("添加研究所", ip, user.id)
                hint = "添加研究所成功"

        #删除研究所
        if request.POST.get('delab'):
            try:
                lab = Lab.objects.get(id = request.POST.get('lab'))
                lab.delete()
                log("删除研究所", ip, user.id)
                hint = "删除研究所成功"
            except:
                hint = "要删除的研究所不存在"

        #添加教师
        if request.POST.get('name'):
            try:
                Teacher.objects.get(name = request.POST.get('name'))
                hint = "该教师已存在"
            except:
                Teacher(name = request.POST.get('name'), labid =  request.POST.get('lab')).save()
                log("添加教师", ip, user.id)
                hint = "添加教师成功"

        #删除教师
        if request.POST.get('delete'):
            try:
                tea = Teacher.objects.get(id = request.POST.get('delete'))
                tea.delete()
                log("删除一名教师", ip, user.id)
                hint = '删除成功'
            except:
                hint = '不存在要删除的教师'

        #修改教师密码
        if request.POST.get('chpwd'):
            try:
                tea = Teacher.objects.get(id = request.POST.get('chpwd'))
                tea.password = hashlib.md5(request.POST.get('passwd')).hexdigest().upper()
                tea.save()
                log("修改教师密码", ip, user.id)
                hint = '密码修改成功'
            except:
                hint = '不存在要修改密码的教师'

        labs = Lab.objects.all()
        teacher = Teacher.objects.all()
        c = locals()
        c.update(csrf(request))
        return render_to_response('main/cms_teas.html', c)


    if method == "tlnk":
        if request.POST.get('title'):
            Nav_top(title = request.POST.get('title'), link = request.POST.get('link')).save()
            log("添加顶部链接", ip, user.id)
        elif request.POST.get('delete'):
            try:
                lnk = Nav_top.objects.get(id = request.POST.get('delete'))
                lnk.delete()
                log("删除一个顶部链接", ip, user.id)
                hint = '删除成功'
            except:
                hint = '不存在要删除的链接'

        bname = '顶部链接'
        link = Nav_top.objects.all()
        c = locals()
        c.update(csrf(request))
        return render_to_response('main/cms_link.html', c)


    if method == "lnav":
        if request.POST.get('title'):
            Nav_lf(title = request.POST.get('title'), link = request.POST.get('link')).save()
            log("添加顶部链接", ip, user.id)
        elif request.POST.get('delete'):
            try:
                lnk = Nav_lf.objects.get(id = request.POST.get('delete'))
                lnk.delete()
                log("删除一个顶部链接", ip, user.id)
                hint = '删除成功'
            except:
                hint = '不存在要删除的链接'
        bname = '左侧导航'
        link = Nav_lf.objects.all()
        c = locals()
        c.update(csrf(request))
        return render_to_response('main/cms_link.html', c)


    if method == "intro":
        if request.POST.get('content'):
            art = Article.objects.filter(bid = 0)[0]
            art.content = request.POST.get('content')
            art.save()
            return HttpResponseRedirect('/cms/')

        bname = '学院概况'
        art = Article.objects.filter(bid = 0)[0]
        c = locals()
        c.update(csrf(request))
        return render_to_response('main/cms_intro.html', c)

    #用户管理
    if method == "user":
        if request.POST.get('add'):
            if request.POST.get('name'):
                User(name = request.POST.get('name'), type = ''.join(request.POST.getlist('authority'))).save()
                log("添加用户", ip, user.id)
                hint = "添加成功"
            else:
                hint = "用户名不能为空"

        if request.POST.get('delete'):
            try:
                usr = User.objects.get(id = request.POST.get('id'))
                usr.delete()
                log("删除用户", ip, user.id)
                hint = "删除成功"
            except:
                hint = "不存在要删除的用户"

        if request.POST.get('modify'):
            try:
                usr = User.objects.get(id = request.POST.get('id'))
                usr.type = ''.join(request.POST.getlist('authority'))
                usr.save()
                log("修改用户权限", ip, user.id)
                hint = "修改成功"
            except:
                hint = "不存在要修改的用户"

        users = User.objects.all()
        bname = '后台用户管理'
        labs = Lab.objects.all()
        teacher = Teacher.objects.all()
        c = locals()
        c.update(csrf(request))
        return render_to_response('main/cms_user.html', c)

    bname = '欢迎使用山东大学化学与化工学院网站内容管理系统!'
    c = locals()
    c.update(csrf(request))
    return render_to_response('main/cms.html', c)

def teacheredit(request, id, method = None):
    ip = getip(request)

    if not request.POST.get('login'):
        if 'teaid' in request.session:
            #修改密码
            if method == "chpwd":
                try:
                    tea = Teacher.objects.get(id = request.session['teaid'])
                except:
                    return HttpResponse("不存在的id")#理论上不会发生
                tea.password = hashlib.md5(request.POST.get('passwd')).hexdigest().upper()
                tea.save()
                log("教师修改密码", ip, tea.id)
                del request.session['teaid']
                return HttpResponse("OK")

            #修改照片
            if method == "photo":
                filehd = request.FILES.get('photo', None)
                if filehd:
                    if filehd.size > 1000000:
                        return HttpResponse("<script>parent.photost('照片文件超过1MB','/');</script>")
                    m = re.match(r'^.+\.(jpg|gif|png)$', filehd.name.lower())
                    if m == None:
                        return HttpResponse("<script>parent.photost('请上传一个图片文件','/');</script>")
                    photo_url = '/static/main/upload/teacher/%s.%s' % (datetime.datetime.now().strftime("%Y%m%d%H%M%S"), m.group(1))
                    target = open(phupload + photo_url,'wb+')
                    target.write(filehd.read())
                    target.close()
                    try:
                        tea = Teacher.objects.get(id = request.session['teaid'])
                    except:
                        return HttpResponse("<script>parent.photost('不存在的id','/');</script>")
                    tea.photo = photo_url
                    tea.save()
                    log("教师修改照片", ip, tea.id)
                    return HttpResponse("<script>parent.photost('OK','%s');</script>" % photo_url)
                else:
                    return HttpResponse("<script>parent.photost('请选择一张您的照片','/');</script>")

            #修改介绍
            if method == "intro":
                try:
                    tea = Teacher.objects.get(id = request.session['teaid'])
                except:
                    return HttpResponseRedirect("/tea-%s.html" % id)
                tea.introduce = request.POST.get('introduce')
                tea.experience = request.POST.get('experience')
                tea.course = request.POST.get('course')
                tea.research = request.POST.get('research')
                tea.article = request.POST.get('article')
                tea.project = request.POST.get('project')
                tea.achievement = request.POST.get('achievement')
                tea.patent = request.POST.get('patent')
                tea.union = request.POST.get('union')
                tea.student = request.POST.get('student')
                tea.save()
                log("教师修改信息", ip, tea.id)
                del request.session['teaid']
                return HttpResponseRedirect("/tea-%s.html" % id)

            #教师登陆后
            nav_top = Nav_top.objects.all()
            nav_lf = Nav_lf.objects.all()
            bname = '导师风采'
            tea = Teacher.objects.get(id = id)
            c = locals()
            c.update(csrf(request))
            return render_to_response('main/teacheredit.html', c)
        else:
            return HttpResponseRedirect("/tea-%s.html" % id)

    #教师登录
    passwd = hashlib.md5(request.POST.get('passwd')).hexdigest().upper()
    try:
        teacher = Teacher.objects.get(id = id)
    except:
        return HttpResponse("教师id错误")

    if passwd != teacher.password:
        log("教师密码错误", ip, teacher.id)
        return HttpResponse("密码错误")

    log("教师登录成功", ip, teacher.id)

    request.session['teaid'] = teacher.id

    return HttpResponse("OK")


def log(log, ip, uid=0):
    Log(uid = uid,
        log = log,
        time = datetime.datetime.now(),
        ip = ip, ).save()
    return