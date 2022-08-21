import hashlib
import os

from django.db import models
from django.contrib.auth.models import AbstractUser
from application import dispatch
from backend.utils.models import CoreModel, table_prefix

# Create your models here.
STATUS_CHOICES = (
    (0, "禁用"),
    (1, "启用"),
)

class StudentInfo(CoreModel,AbstractUser):
    username = models.CharField(max_length=150, unique=True, db_index=True, verbose_name="用户账号", help_text="用户账号")
    email = models.EmailField(max_length=255, verbose_name="邮箱", null=True, blank=True, help_text="邮箱")
    mobile = models.CharField(max_length=255, verbose_name="电话", null=True, blank=True, help_text="电话")
    avatar = models.CharField(max_length=255, verbose_name="头像", null=True, blank=True, help_text="头像")
    name = models.CharField(max_length=40, verbose_name="姓名", help_text="姓名")
    address == models.CharField(max_length=400, verbose_name="家庭地址", null=True, blank=True, help_text="家庭住址")
    is_keypeople = models.BooleanField(default=False, verbose_name="是否为关键人", help_text="是否为关键人")
    GENDER_CHOICES = (
        (0, "未知"),
        (1, "男"),
        (2, "女"),
    )
    gender = models.IntegerField(
        choices=GENDER_CHOICES, default=0, verbose_name="性别", null=True, blank=True, help_text="性别"
    )
    USER_TYPE = (
        (0, "用户"),
        (1, "管理员"),
    )
    user_type = models.IntegerField(
        choices=USER_TYPE, default=0, verbose_name="用户类型", null=True, blank=True, help_text="用户类型"
    )
    post = models.ManyToManyField(to="Post", verbose_name="关联岗位", db_constraint=False, help_text="关联岗位")
    role = models.ManyToManyField(to="Role", verbose_name="关联角色", db_constraint=False, help_text="关联角色")
    dept = models.ForeignKey(
        to="Dept",verbose_name="所属班组",on_delete=models.PROTECT,db_constraint=False,null=True,blank=True,help_text="关联班组"
    )
    workshop = models.ForeignKey(
        to="Workshop",verbose_name="所属车间",on_delete=models.PROTECT,db_constraint=False,null=True,blank=True,help_text="关联车间"
    )
    railway_sections = models.ForeignKey(
        to="Railway_sections",verbose_name="所属站段",on_delete=models.PROTECT,db_constraint=False,null=True,blank=True,help_text="关联站段"
    )

    def set_password(self, raw_password):
        super().set_password(hashlib.md5(raw_password.encode(encoding="UTF-8")).hexdigest())

    class Meta:
        db_table = table_prefix + "system_users"
        verbose_name = "用户表"
        verbose_name_plural = verbose_name
        ordering = ("-create_datetime",)

class Post(CoreModel):
    name = models.CharField(null=False, max_length=64, verbose_name="岗位名称", help_text="岗位名称")
    code = models.CharField(max_length=32, verbose_name="岗位编号", help_text="岗位编号")
    sort = models.IntegerField(default=1, verbose_name="岗位顺序", help_text="岗位顺序")
    STATUS_CHOICES = (
        (0, "离职"),
        (1, "在职"),
    )
    status = models.IntegerField(choices=STATUS_CHOICES, default=1, verbose_name="岗位状态", help_text="岗位状态")

    class Meta:
        db_table = table_prefix + "system_post"
        verbose_name = "岗位表"
        verbose_name_plural = verbose_name
        ordering = ("sort",)


