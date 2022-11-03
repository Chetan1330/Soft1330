# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from importlib.resources import path
from django import template
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.urls import reverse
from django.conf import settings

from django.contrib.auth.models import User
import datetime
import io
from django.core.files.base import ContentFile
from pathlib import Path
from docxtpl import DocxTemplate
from django.core.files import File
import urllib, mimetypes
from django.http import HttpResponse, Http404, StreamingHttpResponse, FileResponse
import os
from django.conf import settings
from wsgiref.util import FileWrapper


from django.shortcuts import redirect, render
from django.contrib import messages
from .models import Folder,File,Img,upload,userprofile
@login_required(login_url="/login/")
def index(request):
    print("User id:",request.user.email)
    u = User.objects.get(id=request.user.id)
    usrinfo = userprofile.objects.filter(usr=request.user.id)
    # for val in usrinfo:
    #     val.delete()
    print("Password is:",u.password)
    # usrinfo = userprofile.objects.get(id=request.user.id)
    # print("Firstname is:",usrinfo.firstName)
    folder = Folder.objects.filter(folderuser=request.user)
    image = Img.objects.filter(filetitle=request.user.id)
    # print("Media root:",file_path11)
    imgurl = []
    if image:
        for img11 in image:
            imgurl.append(img11.file.url.split('/mediafiles')[1])
        # print("Image is:",img11.file.url.split('/mediafiles')[1])
        # print("IMGURL:",imgurl[0])
        # print("IMGURL",imgurl[0])
        # media_root = getattr(settings, 'MEDIA_ROOT', None)
        # if image:
        #     image.delete()
        # print(media_root)
        context = {'folder':folder,'segment':'index','image':"static" + imgurl[0]}
        #return render(request,'home/index.html',context)
        #context = {'segment': 'index'}
        
        print(datetime.datetime.now().strftime ("%I:%M%p on %B %d, %Y"))
        html_template = loader.get_template('home/index.html')
        return HttpResponse(html_template.render(context, request))
    
    else:
        context = {'folder':folder,'segment':'index'}
        html_template = loader.get_template('home/index.html')
        return HttpResponse(html_template.render(context, request))

# Folder with files in it
def folder(request,folderid):
    global folder_name
    global f_id
    f_id = folderid
    folder_user = Folder.objects.get(id=folderid)
    folder_name = folder_user.foldername
    print(folder_user.foldername)

    file_path11 = settings.STATIC_ROOT + '/' + request.user.email + '/' + folder_name
    files = File.objects.filter(folder=folder_user)
    lstdir = os.listdir(file_path11)

    # if os.path.exists(file_path11):
    #     for x in os.listdir(file_path11):
    #         print(x)

    image = Img.objects.filter(filetitle=request.user.id)
    # print("Media root:",file_path11)
    imgurl = []
    for img11 in image:
        imgurl.append(img11.file.url.split('/mediafiles')[1])

    print(len(files),len(lstdir))
    ext = []
    for i in range(len(files)):
        # print(files[i].filetitle.split('.')[1])
        # print("Date is:",files[i].date)
        ext.append([files[i],files[i].filetitle.split('.')[1],files[i].date])
    
    dirfiles = []
    for i in range(len(lstdir)):
        # print(files[i].filetitle.split('.')[1])
        dirfiles.append([lstdir[i],lstdir[i].split('.')[1]])
    print(dirfiles)
    print(ext)
    context = {'folderid':folderid,'files':files,'ext':ext,'dirfiles':dirfiles,'image':"static" + imgurl[0]}
    # file_user = request.FILES.get('file')
    # for f in file_user:
    #     print("Files:",f)

    if request.method == 'POST':
        # file_user = request.FILES.get('file')
        # file_title = request.POST.get('filetitle')
        # fileadd = File.objects.create(filetitle=file_user.name,file=file_user,folder=folder_user)
        
        folder_name = folder_user.foldername 
        folder_desc = folder_user.folderdesc
        print("Folder Desc:",folder_desc)
        # folder = Folder.objects.create(foldername=folder_name,folderdesc=folder_desc,folderuser=request.user)
        # folder.save()
        #file_title = request.FILES['file']
        file_user = request.FILES.getlist('file')
        file_path11 = settings.STATIC_ROOT + '/' + request.user.email + '/' + folder_name
        fpath = settings.STATIC_ROOT
        file_path = settings.MEDIA_ROOT +'/template1.docx'
        for f in file_user:
            # file_title = request.POST.get('filetitle')
            fileadd = File.objects.create(filetitle=f.name,file=f,folder=folder_user)

            

            # if os.path.exists(file_path11):
            #     continue
                # tpl = DocxTemplate(file_path)
                # context = {"title":"Chetan"}
                # tpl.render(context)
                # tpl.save(file_path11 + "/" + "%s.docx" %str(f.name).split('.')[0].replace(" ", "_"))
                # print("File name:",str(f.name).split('.')[0].replace(" ", "_"))
        if not os.path.exists(file_path11):
            os.makedirs(file_path11)
            tpl = DocxTemplate(file_path)
            context = {"title":"Chetan"}
            tpl.render(context)
            tpl.save(file_path11 + "/" + "%s.docx" %str("Output"))
                # print("File name:",str(f.name).split('.')[0].replace(" ", "_"))
        # return redirect("folder",folderid=int(folderid))'image':"static" + imgurl[0]
        return redirect(reverse('folder',folderid=int(folderid), kwargs={ 'image':"static" + imgurl[0] }))
    return render(request,'home/folder.html',context)

