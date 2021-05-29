from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from django.contrib.auth.models import User
from .models import userinfo,getlisted,searchdb,locality,city,userquery
import json as simplejson
from django.http import HttpResponse

# Create your views here.
def hompepageview(request):
    #loads the homepage or userhomepage
    if not request.user.is_authenticated:
        return render(request,'homepage.html')
    else:
        return redirect('userhomepage')

def adminloginview(request):
    #loads the login page for admin
    if not request.user.is_authenticated:
        return render(request,'adminlogin.html')
    else:
        return redirect("adminhomepage")


def userloginview(request):
    #loads the user login page
    return render (request,"userlogin.html")

def faqview(request):
    #loads the faq page
    return render (request,"faq.html")

def aboutandcontactview(request):
    #loads the about and contact page
    return render (request,"about.html")

def adminhomepageview(request):
    if not request.user.is_authenticated:
        return redirect('adminloginpage')
    return render (request,"adminhomepage.html")

def authenticateadmin(request):
    #function to authenticate admin login
    username=request.POST['username']
    password=request.POST['password']
    #authentication
    user = authenticate(username=username, password=password)
    #if the user exists
    if user is not None and user.is_superuser==True:
        #login code
        login(request,user)
        return redirect('adminhomepage')
    #if the user does not exist
    elif user is None:
        messages.add_message(request,messages.ERROR,"Invalid credentials")
        return redirect ('adminloginpage')
    else:
        messages.add_message(request,messages.ERROR,"Superuser account needed")
        return redirect ('adminloginpage')

def logoutadmin(request):
    #code for logout from admin panel
    logout(request)
    return redirect('adminloginpage')

def signupview(request):
    #code to render the signup page
    return render (request,"signup.html")

def signup(request):
    #code for adding user to the database
    firstname=request.POST['firstname']
    lastname=request.POST['lastname']
    username=request.POST['username']
    password=request.POST['password']
    email=request.POST['email']
    dob=request.POST['dob']
    phone=request.POST['phone']
    securityquestion=request.POST['securityquestion']
    securityanswer=request.POST['securityanswer']
    #if the user already exists or username is taken
    if User.objects.filter(username=username).exists():
        messages.add_message(request,messages.ERROR,"Username taken or User already exists")
        return redirect ('signup')
    #if user does not exist
    else:
        User.objects.create_user(username=username,password=password,first_name=firstname,last_name=lastname,email=email).save
        userinfo(username=username,dob=dob,phone=phone,securityquestion=securityquestion,securityanswer=securityanswer).save()
        messages.add_message(request,messages.SUCCESS,"Account created! You can now Login")
        return redirect('signup')

def userhomepageview(request):
    #loading the user homepage
    if not request.user.is_authenticated:
        return redirect('userloginpage')
    username=request.user.username
    context={'username':username}
    return render (request,"userhomepage.html",context)
    
def userauthenticate(request):
    #authenticating the user
    username=request.POST['username']
    password=request.POST['password']

    user= authenticate(username=username,password=password)

    #if user exists
    if user is not None:
        login(request,user)
        return redirect('userhomepage')
    
    #if user does not exists
    if user is None:
        messages.add_message(request,messages.ERROR,"Invalid credentials")
        return redirect('userloginpage')

def userlogout(request):
    #code for logout from user homepage
    logout(request)
    return redirect('homepage')

def resetpasswordview(request):
    #code for loading password reset page
    return render(request,"resetpassword.html")

def reset(request):
    #code for resetting the password
    username=request.POST['username']
    new_password=request.POST['password']
    question=request.POST['securityquestion']
    answer=request.POST['securityanswer']
    user=User.objects.filter(username=username)
    if user is not None:
        if userinfo.objects.filter(username=username).exists():
            u=User.objects.get(username=username,is_superuser=False)
            udata=userinfo.objects.get(username=username)
            if udata.securityquestion==question and udata.securityanswer==answer:
                u.set_password(new_password)
                u.save()
                messages.add_message(request,messages.SUCCESS,"Password Changed Successfully")
                return render(request,"resetpassword.html")
            else:
                messages.add_message(request,messages.SUCCESS,"Invalid credentials")
                return render(request,"resetpassword.html")
        else:
            messages.add_message(request,messages.ERROR,"User does not exist")
            return render(request,"resetpassword.html")
    
    else:
        messages.add_message(request.messages.ERROR,"User does not exist")
        return render(request.META['HTTP_REFERER'])

