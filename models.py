from django.db import models

# Create your models here.
class Author(models.Model):
    name = models.CharField(max_length=50, verbose_name=u"姓名")
    age = models.PositiveIntegerField(default=0, verbose_name=u"年龄")
    class Meta:
        db_table = u"author"

class Category(models.Model):
    name = models.CharField(max_length=20, verbose_name=u"名称")
    class Meta:
        db_table = u"category"

class Blog(models.Model):
    views = models.PositiveIntegerField(default=0, verbose_name=u"阅读量")
    title = models.CharField(max_length=70, verbose_name=u"标题")
    body = models.TextField(verbose_name=u"文章内容")
    create_time = models.DateTimeField(auto_now_add=True, verbose_name=u"创建时间")
    change_time = models.DateTimeField(auto_now=True, verbose_name=u"修改时间")
    digested = models.CharField(max_length=200, verbose_name=u"文章摘要")
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, blank=True, null=True, verbose_name=u"文章分类")
    author = models.ForeignKey(Author, on_delete=models.SET_NULL, blank=True, null=True, verbose_name=u"作者")
    class Meta:
        db_table = u"blog"
        ordering = ['create_time']

class Tag(models.Model):
    name = models.CharField(max_length=15, verbose_name=u"名称")
    class Meta:
        db_table = u"tag"

class BlogTag(models.Model):
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE, verbose_name=u"博文")
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE, verbose_name=u"标签")
    class Meta:
        db_table = u"blogtag"
