from django.db import models
from datetime import datetime
# Create your models here.


# profile
class Profile(models.Model):
    name = models.CharField(max_length=50, default=None)
    email = models.EmailField(max_length=300, default=None)
    status = models.CharField(max_length=50, default=None)
    level = models.CharField(max_length=50, default=None)
    matric = models.CharField(max_length=50, default=None)
    department = models.CharField(max_length=50, default="undefined")
    gender = models.CharField(max_length=50, default="Custom")
    date_of_birth = models.CharField(max_length=50, default="-- - --")
    bio = models.CharField(max_length=500, default="")
    profile_picture = models.ImageField(upload_to='profile_picture/', null=True, blank=True, default=None)
    profile_background_picture = models.ImageField(upload_to='profile_background_picture/', null=True, blank=True,
                                                   default=None)


# chat
class Chat(models.Model):
    users = models.ManyToManyField('Profile', default=[0], related_name="chat_user_list")


# chat messages
class Chatmessage(models.Model):
    sender = models.ForeignKey('Profile', on_delete=models.CASCADE, default=1, related_name="chat_sender")
    chat = models.ForeignKey('Chat', on_delete=models.CASCADE, default=1,)
    message = models.TextField(max_length=3000, default=None)
    time_sent = models.DateTimeField(auto_now_add=True)


# groups
class Group(models.Model):
    groupName = models.CharField(max_length=100, default=None)
    group_description = models.CharField(max_length=3000, default=None, null=True)
    group_creator = models.ForeignKey('Profile', on_delete=models.PROTECT, default=1, related_name="group_creator", null=True)
    users = models.ManyToManyField('Profile', default=[0])
    group_picture = models.ImageField(upload_to='group_picture/', null=True, blank=True)


# group messages
class Groupmessage(models.Model):
    sender = models.ForeignKey('Profile', on_delete=models.CASCADE, default=1, related_name="group_message_sender")
    group = models.ForeignKey('Group', on_delete=models.CASCADE, default=1)
    message = models.TextField(max_length=3000, default=None)
    time_sent = models.DateTimeField(auto_now_add=True)


# Peers
class Peer(models.Model):
    user = models.OneToOneField('Profile', on_delete=models.CASCADE, primary_key=True, default=1)
    friend_list = models.ManyToManyField('Profile', default=[0], related_name="friend_list")


# friend Request
class PeerRequest(models.Model):
    sender = models.ForeignKey('Profile', on_delete=models.CASCADE, default=1, related_name="friend_request_sender")
    receiver = models.ForeignKey('Profile', on_delete=models.CASCADE, default=1)
    status = models.BooleanField(default=False)


# books
class Book(models.Model):
    book_name = models.CharField(max_length=100, default=None)
    book_creator = models.ForeignKey('Profile', on_delete=models.CASCADE, default=1)
    book_file = models.FileField(upload_to='books/', null=True, blank=True)
    book_downloads = models.IntegerField(default=0)
    time_sent = models.DateTimeField(default=datetime.now())


# Podcasts
class Podcast(models.Model):
    pod_name = models.CharField(max_length=100, default=None)
    pod_creator = models.ForeignKey('Profile', on_delete=models.CASCADE, default=1)
    pod_file = models.FileField(upload_to='podcasts/', null=True, blank=True)
    pod_description = models.CharField(max_length=2000, default=None)
    pod_downloads = models.IntegerField(default=0)
    time_sent = models.DateTimeField(default=datetime.now())


# News Box
class News(models.Model):
    news_subject = models.CharField(max_length=100, default=None)
    news_creator = models.ForeignKey('Profile', on_delete=models.CASCADE, default=1)
    news_content = models.CharField(max_length=5000, default=None)
    time_sent = models.DateTimeField(default=datetime.now())


# course Registration
class Registration(models.Model):
    course_code = models.CharField(max_length=30, default=None)
    course_description = models.CharField(max_length=3000, default=None)
    course_unit = models.IntegerField(default=0)
    lecturer = models.ForeignKey('Profile', on_delete=models.CASCADE, default=1)
    students = models.ManyToManyField('Profile', default=[0], related_name="student_list")
    course_length = models.IntegerField(default=0)


# Roster
class Roster(models.Model):
    user = models.ForeignKey('Profile', on_delete=models.CASCADE, default=1, related_name="roster_owner")
    roster_list = models.ForeignKey('Roster', on_delete=models.PROTECT, default=1, related_name="registration")


# spreadsheet
class Spreadsheet(models.Model):
    session = models.CharField(max_length=50, default=None)
    department = models.CharField(max_length=50, default=None)
    mode_of_entry = models.CharField(max_length=50, default=None)
    level = models.CharField(max_length=50, default=None)
    semester = models.CharField(max_length=50, default="")
    number_of_courses = models.CharField(max_length=50, default=None)
    description = models.CharField(max_length=50, default=None)
    staff = models.ForeignKey('Profile', on_delete=models.PROTECT, default=1)
    spreadsheet = models.FileField(upload_to='spreadsheets/', null=True, blank=True)
    info = models.FileField(upload_to='info/', null=True, blank=True)
    missing_result = models.FileField(upload_to='missing_result/', null=True, blank=True)
    probation = models.FileField(upload_to='probation/', null=True, blank=True)
    datasheet = models.FileField(upload_to='datasheets/', null=True, blank=True)


# spreadsheet
class Receipt(models.Model):
    owner = models.ForeignKey('Profile', on_delete=models.PROTECT, default=1)
    hostel = models.CharField(max_length=100)
    department = models.CharField(max_length=100)
    status = models.CharField(max_length=100, default="pending")
    collection_date = models.CharField(max_length=100, default="null")
    purpose = models.CharField(max_length=1000, default="")
    file = models.ImageField(upload_to='receipts/', null=True, blank=True)
    time_sent = models.DateTimeField(default=datetime.now())
