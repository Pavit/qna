from django.db import models
from facepy import GraphAPI
from django.contrib.auth.models import User
from django.utils.translation import gettext as _
from django.db.models.signals import post_save
from datetime import date, datetime
from django.contrib.auth.signals import user_logged_in


class Education(models.Model):
    school_id = models.CharField(max_length=200, blank=True, null=True)
    school_name = models.CharField(max_length=200, blank=True, null=True)
    school_type = models.CharField(max_length=200, blank=True, null=True)
    year = models.CharField(max_length=200, blank=True, null=True)


class Concentration(models.Model):
    conc_id = models.CharField(max_length=200, blank=True, null=True)
    conc_name = models.CharField(max_length=200, blank=True, null=True)
    education = models.ForeignKey(Education)


class UserProfile(models.Model):
    #populated by facebook
    user = models.OneToOneField(User, blank=True, null=True)
    username = models.CharField(max_length=128, unique=False, blank=True, null=True)
    name = models.CharField(max_length=128, unique=False, blank=True, null=True)
    first_name = models.CharField(max_length=200, blank=True, null=True)
    last_name = models.CharField(max_length=200, blank=True, null=True)
    locale = models.CharField(max_length=200, blank=True, null=True)
    gender = models.CharField(max_length=200, blank=True, null=True)
    hometown = models.CharField(max_length=200, blank=True, null=True)
    location = models.CharField(max_length=200, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    birthday = models.DateTimeField(blank=True, null=True)
    timezone = models.CharField(max_length=200, blank=True, null=True)
    relationship_status = models.CharField(max_length=200, blank=True, null=True)
    religion = models.CharField(max_length=200, blank=True, null=True)
    political = models.CharField(max_length=200, blank=True, null=True)
    educations = models.ManyToManyField(Education)
    fb_id = models.CharField(max_length=200, null=True, blank = True)
    fb_access_token = models.CharField(max_length=200, null = True, blank = True)
    work_position_id = models.CharField(max_length=200, blank=True, null=True)
    work_position_name = models.CharField(max_length=200, blank=True, null=True)
    work_start_date = models.CharField(max_length=200, blank=True, null=True)
    work_location_id = models.CharField(max_length=200, blank=True, null=True)
    work_location_name = models.CharField(max_length=200, blank=True, null=True)
    work_employer_id = models.CharField(max_length=200, blank=True, null=True)
    work_employer_name = models.CharField(max_length=200, blank=True, null=True)
    friends = models.ManyToManyField('self')
    fb_id = models.CharField(max_length=200, null=True, blank = True)
    fb_access_token = models.CharField(max_length=200, null = True, blank = True)
    ### Stuff we calculate
    created_at = models.DateTimeField(auto_now_add = True)
    last_login = models.DateTimeField(blank=True, null=True)
    updated_time = models.DateTimeField(blank=True, null=True)
    age = models.IntegerField(blank=True, null=True)
    agegroup = models.CharField(max_length=200, blank=True, null=True)
    #placeholder for region
    region = models.CharField(max_length=200, blank=True, null=True)

    def _get_total_votes(self):
        total=0
        for q in self.submissions.all():
            total+=q.total_vote.count
        return total
    total_votes=property(_get_total_votes)

    def populate_graph_info(self):
        # self.fb_access_token = request.user.social_auth.get(provider='facebook').extra_data["access_token"]
        graphinfo = GraphAPI(self.fb_access_token).get('me/')
        print graphinfo
        if "id" in graphinfo: self.fb_id = graphinfo["id"]
        if "name" in graphinfo: self.username = graphinfo["name"]
        if "first_name" in graphinfo: self.first_name = graphinfo["first_name"]
        if "last_name" in graphinfo: self.last_name = graphinfo["last_name"]
        if "gender" in graphinfo: self.gender = graphinfo["gender"]
        if "email" in graphinfo: self.email = graphinfo["email"]
        if "birthday" in graphinfo:
            self.birthday = datetime.strptime(graphinfo["birthday"], "%m/%d/%Y")
            today = date.today()
            self.age = today.year - self.birthday.year
            if today.month < self.birthday.month or today.month == self.birthday.month and today.day < self.birthday.day:
                self.age -= 1
            self.agegroup = ">56"
            if self.age<56:  self.agegroup="46-55"
            if self.age<46:  self.agegroup="36-45"
            if self.age<36:  self.agegroup="26-35"
            if self.age<26:  self.agegroup="16-25"
            if self.age<16:  self.agegroup="<15"
        if "timezone" in graphinfo: self.timezone = graphinfo["timezone"]
        if "hometown" in graphinfo: self.hometown = graphinfo["hometown"]
        if "location" in graphinfo: self.location = graphinfo["location"]
        if "work" in graphinfo:
            self.work_position_id = graphinfo["work"][0]["position"]["id"]
            self.work_position_name = graphinfo["work"][0]["position"]["name"]
            self.work_start_date = graphinfo["work"][0]["start_date"]
            self.work_location_id = graphinfo["work"][0]["location"]["id"]
            self.work_location_name = graphinfo["work"][0]["location"]["name"]
            self.work_employer_id = graphinfo["work"][0]["employer"]["id"]
            self.work_employer_name = graphinfo["work"][0]["employer"]["name"]
        if "education" in graphinfo:
                for item in graphinfo["education"]:
                    newed = Education.objects.create()
                    if "school" in item:
                        newed.school_id = item["school"]["id"]
                        newed.school_name = item["school"]["name"]
                    if "type" in item: newed.school_type = item["type"]
                    if "year" in item: newed.year = item["year"]["name"]
                    newed.save()
                    if "concentration" in item:
                        for conc in item["concentration"]:
                            newconc = Concentration.objects.create(education = newed)
                            newconc.conc_id = conc["id"]
                            newconc.conc_name = conc["name"]
                            newconc.save()
                    newed.save()
                    self.educations.add(newed)
        self.save()
        return self

    def check_friends(self):
        friendlist = GraphAPI(self.fb_access_token).get('me/friends')
        frienddict = friendlist["data"]
        #check if user's friends are already members of the site
        compare_list = []
        user_fb_ids = UserProfile.objects.values_list('fb_id', flat=True).order_by('fb_id')
        friend_fb_ids = []
        for friend in frienddict:
            friend_fb_ids.append(friend["id"])
            matches = UserProfile.objects.filter(fb_id__in=friend_fb_ids)
        try:
            for match in matches:
                self.friends.add(match)
        except:
            pass
        self.save()
        return self


def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)
        instance.userprofile.populate_graph_info()
        instance.save()

post_save.connect(create_user_profile, sender=User)


def update_user_profile(sender, request, user, **kwargs):
    user.userprofile.populate_graph_info()
    user.userprofile.check_friends()
    print "signal went through"
    user.save()

user_logged_in.connect(update_user_profile, sender=User)
