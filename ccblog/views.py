from django.shortcuts import render
from ccblog.models import User
from ccblog.models import BlogType
from ccblog.models import Blog
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

def login(request):
    if request.method == 'POST':
        username=request.POST['username']
	password=request.POST['password']
	if username=='' or password=='':
	    return render(request, "ccblog/login.html", {"message":"input username and password!"})

        #13888888888   123
        user = User.objects.filter(phone=username).values('id','name' , 'phone', 'password', 'loginCount')
        if list(user)!=[]:
            correctPassword=list(user)[0]['password']
            if correctPassword==password:
                context={}
                context['username'] = username
                #context['name'] = list(user)[0]['name']
                context['message'] = 'login success!'
                context['loginCount'] = list(user)[0]['loginCount']
                request.session['username'] = username
                request.session['userid'] = list(user)[0]['id']
                request.session['loginCount'] = list(user)[0]['loginCount']
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
            context['loginCount'] = request.session.get('loginCount',default=None)
            context['message'] = 'login success!'
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

@csrf_exempt
def user_addblogtype(request):
    if request.method == 'POST':
        name=request.POST['name']
        if name=='':
	    return JsonResponse({"code":-1,"msg":"blog type name can not be empty!"}, safe=False)

        userid = request.session.get('userid',default=None)
        if userid!=None:
            if BlogType.objects.filter(userId=userid,typeName=name).exists():
                return JsonResponse({"code":-1,"msg":"blog type name exists!"}, safe=False)
            else:
                newtype = BlogType(userId=userid,typeName=name)
                newtype.save()
                return JsonResponse({"code":1,"msg":"add blog type success!"}, safe=False)
        else:
            return render(request, "ccblog/login.html")

@csrf_exempt
def user_delblogtype(request):
     if request.method == 'POST':
        blogtypeid=request.POST['id']
        if blogtypeid=='':
	    return JsonResponse({"code":-1,"msg":"id can not be empty!"}, safe=False)

        userid = request.session.get('userid',default=None)
        if userid!=None:
            blogtype = BlogType.objects.filter(userId=userid,id=blogtypeid).all()
            if(len(list(blogtype))>0):
                if Blog.objects.filter(userId=userid, blogTypeId=blogtypeid).exists():
                    return JsonResponse({"code":-1,"msg":"blogs in this type!"}, safe=False)
                
                blogtype[:1][0].delete()
                return JsonResponse({"code":1,"msg":"delete blog type success!"}, safe=False)
                
            else:
                return JsonResponse({"code":-1,"msg":"blog type not exists!"}, safe=False)
        else:
            return render(request, "ccblog/login.html")

@csrf_exempt
def user_editblogtype(request):
     if request.method == 'POST':
        blogtypeid=request.POST['id']
        name=request.POST['name']
        if blogtypeid=='' or name=='':
	    return JsonResponse({"code":-1,"msg":"id and name can not be empty!"}, safe=False)

        userid = request.session.get('userid',default=None)
        if userid!=None:
            blogtype = BlogType.objects.filter(userId=userid,id=blogtypeid).all()
            if(len(list(blogtype))>0):
                if(BlogType.objects.filter(userId=userid,typeName=name).exclude(id=blogtypeid).exists()):
                    return JsonResponse({"code":-1,"msg":"blog type name exists!"}, safe=False)
                
                #BlogType.objects.filter(userId=userid,id=blogtypeid).update(typeName=name)
                editblogtype = blogtype[:1][0]
                editblogtype.typeName=name
                editblogtype.save()
                return JsonResponse({"code":1,"msg":"edit blog type success!"}, safe=False)
                
            else:
                return JsonResponse({"code":-1,"msg":"blog type not exists!"}, safe=False)
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

