# coding: utf-8

from django.core.context_processors import csrf
from django.shortcuts import render_to_response
from django.http import HttpResponseNotFound
from main.models import *

def index(request):
    nav_top = Nav_top.objects.all()
    nav_lf = Nav_lf.objects.all()
    pic = Pic.objects.all().order_by('-id')[:5]
    art = [Article.objects.filter(bid = 1).order_by('-id')[:7], \
           Article.objects.filter(bid = 2).order_by('-id')[:5], \
           Article.objects.filter(bid = 3).order_by('-id')[:10], \
           Article.objects.filter(bid = 4).order_by('-id')[:7]]
    c = locals()
    c.update(csrf(request))
    return render_to_response('main/index.html', c)


def list(request,id):
    nav_top = Nav_top.objects.all()
    nav_lf = Nav_lf.objects.all()
    try:
        bname = Block.objects.get(id = id).name
    except:
        return HttpResponseNotFound('<h1>Page not found</h1>')
    article = Article.objects.filter(bid = id).order_by('-id')[:22]
    c = locals()
    c.update(csrf(request))
    return render_to_response('main/list.html', c)


def article(request,id):
    nav_top = Nav_top.objects.all()
    nav_lf = Nav_lf.objects.all()
    try:
        art = Article.objects.get(id = id)
        bname = Block.objects.get(id = art.bid ).name
    except:
        return HttpResponseNotFound('<h1>Page not found</h1>')
    c = locals()
    c.update(csrf(request))
    return render_to_response('main/article.html', c)

def introduce(request):
    nav_top = Nav_top.objects.all()
    nav_lf = Nav_lf.objects.all()
    bname = '学院概况'
    art = Article.objects.filter(bid = 0)[0]
    c = locals()
    c.update(csrf(request))
    return render_to_response('main/template.html', c)


def teacherls(request):
    nav_top = Nav_top.objects.all()
    nav_lf = Nav_lf.objects.all()
    bname = '师资力量'
    lab = Lab.objects.all()
    c = locals()
    c.update(csrf(request))
    return render_to_response('main/teachers.html', c)


def teacherdetail(request,id):
    nav_top = Nav_top.objects.all()
    nav_lf = Nav_lf.objects.all()
    bname = '导师风采'
    try:
        tea = Teacher.objects.get(id = id)
    except:
        return HttpResponseNotFound('<h1>Page not found</h1>')
    c = locals()
    c.update(csrf(request))
    return render_to_response('main/teacherdetail.html', c)
