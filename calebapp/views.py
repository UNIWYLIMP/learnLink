import random
from django.http import JsonResponse
from django.shortcuts import render, HttpResponse
from django.contrib import messages
from django.contrib.auth.models import auth, User
from django.shortcuts import redirect
from .models import Profile, Peer, PeerRequest, Group, Groupmessage, Spreadsheet, Book, Chat, Chatmessage, Registration, \
    Podcast, News, Receipt
from datetime import datetime
from . import spreadsheet_engine


def index(request):
    return render(request, 'index.html')


def signup(request):
    if request.method == 'POST':
        fullname = request.POST['name']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['repeatpassword']
        if request.POST['status'] == "staff":
            if request.POST['staffId'] == "2002#calebuniv":
                pass
            else:
                messages.info(request, 'Invalid StaffId')
                return redirect('/signup')
            lastname = request.POST['staffId']
            middlename = "staff"
            firstname = "Staff"
        elif request.POST['status'] == "student":
            firstname = request.POST['level']
            middlename = "student"
            lastname = request.POST['matric']
        else:
            return redirect("/index")

        if password == password2:
            if User.objects.filter(username=email).exists():
                messages.info(request, 'Email Already In Use')
                return redirect('/signup')

            elif firstname == "":
                messages.info(request, 'First name can not be empty')
                return redirect('/signup')

            elif fullname == "":
                messages.info(request, 'Name can not be empty')
                return redirect('/signup')

            elif middlename == "":
                messages.info(request, 'Middle name can not be empty')
                return redirect('/signup')

            elif lastname == "":
                messages.info(request, 'Matric can not be empty')
                return redirect('/signup')

            elif email == "":
                messages.info(request, 'Email name can not be empty')
                return redirect('/signup')

            elif len(password) < 8:
                messages.info(request, 'password is too short. Try again')
                return redirect('/signup')

            else:
                user = User.objects.create_user(username=email, email=fullname, password=password,
                                                first_name=middlename, last_name=lastname)
                user.save()
                new_profile = Profile()
                new_profile.name = fullname
                new_profile.email = email
                new_profile.status = middlename
                new_profile.level = firstname
                new_profile.matric = lastname
                new_profile.save()
                new_peer = Peer(user=new_profile)
                new_peer.save()
                l_user = auth.authenticate(username=email, password=password)
                auth.login(request, l_user)
                request.session['userId'] = email
                return redirect('/home')
        else:
            messages.info(request, 'passwords does not match')
            return redirect('/signup')
    else:
        return render(request, 'signup.html')


def login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user = auth.authenticate(username=email, password=password)

        if user is not None:
            auth.login(request, user)
            request.session['userId'] = email
            return redirect('/home')
        else:
            messages.info(request, 'Credentials Invalid')
            return redirect('/login')
    else:
        return render(request, 'login.html')


def home(request):
    if request.method == "POST":
        pass
    else:
        userID = request.session.get('userId')
        print(userID)
        profile = Profile.objects.get(email=userID)
        new_profile_item = {}
        try:
            new_profile_item["profile_background_picture"] = profile.profile_background_picture.url

        except ValueError:
            new_profile_item["profile_background_picture"] = "none"

        try:
            new_profile_item["profile_picture"] = profile.profile_picture.url

        except ValueError:
            new_profile_item["profile_picture"] = "none"

        return render(request, 'home.html',
                      {'Profile': profile, "new_profile_item": new_profile_item, 'bioLength': len(str(profile.bio))})


def calebnews(request):
    userID = request.session.get('userId')
    new_profile = Profile.objects.get(email=userID)
    all_news = News.objects.all()
    latest_news = News.objects.all()
    minor_list = []
    print(all_news)
    for x in list(latest_news):
        minor_list.insert(0, x)
    all_news = minor_list
    if request.method == "POST":
        news_subject = request.POST['news_subject']
        news_content = request.POST['news_content']
        new_news = News()
        new_news.news_subject = news_subject
        new_news.news_content = news_content
        new_news.news_creator = new_profile
        new_news.save()
        return redirect("/calebnews")
    else:
        return render(request, 'calebnews.html', {"news": all_news, "status": new_profile.status})


def viewprofile(request, user_id):
    userID = request.session.get('userId')
    profile = Profile.objects.get(id=user_id)
    if profile.email == userID:
        return redirect('home')
    else:
        pass
    new_profile_item = {}

    try:
        new_profile_item["profile_background_picture"] = profile.profile_background_picture.url

    except ValueError:
        new_profile_item["profile_background_picture"] = "none"

    try:
        new_profile_item["profile_picture"] = profile.profile_picture.url

    except ValueError:
        new_profile_item["profile_picture"] = "none"

    return render(request, 'viewprofile.html',
                  {'Profile': profile, "new_profile_item": new_profile_item, 'bioLength': len(str(profile.bio))})


def book(request):
    userID = request.session.get('userId')
    new_profile = Profile.objects.get(email=userID)
    if request.method == "POST":
        book_name = str(request.POST['book_search']).lower()
        query_return = Book.objects.filter(book_name__contains=book_name)
        print(len(query_return))
        print("here is one")
        return render(request, 'books.html',
                      {'books': query_return, "No_Of_Results": len(query_return), 'searched_book':
                          book_name, 'searched': True, "status": new_profile.status})

    else:
        return render(request, 'books.html', {'searched': False, "status": new_profile.status})


def upload_image_background(request):
    userID = request.session.get('userId')
    new_profile = Profile.objects.get(email=userID)
    if request.method == "POST":
        background_image = request.FILES['image_background']
        new_profile.profile_background_picture = background_image
        new_profile.save()
    else:
        pass
    return redirect("home")


def edit_profile(request):
    userID = request.session.get('userId')
    new_profile = Profile.objects.get(email=userID)
    if request.method == "POST":
        # profile_pic, DOB, Gender, matricNumber, level, telephoneNumber, bio
        profile_pic = request.FILES['profile_pic']
        date_of_birth = request.POST['DOB']
        gender = request.POST['Gender']
        bio = request.POST['bio']
        new_profile.profile_picture = profile_pic
        new_profile.date_of_birth = date_of_birth
        new_profile.gender = gender
        new_profile.bio = bio
        if new_profile.status == "student":
            matric_number = request.POST['matricNumber']
            department = request.POST['department']
            level = request.POST['level']
            new_profile.matric = matric_number
            new_profile.level = level
            new_profile.department = department
        else:
            telephoneNumber = request.POST['telephoneNumber']
            new_profile.matric = telephoneNumber
        new_profile.save()
    else:
        pass
    return redirect("home")


def download_book(request, book_id):
    new_book = Book.objects.get(id=book_id)
    new_book.book_downloads += 1
    new_book.save()
    return redirect(new_book.book_file.url)


def upload_book(request):
    userID = request.session.get('userId')
    new_profile = Profile.objects.get(email=userID)
    if request.method == "POST":
        book_file = request.FILES['file']
        book_name = request.POST['name']
        new_book = Book()
        new_book.book_creator = new_profile
        new_book.book_file = book_file
        new_book.book_name = book_name
        new_book.save()
        messages.info(request, f'{book_name} Uploaded Sucessfully')
        return redirect("/uploadBook")
    else:
        his_book = new_profile.book_set.all()
        return render(request, 'uploadbook.html', {"creator_books": his_book, "numBook": len(his_book)})


def deletebook(request, book_id):
    new_book = Book.objects.get(id=book_id)
    messages.info(request, f'{new_book.book_name} Deleted Sucessfully')
    new_book.delete()
    return redirect("/uploadBook")


def podcast(request):
    userID = request.session.get('userId')
    new_profile = Profile.objects.get(email=userID)

    if request.method == "POST":
        pod_name = str(request.POST['pod_search']).lower()
        query_return = Podcast.objects.filter(pod_name__contains=pod_name)
        print(len(query_return))
        print("here is one")
        return render(request, 'podcasts.html',
                      {'pods': query_return, "No_Of_Results": len(query_return), 'searched_pod':
                          pod_name, 'searched': True, "status": new_profile.status})
    else:
        return render(request, 'podcasts.html', {'searched': False, "status": new_profile.status})


