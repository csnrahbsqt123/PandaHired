from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.
from apps.apply.utils.baseModel import BaseModel


class UserProfile(AbstractUser):
    """
    用户表
    """
    head = models.ImageField(verbose_name='用户头像',
                             upload_to='head/%Y/%m',
                             default='user/201809/23/tx1.png',
                             )
    nick_name = models.CharField(max_length=50, verbose_name="昵称")
    openid = models.CharField(max_length=32, null=True, blank=True)
    session_key = models.CharField(max_length=64, null=True, blank=True)

    class Meta:
        verbose_name = "用户信息"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.username


class PositionType(models.Model):
    job_type = models.CharField(max_length=32, blank=True, null=True)

    class Meta:
        verbose_name = "职位类型表"
        db_table = 'position_type'

    def __str__(self):
        return self.job_type


class Position(models.Model):
    """
    职位表
    """
    job_name = models.CharField(max_length=32, blank=True, null=True)
    type=models.ForeignKey(PositionType, on_delete=models.CASCADE, blank=True, null=True)
    class Meta:
        verbose_name = "职位表"
        db_table = 'position'

    def __str__(self):
        return self.job_name


class Resume(BaseModel):
    """
    简历信息表
    """
    real_name = models.CharField(max_length=16, verbose_name="真实姓名")
    gender = models.CharField(max_length=6, choices=(("male", "男"), ("female", "女")), default="female")
    birthday = models.DateField(verbose_name="生日", null=True, blank=True)
    city = models.CharField(max_length=16, default="")
    mobile = models.CharField(max_length=11, null=True, blank=True, unique=True)
    wx_num = models.CharField(max_length=32, null=True, blank=True, unique=True, verbose_name="微信号")
    cur_status = models.CharField(max_length=32, null=True, blank=True, unique=True, verbose_name="当前身份")
    entry_time = models.DateField(blank=True, null=True, verbose_name="入行时间")
    position = models.ForeignKey(Position, on_delete=models.CASCADE, blank=True, null=True)
    pro_certificate = models.ImageField(verbose_name='从业证书',
                                        upload_to='pro/%Y/%m',
                                        default='pro/201809/23/tx1.png',
                                        )

    id_verify = models.ImageField(verbose_name='身份证',
                                  upload_to='id/%Y/%m',
                                  default='id/201809/23/tx1.png',
                                  )
    describe = models.TextField(blank=True, null=True, verbose_name="自我介绍")
    hobby = models.TextField(blank=True, null=True, verbose_name="兴趣爱好")
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, blank=True, null=True)


    class Meta:
        verbose_name = "简历表"
        db_table = 'resume'


class SkillLabel(models.Model):
    skill_name = models.CharField(max_length=16, blank=True, null=True)
    position = models.ForeignKey(Position, on_delete=models.CASCADE, blank=True, null=True)
    # resume = models.ManyToManyField(to='Resume', through='Skill2Resume', through_fields=('resume', 'skill'))
    class Meta:
        verbose_name = "技能标签"
        db_table = 'skill_label'


class Skill2Resume(models.Model):
    """
    技能标签与简历关联表
    """
    skill = models.ForeignKey('SkillLabel', on_delete=models.CASCADE, blank=True, null=True)
    resume = models.ForeignKey('Resume', on_delete=models.CASCADE, blank=True, null=True)

    class Meta:
        db_table = 'skill_resume'


class WorkExperience(BaseModel):
    """
    工作经历表
    """
    company_name = models.CharField(max_length=32, blank=True, null=True, verbose_name="公司名称")
    position = models.ForeignKey(Position, on_delete=models.CASCADE, blank=True, null=True)
    entry_time = models.DateField(blank=True, null=True, verbose_name="入职时间")
    resignation_time = models.DateField(blank=True, null=True, verbose_name="离职时间")
    job_content = models.TextField(max_length=128, blank=True, null=True, verbose_name="工作内容")
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, blank=True, null=True)

    resume = models.ForeignKey(Resume, on_delete=models.CASCADE, blank=True, null=True)

    class Meta:
        verbose_name = "工作经历"
        db_table = 'work_experience'


