from django.contrib import admin
from .models import Profile, Peer, PeerRequest, Group, Groupmessage, Spreadsheet, Book, Chat, Chatmessage, Registration, Roster, Podcast, News, Receipt

models = [Profile, Peer, PeerRequest, Group, Groupmessage, Spreadsheet, Book, Chat, Chatmessage, Registration, Roster,
          Podcast, News, Receipt]
# Register your models here.

admin.site.register(models)