def upload_podcast(request):
    userID = request.session.get('userId')
    new_profile = Profile.objects.get(email=userID)
    if request.method == "POST":
        pod_file = request.FILES['file']
        pod_name = request.POST['name']
        pod_description = request.POST['description']
        new_pod = Podcast()
        new_pod.pod_creator = new_profile
        new_pod.pod_file = pod_file
        new_pod.pod_name = pod_name
        new_pod.pod_description = pod_description
        new_pod.save()
        messages.info(request, f'{pod_name} Uploaded Sucessfully')
        return redirect("/uploadPodcast")
    else:
        his_pods = new_profile.podcast_set.all()
        return render(request, 'uploadpodcast.html', {"creator_pods": his_pods, "numPod": len(his_pods)})


def deletepod(request, pod_id):
    new_pod = Podcast.objects.get(id=pod_id)
    messages.info(request, f'{new_pod.pod_name} Deleted Successfully')
    new_pod.delete()
    return redirect("/uploadPodcast")


def viewpodcast(request, pod_id):
    new_pod = Podcast.objects.get(id=pod_id)
    new_pod.pod_downloads += 1
    new_pod.save()
    return render(request, "viewpodcast.html", {"podcast": new_pod})


def peers(request):
    userId = request.session.get('userId')
    new_profile = Profile.objects.get(email=userId)
    if request.method == "POST":
        search_result = request.POST['search_friend']
        new_friend_search = new_profile.peer.friend_list.filter(name__contains=search_result)
        friend_search = []
        for x in new_friend_search:
            member_name = x.name
            try:
                member_picture = x.profile_picture.url
            except ValueError:
                member_picture = "none"

            member_status = x.status
            member_id = x.id
            new_item = {"member_name": member_name, "member_picture": member_picture,
                        "member_status": member_status,
                        "member_id": member_id}
            friend_search.append(new_item)
        return render(request, 'peers.html', {"friend_search": friend_search, "No_Of_Results": len(friend_search),
                                                  "is_search": True, "searched_friend": search_result})
    else:
        all_friends = new_profile.peer.friend_list.all()
        friend_list = []
        for x in all_friends:
            member_name = x.name
            try:
                member_picture = x.profile_picture.url

            except ValueError:
                member_picture = "none"

            member_status = x.status
            member_id = x.id
            new_item = {"member_name": member_name, "member_picture": member_picture,
                        "member_status": member_status,
                        "member_id": member_id}
            friend_list.append(new_item)
        return render(request, 'peers.html', {"friend_List": friend_list, "No_Of_Results": len(friend_list),
                                              "is_search": False})


def delete_friend(request, peer_id):
    userId = request.session.get('userId')
    new_profile = Profile.objects.get(email=userId)
    friend = Profile.objects.get(id=peer_id)
    all_user_chats = Chat.objects.filter(users__id=new_profile.id)
    print(all_user_chats)
    for chat in all_user_chats:
        print(chat.users.all())
        for user in list(chat.users.all()):
            if str(user.id) == str(peer_id):
                new_chat = Chat.objects.get(id=chat.id)
                new_chat.delete()
            else:
                pass
    new_profile.peer.friend_list.remove(friend)
    friend.peer.friend_list.remove(new_profile)
    return redirect("/peers")


def delete_friend_chat(request, peer_id):
    userId = request.session.get('userId')
    new_profile = Profile.objects.get(email=userId)
    friend = Profile.objects.get(id=peer_id)
    all_user_chats = Chat.objects.filter(users__id=new_profile.id)
    print(all_user_chats)
    for chat in all_user_chats:
        print(chat.users.all())
        for user in list(chat.users.all()):
            if str(user.id) == str(peer_id):
                new_chat = Chat.objects.get(id=chat.id)
                new_chat.delete()
            else:
                pass
    new_profile.peer.friend_list.remove(friend)
    friend.peer.friend_list.remove(new_profile)
    return redirect("/chats")


def findpeers(request):
    userId = request.session.get('userId')
    new_profile = Profile.objects.get(email=userId)
    all_profile = Profile.objects.all()
    # friend_search = new_profile.peer.friend_list.filter(id=id).exist()
    list_of_finds = []
    suggestion = []
    request_list = []
    three_request = []
    for y in range(4):
        new_list = []
        for x in range(4):
            while True:
                random_profile = all_profile[(random.randint(1, len(all_profile))) - 1]
                if new_profile.peer.friend_list.filter(id=random_profile.id).exists():
                    pass
                elif random_profile.id == new_profile.id:
                    pass
                elif random_profile.id in list_of_finds:
                    pass
                elif PeerRequest.objects.filter(receiver=random_profile, sender=new_profile).exists():
                    pass
                elif PeerRequest.objects.filter(sender=random_profile, receiver=new_profile).exists():
                    pass
                else:
                    break
            member_name = random_profile.name
            try:
                member_picture = random_profile.profile_picture.url
            except ValueError:
                member_picture = "none"

            member_status = random_profile.status
            member_id = random_profile.id
            new_item = {"member_name": member_name, "member_picture": member_picture,
                        "member_status": member_status,
                        "member_id": member_id}
            new_list.append(new_item)
            list_of_finds.append(random_profile.id)
        suggestion.append(new_list)
        request_list = []
        all_request = PeerRequest.objects.filter(receiver__id=new_profile.id)
        for x in range(len(all_request)):
            member_name = all_request[x].sender.name
            try:
                member_picture = all_request[x].sender.profile_picture.url

            except ValueError:
                member_picture = "none"

            member_status = all_request[x].sender.status
            member_id = all_request[x].sender.id
            new_item = {"member_name": member_name, "member_picture": member_picture,
                        "member_status": member_status,
                        "member_id": member_id, "invite_id": all_request[x].id}
            request_list.insert(0, new_item)
        three_request = request_list[0:3]
    if request.method == "POST":
        searched_value = request.POST['person_search']
        results_latex = Profile.objects.filter(name__contains=searched_value)
        results = []
        for x in results_latex:
            if new_profile.peer.friend_list.filter(id=x.id).exists():
                pass
            elif x.id == new_profile.id:
                pass
            elif PeerRequest.objects.filter(receiver=x, sender=new_profile).exists():
                pass
            elif PeerRequest.objects.filter(sender=x, receiver=new_profile).exists():
                pass
            else:
                member_name = x.name
                try:
                    member_picture = x.profile_picture.url
                except ValueError:
                    member_picture = "none"

                member_status = x.status
                member_id = x.id
                new_item = {"member_name": member_name, "member_picture": member_picture,
                            "member_status": member_status,
                            "member_id": member_id}
                results.append(new_item)

        return render(request, 'findpeers.html', {"search_result": results, "No_of_search": len(results),
                                                  "is_searched": True, "searched_peer": searched_value})
    else:
        return render(request, 'findpeers.html', {"suggestion": suggestion, "No_of_request": len(request_list),
                                                  "Friend_requests": request_list,
                                                  "Friend_requests_three": three_request, "is_searched": False})


def confirmrequest(request):
    status = True
    if request.method == 'GET':
        value_status = request.GET.get('status')
        confirm_status = str(request.GET.get('receiver'))
        request_diminish = PeerRequest.objects.get(id=confirm_status)
        print(f"my confirm id is {confirm_status} and friend request is {request_diminish.sender}")
        print(value_status, " my confirm status")
        if value_status == "accepted":
            userId = request.session.get('userId')
            receiver = Profile.objects.get(email=userId)
            sender = request_diminish.sender
            print(PeerRequest.objects.filter(sender=sender, receiver=receiver).exists())
            if PeerRequest.objects.filter(sender=sender, receiver=receiver).exists():
                print("request 1")
                # Accept friend request
                status = True
                receiver.peer.friend_list.add(sender)
                sender.peer.friend_list.add(receiver)
                existing_request = PeerRequest.objects.filter(sender=sender, receiver=receiver)
                existing_request.delete()
        elif value_status == "deleted":
            userId = request.session.get('userId')
            receiver = Profile.objects.get(email=userId)
            sender = request_diminish.sender
            if PeerRequest.objects.filter(sender=sender, receiver=receiver).exists():
                existing_request = PeerRequest.objects.filter(sender=sender, receiver=receiver)
                existing_request.delete()
                print("request 1")
                # Deny friend request
                status = False
            pass
        else:
            return redirect('/findpeers')

    return JsonResponse({'Status': status})