class Role(CoreModel):
    name = models.CharField(max_length=64, verbose_name="角色名称", help_text="角色名称")
    key = models.CharField(max_length=64, unique=True, verbose_name="权限字符", help_text="权限字符")
    sort = models.IntegerField(default=1, verbose_name="角色顺序", help_text="角色顺序")
    status = models.BooleanField(default=True, verbose_name="角色状态", help_text="角色状态")
    admin = models.BooleanField(default=False, verbose_name="是否为admin", help_text="是否为admin")
    DATASCOPE_CHOICES = (
        (0, "仅本人数据权限"),
        (1, "本部门及以下数据权限"),
        (2, "本部门数据权限"),
        (3, "全部数据权限"),
        (4, "自定数据权限"),
    )
    data_range = models.IntegerField(default=0, choices=DATASCOPE_CHOICES, verbose_name="数据权限范围", help_text="数据权限范围")
    remark = models.TextField(verbose_name="备注", help_text="备注", null=True, blank=True)
    dept = models.ManyToManyField(to="Dept", verbose_name="数据权限-关联班组", db_constraint=False, help_text="数据权限-关联班组")
    menu = models.ManyToManyField(to="Menu", verbose_name="关联菜单", db_constraint=False, help_text="关联菜单")
    permission = models.ManyToManyField(
        to="MenuButton", verbose_name="关联菜单的接口按钮", db_constraint=False, help_text="关联菜单的接口按钮"
    )

    class Meta:
        db_table = table_prefix + "system_role"
        verbose_name = "角色表"
        verbose_name_plural = verbose_name
        ordering = ("sort",)


class Dept(CoreModel):
    name = models.CharField(max_length=64, verbose_name="班组名称", help_text="班组名称")
    sort = models.IntegerField(default=1, verbose_name="显示排序", help_text="显示排序")
    owner = models.CharField(max_length=32, verbose_name="负责人", null=True, blank=True, help_text="负责人")
    phone = models.CharField(max_length=32, verbose_name="联系电话", null=True, blank=True, help_text="联系电话")
    email = models.EmailField(max_length=32, verbose_name="邮箱", null=True, blank=True, help_text="邮箱")
    status = models.BooleanField(default=True, verbose_name="班组状态", null=True, blank=True, help_text="班组状态")
    parent = models.ForeignKey(
        to="Dept",
        on_delete=models.CASCADE,
        default=None,
        verbose_name="上级班组",
        db_constraint=False,
        null=True,
        blank=True,
        help_text="上级班组",
    )

    class Meta:
        db_table = table_prefix + "system_dept"
        verbose_name = "班组表"
        verbose_name_plural = verbose_name
        ordering = ("sort",)


class Workshop(CoreModel):
    name = models.CharField(max_length=64, verbose_name="车间名称", help_text="车间名称")
    sort = models.IntegerField(default=1, verbose_name="显示排序", help_text="显示排序")
    owner = models.CharField(max_length=32, verbose_name="负责人", null=True, blank=True, help_text="负责人")
    phone = models.CharField(max_length=32, verbose_name="联系电话", null=True, blank=True, help_text="联系电话")
    email = models.EmailField(max_length=32, verbose_name="邮箱", null=True, blank=True, help_text="邮箱")
    status = models.BooleanField(default=True, verbose_name="车间状态", null=True, blank=True, help_text="车间状态")
    parent = models.ForeignKey(
        to="Workshop",
        on_delete=models.CASCADE,
        default=None,
        verbose_name="上级车间",
        db_constraint=False,
        null=True,
        blank=True,
        help_text="上级车间",
    )

    class Meta:
        db_table = table_prefix + "system_workshopt"
        verbose_name = "车间表"
        verbose_name_plural = verbose_name
        ordering = ("sort",)

class Railway_sections(CoreModel):
    name = models.CharField(max_length=64, verbose_name="站段名称", help_text="站段名称")
    sort = models.IntegerField(default=1, verbose_name="显示排序", help_text="显示排序")
    owner = models.CharField(max_length=32, verbose_name="负责人", null=True, blank=True, help_text="负责人")
    phone = models.CharField(max_length=32, verbose_name="联系电话", null=True, blank=True, help_text="联系电话")
    email = models.EmailField(max_length=32, verbose_name="邮箱", null=True, blank=True, help_text="邮箱")
    status = models.BooleanField(default=True, verbose_name="站段状态", null=True, blank=True, help_text="站段状态")
    parent = models.ForeignKey(
        to="Workshop",
        on_delete=models.CASCADE,
        default=None,
        verbose_name="上级站段",
        db_constraint=False,
        null=True,
        blank=True,
        help_text="上级站段",
    )

    class Meta:
        db_table = table_prefix + "system_railway_sections"
        verbose_name = "站段表"
        verbose_name_plural = verbose_name
        ordering = ("sort",)