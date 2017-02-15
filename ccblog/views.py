from django.shortcuts import render
from ccblog.models import User
from ccblog.models import BlogType

def login(request):
    if request.method == 'POST':
        username=request.POST['username']
	password=request.POST['password']
	if username=='' or password=='':
	    return render(request, "ccblog/login.html", {"message":"input username and password!"})

        user = User.objects.filter(phone=username).values('id', 'phone', 'password')
        if list(user)!=[]:
            correctPassword=list(user)[0]['password']
            if correctPassword==password:
                context={}
                context['username'] = username
                context['message'] = 'login success!:'
                request.session['username'] = username
                request.session['userid'] = list(user)[0]['id']
                return render(request, "ccblog/home.html", context)
            else:
                return render(request, "ccblog/login.html",{"message":"wrong password!"})
        else:
            return render(request, "ccblog/login.html",{"message":"wrong username!"})
        
    if request.method == 'GET':
        userSession = request.session.get('username',default=None)
        if userSession!=None:
            context={}
            context['username'] = userSession
            context['message'] = 'login success!:'
            return render(request, "ccblog/home.html", context)
        
    return render(request, "ccblog/login.html")

def logout(request):
    username = request.session.get('username',default=None)
    if username!=None:
        del request.session['username']
        
    userid = request.session.get('userid',default=None)
    if userid!=None:
        del request.session['userid']
            
    return render(request, "ccblog/login.html")


def user_blogtype(request):
    userid = request.session.get('userid',default=None)
    if userid!=None:
        BlogType.objects.filter(userId=userid).values('userId', 'id', 'typeName')
    else:
        return render(request, "ccblog/login.html")