def friendrequest(request):
    status = True
    if request.method == 'GET':
        userId = request.session.get('userId')
        sender = Profile.objects.get(email=userId)
        value = request.GET.get('receiver')
        receiver = Profile.objects.get(id=value)
        if PeerRequest.objects.filter(sender=sender, receiver=receiver).exists():
            existing_request = PeerRequest.objects.filter(sender=sender, receiver=receiver)
            existing_request.delete()
            # delete friend request
            status = False
        else:
            # Create a new Friend Request
            new_friendship = PeerRequest(sender=sender, receiver=receiver)
            new_friendship.save()
            status = True
    return JsonResponse({'Status': status})


def getrequest(request):
    userId = request.session.get('userId')
    new_profile = Profile.objects.get(email=userId)
    all_request = PeerRequest.objects.filter(receiver__id=new_profile.id)
    request_list = []
    for x in range(len(all_request)):
        member_name = all_request[x].sender.name
        try:
            member_picture = all_request[x].sender.profile_picture.url

        except ValueError:
            member_picture = "none"

        member_status = all_request[x].sender.status
        member_id = all_request[x].sender.id
        new_item = {"member_name": member_name, "member_picture": member_picture,
                    "member_status": member_status,
                    "member_id": member_id, "invite_id": all_request[x].id}
        request_list.insert(0, new_item)
    return JsonResponse({"friend_request_all": request_list})


def groups(request):
    minutes = 1
    userId = request.session.get('userId')
    new_profile = Profile.objects.get(email=userId)
    all_user_groups = Group.objects.filter(users__id=new_profile.id)
    print(all_user_groups)
    group_info = []
    group_info_temporary = []
    for x in list(all_user_groups):
        print(x)
        new_group_item = {"id": x.id, 'group_name': x.groupName}
        try:
            new_group_item["group_picture"] = x.group_picture.url

        except ValueError:
            new_group_item["group_picture"] = "none"
        all_messages_in_a_group = x.groupmessage_set.all()
        last_message = all_messages_in_a_group[len(all_messages_in_a_group) - 1]
        msg = f"{str(last_message.sender.name).split()[0]}: {last_message.message}"
        hellos = datetime(last_message.time_sent.year, last_message.time_sent.month, last_message.time_sent.day,
                          last_message.time_sent.hour, last_message.time_sent.minute, last_message.time_sent.second)
        tellos = datetime.now()
        timemat = tellos - hellos
        days = timemat.days
        seconds = int(timemat.seconds)
        minutes = int(timemat.seconds / 60)
        if days == 0:
            print(f"yes our {minutes} and seconds {seconds}")
            if minutes - 60 == 0:
                new_group_item['last_message_time'] = f"{int(seconds) - 3600} secs ago"

            elif int(minutes / 60) - 1 == 0:
                new_group_item['last_message_time'] = f"{int(minutes - 60)} mins ago"

            else:
                if int(minutes / 60) - 1 == 25:
                    new_group_item['last_message_time'] = f"1 day ago"
                else:
                    new_group_item['last_message_time'] = f"{int(minutes / 60) - 1} hrs ago"
        elif days < 7:
            new_group_item['last_message_time'] = f"{int(days)} days ago"
        elif 7 <= days <= 30:
            new_group_item['last_message_time'] = f"{int(days / 7)} weeks ago"
        elif 30 < days < 365:
            new_group_item['last_message_time'] = f"{hellos.strftime('%B')} {hellos.strftime('%d')}," \
                                                  f" {hellos.strftime('%Y')}"
        elif days > 365:
            new_group_item['last_message_time'] = f"{int(tellos.year - hellos.year)} yrs ago"
        new_group_item['last_message'] = msg
        new_group_item['time_value'] = seconds
        print(f"{last_message.time_sent} this is it yearly")
        print(f"{hellos.strftime('%B')} {hellos.strftime('%d')}, {hellos.strftime('%Y')}")
        group_info_temporary.append(new_group_item)
    group_info = sorted(group_info_temporary, key=lambda j: j['time_value'])
    if request.method == "POST":
        pass
    else:
        return render(request, "groups.html", {"super_group_info": group_info, "group_length": len(group_info)})


def reloadgroup(request):
    minutes = 1
    userId = request.session.get('userId')
    new_profile = Profile.objects.get(email=userId)
    all_user_groups = Group.objects.filter(users__id=new_profile.id)
    print(all_user_groups)
    group_info = []
    group_info_temporary = []
    for x in list(all_user_groups):
        print(x)
        new_group_item = {"id": x.id, 'group_name': x.groupName}
        try:
            new_group_item["group_picture"] = x.group_picture.url

        except ValueError:
            new_group_item["group_picture"] = "none"
        all_messages_in_a_group = x.groupmessage_set.all()
        last_message = all_messages_in_a_group[len(all_messages_in_a_group) - 1]
        msg = f"{str(last_message.sender.name).split()[0]}: {last_message.message}"
        hellos = datetime(last_message.time_sent.year, last_message.time_sent.month, last_message.time_sent.day,
                          last_message.time_sent.hour, last_message.time_sent.minute, last_message.time_sent.second)
        tellos = datetime.now()
        timemat = tellos - hellos
        days = timemat.days
        seconds = int(timemat.seconds)
        minutes = int(timemat.seconds / 60)
        if days == 0:
            print(f"yes our {minutes} and seconds {seconds}")
            if minutes - 60 == 0:
                new_group_item['last_message_time'] = f"{int(seconds) - 3600} secs ago"

            elif int(minutes / 60) - 1 == 0:
                new_group_item['last_message_time'] = f"{int(minutes - 60)} mins ago"

            else:
                if int(minutes / 60) - 1 == 25:
                    new_group_item['last_message_time'] = f"1 day ago"
                else:
                    new_group_item['last_message_time'] = f"{int(minutes / 60) - 1} hrs ago"
        elif days < 7:
            new_group_item['last_message_time'] = f"{int(days)} days ago"
        elif 7 <= days <= 30:
            new_group_item['last_message_time'] = f"{int(days / 7)} weeks ago"
        elif 30 < days < 365:
            new_group_item['last_message_time'] = f"{hellos.strftime('%B')} {hellos.strftime('%d')}," \
                                                  f" {hellos.strftime('%Y')}"
        elif days > 365:
            new_group_item['last_message_time'] = f"{int(tellos.year - hellos.year)} yrs ago"
        new_group_item['last_message'] = msg
        new_group_item['time_value'] = seconds
        print(f"{last_message.time_sent} this is it yearly")
        print(f"{hellos.strftime('%B')} {hellos.strftime('%d')}, {hellos.strftime('%Y')}")
        group_info_temporary.append(new_group_item)
    group_info = sorted(group_info_temporary, key=lambda j: j['time_value'])
    print(group_info_temporary)
    print(group_info)
    all_list_id = []
    for p in group_info:
        all_list_id.append(p.get('id'))
    print(all_list_id)
    return JsonResponse({"super_group_info": group_info, "all_list_id": all_list_id, "group_length": len(group_info)})


def privategroup(request, id_group):
    print(f"{id_group} this is your group id")
    request.session['private_group_reload_id'] = id_group
    private_reload_id = request.session.get('private_group_reload_id')
    print("this is the private id session", private_reload_id)
    get_group = Group.objects.get(id=id_group)
    group_name = get_group.groupName
    group_id = get_group.id
    try:
        group_picture = get_group.group_picture.url

    except ValueError:
        group_picture = "none"
    group_description = get_group.group_description
    userId = request.session.get('userId')
    new_profile = Profile.objects.get(email=userId)
    user_set = get_group.users.all()
    ratter = False
    request.session['private_group_reload_num'] = 0
    for x in list(user_set):
        if x.id == new_profile.id:
            ratter = True
        else:
            pass
    if not ratter:
        return redirect("/groups")
    else:
        pass
    all_messages_in_a_group = get_group.groupmessage_set.all()
    list_of_messages = {}
    list_of_messages_id = []
    for message in all_messages_in_a_group:
        if message.sender.id == new_profile.id:
            sender = "me"
        else:
            sender = f"{message.sender.name}"
        try:
            van = list_of_messages[str(message.time_sent.date())]
            if message.time_sent.minute < 10:
                min_str = "0" + str(message.time_sent.minute)
                list_of_messages[str(message.time_sent.date())] += [{"messages": message.message,
                                                                     "time_sent": str(
                                                                         message.time_sent.hour + 1) + ":" +
                                                                                  min_str, "sender": sender}]
            else:
                list_of_messages[str(message.time_sent.date())] += [{"messages": message.message,
                                                                     "time_sent": str(
                                                                         message.time_sent.hour + 1) + ":" +
                                                                                  str(message.time_sent.minute),
                                                                     "sender": sender}]
        except KeyError:
            if message.time_sent.minute < 10:
                min_str = "0" + str(message.time_sent.minute)
                list_of_messages[str(message.time_sent.date())] = [{"messages": message.message,
                                                                    "time_sent": str(message.time_sent.hour + 1) + ":" +
                                                                                 min_str, "sender": sender}]
            else:
                list_of_messages[str(message.time_sent.date())] = [{"messages": message.message,
                                                                    "time_sent": str(message.time_sent.hour + 1) + ":" +
                                                                                 str(message.time_sent.minute),
                                                                    "sender": sender}]
            list_of_messages_id.append(str(message.time_sent.date()))
    new_digit_list = []
    for x in list_of_messages_id:
        valuations = x.split("-")
        valuation = ""
        for p in valuations:
            valuation += p
        new_digit_list.append(int(valuation))
    new_digit_list.sort()
    list_of_messages_id = []
    for z in new_digit_list:
        list_of_messages_id.append(str(str(z)[0:4] + "-" + str(z)[4:6] + "-" + str(z)[6] + str(z)[-1]))
    print(list_of_messages_id, " this is t")
    print("reached!!!")
    print(list_of_messages, " nal ne mesa")
    print(list_of_messages_id, " nal 22 24ne mesa")
    print(all_messages_in_a_group[0].time_sent.date(), " this are the message")
    print(f"{get_group.users.all()} certain chat")
    print(f"{user_set} all user")
    return render(request, "privategroup.html", {"list_of_messages_id": list_of_messages_id,
                                                 "list_of_messages": list_of_messages, "group_name": group_name,
                                                 "group_picture": group_picture, "group_description":
                                                     group_description, "group_id": group_id})