# Delete Folder with files in it
def delete(request,deleteid):
    
    folder_user = Folder.objects.get(id=deleteid)
    folder_name = folder_user.foldername
    files = File.objects.filter(folder=folder_user)
    files.delete()
    folder_user.delete()
    context = {'folder':folder,'segment':'index'}

    return redirect("index")

# Delete Folder with files in it
def fdelete(request,fileid):
    
    file_user = File.objects.get(id=fileid)
    # folder_name = folder_user.foldername
    # files = File.objects.filter(folder=folder_user)
    file_user.delete()
    # folder_user.delete()
    context = {'folder':folder,'segment':'index'}

    return redirect("folder",folderid=int(f_id))


# Folder with files in it
def image(request):
    
    # image_user = Img.objects.get(id=folderid)
    # files = File.objects.filter(folder=folder_user)
    # context = {'folderid':folderid,'files':files}
    image = Img.objects.filter(filetitle=request.user.id)
    imgurl = []
    if image:
        for img11 in image:
            imgurl.append(img11.file.url.split('/mediafiles')[1])
    # usrinfo = userprofile.objects.get(id=request.user.id)
    usrinfo = userprofile.objects.filter(usr=request.user.id)
    # print("Firstname is:",usrinfo.firstName)
    context = {'segment':'account-settings.html'}
    if image:
        image.delete()
    if usrinfo:
        usrinfo.delete()
    if request.method == 'POST':

        usr = request.POST  
        firstName = str(usr.dict()['firstName'])
        print("Firstname is:",firstName)
        lastName = str(usr.dict()['lastName'])
        choicesgender = str(usr.dict()['choices-gender'])
        choicesmonth = str(usr.dict()['choices-month'])
        
        choicesday = str(usr.dict()['choices-day'])
        choicesyear = str(usr.dict()['choices-year'])
        email = str(usr.dict()['email'])
        confirmation = str(usr.dict()['confirmation'])
        location = str(usr.dict()['location'])
        phone = str(usr.dict()['phone'])
        choiceslanguage = str(usr.dict()['choices-language'])
        skill = str(usr.dict()['skill'])
        print("Skill is:",skill)

        file_user = request.FILES.get('imgfile')
        fileadd = Img.objects.create(filetitle=request.user.id,file=file_user)
        if usrinfo:
            userprofile.objects.update(usr=str(request.user.id),firstName=firstName,lastName=lastName,choicesgender=choicesgender,
                        choicesmonth=choicesmonth,choicesday=choicesday,choicesyear=choicesyear,email=email,
                        confirmation=confirmation,location=location,phone=phone,choiceslanguage=choiceslanguage,
                        skill=skill)
            context['firstName']     = firstName
            context['lastName']     = lastName
            context['choicesgender']     = choicesgender
            context['choicesmonth']     = choicesmonth
            context['choicesday']     = choicesday
            context['choicesyear']     = choicesyear
            context['email']     = email
            context['location']     = location
            context['phone']     = phone
            context['choiceslanguage']     = choiceslanguage
            context['skill']     = skill


            image = Img.objects.filter(filetitle=request.user.id)
            imgurl = []
            if image:
                for img11 in image:
                    imgurl.append(img11.file.url.split('/mediafiles')[1])
            context['image'] = "static" + imgurl[0]
        
            # context['segment']     = segment
            # context['active_menu'] = active_menu
            return render(request,"home/account-settings.html",context)
            
        else:
            userprofile.objects.create(usr=str(request.user.id),firstName=firstName,lastName=lastName,choicesgender=choicesgender,
                        choicesmonth=choicesmonth,choicesday=choicesday,choicesyear=choicesyear,email=email,
                        confirmation=confirmation,location=location,phone=phone,choiceslanguage=choiceslanguage,
                        skill=skill)
            context['firstName']     = firstName
            context['lastName']     = lastName
            context['choicesgender']     = choicesgender
            context['choicesmonth']     = choicesmonth
            context['choicesday']     = choicesday
            context['choicesyear']     = choicesyear
            context['email']     = email
            context['location']     = location
            context['phone']     = phone
            context['choiceslanguage']     = choiceslanguage
            context['skill']     = skill

            image = Img.objects.filter(filetitle=request.user.id)
            imgurl = []
            if image:
                for img11 in image:
                    imgurl.append(img11.file.url.split('/mediafiles')[1])
            context['image'] = "static" + imgurl[0]
        
            # context['segment']     = segment
            # context['active_menu'] = active_menu
            return render(request,"home/account-settings.html",context)
            

        context['firstName']     = firstName
        context['lastName']     = lastName
        context['choicesgender']     = choicesgender
        context['choicesmonth']     = choicesmonth
        context['choicesday']     = choicesday
        context['choicesyear']     = choicesyear
        context['email']     = email
        context['location']     = location
        context['phone']     = phone
        context['choiceslanguage']     = choiceslanguage
        context['skill']     = skill
        
        image = Img.objects.filter(filetitle=request.user.id)
        imgurl = []
        if image:
            for img11 in image:
                imgurl.append(img11.file.url.split('/mediafiles')[1])
        context['image'] = "static" + imgurl[0]
    
        # context['segment']     = segment
        # context['active_menu'] = active_menu
        return render(request,"home/account-settings.html",context)
    # return redirect('/account-settings.html')

