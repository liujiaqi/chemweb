# coding: utf-8

from django.core.context_processors import csrf
from django.shortcuts import render_to_response
from django.http import HttpResponseNotFound
from main.models import *
from main.cms import divpage

def index(request):
    nav_top = Nav_top.objects.all()
    nav_lf = Nav_lf.objects.all()
    pic = Pic.objects.filter(state = 1).order_by('-id')[:5]
    art = [Article.objects.filter(bid = 1, state = 1).order_by('-id')[:7], \
           Article.objects.filter(bid = 2, state = 1).order_by('-id')[:5], \
           Article.objects.filter(bid = 3, state = 1).order_by('-id')[:10], \
           Article.objects.filter(bid = 4, state = 1).order_by('-id')[:7]]
    c = locals()
    c.update(csrf(request))
    return render_to_response('main/index.html', c)


def list(request, id):
    nav_top = Nav_top.objects.all()
    nav_lf = Nav_lf.objects.all()
    try:
        bname = Block.objects.get(id = id).name
    except:
        return HttpResponseNotFound('<h1>Page not found</h1>')

    try:
        curpage = int(request.GET.get('page'))
    except:
        curpage = 1

    page = divpage(Article.objects.filter(bid = id, state = 1).count(), 20, curpage)

    article = Article.objects.filter(bid = id, state = 1).order_by('-id')[(page['page']-1)*20:page['page']*20]
    c = locals()
    c.update(csrf(request))
    return render_to_response('main/list.html', c)


def article(request, id):
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

def introduce(request, id):
    nav_top = Nav_top.objects.all()
    nav_lf = []
    for a in Article.objects.filter(bid = 5, state = 1).order_by('id'):
        nav_lf.append({"title":a.title, "link":"/intro-%d.html" % a.id})
    try:
        art = Article.objects.get(id = id)
    except:
        art = {}
    bname = art.title
    c = locals()
    c.update(csrf(request))
    return render_to_response('main/template.html', c)

def institute(request, id):
    nav_top = Nav_top.objects.all()
    nav_lf = []
    for b in Block.objects.filter(type = 2).order_by('id'):
        nav_lf.append({"title":b.name, "link":"/inst-%d.html" % b.id})
    try:
        block = Block.objects.get(id = id)
    except:
        block = {}
    bname = block.name

    try:
        curpage = int(request.GET.get('page'))
    except:
        curpage = 1

    page = divpage(Article.objects.filter(bid = id, state = 1).count(), 20, curpage)
    article = Article.objects.filter(bid = id, state = 1).order_by('-id')[(page['page']-1)*20:page['page']*20]
    c = locals()
    c.update(csrf(request))
    return render_to_response('main/list.html', c)


def teacherls(request):
    nav_top = Nav_top.objects.all()
    nav_lf = Nav_lf.objects.all()
    bname = '师资力量'
    lab = Lab.objects.filter(state = 1)
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