def reloadprivategroup(request):
    id_group = request.session.get('private_group_reload_id')
    print("this is the private id session", id_group)
    get_group = Group.objects.get(id=id_group)
    userId = request.session.get('userId')
    new_profile = Profile.objects.get(email=userId)
    user_set = get_group.users.all()
    group_name = get_group.groupName
    group_id = get_group.id
    try:
        group_picture = get_group.group_picture.url
        print("\n\n\n\n", group_picture)

    except ValueError:
        group_picture = "none"
        print("\n\n\n\n", group_picture)
    group_description = get_group.group_description
    ratter = False
    for x in list(user_set):
        if x.id == new_profile.id:
            ratter = True
        else:
            pass
    if not ratter:
        return redirect("/groups")
    else:
        pass
    all_messages_in_a_group = get_group.groupmessage_set.all()
    list_of_messages = {}
    list_of_messages_id = []
    for message in all_messages_in_a_group:
        if message.sender.id == new_profile.id:
            sender = "me"
        else:
            sender = f"{message.sender.name}"
        try:
            van = list_of_messages[str(message.time_sent.date())]
            if message.time_sent.minute < 10:
                min_str = "0" + str(message.time_sent.minute)
                list_of_messages[str(message.time_sent.date())] += [{"messages": message.message,
                                                                     "time_sent": str(
                                                                         message.time_sent.hour + 1) + ":" +
                                                                                  min_str,
                                                                     "sender": sender}]
            else:
                list_of_messages[str(message.time_sent.date())] += [{"messages": message.message,
                                                                     "time_sent": str(
                                                                         message.time_sent.hour + 1) + ":" +
                                                                                  str(message.time_sent.minute),
                                                                     "sender": sender}]
        except KeyError:
            if message.time_sent.minute < 10:
                min_str = "0" + str(message.time_sent.minute)
                list_of_messages[str(message.time_sent.date())] = [{"messages": message.message,
                                                                    "time_sent": str(message.time_sent.hour + 1) + ":" +
                                                                                 min_str,
                                                                    "sender": sender}]
            else:
                list_of_messages[str(message.time_sent.date())] = [{"messages": message.message,
                                                                    "time_sent": str(message.time_sent.hour + 1) + ":" +
                                                                                 str(message.time_sent.minute),
                                                                    "sender": sender}]
            list_of_messages_id.append(str(message.time_sent.date()))
    new_digit_list = []
    for x in list_of_messages_id:
        valuations = x.split("-")
        valuation = ""
        for p in valuations:
            valuation += p
        new_digit_list.append(int(valuation))
    new_digit_list.sort()
    list_of_messages_id = []
    for z in new_digit_list:
        list_of_messages_id.append(str(str(z)[0:4] + "-" + str(z)[4:6] + "-" + str(z)[6] + str(z)[-1]))
    previous_messages_length = request.session.get("old_group_message_length")
    current_messages_length = len(all_messages_in_a_group)
    if previous_messages_length is None:
        previous_messages_length = len(all_messages_in_a_group)
    else:
        pass
    if previous_messages_length < current_messages_length:
        new_message = True
    else:
        new_message = False

    print("\n\n\n\n", request.session.get('private_group_reload_num'))
    if request.session.get('private_group_reload_num') is None:
        request.session['private_group_reload_num'] = 1
    request.session['private_group_reload_num'] += 1
    request.session['old_group_message_length'] = len(all_messages_in_a_group)
    print("there is a new message: ", new_message)
    return JsonResponse({"list_of_messages_id": list_of_messages_id, "list_of_messages": list_of_messages,
                         "new_message": new_message,
                         'private_group_reload_num': request.session.get('private_group_reload_num'),
                         "group_name": group_name, "group_picture": group_picture,
                         "group_description": group_description, "group_id": group_id})


def editgroup(request, id_group):
    new_group = Group.objects.get(id=id_group)
    userId = request.session.get('userId')
    new_profile = Profile.objects.get(email=userId)
    user_set = new_group.users.all()
    ratter = False
    group_name = new_group.groupName
    group_id = new_group.id
    request.session["group_id"] = group_id
    try:
        group_picture = new_group.group_picture.url
        print("\n\n\n\n", group_picture)

    except ValueError:
        group_picture = "none"
        print("\n\n\n\n", group_picture)
    group_description = new_group.group_description
    if new_group.group_creator.id == new_profile.id:
        admin_group = "True"
    else:
        admin_group = "False"
    list_of_members = []
    for x in list(user_set):
        if x.id == new_profile.id:
            ratter = True
            member_name = x.name
            try:
                member_picture = x.profile_picture.url

            except ValueError:
                member_picture = "none"

            member_status = x.status
            member_id = x.id
            new_item = {"member_name": member_name, "member_picture": member_picture, "member_status": member_status,
                        "member_id": member_id}
            list_of_members.append(new_item)

        else:
            member_name = x.name
            try:
                member_picture = x.profile_picture.url
            except ValueError:
                member_picture = "none"

            member_status = x.status
            member_id = x.id
            new_item = {"member_name": member_name, "member_picture": member_picture, "member_status": member_status,
                        "member_id": member_id}
            list_of_members.append(new_item)
    if not ratter:
        return redirect("/groups")
    else:
        pass
    return render(request, "editgroup.html", {"group_picture": group_picture, "group_name": group_name, "group_id":
        group_id, "admin_status": admin_group, "group_description": group_description,
                                              "list_of_members": list_of_members, "user_id": new_profile.id,
                                              "number_of_members": len(list(new_group.users.all()))})


def change_group_info(request):
    id_group = request.session.get("group_id")
    if request.method == "POST":
        print("\n\n\n", id_group, "\n\n\nthis is group")
        get_group = Group.objects.get(id=id_group)
        get_group.groupName = request.POST['group_name']
        get_group.group_description = request.POST['group_description']
        get_group.group_picture = request.FILES['file']
        get_group.save()
        return redirect(f"/editgroup/{id_group}")
    else:
        return redirect("/groups")


def make_group(request):
    if request.method == "POST":
        userId = request.session.get('userId')
        new_profile = Profile.objects.get(email=userId)
        get_group = Group()
        get_group.groupName = request.POST['group_name']
        get_group.group_description = request.POST['group_description']
        get_group.group_picture = request.FILES['file']
        get_group.group_creator = new_profile
        get_group.save()
        get_group.users.add(new_profile)
        new_message = Groupmessage()
        new_message.message = "This is the beginning of a new conversation!"
        new_message.group = get_group
        new_message.sender = new_profile
        new_message.save()
        return redirect(f"/privategroup/{get_group.id}")
    else:
        return redirect("/groups")


