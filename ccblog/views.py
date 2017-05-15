from django.shortcuts import render
from ccblog.models import User
from ccblog.models import BlogType
from ccblog.models import Blog
from django.http import JsonResponse

def login(request):
    if request.method == 'POST':
        username=request.POST['username']
	password=request.POST['password']
	if username=='' or password=='':
	    return render(request, "ccblog/login.html", {"message":"input username and password!"})

        #13888888888   123
        user = User.objects.filter(phone=username).values('id','name' , 'phone', 'password')
        if list(user)!=[]:
            correctPassword=list(user)[0]['password']
            if correctPassword==password:
                context={}
                context['username'] = username
                #context['name'] = list(user)[0]['name']
                context['message'] = 'login success!'
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
        blogtype = BlogType.objects.filter(userId=userid).values('userId', 'id', 'typeName').order_by("typeName")
        return JsonResponse(list(blogtype), safe=False)
    else:
        return render(request, "ccblog/login.html")

def user_blog(request):
    userid = request.session.get('userid',default=None)
    blogtypeid = 0
    if request.GET.get('blogtypeid')!=None:
        blogtypeid = request.GET['blogtypeid']
    
    if userid!=None:
        blog = Blog.objects.filter(userId=userid, blogTypeId=blogtypeid).values('userId','blogTypeId','title','content','createTime').order_by("createTime")
        return JsonResponse(list(blog), safe=False)
    else:
        return render(request, "ccblog/login.html")

