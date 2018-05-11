from django.conf.urls import url, include
from . import views

app_name = 'videos'

urlpatterns = [

    #login
    url(r'^$', views.LoginFormView.as_view(), name='login'),
    #Logout
    url(r'logout/', views.logout, name='logout'),
    #indexview
    url(r'index/', views.indexView, name='index'),

    url(r'register/', views.UserFormView.as_view(), name='register'),

    url(r'subject/', views.SubjFormView.as_view(), name='subr'),
    #studentindex
    url(r'studentlogin/$', views.studentView, name='studentsview'),
    #facultyindex
    url(r'facultylogin/$', views.facultyView, name='facultyview'),
    #cordinatorview
    url(r'cordinatorlogin/$', views.cordView, name='cordview'),
    #uploadView
    url(r'add/', views.upload, name='add'),
    #delete_object
    url(r'delete/(?P<video_id>(.*?))$', views.delete, name='delete'),
    #search_object
    url(r'search/', views.search, name='search'),
    #player
    url(r'player/(?P<video_id>(.*?))$', views.player, name='player'),
    #filter
    url(r'filter/(?P<sub>[0-9]+)$', views.filter, name='filter'),
    #rfilter
    url(r'rated/(?P<sub>[0-9]+)$', views.rated, name='rated'),
    #rate
    url(r'rate/(?P<video>(.*?))$', views.rate, name='rate'),
    #facrated
    url(r'facrated/$', views.facrated, name='facrated'),
    #gen report
    url(r'gen/', views.gen, name='gen'),

    url(r'udel/', views.udel, name='udel'),

    url(r'rem/', views.rem, name='rem'),

    url(r'delsub/', views.sdel, name='sdel'),

    url(r'tsub/', views.tdel, name='tdel'),

]