def deletegroup(request, id_group):
    new_group = Group.objects.get(id=id_group)
    userId = request.session.get('userId')
    new_profile = Profile.objects.get(email=userId)
    if new_group.group_creator.id == new_profile.id:
        pass
    else:
        return redirect("/groups")
    new_group.delete()
    return redirect("/groups")


def remove_all_members(request, id_group):
    new_group = Group.objects.get(id=id_group)
    userId = request.session.get('userId')
    new_profile = Profile.objects.get(email=userId)
    if new_group.group_creator.id == new_profile.id:
        pass
    else:
        return redirect("/groups")
    all_members = new_group.users.all()
    for member in all_members:
        if member.id == new_group.group_creator.id:
            pass
        else:
            new_group.users.remove(member)
    return redirect(f"/editgroup/{request.session.get('group_id')}")


def adduser(request, user_id):
    id_group = request.session.get("group_id")
    userId = request.session.get('userId')
    new_user = Profile.objects.get(id=user_id)
    new_group = Group.objects.get(id=id_group)
    new_group.users.add(new_user)
    return redirect("/addgroupmember")


def add_group_member(request):
    id_group = request.session.get("group_id")
    get_group = Group.objects.get(id=id_group)
    userId = request.session.get('userId')
    new_profile = Profile.objects.get(email=userId)
    if request.method == "POST":
        search_result = request.POST['search_friend']
        new_friend_search = Profile.objects.filter(name__contains=search_result)
        friend_search = []
        for x in new_friend_search:
            if x.id == new_profile.id:
                pass
            elif get_group.users.filter(id=x.id):
                pass
            else:
                member_name = x.name
                try:
                    member_picture = x.profile_picture.url
                except ValueError:
                    member_picture = "none"

                member_status = x.status
                member_id = x.id
                new_item = {"member_name": member_name, "member_picture": member_picture,
                            "member_status": member_status,
                            "member_id": member_id}
                friend_search.append(new_item)
        return render(request, 'addgroupmember.html', {"friend_search": friend_search, "is_search": True,
                                                       "searched_friend": search_result,
                                                       "No_Of_Results": len(friend_search),
                                                       "id_group": id_group})
    else:
        all_friends = new_profile.peer.friend_list.all()
        friend_list = []
        for x in all_friends:
            if x.id == new_profile.id:
                pass
            elif get_group.users.filter(id=x.id):
                pass
            else:
                member_name = x.name
                try:
                    member_picture = x.profile_picture.url
                except ValueError:
                    member_picture = "none"

                member_status = x.status
                member_id = x.id
                new_item = {"member_name": member_name, "member_picture": member_picture,
                            "member_status": member_status,
                            "member_id": member_id}
                friend_list.append(new_item)
        print(friend_list)
        return render(request, 'addgroupmember.html', {"friend_List": friend_list, "No_Of_Results": len(friend_list),
                                                       "is_search": False, "id_group": id_group})


def remove_member(request, id_member):
    new_group = Group.objects.get(id=request.session.get("group_id"))
    userId = request.session.get('userId')
    new_profile = Profile.objects.get(email=userId)
    certain_profile = Profile.objects.get(id=id_member)
    if new_group.group_creator.id == new_profile.id:
        pass
    else:
        return redirect("/groups")
    new_group.users.remove(certain_profile)
    return redirect(f"/editgroup/{request.session.get('group_id')}")


def send_groupmessage(request):
    if request.method == "GET":
        message = request.GET.get('new_message')
        print(message + " this is rel \n\n\n\n\n\n\n\n\n\n\n\n\n")
        userId = request.session.get('userId')
        new_profile = Profile.objects.get(email=userId)
        id_group = request.session.get('private_group_reload_id')
        print("this is the private id session", id_group)
        current_group = Group.objects.get(id=id_group)
        new_message = Groupmessage(sender=new_profile, group=current_group, message=message)
        new_message.save()
    else:
        pass
    return JsonResponse({"value": "message_sent"})


def chats(request):
    minutes = 1
    userId = request.session.get('userId')
    new_profile = Profile.objects.get(email=userId)
    all_user_chats = Chat.objects.filter(users__id=new_profile.id)
    print(all_user_chats)
    chat_info = []
    chat_info_temporary = []
    for x in list(all_user_chats):
        print(x)
        new_chat_item = {
            "id": x.id,
        }
        for y in list(x.users.all()):
            if y.id != new_profile.id:
                new_chat_item['friend_name'] = y.name
                try:
                    new_chat_item['friend_profile_img'] = y.profile_picture.url
                except ValueError:
                    new_chat_item['friend_profile_img'] = "none"

            else:
                pass
        all_messages_in_a_chat = x.chatmessage_set.all()
        last_message = all_messages_in_a_chat[len(all_messages_in_a_chat) - 1]
        msg = last_message.message
        msg_time_sent = f"{str(last_message.time_sent).split(' ')} {str(last_message.time_sent).split(' ')}"
        hellos = datetime(last_message.time_sent.year, last_message.time_sent.month, last_message.time_sent.day,
                          last_message.time_sent.hour, last_message.time_sent.minute, last_message.time_sent.second)
        tellos = datetime.now()
        timemat = tellos - hellos
        days = timemat.days
        seconds = int(timemat.seconds)
        minutes = int(timemat.seconds / 60)
        if days == 0:
            print(f"yes our {minutes} and seconds {seconds}")
            if minutes - 60 == 0:
                new_chat_item['last_message_time'] = f"{int(seconds) - 3600} secs ago"

            elif int(minutes / 60) - 1 == 0:
                new_chat_item['last_message_time'] = f"{int(minutes - 60)} mins ago"

            else:
                if int(minutes / 60) - 1 == 25:
                    new_chat_item['last_message_time'] = f"1 day ago"
                else:
                    new_chat_item['last_message_time'] = f"{int(minutes / 60) - 1} hrs ago"
        elif days < 7:
            new_chat_item['last_message_time'] = f"{int(days)} days ago"
        elif 7 <= days <= 30:
            new_chat_item['last_message_time'] = f"{int(days / 7)} weeks ago"
        elif 30 < days < 365:
            new_chat_item['last_message_time'] = f"{hellos.strftime('%B')} {hellos.strftime('%d')}," \
                                                 f" {hellos.strftime('%Y')}"
        elif days > 365:
            new_chat_item['last_message_time'] = f"{int(tellos.year - hellos.year)} yrs ago"
        new_chat_item['last_message'] = msg
        new_chat_item['time_value'] = seconds
        print(f"{last_message.time_sent} this is it yearly")
        print(f"{hellos.strftime('%B')} {hellos.strftime('%d')}, {hellos.strftime('%Y')}")
        chat_info_temporary.append(new_chat_item)
    chat_info = sorted(chat_info_temporary, key=lambda j: j['time_value'])
    if request.method == "POST":
        return redirect("/chats")
    else:
        return render(request, "chats.html", {"super_chat_info": chat_info, "chat_length": len(chat_info)})


def searched_chats(request):
    userId = request.session.get('userId')
    new_profile = Profile.objects.get(email=userId)
    all_user_chats = Chat.objects.filter(users__id=new_profile.id)
    if request.method == "POST":
        print("\nSEARCHED CHATS new\n")
        searched_chat = request.POST['chat_name']
        search_result = []
        for chat in all_user_chats:
            for user in list(chat.users.all()):
                if user.id == new_profile.id:
                    pass
                else:
                    if str(searched_chat).lower() in str(user.name).lower():
                        new_chat_item = {"id": chat.id, 'friend_name': user.name
                                         }
                        try:
                            new_chat_item['friend_profile_img'] = user.profile_picture.url
                        except ValueError:
                            new_chat_item['friend_profile_img'] = "none"
                        search_result.append(new_chat_item)
                    else:
                        pass
        print("\n search result", search_result)
        return render(request, "searchedchat.html", {"search_result": search_result, "No_of_search": len(search_result),
                                                     "searched_peer": searched_chat})
    else:
        return redirect("/chats")