def userform(request):
    if request.method == 'POST':
        usr = request.POST           
        usrname = usr.dict()['firstName']
        # lastName = usr.dict()['lastName']
        # choicesgender = usr.dict()['choices-gender']
        # choicesmonth = usr.dict()['choices-month']
        # choicesday = usr.dict()['choices-day']
        # choicesyear = usr.dict()['choices-year']
        email = usr.dict()['email']
        confirmation = usr.dict()['confirmation']
        password11 = usr.dict()['password']
        confirmpass = usr.dict()['confirpass']
        # location = usr.dict()['location']
        # phone = usr.dict()['phone']
        # choiceslanguage = usr.dict()['choices-language']
        # skill = usr.dict()['skill']
        
        u1 = User.objects.create(username=usrname,email=email)
        u1.set_password(password11)
        # print("Firstname is:",choicesmonth)
        # is_private = 'is_private' in request.POST
        # print(is_private)
        return redirect('/userform.html')


# Add Folder View
def addfolder(request):
    # folder_user = Folder.objects.get(id=folderid)
    # files = File.objects.filter(folder=folder_user)
    # context = {'folderid':folderid,'files':files}
    CORE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    
    if request.method == 'POST':
        # global folder_name
        folder_name = request.POST['foldername']
        folder_desc = request.POST['desc']
        print("Folder Desc:",folder_desc)
        folder = Folder.objects.create(foldername=folder_name,folderdesc=folder_desc,folderuser=request.user)
        folder.save()
        #file_title = request.FILES['file']
        file_user = request.FILES.getlist('file')
        file_path11 = settings.STATIC_ROOT + '/' + request.user.email + '/' + folder_name
        fpath = settings.STATIC_ROOT
        file_path = settings.MEDIA_ROOT +'/template1.docx'

        for f in file_user:
            # file_title = request.POST.get('filetitle')
            fileadd = File.objects.create(filetitle=f.name,file=f,folder=folder)
            

            

            # if os.path.exists(file_path11):
            #     tpl = DocxTemplate(file_path)
            #     context = {"title":"Chetan"}
            #     tpl.render(context)
            #     tpl.save(file_path11 + "/" + "%s.docx" %str(f.name).split('.')[0].replace(" ", "_"))
                # print("File name:",str(f.name).split('.')[0].replace(" ", "_"))
        if not os.path.exists(file_path11):
            os.makedirs(file_path11)
            tpl = DocxTemplate(file_path)
            context = {"title":"Chetan"}
            tpl.render(context)
            tpl.save(file_path11 + "/" + "%s.docx" %str("Output"))
                # print("File name:",str(f.name).split('.')[0].replace(" ", "_"))

            
            # file_bytes = io.BytesIO()
            # File.save('file', ContentFile(file_bytes.read()))
            # fileadd1 = File.objects.create(filetitle=f.name,file=ContentFile(file_bytes.read()),folder=folder)
            # fileadd1.save('file', ContentFile(file_bytes.read()))
            # upload.save('file', ContentFile(file_bytes.read()))

        # if os.path.exists(file_path11):
        #     for x in os.listdir(file_path11):
        #         print("Files are:",x)
        #         # file = open(os.path.join(file_path11, x),'rb')
        #         file = open(os.path.join(file_path11))
        #         assert os.path.isfile(file_path11 + '/' + str(x))
        #         with open(os.path.join(file_path11 + '/' + str(x)), 'r') as f11:
        #             print(f11)
        #             file_bytes = io.BytesIO()
        #             fileadd = File.objects.create(filetitle=x,file=ContentFile(file_bytes.read()),folder=folder)
        #             # fileadd.save()
        # for f in file_user:  
        if folder:
            return redirect("index")
        else:
            messages.error(request,"Folder Not Created")
            return redirect("index")


