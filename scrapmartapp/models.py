from django.db import models

# Create your models here.
class userinfo(models.Model):
    username=models.CharField(max_length=10)
    dob=models.DateField()
    phone=models.CharField(max_length=10)
    securityquestion=models.CharField(max_length=50)
    securityanswer=models.CharField(max_length=50)
 
class getlisted(models.Model):
    username=models.CharField(max_length=10)
    city=models.CharField(max_length=20)
    locality=models.CharField(max_length=30)
    shopname=models.CharField(max_length=100)
    shopaddress=models.CharField(max_length=500)
    shopcontact=models.CharField(max_length=12)
    shopimage=models.ImageField(upload_to ='uploads/')
    status=models.CharField(max_length=20,default="PENDING")

class searchdb(models.Model):
    username=models.CharField(max_length=10)
    city=models.CharField(max_length=20)
    locality=models.CharField(max_length=30)
    shopname=models.CharField(max_length=100)
    shopaddress=models.CharField(max_length=500)
    shopcontact=models.CharField(max_length=12)
    shopimage=models.ImageField(upload_to ='searchdb/')

class locality(models.Model):
    name = models.CharField(max_length=50)
    city = models.ForeignKey("city", on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    def __unicode__(self):
        return u'%s' % (self.name)


class city(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

    def __unicode__(self):
        return u'%s' % (self.name)

class userquery(models.Model):
    email=models.CharField(max_length=50)
    username=models.CharField(max_length=100)
    query=models.CharField(max_length=5000)
    status=models.CharField(max_length=20,default="NOT RESPONDED")


