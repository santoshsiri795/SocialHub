
from django.core.paginator import Paginator
from .form import ProfileForm
from .models import LikePost, Profile,Post,Comment,FriendRequest
from django.shortcuts import redirect, render
from django.contrib.auth.models import User,auth
from django.contrib import messages
from django.contrib.auth.decorators import login_required

@login_required(login_url='login')
def home(request):
    user_info = Profile.objects.get(user=request.user)
    contact_list = Post.objects.all()
    paginator = Paginator(contact_list, 4)

    page_number = request.GET.get('page')
    posts = paginator.get_page(page_number)
    context = {
        'posts':posts,
        'user_info':user_info,
    

    }
    return render(request,'index.html',context)


@login_required(login_url='login')
def profile(request,pk):

    user_profile = Profile.objects.get(id=pk)

    context = {
        'user_profile':user_profile
    }
    return render(request,'profile.html',context)

def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        try:
            user =User.objects.get(username=username)
            user = auth.authenticate(username=username,password=password)
            if user is not None:
                auth.login(request,user)
                return redirect('home')
            else :
                messages.error(request, 'Password is incorrect')
        except:
            messages.info(request,'User not Found')

        return redirect('home')
    return render(request,'login.html',)



def register(request):
    if request.method == 'POST':
        first_name =  request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password1 = request.POST['password1']
        if password==password1 :
            if User.objects.filter(username=username).exists():
                messages.info(request,"User Name Already Exist")
            elif User.objects.filter(email=email).exists():
                messages.info(request,'Email Already Taken')
            else :
                user = User.objects.create_user(first_name=first_name,last_name=last_name,username=username,email=email,password=password)
                user.save()
                user_login = auth.authenticate(username=username,password=password)
                auth.login(request,user_login)
                user_model = User.objects.get(username=username)
                name = first_name + ' ' + last_name
                email=email
                new_profile = Profile.objects.create(user=user_model,name=name,email=email)
                new_profile.save()
                username = request.POST['username']
                password = request.POST['password']
                user = auth.authenticate(username=username,password=password)
                auth.login(request,user)
                return redirect('home')

        else : 
            messages.info(request,"Password not Match")
        
    return render(request,'register.html')
def logout(request):
    auth.logout(request)
    return redirect('home')

def upload_post(request):
    user_info = Profile.objects.get(user=request.user)
    if request.method == 'POST':
        desc = request.POST['desc']
        post_img = request.FILES.get('post_img')
        user = user_info
        new_post = Post.objects.create(user=user,desc=desc,post_img=post_img)
        new_post.save()
        return redirect('home')
    return redirect('home')

def comment(request,pk):
    user_info = Profile.objects.get(user=request.user)
    post_info = Post.objects.get(id=pk)
    if request.method == 'POST':
        txt = request.POST['txt']
        user = user_info
        post_commnet = post_info
        new_comment = Comment.objects.create(txt=txt,user=user,post_commnet=post_commnet)
        new_comment.save()
        return redirect('home')
    return redirect('home')
def edit_profile(request):


    user_info = Profile.objects.get(user=request.user)
    form = ProfileForm(instance=user_info)
    if request.method == 'POST':
        form = ProfileForm(request.POST,request.FILES,instance=user_info)
        if form.is_valid():
            form.save()
            return redirect('edit_profile')

    context = {
        'user_info':user_info,
        'form':form
    }
    return render(request,'edit_profile.html',context)

def edit_profile_pic(request):

    if request.method == 'POST':
        profilepic = request.FILES.get('profilepic')
        new_pic =Profile.objects.get(user=request.user)
        new_pic.profilepic = profilepic
        new_pic.save()
        return redirect('edit_profile')
    return redirect('edit_profile')

def edit_profile_thumb(request):

    if request.method == 'POST':
        thumbimg = request.FILES.get('thumbimg')
        new_pic =Profile.objects.get(user=request.user)
        new_pic.thumbimg= thumbimg
        new_pic.save()
        return redirect('edit_profile')
    return redirect('edit_profile')
