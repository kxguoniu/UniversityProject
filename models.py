from django.db import models

# Create your models here.
class Permission(models.Model):
    name = models.CharField(max_length=50, verbose_name=u"权限名")
    fun_name = models.CharField(max_length=50, verbose_name=u"函数名")
    class Meta:
        db_table = u"permission"

class Group(models.Model):
    name = models.CharField(max_length=50, verbose_name=u"用户组")
    permiss_list = models.CharField(max_length=100, verbose_name=u"权限列表")
    desc = models.CharField(max_length=50, verbose_name=u"备注")
    class Meta:
        db_table = u"group"

class Author(models.Model):
    name = models.CharField(max_length=50, verbose_name=u"姓名")
    passwd = models.CharField(max_length=300, verbose_name=u"密码")
    img = models.CharField(max_length=50, verbose_name=u"头像")
    age = models.PositiveIntegerField(default=0, verbose_name=u"年龄")
    group = models.ForeignKey(Group, on_delete=models.SET_NULL, blank=True, null=True, verbose_name=u"用户组")
    class Meta:
        db_table = u"author"

class Category(models.Model):
    name = models.CharField(max_length=20, verbose_name=u"名称")
    class Meta:
        db_table = u"category"

class Blog(models.Model):
    views = models.PositiveIntegerField(default=0, verbose_name=u"阅读量")
    title = models.CharField(max_length=70, verbose_name=u"标题")
    weight = models.PositiveIntegerField(default=1, verbose_name=u"权重")
    body = models.TextField(verbose_name=u"文章内容")
    html = models.TextField(verbose_name=u"HTML内容")
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

class Skynet(models.Model):
    min1 = models.FloatField(default=0, verbose_name=u"一分钟负载")
    min5 = models.FloatField(default=0, verbose_name=u"五分钟负载")
    min15 = models.FloatField(default=0, verbose_name=u"十五分钟负载")

    uscpu = models.FloatField(default=0, verbose_name=u"用户Cpu")
    sycpu = models.FloatField(default=0, verbose_name=u"系统Cpu")

    total = models.PositiveIntegerField(default=0, verbose_name=u"总内存")
    used = models.PositiveIntegerField(default=0, verbose_name=u"使用内存")
    free = models.PositiveIntegerField(default=0, verbose_name=u"空闲内存")

    netin = models.PositiveIntegerField(default=0, verbose_name=u"下载流量")
    netout = models.PositiveIntegerField(default=0, verbose_name=u"上传流量")

    create_time = models.DateTimeField(auto_now_add=True, verbose_name=u"创建时间")
    class Meta:
        db_table = u"skynet"

class Message(models.Model):
    fromaddr = models.CharField(max_length=100, verbose_name=u"发件人")
    toaddr = models.CharField(max_length=100, verbose_name=u"收件人")
    title = models.CharField(max_length=200, verbose_name=u"标题")
    content = models.CharField(max_length=300, verbose_name=u"内容")
    status = models.PositiveIntegerField(default=0, verbose_name=u"状态")
    create_time = models.DateTimeField(auto_now_add=True, verbose_name=u"创建时间")
    class Meta:
        db_table = u"message"


class VisitorCount(models.Model):
    time = models.DateField(auto_now_add=True, verbose_name=u"时间")
    sums = models.PositiveIntegerField(default=0, verbose_name=u"访问量")
    class Meta:
        db_table = u"visitor"


class Comment(models.Model):
    user = models.CharField(max_length=15, verbose_name=u"用户")
    img = models.CharField(max_length=50, verbose_name=u"头像")
    message = models.TextField(verbose_name=u"评论")
    create_time = models.DateTimeField(auto_now_add=True, verbose_name=u"创建时间")
    floor = models.PositiveIntegerField(default=0, verbose_name=u"楼层")
    blog = models.ForeignKey(Blog, verbose_name=u"博文id")
    class Meta:
        db_table = u"comment"

class Reply(models.Model):
    user = models.CharField(max_length=15, verbose_name=u"from")
    img = models.CharField(max_length=50, verbose_name=u"头像")
    message = models.TextField(verbose_name=u"回复")
    replyuser = models.CharField(max_length=15, verbose_name=u"to")
    create_time = models.DateTimeField(auto_now_add=True, verbose_name=u"创建时间")
    comment = models.ForeignKey(Comment, verbose_name=u"评论")
    class Meta:
        db_table = u"reply"

class TodoList(models.Model):
    title = models.CharField(max_length=100, verbose_name=u"事件")
    status = models.CharField(max_length=5, verbose_name=u"状态")
    class Meta:
        db_table = u"todolist"