def reloadchat(request):
    userId = request.session.get('userId')
    new_profile = Profile.objects.get(email=userId)
    all_user_chats = Chat.objects.filter(users__id=new_profile.id)
    print(all_user_chats)
    chat_info = []
    chat_info_temporary = []
    for x in list(all_user_chats):
        print(x)
        new_chat_item = {
            "id": x.id,
        }
        for y in list(x.users.all()):
            if y.id != new_profile.id:
                new_chat_item['friend_name'] = y.name
                try:
                    new_chat_item['friend_profile_img'] = y.profile_picture.url
                except ValueError:
                    new_chat_item['friend_profile_img'] = "none"
            else:
                pass
        all_messages_in_a_chat = x.chatmessage_set.all()
        last_message = all_messages_in_a_chat[len(all_messages_in_a_chat) - 1]
        msg = last_message.message
        msg_time_sent = f"{str(last_message.time_sent).split(' ')} {str(last_message.time_sent).split(' ')}"
        hellos = datetime(last_message.time_sent.year, last_message.time_sent.month, last_message.time_sent.day,
                          last_message.time_sent.hour, last_message.time_sent.minute, last_message.time_sent.second)
        tellos = datetime.now()
        timemat = tellos - hellos
        days = timemat.days
        seconds = (int(timemat.seconds)) + (days * 24 * 60 * 60)
        minutes = int(timemat.seconds / 60)
        print(f"This our Day Value: {days}, this our minutes value: {minutes}, this our second value: {seconds}")
        if days == 0:
            print(f"yes our {minutes} and seconds {seconds}")
            if minutes - 60 == 0:
                new_chat_item['last_message_time'] = f"{int(seconds) - 3600} secs ago"

            elif int(minutes / 60) - 1 == 0:
                new_chat_item['last_message_time'] = f"{int(minutes - 60)} mins ago"

            else:
                if int(minutes / 60) - 1 == 25:
                    new_chat_item['last_message_time'] = f"1 day ago"
                else:
                    new_chat_item['last_message_time'] = f"{int(minutes / 60) - 1} hrs ago"
        elif days < 7:
            new_chat_item['last_message_time'] = f"{int(days)} days ago"
        elif 7 <= days <= 30:
            new_chat_item['last_message_time'] = f"{int(days / 7)} weeks ago"
        elif 30 < days < 365:
            new_chat_item['last_message_time'] = f"{hellos.strftime('%B')} {hellos.strftime('%d')}," \
                                                 f" {hellos.strftime('%Y')}"
        elif days > 365:
            new_chat_item['last_message_time'] = f"{int(tellos.year - hellos.year)} yrs ago"
        new_chat_item['last_message'] = msg
        new_chat_item['time_value'] = seconds
        print(f"{last_message.time_sent} this is it yearly")
        print(f"{hellos.strftime('%B')} {hellos.strftime('%d')}, {hellos.strftime('%Y')}")
        chat_info_temporary.append(new_chat_item)
    chat_info = sorted(chat_info_temporary, key=lambda j: j['time_value'])
    print(chat_info_temporary)
    print(chat_info)
    all_list_id = []
    for p in chat_info:
        all_list_id.append(p.get('id'))
    print(all_list_id)
    return JsonResponse({"super_chat_info": chat_info, "all_list_id": all_list_id, "chat_length": len(chat_info)})


def privatechat(request, id_chat):
    print(f"{id_chat} this is your chat id")
    request.session['private_reload_id'] = id_chat
    private_reload_id = request.session.get('private_reload_id')
    print("this is the private id session", private_reload_id)
    get_chat = Chat.objects.get(id=id_chat)
    userId = request.session.get('userId')
    new_profile = Profile.objects.get(email=userId)
    user_set = get_chat.users.all()
    ratter = False
    request.session['private_chat_reload_num'] = 0
    profile_name = ""
    profile_picture = ""
    for x in list(user_set):
        if x.id == new_profile.id:
            ratter = True
        else:
            profile_name = x.name
            profile_picture = x.profile_picture
    if not ratter:
        return redirect("/chats")
    else:
        pass
    all_messages_in_a_chat = get_chat.chatmessage_set.all()
    list_of_messages = {}
    list_of_messages_id = []
    for message in all_messages_in_a_chat:
        if message.sender.id == new_profile.id:
            sender = "me"
        else:
            sender = "ex"
        try:
            van = list_of_messages[str(message.time_sent.date())]
            if message.time_sent.minute < 10:
                min_str = "0" + str(message.time_sent.minute)
                list_of_messages[str(message.time_sent.date())] += [{"messages": message.message,
                                                                     "time_sent": str(
                                                                         message.time_sent.hour + 1) + ":" +
                                                                                  min_str, "sender": sender}]
            else:
                list_of_messages[str(message.time_sent.date())] += [{"messages": message.message,
                                                                     "time_sent": str(
                                                                         message.time_sent.hour + 1) + ":" +
                                                                                  str(message.time_sent.minute),
                                                                     "sender": sender}]
        except KeyError:
            if message.time_sent.minute < 10:
                min_str = "0" + str(message.time_sent.minute)
                list_of_messages[str(message.time_sent.date())] = [{"messages": message.message,
                                                                    "time_sent": str(message.time_sent.hour + 1) + ":" +
                                                                                 min_str, "sender": sender}]
            else:
                list_of_messages[str(message.time_sent.date())] = [{"messages": message.message,
                                                                    "time_sent": str(message.time_sent.hour + 1) + ":" +
                                                                                 str(message.time_sent.minute),
                                                                    "sender": sender}]
            list_of_messages_id.append(str(message.time_sent.date()))
    new_digit_list = []
    for x in list_of_messages_id:
        valuations = x.split("-")
        valuation = ""
        for p in valuations:
            valuation += p
        new_digit_list.append(int(valuation))
    new_digit_list.sort()
    list_of_messages_id = []
    for z in new_digit_list:
        list_of_messages_id.append(str(str(z)[0:4] + "-" + str(z)[4:6] + "-" + str(z)[6] + str(z)[-1]))
    print(list_of_messages_id, " this is t")
    print("reached!!!")
    print(list_of_messages, " nal ne mesa")
    print(list_of_messages_id, " nal 22 24ne mesa")
    print(all_messages_in_a_chat[0].time_sent.date(), " this are the message")
    print(f"{get_chat.users.all()} certain chat")
    print(f"{user_set} all user")

    try:
        print("\n\n\n\n", profile_picture.url)
        new_profile_picture = profile_picture.url
    except ValueError:
        new_profile_picture = "none"
    return render(request, "privatechat.html", {"list_of_messages_id": list_of_messages_id,
                                                "list_of_messages": list_of_messages, "profile_name": profile_name,
                                                "profile_picture": new_profile_picture, "chat_id": id_chat})


def reloadprivatechat(request):
    id_chat = request.session.get('private_reload_id')
    print("this is the private id session", id_chat)
    get_chat = Chat.objects.get(id=id_chat)
    userId = request.session.get('userId')
    new_profile = Profile.objects.get(email=userId)
    user_set = get_chat.users.all()
    ratter = False
    profile_name = ""
    profile_picture = ""
    for x in list(user_set):
        if x.id == new_profile.id:
            ratter = True
        else:
            profile_name = x.name
            profile_picture = x.profile_picture
    if not ratter:
        return redirect("/chats")
    else:
        pass
    all_messages_in_a_chat = get_chat.chatmessage_set.all()
    list_of_messages = {}
    list_of_messages_id = []
    for message in all_messages_in_a_chat:
        if message.sender.id == new_profile.id:
            sender = "me"
        else:
            sender = "ex"
        try:
            van = list_of_messages[str(message.time_sent.date())]
            if message.time_sent.minute < 10:
                min_str = "0" + str(message.time_sent.minute)
                list_of_messages[str(message.time_sent.date())] += [{"messages": message.message,
                                                                     "time_sent": str(
                                                                         message.time_sent.hour + 1) + ":" +
                                                                                  min_str,
                                                                     "sender": sender}]
            else:
                list_of_messages[str(message.time_sent.date())] += [{"messages": message.message,
                                                                     "time_sent": str(
                                                                         message.time_sent.hour + 1) + ":" +
                                                                                  str(message.time_sent.minute),
                                                                     "sender": sender}]
        except KeyError:
            if message.time_sent.minute < 10:
                min_str = "0" + str(message.time_sent.minute)
                list_of_messages[str(message.time_sent.date())] = [{"messages": message.message,
                                                                    "time_sent": str(message.time_sent.hour + 1) + ":" +
                                                                                 min_str,
                                                                    "sender": sender}]
            else:
                list_of_messages[str(message.time_sent.date())] = [{"messages": message.message,
                                                                    "time_sent": str(message.time_sent.hour + 1) + ":" +
                                                                                 str(message.time_sent.minute),
                                                                    "sender": sender}]
            list_of_messages_id.append(str(message.time_sent.date()))
    new_digit_list = []
    for x in list_of_messages_id:
        valuations = x.split("-")
        valuation = ""
        for p in valuations:
            valuation += p
        new_digit_list.append(int(valuation))
    new_digit_list.sort()
    list_of_messages_id = []
    for z in new_digit_list:
        list_of_messages_id.append(str(str(z)[0:4] + "-" + str(z)[4:6] + "-" + str(z)[6] + str(z)[-1]))
    print(list_of_messages_id, " this is t")
    print("reached!!!")
    print(list_of_messages, " nal ne mesa")
    print(list_of_messages_id, " nal 22 24ne mesa")
    print(all_messages_in_a_chat[0].time_sent.date(), " this are the message")
    print(f"{get_chat.users.all()} certain chat")
    previous_messages_length = request.session.get("old_message_length")
    current_messages_length = len(all_messages_in_a_chat)
    if previous_messages_length is None:
        previous_messages_length = len(all_messages_in_a_chat)
    else:
        pass
    if previous_messages_length < current_messages_length:
        new_message = True
    else:
        new_message = False
    if request.session.get('private_chat_reload_num') is None:
        request.session['private_chat_reload_num'] = 1
    request.session['private_chat_reload_num'] += 1
    request.session['old_message_length'] = len(all_messages_in_a_chat)
    print("there is a new message: ", new_message)
    try:
        print("\n\n\n\n", profile_picture.url)
        new_profile_picture = profile_picture.url
    except ValueError:
        new_profile_picture = "none"
    return JsonResponse({"list_of_messages_id": list_of_messages_id, "list_of_messages": list_of_messages,
                         "new_message": new_message, 'private_chat_reload_num':
                             request.session.get('private_chat_reload_num'), "chat_id": id_chat,
                         "profile_name": profile_name, "profile_picture": new_profile_picture})


