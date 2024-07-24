from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Religion(models.Model):
    name = models.CharField(max_length=125, unique=True)
    description = models.TextField(null=True, blank=True)
    created = models.DateTimeField(default=timezone.now)
    updated = models.DateTimeField(default=timezone.now, null=False)

    class Meta:
        verbose_name = 'Religion'
        verbose_name_plural = 'Religions'
        ordering = ['name']

    def __str__(self):
        return self.name


class Role(models.Model):
    name = models.CharField(max_length=125)
    description = models.CharField(max_length=125, null=True, blank=True)
    created = models.DateTimeField(default=timezone.now)
    updated = models.DateTimeField(default=timezone.now, null=False)

    class Meta:
        verbose_name = 'Role'
        verbose_name_plural = 'Roles'
        ordering = ['name', 'created']

    def __str__(self):
        return self.name


class Department(models.Model):
    name = models.CharField(max_length=125)
    description = models.CharField(max_length=125, null=True, blank=True)
    created = models.DateTimeField(default=timezone.now)
    updated = models.DateTimeField(default=timezone.now, null=False)

    class Meta:
        verbose_name = 'Department'
        verbose_name_plural = 'Departments'
        ordering = ['name', 'created']

    def __str__(self):
        return self.name


class Nationality(models.Model):
    name = models.CharField(max_length=125, unique=True)
    description = models.TextField(null=True, blank=True)
    created = models.DateTimeField(default=timezone.now)
    updated = models.DateTimeField(default=timezone.now, null=False)

    class Meta:
        verbose_name = 'Nationality'
        verbose_name_plural = 'Nationalities'
        ordering = ['name']

    def __str__(self):
        return self.name


class Employee(models.Model):
    MALE = 'male'
    FEMALE = 'female'
    OTHER = 'other'
    NOT_KNOWN = 'not_known'

    GENDER_CHOICES = [
        (MALE, 'Male'),
        (FEMALE, 'Female'),
        (OTHER, 'Other'),
        (NOT_KNOWN, 'Not Known'),
    ]

    MR = 'Mr'
    MRS = 'Mrs'
    MSS = 'Mss'
    DR = 'Dr'
    SIR = 'Sir'
    MADAM = 'Madam'

    TITLE_CHOICES = [
        (MR, 'Mr'),
        (MRS, 'Mrs'),
        (MSS, 'Mss'),
        (DR, 'Dr'),
        (SIR, 'Sir'),
        (MADAM, 'Madam'),
    ]

    FULL_TIME = 'Full-Time'
    PART_TIME = 'Part-Time'
    CONTRACT = 'Contract'
    INTERN = 'Intern'

    EMPLOYMENT_TYPE_CHOICES = [
        (FULL_TIME, 'Full-Time'),
        (PART_TIME, 'Part-Time'),
        (CONTRACT, 'Contract'),
        (INTERN, 'Intern'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='profiles', default='profiles/default.png', blank=True, null=True)
    firstname = models.CharField(max_length=125)
    lastname = models.CharField(max_length=125)
    othername = models.CharField(max_length=125, null=True, blank=True)
    birthday = models.DateField()
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True, blank=True)
    role = models.ForeignKey(Role, on_delete=models.SET_NULL, null=True, blank=True)
    nationality = models.ForeignKey(Nationality, on_delete=models.SET_NULL, null=True, blank=True)  # Added line
    startdate = models.DateField(default=timezone.now().date)
    enddate = models.DateField(default=timezone.now().date)
    employeetype = models.CharField(max_length=15, choices=EMPLOYMENT_TYPE_CHOICES, default=FULL_TIME)
    employeeid = models.CharField(max_length=10, null=True, blank=True)
    dateissued = models.DateField(null=True, blank=True)
    is_blocked = models.BooleanField(default=False)
    is_deleted = models.BooleanField(default=False)
    created = models.DateTimeField(default=timezone.now)
    updated = models.DateTimeField(default=timezone.now, null=False)

    def __str__(self):
        return f"{self.firstname} {self.lastname}"

    @property
    def get_full_name(self):
        return f"{self.firstname} {self.lastname} {self.othername or ''}".strip()
