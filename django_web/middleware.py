from ccblog.models import User
from django.http import HttpResponse


class ccBlogMiddleware(object):
    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization.
 
    def __call__(self, request):
        # Code to be executed for each request before the view (and later middleware) are called.

        # print request.META['HTTP_HOST']+ request.META['PATH_INFO'] + request.META['QUERY_STRING']
        if request.path != '/login/' and request.path != '/':
            userSession = request.session.get('userid', default=None)
            if userSession is None:
                return HttpResponse('<h1>Forbidden, please login</h1><a href=''http://'+request.get_host() + '/login>login</a>')
                
        response = self.get_response(request)

        # Code to be executed for each request/response after the view is called.
        if request.POST and request.path == '/login/':
            print request.method
            username = request.POST['username']
            password = request.POST['password']

            if User.objects.filter(phone=username).filter(password=password).exists():
                user = User.objects.get(phone=username)
                count = user.loginCount
                user.loginCount = count+1
                user.save()
 
        return response