def startchat(request, id_peer):
    userId = request.session.get('userId')
    new_profile = Profile.objects.get(email=userId)
    all_user_chats = Chat.objects.filter(users__id=new_profile.id)
    for chat in all_user_chats:
        if chat.users.filter(id=id_peer).exists():
            return redirect(f"/privatechat/{chat.id}")
        else:
            pass
    new_chat = Chat()
    new_chat.save()
    new_friend = Profile.objects.get(id=id_peer)
    new_chat.users.add(new_profile)
    new_chat.users.add(new_friend)
    new_chat.save()
    new_message = Chatmessage(sender=new_profile, chat=new_chat, message="This is the beginning of a new conversation,"
                                                                         " let's chat!")
    new_message.save()
    return redirect(f"/privatechat/{new_chat.id}")


def send_message(request):
    if request.method == "GET":
        message = request.GET.get('new_message')
        print(message + " this is rel \n\n\n\n\n\n\n\n\n\n\n\n\n")
        userId = request.session.get('userId')
        new_profile = Profile.objects.get(email=userId)
        id_chat = request.session.get('private_reload_id')
        print("this is the private id session", id_chat)
        current_chat = Chat.objects.get(id=id_chat)
        new_message = Chatmessage(sender=new_profile, chat=current_chat, message=message)
        new_message.save()
    else:
        pass
    return JsonResponse({"value": "message_sent"})


def editchat(request, id_chat):
    new_chat = Chat.objects.get(id=id_chat)
    userId = request.session.get('userId')
    new_profile = Profile.objects.get(email=userId)
    user_set = new_chat.users.all()
    ratter = False
    profile_name = ""
    profile_picture = ""
    profile_background_picture = ""
    profile_status = ""
    profile_id = ""
    for x in list(user_set):
        if x.id == new_profile.id:
            ratter = True
        else:
            profile_name = x.name
            profile_picture = x.profile_picture
            profile_background_picture = x.profile_background_picture
            profile_status = x.status
            profile_id = x.id
    if not ratter:
        return redirect("/chats")
    else:
        pass
    try:
        print("\n\n\n\n", profile_picture.url)
        new_profile_picture = profile_picture
    except ValueError:
        new_profile_picture = "none"
    except:
        new_profile_picture = "none"
    try:
        print("\n\n\n\n", profile_background_picture.url)
        new_profile_background_picture = profile_background_picture
    except ValueError:
        new_profile_background_picture = "none"
    return render(request, "editchat.html", {"profile_picture": new_profile_picture, "profile_name": profile_name,
                                             "profile_id": profile_id, "chat_id": id_chat,
                                             "profile_background_picture": new_profile_background_picture,
                                             "profile_status": profile_status})


def delete_chat(request, chat_id):
    new_chat = Chat.objects.get(id=chat_id)
    new_chat.delete()
    return redirect("/chats")


def lecturer_register(request):
    userId = request.session.get('userId')
    new_profile = Profile.objects.get(email=userId)
    all_registration = new_profile.registration_set.all()
    if request.method == "POST":
        new_registration = Registration()
        course_code = request.POST['course_code']
        course_description = request.POST['course_description']
        course_unit = request.POST['course_unit']
        new_registration.course_code = course_code
        new_registration.course_unit = course_unit
        new_registration.course_description = course_description
        new_registration.lecturer = new_profile
        new_registration.save()
        messages.info(request, f'{course_code} Uploaded Sucessfully')
        return redirect("/lecturerRegister")
        pass
    else:
        return render(request, "lecturerregister.html",
                      {"all_registration": all_registration, "num_reg": len(list(all_registration))})


def deletecourse(request, course_id):
    new_course = Registration.objects.get(id=course_id)
    new_course.delete()
    messages.info(request, f'{new_course.course_code} Deleted Successfully')
    return redirect("/lecturerRegister")


def viewcourse(request, course_id):
    new_course = Registration.objects.get(id=course_id)
    list_of_student = new_course.students.all()
    return render(request, 'listofreg.html', {"course": new_course, "list_of_student": list(list_of_student),
                                              "no_of_student": len(list(list_of_student))})


def student_register(request):
    if request.method == "POST":
        search_course = request.POST['search_course']
        search_result = Registration.objects.filter(course_code__contains=search_course)
        return render(request, "studentregister.html", {"search_result": list(search_result), "is_search": True,
                                                        "No_Of_Results": len(list(search_result.all())),
                                                        "searched_course": search_course})
    else:
        return render(request, "studentregister.html")


def registercourse(request, course_id):
    userId = request.session.get('userId')
    new_profile = Profile.objects.get(email=userId)
    course = Registration.objects.get(id=course_id)
    user_register = course.students.filter(id=new_profile.id).exists()
    print(f"those course member exit: {user_register}")
    return render(request, "singleregister.html", {"user_register": user_register, "course": course})


def clickregister(request, course_id):
    userId = request.session.get('userId')
    new_profile = Profile.objects.get(email=userId)
    course = Registration.objects.get(id=course_id)
    user_register = course.students.filter(id=new_profile.id).exists()
    if not user_register:
        course.students.add(new_profile)
        course.course_length += 1
        course.save()
    elif user_register:
        course.students.remove(new_profile)
        course.course_length -= 1
        course.save()
    else:
        pass
    print(f"those course member exit: {user_register}")
    return redirect(f"/registerCourse/{course_id}")


def busier_upload(request):
    userId = request.session.get('userId')
    new_profile = Profile.objects.get(email=userId)
    new_associate = new_profile.receipt_set.all()
    all_associate = []
    for x in list(new_associate):
        all_associate.insert(0, x)
    print(all_associate)
    if request.method == "POST":
        file = request.FILES['file']
        hostel = request.POST['hostel']
        department = request.POST['department']
        purpose = request.POST['purpose']
        new_receipt = Receipt()
        new_receipt.file = file
        new_receipt.owner = new_profile
        new_receipt.hostel = hostel
        new_receipt.department = department
        new_receipt.purpose = purpose
        new_receipt.save()
        return redirect("/busierUpload")
    else:
        return render(request, "studentbusier.html", {"status": new_profile.status, "all_associate": all_associate,
                                                      "No_Of_Results": len(list(all_associate))})


def busier_authentication(request):
    request.session['busierstatus'] = False
    if request.method == "POST":
        pin = request.POST['buspin']
        if pin == "CalebElementaryBus36743":
            request.session['busierstatus'] = True
            return redirect("/busier")
        else:
            request.session['busierstatus'] = False
            messages.info(request, f'Incorrect Response!')
            return redirect("/busierAuthentication")
    return render(request, "busierlogin.html")


