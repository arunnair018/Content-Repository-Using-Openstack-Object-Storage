from django.shortcuts import render,redirect
from django.views import generic
from django.views.generic import View
from django.views.generic.edit import CreateView
from django.contrib.auth.models import User,Group
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.contrib.auth.views import login
from django.conf import settings as set
from .forms import LoginForm,DocumentForm,UserForm,SubjForm
from .models import Video,Subject,Exp
import swiftclient

######################Login()###########################################
class LoginFormView(View):
    username=''
    form_class = LoginForm
    template_name = 'auth/index.html'

    def get(self,request):
        if request.session.has_key('username'):
          return redirect('videos:index')
        else :
            form = self.form_class(None)
            return render(request, self.template_name, {'form':form,})

    def post(self, request):
        p="Credentials not correct! Try again."
        form = self.form_class(request.POST)
        user = authenticate(username=request.POST['username'].lower(), password=request.POST['password'])

        if user is not None:
            if user.groups.filter(name='faculty').exists():
                if user.is_active:
                    login(request, user)
                    username = us
                    request.session['username'] = username
                    request.session['userid'] = 'fac'
                    return redirect('videos:index')
            elif user.groups.filter(name='coursecordinator').exists():
                if user.is_active:
                    login(request, user)
                    username = user.username
                    request.session['username'] = username
                    request.session['userid'] = 'cc'
                    return redirect('videos:index')
            else :
                if user.is_active:
                    login(request, user)
                    username = user.username
                    request.session['username'] = username
                    request.session['userid'] = 'st'
                    return redirect('videos:index')
        else :
            return render(request, self.template_name, {'form':form,'p':p})

        return render(request, self.template_name, {'form':form,})

################################################################################

class UserFormView(View):
    form_class = UserForm
    template_name = 'auth/signup.html'
    def get(self,request):
        form = self.form_class(None)
        return render(request, self.template_name, {'form':form,})

    def post(self, request):
        p=""
        form = self.form_class(request.POST)

        if form.is_valid():
            user = form.save(commit=False)

            user.username = form.cleaned_data['username'].lower()
            password = form.cleaned_data['password']
            user.set_password(password)
            group = form.cleaned_data['groups']
            user.save()
            user.groups.add(group)
            p="User Added!"

        return render(request, self.template_name, {'form':form,'p':p})

###############################################################################

class SubjFormView(View):
    form_class = SubjForm
    template_name = 'auth/sub.html'

    def get(self,request):
        form = self.form_class(None)
        return render(request, self.template_name, {'form':form,})

    def post(self, request):
        form = self.form_class(request.POST)

        if form.is_valid():
            form.save()

        return render(request, self.template_name, {'form':form,})

################Logout()########################################################
def logout(request):
    try:
        del request.session['username']
        del request.session['userid']
        conn.close()
    except:
        pass
    return redirect('videos:login')
########################indexes()###############################################
def indexView(request):
    if request.session.has_key('userid'):
        userid = request.session['userid']
        if userid == 'fac':
            return redirect('videos:facultyview')
    if request.session.has_key('userid'):
        userid = request.session['userid']
        if userid == 'st':
            return redirect('videos:studentsview')
    if request.session.has_key('userid'):
        userid = request.session['userid']
        if userid == 'cc':
            return redirect('videos:register')

###########swiftauth()##########################################################
def swiftauth():
    conn = swiftclient.Connection(set.SWIFT_AUTH_URL,set.SWIFT_USERNAME,set.SWIFT_KEY,auth_version=set.SWIFT_AUTH_VERSION,tenant_name=set.SWIFT_TENANT_NAME)
    return conn

###############views()##########################################################

def facultyView(request):
    if request.session.has_key('userid'):
        username = request.session['userid']
        if request.session['userid'] == 'fac':
            x = Video.objects.filter(faculty=request.user)
            y = Subject.objects.all()
            return render(request, 'videos/fac.html', {"username" : request.user , 'x':x, 'sub':y})
    else:
        return redirect('/')

def studentView(request):
    if request.session.has_key('username'):
        username = request.session['username']
        if request.session['userid'] == 'st':
            x = request.user.video_set.all()
            return render(request, 'videos/yupload.html', {"username" : request.user , 'x':x})
    else:
        return redirect('/')

def cordView(request):
    if request.session['userid'] == 'cc':
        return render(request,'cordinator/cord.html')
    else:
        return redirect('/')    

############upload()############################################################
def upload(request):
    if request.session['userid'] == 'st':
        if request.method == 'POST':
            form = DocumentForm(request.POST, request.FILES)
            if form.is_valid():
                new = form.save(commit=False)
                new.owner = request.user
                new.save()
                return redirect('/')
        else:
            form = DocumentForm()
        return render(request, 'videos/upload.html', {
            'form': form,'username':request.user,
        })
    else:
        return redirect('/')

