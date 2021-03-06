from django.db import models

class Nav_top(models.Model):
    id = models.AutoField(primary_key = True)
    title = models.CharField(max_length = 20)
    link = models.CharField(max_length = 100, default = '#')
    priority = models.IntegerField()
    state = models.IntegerField(default = 1)

    class Meta:
        db_table = 'nav_top'


class Nav_lf(models.Model):
    id = models.AutoField(primary_key = True)
    title = models.CharField(max_length = 20)
    link = models.CharField(max_length = 100, default = '#')
    priority = models.IntegerField()
    state = models.IntegerField(default = 1)

    class Meta:
        db_table = 'nav_lf'


class Pic(models.Model):
    id = models.AutoField(primary_key = True)
    title = models.CharField(max_length = 20)
    link = models.CharField(max_length = 100, default = '#')
    src = models.CharField(max_length = 100)
    state = models.IntegerField(default = 1)
    class Meta:
        db_table = 'picture'


class Block(models.Model):
    id = models.AutoField(primary_key = True)
    name = models.CharField(max_length = 10)
    type = models.IntegerField()
    class Meta:
        db_table = 'block'


class Article(models.Model):
    id = models.AutoField(primary_key = True)
    bid = models.IntegerField()
    title = models.CharField(max_length = 100)
    author = models.CharField(max_length = 15)
    content = models.TextField()
    time = models.DateTimeField()
    type = models.CharField(max_length = 8)
    state = models.IntegerField(default = 1)

    def link(self):
        return '/art-%d.html' % self.id

    class Meta:
        db_table = 'article'


class Lab(models.Model):
    id = models.AutoField(primary_key = True)
    name = models.CharField(max_length = 20)
    state = models.IntegerField(default = 1)

    def teacher(self):
        return Teacher.objects.filter(labid = self.id, state = 1).order_by("name")

    class Meta:
        db_table = 'lab'


class Teacher(models.Model):
    id = models.AutoField(primary_key = True)
    name = models.CharField(max_length = 10)
    labid = models.IntegerField()
    password = models.CharField(max_length = 50, default = '96E79218965EB72C92A549DD5A330112')
    photo = models.CharField(max_length = 50)
    introduce = models.TextField(default = '<ul><li>&nbsp;</li><li>&nbsp;</li></ul>')
    experience = models.TextField(default = '<ul><li>&nbsp;</li><li>&nbsp;</li></ul>')
    course = models.TextField(default = '<ul><li>&nbsp;</li><li>&nbsp;</li></ul>')
    research = models.TextField(default = '<ul><li>&nbsp;</li><li>&nbsp;</li></ul>')
    article = models.TextField(default = '<ul><li>&nbsp;</li><li>&nbsp;</li></ul>')
    project = models.TextField(default = '<ul><li>&nbsp;</li><li>&nbsp;</li></ul>')
    achievement = models.TextField(default = '<ul><li>&nbsp;</li><li>&nbsp;</li></ul>')
    patent = models.TextField(default = '<ul><li>&nbsp;</li><li>&nbsp;</li></ul>')
    union = models.TextField(default = '<ul><li>&nbsp;</li><li>&nbsp;</li></ul>')
    student = models.TextField(default = '<ul><li>&nbsp;</li><li>&nbsp;</li></ul>')
    state = models.IntegerField(default = 1)

    def link(self):
        return '/tea-%d.html' % self.id

    def lab(self):
        return Lab.objects.get(id = self.labid).name

    class Meta:
        db_table = 'teacher'


class User(models.Model):
    id = models.AutoField(primary_key = True)
    name = models.CharField(max_length = 15)
    password = models.CharField(max_length = 50, default = '96E79218965EB72C92A549DD5A330112')
    type = models.CharField(max_length = 10)

    class Meta:
        db_table = 'user'


class Log(models.Model):
    id = models.AutoField(primary_key = True)
    uid = models.IntegerField()
    log = models.TextField()
    time = models.DateTimeField()
    ip = models.IPAddressField()
    
    class Meta:
        db_table = 'log'