class EducationExperience(BaseModel):
    """
    教育经历表
    """
    school_name = models.CharField(max_length=32, blank=True, null=True, verbose_name="学校名称")
    education = models.CharField(max_length=16, blank=True, null=True, verbose_name="学历")
    major = models.CharField(max_length=16, blank=True, null=True, verbose_name="专业")
    entry_time = models.DateField(blank=True, null=True, verbose_name="入学时间")
    graduate_time = models.DateField(blank=True, null=True, verbose_name="毕业时间")
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, blank=True, null=True)

    resume = models.ForeignKey(Resume, on_delete=models.CASCADE, blank=True, null=True)

    class Meta:
        verbose_name = "教育经历"
        db_table = 'education_experience'


class StoreAuthentication(BaseModel):
    """
    店铺认证表
    """
    is_verify = models.BooleanField(verbose_name="是否审核",
                                    default=False,
                                    )
    company_name = models.CharField(max_length=32, blank=True, null=True)
    open_time = models.DateField(blank=True, null=True)
    addr = models.CharField(max_length=32, blank=True, null=True)
    shop_pic = models.ImageField(verbose_name='店铺照片',
                                 upload_to='shop/%Y/%m',
                                 default='shop/201809/23/tx1.png',
                                 )
    business_licens = models.ImageField(verbose_name='营业执照',
                                        upload_to='business/%Y/%m',
                                        default='business/201809/23/tx1.png',
                                        )
    name = models.CharField(max_length=8, blank=True, null=True)
    sex = models.CharField(max_length=2, blank=True, null=True)
    birthday = models.DateField(blank=True, null=True)
    entry_time = models.DateField(blank=True, null=True)
    id_verify = models.ImageField(verbose_name='身份证',
                                  upload_to='id/%Y/%m',
                                  default='id/201809/23/tx1.png',
                                  )
    wx = models.CharField(max_length=16, blank=True, null=True)
    phone = models.CharField(max_length=16, blank=True, null=True)
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, blank=True, null=True)

    class Meta:
        verbose_name = "店铺认证"
        db_table = 'store_authentication'


class CompanyHring(BaseModel):
    """
    岗位信息表
    """
    job = models.ForeignKey(Position, on_delete=models.CASCADE, blank=True, null=True)
    company = models.ForeignKey(StoreAuthentication, on_delete=models.CASCADE, blank=True, null=True)
    job_name = models.CharField(max_length=16, blank=True, null=True)
    salary_range = models.CharField(max_length=16, blank=True, null=True)
    city = models.CharField(max_length=16, blank=True, null=True)
    scope_commission = models.CharField(max_length=16, blank=True, null=True)
    work_des = models.TextField(blank=True, null=True)
    nature = models.CharField(max_length=32, blank=True, null=True)
    work_nature = models.CharField(max_length=32, blank=True, null=True)
    age = models.CharField(max_length=8, blank=True, null=True)
    sex = models.CharField(max_length=8, blank=True, null=True)
    experience = models.CharField(max_length=8, blank=True, null=True)
    certificate = models.CharField(max_length=32, blank=True, null=True)
    education = models.CharField(max_length=8, blank=True, null=True)
    user = models.CharField(max_length=8, blank=True, null=True)
    phone = models.CharField(max_length=16, blank=True, null=True)
    is_call = models.BooleanField(verbose_name="是否允许打电话",
                                  default=False,
                                  )
    status = models.CharField(max_length=6, choices=(("on", "招聘中"), ("stop", "暂停招聘"), ("full", "招满")), default="on")
    # resume = models.ManyToManyField(to='Resume', through='Position2Resume', through_fields=('resume', 'position'))

    class Meta:
        verbose_name = "岗位信息"
        db_table = 'company_hring'


#
class Position2Resume(models.Model):
    """
    职位与简历多对多关系
    """
    position = models.ForeignKey(to="CompanyHring", on_delete=models.CASCADE, blank=True, null=True,to_field='id')
    resume = models.ForeignKey(to="Resume", on_delete=models.CASCADE, blank=True, null=True,to_field='id')

    class Meta:
        db_table = 'position_resume'


class User2Company(models.Model):
    """
    职位信息收藏
    """
    Position = models.ForeignKey('CompanyHring', on_delete=models.CASCADE, blank=True, null=True)
    user = models.ForeignKey('UserProfile', on_delete=models.CASCADE, blank=True, null=True)

    class Meta:
        db_table = 'position_user'


class Resume2Store(models.Model):
    """
    简历收藏
    """
    store = models.ForeignKey('StoreAuthentication', on_delete=models.CASCADE, blank=True, null=True)
    resume = models.ForeignKey('Resume', on_delete=models.CASCADE, blank=True, null=True)

    class Meta:
        db_table = 'store_resume'