def profilepage(request):
    #code to load the profile page of the user
    username=request.user.username
    firstname=request.user.first_name
    lastname=request.user.last_name
    email=request.user.email
    datejoined=request.user.date_joined
    data=userinfo.objects.filter(username=username)
    context={'username':username,'firstname':firstname,'lastname':lastname,'email':email,'datejoined':datejoined,'datas':data}
    return render(request,"profilepage.html",context)

def getlistedview(request):
    #code to load listing form
    if not request.user.is_authenticated:
        messages.add_message(request,messages.INFO,"Please Login first")
        return redirect('userloginpage')
    else:
        context={'cities':city.objects.all()}
        return render(request,'getlisted.html',context)

def getlistedformsubmit(request):
    # code to submit the listing request form data for approval in admin panel
    username=request.user.username
    city=request.POST['selectcities']
    locality=request.POST['selectlocalities']
    shopname=request.POST['shopname']
    shopaddress=request.POST['shopaddress']
    shopcontact=request.POST['shopcontact']
    shopimage=request.FILES['img']
    #if the user has already submitted a request
    if getlisted.objects.filter(username=username).exists():
        messages.add_message(request,messages.ERROR,"You have already submitted a request. Check Status from Homepage.")
        return redirect ('getlisted')
    else:
        u=getlisted(username=username,shopname=shopname,city=city,locality=locality,shopaddress=shopaddress,shopcontact=shopcontact,shopimage=shopimage)
        u.save()
        messages.add_message(request,messages.SUCCESS,"Your Request Has been submitted")
        return redirect ('getlisted')

def submissionstatus(request):
    #code to retrieve status page after submission
    username=request.user.username
    if getlisted.objects.filter(username=username).exists():
        infos=getlisted.objects.filter(username=username)
        context={'infos':infos}
        return render(request,"submissionstatus.html",context)
    else:
        messages.add_message(request,messages.INFO,"Please apply for listing to check the status.")
        return redirect('getlisted')

def searchview(request):
    #code to fetch search query and show search results page
    if not request.user.is_authenticated:
        messages.add_message(request,messages.INFO,"Please Login first")
        return redirect('userloginpage')
    else:
        context={'cities':city.objects.all()}
        return render (request,"search.html",context)

def adminrequests(request):
    #code to retrieve the admin panel approval requests page
    requests=getlisted.objects.filter(status="PENDING")
    context={'requests':requests}
    return render(request,"approvalrequests.html",context)

def userqueries(request):
    #code to retrieve the user queries for admin
    queries=userquery.objects.filter(status="NOT RESPONDED")
    context={'queries':queries}
    return render(request,"userqueries.html",context)

def listingapprove(request,listingpk):
    #Approving listing request and adding data to search db
    u=getlisted.objects.get(id=listingpk)
    searchdb(username=u.username,city=u.city,locality=u.locality,shopname=u.shopname,shopaddress=u.shopaddress,shopcontact=u.shopcontact,shopimage=u.shopimage).save()
    u.status="APPROVED"
    u.save()
    return redirect('approvalrequests')

def listingreject(request,listingpk):
    #Rejecting a listing request 
    u=getlisted.objects.filter(id=listingpk)[0]
    u.status="REJECTED"
    u.save()
    return redirect('approvalrequests')

def getdetails(request):
    #code for dependent drop down menu in search console
    city_name = request.GET['cnt']
    print("ajax " + str(city_name))

    result_set = []
    all_cities = []

    answer = str(city_name)
    selected_city = city.objects.get(name=answer)
    print("selected city name " + str(selected_city))


    all_localities = selected_city.locality_set.all()
    for locality in all_localities:
        result_set.append({'name': locality.name})
        print("locality name " + str(locality.name))
    return HttpResponse(simplejson.dumps(result_set), content_type='application/json')

def searchresult(request):
    #code for accepting input from user and displaying results
    city_fetch=request.POST['selectcities']
    locality=request.POST['selectlocalities']
    results=searchdb.objects.filter(city=city_fetch,locality=locality)
    context={'results': results,'cities':city.objects.all()}
    return render(request,"search.html",context)