@login_required(login_url="/login/")
def pages(request):
    context = {}
    image = Img.objects.filter(filetitle=request.user.id)
    imgurl = []
    if image:
        for img11 in image:
            imgurl.append(img11.file.url.split('/mediafiles')[1])

            # context = {'image':"static" + imgurl[0],}
            # segment, active_menu = get_segment( request )
            # context
            # context['segment']     = segment
            # context['active_menu'] = active_menu

    usrinfo = userprofile.objects.filter(usr=request.user.id)
    if usrinfo:
        print("TRue")
    else:
        print("False")
    # frmval = []
    # for val in usrinfo:
    #     frmval.append
    #     print("First name:",val.firstName[0])
    print("First name:",usrinfo)
    # All resource paths end in .html.
    # Pick out the html file name from the url. And load that template.
    try:

        load_template = request.path.split('/')[-1]
        print("Load temp:",load_template)

        if str(load_template).endswith("docx"):
            # if request.method == 'POST':
            print("YESELKLHK")
            # print(request.POST['foldername'])
            print("Folder name:",folder_name)
            file_path11 = settings.STATIC_ROOT + '/' + request.user.email + '/' + folder_name + '/' + load_template
            file_wrapper = FileWrapper(open(file_path11,'rb'))
            file_mimetype = mimetypes.guess_type(file_path11)
            response = HttpResponse(file_wrapper, content_type=file_mimetype )
            response['X-Sendfile'] = file_path11
            response['Content-Length'] = os.stat(file_path11).st_size
            response['Content-Disposition'] = 'attachment; filename=' + load_template
            return response


        if str(load_template).endswith("txt"):
            print("YESELKLHK")
            file_path = settings.MEDIA_ROOT +'/files/'+ load_template
            file_wrapper = FileWrapper(open(file_path,'rb'))
            file_mimetype = mimetypes.guess_type(file_path)
            response = HttpResponse(file_wrapper, content_type=file_mimetype )
            response['X-Sendfile'] = file_path
            response['Content-Length'] = os.stat(file_path).st_size
            response['Content-Disposition'] = 'attachment; filename=' + load_template
            return response

        if load_template == 'admin':
            return HttpResponseRedirect(reverse('admin:index'))
 	
        if load_template == 'account-settings.html':
            
            # usrinfo = userprofile.objects.get(id=request.user.id)
            # # userinfo = userprofile.objects.filter(user=request.user.email)
            # # usrinfo = userprofile.objects.get(id=request.user.id)
            # # usrinfo = userprofile.objects.get(id=request.user.id)
                
            # # print(userprofile.objects.get(id=request.user.id))
            if usrinfo:
                uinfo = []
                for u in usrinfo:
                    print(u.firstName)

                    context['firstName']     = u.firstName
                    context['lastName']     = u.lastName
                    context['choicesgender']     = u.choicesgender
                    context['choicesmonth']     = u.choicesmonth
                    context['choicesday']     = u.choicesday
                    context['choicesyear']     = u.choicesyear
                    context['email']     = u.email
                    context['location']     = u.location
                    context['phone']     = u.phone
                    context['choiceslanguage']     = u.choiceslanguage
                    context['skill']     = u.skill

                    context['image'] = "static" + imgurl[0]
                    segment, active_menu = get_segment( request )
        
                    context['segment']     = segment
                    context['active_menu'] = active_menu
                    
                    
                    html_template = loader.get_template('home/' + load_template)
                    return HttpResponse(html_template.render(context, request))
                    # uinfo.append(img11.file.url.split('/mediafiles')[1])
            #     print("First name:",usrinfo.firstName)
            #     print("Firstname is:",firstName)
            #     # if usrinfo:
            #     firstName = usrinfo.firstName
            #     lastName = usrinfo.lastName
            #     choicesgender = usrinfo.choicesgender
            #     choicesmonth = usrinfo.choicesmonth
            #     choicesday = usrinfo.choicesday
            #     choicesyear = usrinfo.choicesyear
            #     email = usrinfo.email
            #     confirmation = usrinfo.confirmation
            #     location = usrinfo.location
            #     phone = usrinfo.phone
            #     choiceslanguage = usrinfo.choiceslanguage
            #     skill = usrinfo.skill


                    
            # print("Username is:",userinfo.get('firstName'))
                # html_template = loader.get_template('home/' + load_template)
                # return HttpResponse(html_template.render(context, request))

            if request.method == "POST":
                # print("account setting")
                # usr = request.POST  
                # usermail = request.user.email       
                # firstName = str(usr.dict()['firstName'])
                # lastName = str(usr.dict()['lastName'])
                # choicesgender = str(usr.dict()['choices-gender'])
                # choicesmonth = str(usr.dict()['choices-month'])
                # choicesday = str(usr.dict()['choices-day'])
                # choicesyear = str(usr.dict()['choices-year'])
                # email = str(usr.dict()['email'])
                # confirmation = str(usr.dict()['confirmation'])
                # location = str(usr.dict()['location'])
                # phone = str(usr.dict()['phone'])
                # choiceslanguage = str(usr.dict()['choices-language'])
                # skill = str(usr.dict()['skill'])
                curpass = request.POST['curpass']
                newpass = request.POST['newpass']
                newpass1 = request.POST['newpass1']
                print("CurrrPass is:",curpass)
                
                # if firstName:
                #     usrinfo = userprofile.objects.get(id=request.user.id)
                #     if usrinfo:
                #         userprofile.objects.create(user=usermail,firstName=firstName,lastName=lastName,choicesgender=choicesgender,
                #         choicesmonth=choicesmonth,choicesday=choicesday,choicesyear=choicesyear,email=email,
                #         confirmation=confirmation,location=location,phone=phone,choiceslanguage=choiceslanguage,
                #         skill=skill)
                #     userprofile.objects.create(user=usermail,firstName=firstName,lastName=lastName,choicesgender=choicesgender,
                #     choicesmonth=choicesmonth,choicesday=choicesday,choicesyear=choicesyear,email=email,
                #     confirmation=confirmation,location=location,phone=phone,choiceslanguage=choiceslanguage,
                #     skill=skill)

                
                u = User.objects.get(id=request.user.id)
                if str(u.check_password(curpass)) == "False":
                    segment, active_menu = get_segment( request )
                    context = {"msg":"False",'image':"static" + imgurl[0],'segment':"account-setting.html"}
                        # context = {}
                    context['segment']     = segment
                    context['active_menu'] = active_menu
                    return render(request,"home/account-settings.html",context)
                if str(u.check_password(curpass)) == "True":
                    if str(newpass) == str(newpass1):
                        u.set_password(newpass)
                        u.save()
                        return redirect("/account-settings.html")

                    if str(newpass) != str(newpass1):
                        segment, active_menu = get_segment( request )
                        context = {"msg":"mismatch",'image':"static" + imgurl[0],'segment':"account-setting.html"}
                        # context = {}
                        context['segment']     = segment
                        context['active_menu'] = active_menu
                        return render(request,"home/account-settings.html",context)
            
            segment, active_menu = get_segment( request )
            # context = {"firstName":firstName,"lastName":lastName,"choicesgender":choicesgender,"choicesmonth":choicesmonth,
            #             "choicesday":choicesday,"choicesyear":choicesyear,"email":email,"location":location,
            #             "phone":phone,"choiceslanguage":choiceslanguage,"skill":skill,'segment':"account-setting.html"}
            # context = {}
            context['segment']     = segment
            context['active_menu'] = active_menu
            return render(request,"home/account-settings.html",context)

        segment, active_menu = get_segment( request )
        
        context['segment']     = segment
        context['active_menu'] = active_menu
        
        
        html_template = loader.get_template('home/' + load_template)
        return HttpResponse(html_template.render(context, request))

    except template.TemplateDoesNotExist:

        html_template = loader.get_template('home/page-404.html')
        return HttpResponse(html_template.render(context, request))

    except:
        html_template = loader.get_template('home/page-500.html')
        return HttpResponse(html_template.render(context, request))

# Helper - Extract current page name from request 
def get_segment( request ): 

    try:

        segment     = request.path.split('/')[-1]
        active_menu = None

        if segment == '' or segment == 'index.html':
            segment     = 'index'
            active_menu = 'dashboard'

        if segment.startswith('dashboards-'):
            active_menu = 'dashboard'

        if segment.startswith('account-') or segment.startswith('users-') or segment.startswith('profile-') or segment.startswith('projects-'):
            active_menu = 'pages'

        if  segment.startswith('notifications') or segment.startswith('sweet-alerts') or segment.startswith('charts.html') or segment.startswith('widgets') or segment.startswith('pricing'):
            active_menu = 'pages'            

        return segment, active_menu     

    except:
        return 'index', 'dashboard'  