def inbox(request):


    user_info = request.user.profile
    inbox = user_info.msg.all()
    msgcount = inbox.filter(isread=False).count()

    context = {
        'inbox': inbox,
        'msgcount':msgcount,
        'user_info':user_info
    }
    return render(request,'inbox.html',context)
def like_post(request):
    user = request.user
    if request.method == 'POST':
        user=request.user
        post_id =request.POST.get('post_id')
        
        post_like =Post.objects.get(id=post_id)
        if user in post_like.liked.all():
            post_like.liked.remove(user)
        else:
            post_like.liked.add(user)
           
        # like , created  = LikePost.objects.get_or_create(user=user,post=post_like)
        # if not created:
        #     if like.value == 'True':
        #         like.value='False'
        #     else :
        #         like.value ='True'
        # like.save()
    return redirect('home')
def send_friend_request(request):
    if request.method == 'POST':
        user_id =request.POST['user_id']
        current_path =request.POST['current_path']
        receiver_profile = Profile.objects.get(id=user_id)
        sender_profile = Profile.objects.get(user=request.user)
        if request.user not in sender_profile.friend_request.all() and request.user not in receiver_profile.friend_request.all():
            sender_profile.friend_request.add(receiver_profile.user)
            friend_request = FriendRequest.objects.create(sender=sender_profile.user,receiver=receiver_profile.user)
            friend_request.save()
            return redirect(current_path)

        else :
            messages.info(request,'Request Already Sent')
            return redirect('profile/'+ user_id)
 
    return redirect('profile/'+ user_id)


def accept_friend_request(request):
    if request.method == 'POST':
        user_id =request.POST['user_id']
        current_path =request.POST['current_path']
        friend_profile = Profile.objects.get(id=user_id)
        my_profile = Profile.objects.get(user=request.user)
        decline_request = FriendRequest.objects.filter(sender=friend_profile.user,receiver=my_profile.user)
        decline_request.delete()
        friend_profile.friend_request.remove(my_profile.user)
        friend_profile.friends.add(my_profile.user)
        my_profile.friends.add(friend_profile.user)
        
        return redirect(current_path)

    
def decline_friend_request(request):
    if request.method == 'POST':
        user_id =request.POST['user_id']
        friend_profile = Profile.objects.get(id=user_id)
        current_path =request.POST['current_path']
        my_profile = Profile.objects.get(user=request.user)
        decline_request = FriendRequest.objects.filter(sender=friend_profile.user,receiver=my_profile.user)
        decline_request.delete()    
        friend_profile.friend_request.remove(my_profile.user)
        return redirect(current_path)

    return redirect(current_path)

def un_friend(request):
    if request.method == 'POST':
        user_id =request.POST['user_id']
        current_path =request.POST['current_path']
        friend_profile = Profile.objects.get(id=user_id)

        my_profile = Profile.objects.get(user=request.user)
        friend_profile.friends.remove(my_profile.user)
        my_profile.friends.remove(friend_profile.user)
        return redirect(current_path)

    return redirect(current_path)

def cancel_friend_request(request):
    if request.method == 'POST':
        user_id =request.POST['user_id']
        current_path =request.POST['current_path']
        receiver_profile = Profile.objects.get(id=user_id)
        sender_profile = Profile.objects.get(user=request.user)
        decline_request = FriendRequest.objects.filter(sender=sender_profile.user,receiver=receiver_profile.user)
        decline_request.delete()    
        print(FriendRequest.objects.filter(sender=sender_profile.user,receiver=receiver_profile.user),'**************************************************************************************8')
        
        if request.user not in sender_profile.friend_request.all() and request.user not in receiver_profile.friend_request.all():
            sender_profile.friend_request.remove(receiver_profile.user)
            return redirect(current_path)

    return redirect(current_path)


def request_list(request):

    user_profile = Profile.objects.get(user=request.user)
    Friend_request =FriendRequest.objects.filter(receiver=request.user)
    context = {
        'user_profile':user_profile,
        'Friend_request':Friend_request
    }
    return render(request,'request_list.html',context)