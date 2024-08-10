import datetime
from django.utils import timezone
from django.db import models
from employee.managers import EmployeeManager
from phonenumber_field.modelfields import PhoneNumberField
from django.utils.translation import gettext as _
from django.contrib.auth.models import User
from leave.models import Leave

# Create your models here.
class Role(models.Model):
    name = models.CharField(max_length=125)
    description = models.CharField(max_length=125, null=True, blank=True)
    created = models.DateTimeField(verbose_name=_('Created'), auto_now_add=True)
    updated = models.DateTimeField(verbose_name=_('Updated'), default=timezone.now)

    class Meta:
        verbose_name = _('Role')
        verbose_name_plural = _('Roles')
        ordering = ['name', 'created']

    def __str__(self):
        return self.name

class Department(models.Model):
    name = models.CharField(max_length=125)
    description = models.CharField(max_length=125, null=True, blank=True)
    created = models.DateTimeField(verbose_name=_('Created'), auto_now_add=True)
    updated = models.DateTimeField(verbose_name=_('Updated'), default=timezone.now)


    class Meta:
        verbose_name = _('Department')
        verbose_name_plural = _('Departments')
        ordering = ['name', 'created']
    
    def __str__(self):
        return self.name

class Nationality(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=10, unique=True, null=True, blank=True)

    class Meta:
        verbose_name = _('Nationality')
        verbose_name_plural = _('Nationalities')
        ordering = ['name']

    def __str__(self):
        return self.name

class Employee(models.Model):
    MALE = 'male'
    FEMALE = 'female'
    OTHER = 'other'
    NOT_KNOWN = 'Not Known'

    GENDER = (
        (MALE, 'Male'),
        (FEMALE, 'Female'),
        (OTHER, 'Other'),
        (NOT_KNOWN, 'Not Known'),
    )

    MR = 'Mr'
    MRS = 'Mrs'
    MSS = 'Mss'
    DR = 'Dr'
    SIR = 'Sir'
    MADAM = 'Madam'

    TITLE = (
        (MR, 'Mr'),
        (MRS, 'Mrs'),
        (MSS, 'Mss'),
        (DR, 'Dr'),
        (SIR, 'Sir'),
        (MADAM, 'Madam'),
    )

    FULL_TIME = 'Full-Time'
    PART_TIME = 'Part-Time'
    CONTRACT = 'Contract'
    INTERN = 'Intern'

    EMPLOYEETYPE = (
        (FULL_TIME, 'Full-Time'),
        (PART_TIME, 'Part-Time'),
        (CONTRACT, 'Contract'),
        (INTERN, 'Intern'),
    )

    # PERSONAL DATA
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    image = models.FileField(_('Profile Image'), upload_to='profiles', default='default.png', blank=True, null=True, help_text='Upload image size less than 2.0MB')
    firstname = models.CharField(_('Firstname'), max_length=125)
    lastname = models.CharField(_('Lastname'), max_length=125)
    othername = models.CharField(_('Othername (optional)'), max_length=125, null=True, blank=True)
    birthday = models.DateField(_('Birthday'), default=datetime.date.today)
    department = models.ForeignKey(Department, verbose_name=_('Department'), on_delete=models.SET_NULL, null=True, default=None)
    role = models.ForeignKey(Role, verbose_name=_('Role'), on_delete=models.SET_NULL, null=True, default=None)
    startdate = models.DateField(_('Employement Date'), default=timezone.now, help_text='date of employment')
    employeetype = models.CharField(_('Employee Type'), max_length=15, default=FULL_TIME, choices=EMPLOYEETYPE)
    employeeid = models.CharField(_('Employee ID Number'), max_length=10, null=True, blank=True)
    dateissued = models.DateField(_('Date Issued'), default=timezone.now)
    # app related
    is_blocked = models.BooleanField(_('Is Blocked'), default=False)
    is_deleted = models.BooleanField(_('Is Deleted'), default=False)

    created = models.DateTimeField(verbose_name=_('Created'), auto_now_add=True, null=True)
    updated = models.DateTimeField(verbose_name=_('Updated'), default=timezone.now)

    # PLUG MANAGERS
    objects = EmployeeManager()

    class Meta:
        verbose_name = _('Employee')
        verbose_name_plural = _('Employees')
        ordering = ['-created']

    def __str__(self):
        return self.get_full_name

    @property
    def get_full_name(self):
        fullname = f"{self.firstname} {self.lastname}"
        if self.othername:
            fullname += f" {self.othername}"
        return fullname

    @property
    def get_age(self):
        current_year = datetime.date.today().year
        dateofbirth_year = self.birthday.year
        if dateofbirth_year:
            return current_year - dateofbirth_year
        return 0

    @property
    def can_apply_leave(self):
        # Implement logic here
        pass

    def save(self, *args, **kwargs):
        '''
        Override the save method - format employee ID before saving
        '''
        self.employeeid = code_format(self.employeeid)
        super().save(*args, **kwargs)