############delete()########################################################
def delete(request,video_id):
    video = Video.objects.get(file_file=video_id)
    # return render(request,'videos/test.html',{'a':video,'b':request.session['username']})
    if str(video.owner) == str(request.session['username']):
        conn = swiftauth()
        try:
            conn.delete_object(set.SWIFT_CONTAINER_NAME,video_id)
        except:
            pass
        video.delete()
        return redirect('videos:studentsview')
    else:
        return redirect('/')
##########search()#############################################################

def search(request):
    if request.session.has_key('userid'):
        userid = request.session['userid']
        title = request.GET.get("q")
        try:
            y = Exp.objects.get(name=title)
            if userid == 'fac':
                x = Video.objects.filter(video_title=y.id,faculty=request.user)
                return render(request,'videos/search.html',{'x':x,'username':request.user})
            else:
                x = Video.objects.filter(video_title=y.id,owner=request.user)
                return render(request,'videos/studentsearch.html',{'x':x,'username':request.user})
        except:
            p = "No such videos..."
            if userid == 'fac':
                return render(request,'videos/search.html',{'p':p,'username':request.user})
            else:
                return render(request,'videos/yupload.html',{'p':p,'username':request.user})
    else:
        return redirect('/')
#################player()########################################################

def player(request,video_id):
    if request.session.has_key('userid'):
        userid = request.session['userid']
        video = Video.objects.filter(file_file=video_id)
        if userid == 'fac':
            return render(request,'videos/player.html',{'video':video,'username':request.user})
        if userid == 'st':
                return render(request,'videos/stplayer.html',{'video':video,'username':request.user})
    else:
        return redirect('/')
######################filter()##################################################
def filter(request,sub):
    if request.session.has_key('userid'):
        if request.session['userid'] == 'fac':
            x = Video.objects.filter(faculty=request.user,subject=sub)
            y = Subject.objects.all()
            return render(request, 'videos/fac.html', {"username" : request.session['username'] , 'x':x, 'sub':y})
    else:
        return redirect('/')

def rated(request,sub):
    if request.session.has_key('userid'):
        if request.session['userid'] == 'fac':
            m = Video.objects.filter(faculty=request.user,subject=sub)
            n = Subject.objects.all()
            return render(request,'videos/facrated.html', {"username" : request.session['username'] , 'x':m, 'sub':n})
    else:
        return redirect('/')

#################rate()#########################################################
def rate(request,video):
    if request.session.has_key('userid'):
        if request.session['userid'] == 'fac':
            x = Video.objects.get(file_file=video)
            x.rating=request.GET.get('rate')
            x.comment=request.GET.get('comment')
            x.redo=request.GET.get('redo')
            x.save()
        else:
            return redirect('/')
    return redirect('videos:facrated')
################facrated########################################################
def facrated(request):
    if request.session.has_key('userid'):
        username = request.session['userid']
        if request.session['userid'] == 'fac':
            x = Video.objects.filter(faculty=request.user)
            y = Subject.objects.all()
            return render(request, 'videos/facrated.html', {'username':request.user , 'x':x, 'sub':y})
        if request.session['userid'] == 'st':
            x = request.user.video_set.all()
            return render(request, 'videos/strated.html', {"username" : request.user , 'x':x})
    else:
        return redirect('/')
########################generate()###############################################
def gen(request):
    if request.session.has_key('userid'):
        username = request.session['userid']
        if request.session['userid'] == 'fac':
            if request.GET.get('subj'):
                x = Video.objects.filter(faculty=request.user,subject=request.GET.get('subj'),redo=False).order_by('owner','subject','video_title')
                y = Subject.objects.all()
                return render(request, 'videos/gen.html', {"username" : request.user , 'x':x,'sub':y})
            else:
                x = Video.objects.filter(faculty=request.user,redo=False).order_by('owner','subject','video_title')
                y = Subject.objects.all()
                return render(request, 'videos/gen.html', {"username" : request.user , 'x':x,'sub':y})
    else:
        return redirect('/')

######################delete user#################################################

def udel(request):
    if request.session.has_key('userid'):
        if request.session['userid'] == 'cc':
            fac = Group.objects.get(name="faculty").user_set.all()
            stu = Group.objects.get(name="student").user_set.all()
            return render(request,'cordinator/udelete.html',{'fac':fac,'stu':stu,})
    else:
        return redirect('/')

def rem(request):
    if request.session.has_key('userid'):
        if request.session['userid'] == 'cc':
            u = request.GET.get('u')
            x=User.objects.get(username=u)
            x.delete()
            return redirect('videos:udel')
    else:
        return redirect('/')

def tdel(request):
    if request.session.has_key('userid'):
        if request.session['userid'] == 'cc':
            sub = Subject.objects.all()
            return render(request,'cordinator/tdel.html',{'sub':sub,})
    else:
        return redirect('/')

def sdel(request):
    if request.session.has_key('userid'):
        if request.session['userid'] == 'cc':
            u = request.GET.get('z')
            x=Subject.objects.get(name=u)
            x.delete()
            return redirect('videos:tdel')
    else:
        return redirect('/')