def busier(request):
    if not request.session.get('busierstatus'):
        return redirect("/busierAuthentication")
    else:
        pass
    request.session['first_interval'] = False
    pending_receipt = Receipt.objects.filter(status__contains="pending")
    processing_receipt = Receipt.objects.filter(status__contains="processing")
    processed_receipt = Receipt.objects.filter(status__contains="processed")
    return render(request, "busier.html")


def get_receipt(request):
    if not request.session.get('busierstatus'):
        return redirect("/busierAuthentication")
    else:
        pass
    pending_receipt = Receipt.objects.filter(status__contains="pending")
    processing_receipt = Receipt.objects.filter(status__contains="processing")
    processed_receipt = Receipt.objects.filter(status__contains="processed")
    list_of_pending = []
    list_of_processing = []
    list_of_processed = []
    for x in list(pending_receipt):
        single = {"owner_name": x.owner.name, "owner_email": x.owner.email, "owner_matric": x.owner.matric,
                  "owner_level": x.owner.level, "hostel": x.hostel, "department": x.department, "status": x.status,
                  "purpose": x.purpose, "file": x.file.url, "date": f"{x.time_sent.strftime('%d')}"
                                                                    f" {x.time_sent.strftime('%B')},"
                                                                    f" {x.time_sent.strftime('%Y')}", "id": x.id
                  }

        list_of_pending.insert(0, single)

    for x in list(processing_receipt):
        single = {"owner_name": x.owner.name, "owner_email": x.owner.email, "owner_matric": x.owner.matric,
                  "owner_level": x.owner.level, "hostel": x.hostel, "department": x.department, "status": x.status,
                  "purpose": x.purpose, "file": x.file.url, "date": f"{x.time_sent.strftime('%d')}"
                                                                    f" {x.time_sent.strftime('%B')},"
                                                                    f" {x.time_sent.strftime('%Y')}", "id": x.id
                  }

        list_of_processing.insert(0, single)

    for x in list(processed_receipt):
        single = {"owner_name": x.owner.name, "owner_email": x.owner.email, "owner_matric": x.owner.matric,
                  "owner_level": x.owner.level, "hostel": x.hostel,
                  "department": x.department, "status": x.status,
                  "purpose": x.purpose, "file": x.file.url, "date": f"{x.time_sent.strftime('%d')}"
                                                                    f" {x.time_sent.strftime('%B')},"
                                                                    f" {x.time_sent.strftime('%Y')}", "id": x.id
                  }

        list_of_processed.insert(0, single)
    reload_page = False
    if not request.session.get('first_interval'):
        request.session['first_interval'] = True
        reload_page = True
    else:
        if request.session.get('old_length_receipt_one') < len(list(list_of_pending)):
            reload_page = True
        elif request.session.get('old_length_receipt_two') < len(list(list_of_processing)):
            reload_page = True
        elif request.session.get('old_length_receipt_three') < len(list(list_of_processed)):
            reload_page = True
        else:
            pass
    '''
    print("\n Processing\n Processing\n Processing\n Processing")
    print(list_of_processing)
    print("\n Pending\n Pending\n Pending\n Pending")
    print(list_of_pending)
    print("\n Processed\n Processed\n Processed\n Processed")
    print(list_of_processed)'''
    request.session['old_length_receipt_one'] = len(list(list_of_pending))
    request.session['old_length_receipt_two'] = len(list(list_of_processing))
    request.session['old_length_receipt_three'] = len(list(list_of_processed))

    return JsonResponse({"pending_receipt": list(list_of_pending), "processing_receipt": list(list_of_processing),
                         "processed_receipt": list(list_of_processed), "first_length": len(list(list_of_pending)),
                         "second_length": len(list(list_of_processing)), "third_length": len(list(list_of_processed)),
                         "reload_page": reload_page})


def start_processing(request):
    receipt_id = request.GET.get('receipt_id')
    new_receipt = Receipt.objects.get(id=receipt_id)
    new_receipt.status = "processing"
    new_receipt.save()
    Status = True
    return JsonResponse({"Status": Status})


def cancel_receipt(request):
    receipt_id = request.GET.get('receipt_id')
    new_receipt = Receipt.objects.get(id=receipt_id)
    new_receipt.status = "processed failed"
    new_receipt.save()
    Status = True
    return JsonResponse({"Status": Status})


def download_receipt(request, receipt_id):
    new_receipt = Receipt.objects.get(id=receipt_id)
    return redirect(new_receipt.file.url)


def processed_receipts(request):
    if request.method == "GET":
        receipt_id = request.GET.get('receipt_id')
        date = request.GET.get('date')
        print(date, "\n\n\n\n")
        print(receipt_id, "\n\n\n\n")
        new_receipt = Receipt.objects.get(id=receipt_id)
        new_receipt.status = "processed successfully"
        new_receipt.collection_date = date
        new_receipt.save()
        Status = True
        return HttpResponse(status=200)
    else:
        pass


def spreadsheet(request):
    userId = request.session.get('userId')
    new_profile = Profile.objects.get(email=userId)
    if new_profile.status == "student":
        return redirect("/home")
    if request.method == "POST":
        request.session['session'] = request.POST['session']
        request.session['department'] = request.POST['department']
        request.session['mode_of_entry'] = request.POST['mode_of_entry']
        request.session['level'] = request.POST['level']
        request.session['semester'] = request.POST['semester']
        request.session['number_of_courses'] = request.POST['number_of_courses']
        request.session['description'] = request.POST['spreadsheet_description']
        return redirect("/getSingleCourse")
    else:
        list_of_spreadsheet = Spreadsheet.objects.filter(staff__id=new_profile.id)
        return render(request, "spreadsheet.html", {"list_of_spreadsheet": list_of_spreadsheet})


def get_single_courses(request):
    userId = request.session.get('userId')
    new_profile = Profile.objects.get(email=userId)
    session = request.session.get("session")
    department = request.session.get("department")
    mode_of_entry = request.session.get("mode_of_entry")
    level = int(request.session.get("level"))
    description = request.session.get("description")
    semester = int(request.session.get("semester"))
    NOC = int(request.session.get("number_of_courses"))
    NOC_List = list(range(1, int(NOC) + 1))
    if request.method == "POST":
        courses = []
        courses_files = []
        for x in NOC_List:
            course_name_x = request.POST[f"course_name_{x}"]
            course_unit_x = request.POST[f"course_unit_{x}"]
            course_file_x = request.FILES[f"course_file_{x}"]
            new_instance = [course_name_x, int(course_unit_x)]
            courses.append(new_instance)
            courses_files.append(course_file_x)
        data_set = request.FILES["data_set_file"]
        spreadsheet_instantiation = spreadsheet_engine.SpreadSheetGenerator()
        folder_name = spreadsheet_instantiation.generator(session, department, mode_of_entry, level, description, NOC,
                                                          courses, courses_files, data_set, semester)
        request.session['folder_name'] = folder_name
        new_spreadsheet = Spreadsheet()
        new_spreadsheet.staff = new_profile
        new_spreadsheet.session = session
        new_spreadsheet.department = department
        new_spreadsheet.mode_of_entry = mode_of_entry
        new_spreadsheet.level = level
        new_spreadsheet.number_of_courses = NOC
        new_spreadsheet.description = description
        new_spreadsheet.semester = semester
        spread_file = f"/RESULTSET/{folder_name}/Spreadsheet.xlsx"
        info_file = f"/RESULTSET/{folder_name}/info.txt"
        missing_file = f"/RESULTSET/{folder_name}/Missing Result List.xlsx"
        probation_file = f"/RESULTSET/{folder_name}/Probation List.xlsx"
        datasheet_file = f"/RESULTSET/{folder_name}/datasheet.xlsx"
        new_spreadsheet.spreadsheet = spread_file
        new_spreadsheet.info = info_file
        new_spreadsheet.missing_result = missing_file
        new_spreadsheet.probation = probation_file
        new_spreadsheet.datasheet = datasheet_file
        new_spreadsheet.save()
        return redirect(f"/spreadsheetResult/{new_spreadsheet.id}")
    else:
        return render(request, "getsinglecourses.html", {"NOC": list(range(1, NOC + 1))})


def spreadsheet_result(request, spreadsheet_id):
    new_spreadsheet = Spreadsheet.objects.get(id=spreadsheet_id)
    return render(request, "spreadsheetresult.html", {"spreadsheet": new_spreadsheet})


def logout(request):
    auth.logout(request)
    return redirect('/login')