def searchprofile(request,profilepk):
    #loading the profile page of a shop
    profileresult=searchdb.objects.filter(id=profilepk)
    context={'results':profileresult}
    return render(request,"searchprofile.html",context)

def contactview(request):
    #load the contact us page for user to submit queries
    return render(request,"contactpage.html")

def adminaddshopview(request):
    #code to render admin panel add shop function
    context={'cities':city.objects.all()}
    return render(request,'adminaddshop.html',context)

def adminaddshops(request):
    #code to add the shop data from admin side to the search db
    username=request.POST['username']
    city_fetch=request.POST['selectcities']
    locality=request.POST['selectlocalities']
    shopname=request.POST['shopname']
    shopaddress=request.POST['shopaddress']
    shopcontact=request.POST['shopcontact']
    shopimage=request.FILES['img']
    #if the user has already submitted a request
    if getlisted.objects.filter(username=username).exists():
        messages.add_message(request,messages.ERROR,"User has already submitted their request please check the listing approvals.")
        return render (request,'adminaddshop.html')
    else:
        u=searchdb(username=username,shopname=shopname,city=city_fetch,locality=locality,shopaddress=shopaddress,shopcontact=shopcontact,shopimage=shopimage)
        u.save()
        messages.add_message(request,messages.SUCCESS,"Shop added successfully")
        return render (request,'addminaddshop.html')

def adminlocations(request):
    #code to render the edit locations page from the admin panel
    context={'cities':city.objects.all(),'localities':locality.objects.all()}
    return render(request,'editlocations.html',context)

def addlocation(request):
    #code to add the city and locality to their respective databases
    city_fetch=request.POST['city']
    locality_fetch=request.POST['locality']
    #if the city already exists
    if city.objects.filter(name=city_fetch).exists():
        if locality.objects.filter(name=locality_fetch).exists():
            #code that will run if both city and locality already exist
            messages.add_message(request,messages.ERROR,"City and locality already exist")
            return redirect('editlocations')
        else:
            #code that will run if the city exists but locality does not exist
            cityget=city.objects.get(name=city_fetch)
            locality(name=locality_fetch,city_id=cityget.id).save()
            messages.add_message(request,messages.SUCCESS,"Locality Added successfully")
            return redirect('editlocations')
    else:
        #code that will run if both don't exist
        city(name=city_fetch).save()
        cityget=city.objects.get(name=city_fetch)
        locality(name=locality_fetch,city_id=cityget.id).save()
        messages.add_message(request,messages.SUCCESS,"City and Locality Added successfully")
        return redirect ('editlocations')

def deletelocality(request,deletepk):
    #code to delete a city or locality
    localitydb=locality.objects.get(id=deletepk)
    localitydb.delete()
    context={'cities':city.objects.all(),'localities':locality.objects.all()}
    return render(request,"editlocations.html",context)

def deletecity(request,deletepk):
    #code to delete a city or locality
    citydb=locality.objects.get(id=deletepk)
    citydb.delete()
    context={'cities':city.objects.all(),'localities':locality.objects.all()}
    return render(request,"editlocations.html",context)

def querysubmit(request):
    #accept user query and add it to the query database
    email=request.POST['email']
    username=request.POST['username']
    query=request.POST['query']
    #if the user already has a query pending
    if userquery.objects.filter(username=username,email=email,status="NOT RESPONDED").exists():
        messages.add_message(request,messages.INFO,"You have already one query pending, please wait while we respond to it. ")
        return redirect('contactus')
    #if the user is submitting a new query
    else:
        userquery(username=username,email=email,query=query).save()
        messages.add_message(request,messages.INFO,"Your query has been submitted. Please wait while we respond")
        return redirect('contactus')

def queryresponded(request,querypk):
    #when the admin responds to a query and marks it responded
    q=userquery.objects.get(id=querypk)
    q.status="RESPONDED"
    q.save()
    return redirect('adminqueries')

def querydelete(request,querypk):
    #if the admin wishes to delete a query
    q=userquery.objects.get(id=querypk)
    q.delete()
    return redirect('adminqueries')

