"""
Definition of urls for Django.
"""
from django.contrib import admin
from django.conf.urls import include, url
from app import views as app_views

from django.conf import settings
from django.views.static import serve
# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = [
    # Examples:
    # url(r'^$', Django.views.home, name='home'),
    # url(r'^Django/', include('Django.Django.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    #url(r'^', admin.site.urls),
    url(r'^student_course_find$',app_views.student_course_find),
    url(r'^student_exame_find$',app_views.student_exame_find),
    url(r'^student_grade_find$',app_views.student_grade_find),
    url(r'^teacher_course_find$',app_views.teacher_course_find),
    url(r'^captcha',app_views.updata_captcha),
    url(r'^login$',app_views.login),
    url(r'^section_course_find$',app_views.section_course_find),
    url(r'^get_section_course$',app_views.get_section_course),
    url(r'^class_course_find$',app_views.class_course_find),
    url(r'^get_class_course$',app_views.get_class_course),
    url(r'^school_calendar$',app_views.school_calendar),
    url(r'^school_car$',app_views.school_car),
    url(r'^trip$',app_views.trip),
    url(r'^file$',app_views.file),
    url(r'^need_file',app_views.need_file),
    url(r'^upload$',app_views.upload),
    url(r'^app$',app_views.app),
    url(r'static/(?P<path>.*)$',serve,{'document_root':settings.STATIC_ROOT}),
    url(r'media/(?P<path>.*)$',serve,{'document_root':settings.MEDIA_ROOT})
    
    ]
