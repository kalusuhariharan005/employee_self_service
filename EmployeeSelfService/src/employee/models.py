# employee/models.py

import datetime
from django.db import models
from django.utils.translation import gettext as _
from django.contrib.auth.models import User
from employee.utility import code_format
from employee.managers import EmployeeManager
from phonenumber_field.modelfields import PhoneNumberField
from leave.models import Leave

# Create your models here.

class Role(models.Model):
    name = models.CharField(max_length=125)
    description = models.CharField(max_length=125, null=True, blank=True)

    created = models.DateTimeField(verbose_name=_('Created'), auto_now_add=True)
    updated = models.DateTimeField(verbose_name=_('Updated'), auto_now=True)

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
    updated = models.DateTimeField(verbose_name=_('Updated'), auto_now=True)

    class Meta:
        verbose_name = _('Department')
        verbose_name_plural = _('Departments')
        ordering = ['name', 'created']

    def __str__(self):
        return self.name


class Religion(models.Model):
    name = models.CharField(max_length=125)
    description = models.CharField(max_length=125, null=True, blank=True)

    created = models.DateTimeField(verbose_name=_('Created'), auto_now_add=True)
    updated = models.DateTimeField(verbose_name=_('Updated'), auto_now=True)

    class Meta:
        verbose_name = _('Religion')
        verbose_name_plural = _('Religions')
        ordering = ['name', 'created']

    def __str__(self):
        return self.name


class Nationality(models.Model):
    name = models.CharField(max_length=125)
    description = models.CharField(max_length=125, null=True, blank=True)

    created = models.DateTimeField(verbose_name=_('Created'), auto_now_add=True)
    updated = models.DateTimeField(verbose_name=_('Updated'), auto_now=True)

    class Meta:
        verbose_name = _('Nationality')
        verbose_name_plural = _('Nationalities')
        ordering = ['name', 'created']

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
    firstname = models.CharField(_('Firstname'), max_length=125, null=False, blank=False)
    lastname = models.CharField(_('Lastname'), max_length=125, null=False, blank=False)
    othername = models.CharField(_('Othername (optional)'), max_length=125, null=True, blank=True)
    birthday = models.DateField(_('Birthday'), blank=False, null=False)
    department = models.ForeignKey(Department, verbose_name=_('Department'), on_delete=models.SET_NULL, null=True, default=None)
    role = models.ForeignKey(Role, verbose_name=_('Role'), on_delete=models.SET_NULL, null=True, default=None)
    startdate = models.DateField(_('Employment Date'), help_text='Date of employment', blank=False, null=True)
    employeetype = models.CharField(_('Employee Type'), max_length=15, default=FULL_TIME, choices=EMPLOYEETYPE, blank=False, null=True)
    employeeid = models.CharField(_('Employee ID Number'), max_length=10, null=True, blank=True)
    dateissued = models.DateField(_('Date Issued'), help_text='Date staff ID was issued', blank=False, null=True)

    # App related
    is_blocked = models.BooleanField(_('Is Blocked'), help_text='Button to toggle employee block and unblock', default=False)
    is_deleted = models.BooleanField(_('Is Deleted'), help_text='Button to toggle employee deleted and undelete', default=False)

    created = models.DateTimeField(verbose_name=_('Created'), auto_now_add=True, null=True)
    updated = models.DateTimeField(verbose_name=_('Updated'), auto_now=True, null=True)

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
        fullname = ''
        firstname = self.firstname
        lastname = self.lastname
        othername = self.othername

        if (firstname and lastname) or othername is None:
            fullname = firstname + ' ' + lastname
            return fullname
        elif othername:
            fullname = firstname + ' ' + lastname + ' ' + othername
            return fullname
        return

    @property
    def get_age(self):
        current_year = datetime.date.today().year
        dateofbirth_year = self.birthday.year
        if dateofbirth_year:
            return current_year - dateofbirth_year
        return

    @property
    def can_apply_leave(self):
        pass

    def save(self, *args, **kwargs):
        '''
        Overriding the save method - for every instance that calls the save method 
        perform this action on its employee_id
        added : March, 03 2019 - 11:08 PM
        '''
        get_id = self.employeeid  # Grab employee_id number from submitted form field
        data = code_format(get_id)
        self.employeeid = data  # Pass the new code to the employee_id as its original or actual code
        super().save(*args, **kwargs)  # Call the parent save method
