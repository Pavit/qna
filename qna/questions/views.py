from django.shortcuts import render_to_response, redirect, get_object_or_404
from django.template import RequestContext
from django.http import HttpResponseRedirect, HttpResponse
from django.db.models import Q, Count
from django import forms
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.core.urlresolvers import reverse
from django.utils import simplejson
from django.forms.formsets import formset_factory, BaseFormSet
from django.core.context_processors import csrf
from questions.models import Question, Answer, Vote
from questions.forms import QuestionForm, AnswerForm, StatForm
from questions.utils import *
from django.core import serializers
from qna.settings import FACEBOOK_APP_ID, FACEBOOK_API_SECRET
from facepy import GraphAPI
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.template import loader
from questions.utils import render_block_to_string
import math

# def current_question(request, current_question_id):
#     p = int(request.GET.get('page', 1))
#     if p == 1:
#         title = 'Welcome to my site'
#         content = mark_safe('Hi, <a href="/?page=2">Click me</a>')
#     else:
#         title = 'Loaded via AJAX'
#         content = 'Impressive, now try forward and back buttons'
#     c = {'title': title, 'content': content}
#     return TemplateResponse(request, 'page.html', c, ajax_blocks=('title', 'content'))


def index(request):
    current_question = Question.objects.all().order_by('?')[:1].get()
    return HttpResponseRedirect(reverse('questions.views.current_question', args=(current_question.id,)))

def facebook_login_success(request):
    access_token = request.GET.get("access_token")
    fb_id=GraphAPI(access_token).get('me/')["id"]
    try:
        user = User.objects.get(username=fb_id)
        print "got use"
    except:
        user = User.objects.create_user(fb_id)
    user.userprofile.fb_access_token=access_token
    print "ok"
    user.userprofile.populate_graph_info()
    user.save()
    user.backend = 'django.contrib.auth.backends.ModelBackend'
    login(request, user)
    print user.userprofile
    current_question = Question.objects.all().order_by('?')[:1].get()
    return HttpResponseRedirect(reverse('questions.views.current_question', args=(current_question.id,)))


# def index(request):
#     if request.user.is_authenticated():
#         current_question = Question.objects.all().order_by('?')[:1].get()
#         return HttpResponseRedirect(reverse('questions.views.current_question', args=(current_question.id,)))
#     else:
#         current_question = Question.objects.all().order_by('?')[:1].get()
#         return render_to_response("index.html", {"current_question": current_question,}, context_instance = RequestContext(request))

def sunburstplay(request):
    return render_to_response("sunburstplay.html")

def ajax_view(request):
    # some random context
    context = Context({'items': range(100)})
    # passing the template_name + block_name + context
    return_str = render_block_to_string('current_question.html', 'current_question', context)
    return HttpResponse(return_str)


def current_question(request, current_question_id):
    current_question = get_object_or_404(Question, pk=current_question_id)
    next_question = Question.objects.filter(~Q(id = current_question.id)).order_by('?')[:1].get()
    print "WTF"
    if request.is_ajax():
        print "vote is ajax"
        print current_question
        context = Context({'current_question': current_question})
        return_str = render_block_to_string('current_question.html', 'current_question', context)
        return HttpResponse(return_str)
        # return TemplateResponse(request, 'current_question.html', {"current_question": current_question.question}, ajax_blocks=('current_question'))
        # return render_to_response("view_question.html", {"current_question":current_question}, context_instance = RequestContext(request))
    return render_to_response("current_question.html", {"current_question": current_question, "next_question": next_question}, context_instance = RequestContext(request))


def previous_question(request, previous_question_id):
    previous_question = get_object_or_404(Question, pk=previous_question_id)
    resp_array = []
    votes_array = []
    final_array = []
    total = 0.0
    x = 0
    percent_array = []
    resp_dict = {}
    for a in previous_question.answer_set.all():
        resp_array.append(a.answer)
        votes_array.append(a.votes.count())
    
    for a in votes_array:
        total = total + a
    
    for a in votes_array:
        percent_array.append(int(math.ceil((a/total) *100)*100/100))
    
    for i in resp_array:
        info = {
            'answer': resp_array[x],
            'num': percent_array[x],
        }
        final_array.append(info)
        x = x+1

    json2 = simplejson.dumps(final_array)
    json = simplejson.dumps(total)
    context = Context({'previous_question': previous_question, 'json':json, 'json2':json2, 'final_array':final_array, 'percent_array':percent_array, 'votes_array':votes_array})
    return_str = render_block_to_string('previous_question.html', 'previous_question', context)
    return HttpResponse(return_str)
    # return render_to_response("previous_question.html", {"previous_question":previous_question})


############### OLD SUNBURST #########################################################
# def question_details(request, question_id):
#     question = get_object_or_404(Question, pk=question_id)
#     resp_dict = dict()
#     resp_dict["name"] = question.question
#     resp_dict["children"] = []
#     for a in question.answer_set.all():
#         resp_dict["children"].append({"name":a.answer, "size":a.votes.count() })
#     if request.is_ajax():
#         dropdownlist = request.GET.getlist('dropdowns[]')
#         dropdowns=[]
#         for x in dropdownlist:
#             if x != '-' and x not in dropdowns:
#                 dropdowns.append(x)
#         if len(dropdowns)==0:
#             return HttpResponse(simplejson.dumps(resp_dict), mimetype="application/json")
#         for child in resp_dict["children"]:
#             answer = Answer.objects.get(answer=child["name"])
#             layer = answer.selected_by.values(dropdowns[0]).annotate(size=Count(dropdowns[0]))
#             for item in layer:
#                 item["name"] = item[dropdowns[0]]
#                 if len(dropdowns) > 1:
#                     filter = dropdowns[0]
#                     layer2 = layer.filter(**{filter:item["name"]}).values(dropdowns[1]).annotate(size=Count(dropdowns[1]))
#                     for item2 in layer2:
#                         item2["name"] = item2[dropdowns[1]]
#                     item["children"] = list(layer2)
#             child["children"] = list(layer)
#         json = simplejson.dumps(resp_dict)
#         return HttpResponse(json, mimetype="application/json")
#     initialjson = simplejson.dumps(resp_dict).replace("'", r"\'")
#     stat_form1 = StatForm(initial = {'stat':'--'})
#     stat_form2 = StatForm(initial = {'stat':'--'})
#     return render_to_response("question_details.html", {"question":question, "initialjson":initialjson, "stat_form1":stat_form1, "stat_form2":stat_form2}, context_instance=RequestContext(request))

###################### THIS IS DAT NEW SHIT - BASED ON GAYVE'S 6/25 FILES ###################################
def question_details(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    allquestions = Question.objects.all().values("pk").order_by("pk")
    context = {
        "question":question,
        "allquestions":allquestions,
    }
    return render_to_response("question_details.html", context, context_instance=RequestContext(request))

def getjson(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    resp_dict={
        "question":question.question,
        "value":question.total_vote_count,
        "answers":[],
    }
    for answer in question.answer_set.all():
        resp_dict["answers"].append({
            "answer":answer.answer,
            "count":answer.votes.count(),
            "data":list(answer.selected_by.values('gender','agegroup','political').annotate(count=Count('id'))),
        })
    json = simplejson.dumps(resp_dict).replace("'",r"\'")
    return HttpResponse(json, mimetype="application/json")
#####################################################################################################



def vote(request, answer_id):
    selected_answer = Answer.objects.get(pk=answer_id)
    previous_question = selected_answer.question
    if request.user.is_authenticated():
        userprofile = request.user.userprofile
        selected_answer.selected_by.add(userprofile)
        previous_question.answered_by.add(userprofile)
        userprofile.save()
    else:
        userprofile = None
    vote = Vote.objects.create(answer_id=selected_answer.id)
    vote.voter = userprofile
    vote.save()
    selected_answer.save()
    previous_question.save()
    current_question = Question.objects.filter(~Q(id=previous_question.id)).order_by('?')[:1].get()
    data = {
        "previous_question_pk": previous_question.id,
        "current_question_pk": current_question.id,
    }
    json = simplejson.dumps(data)
    return HttpResponse(json, mimetype='application/json')
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.

    # return render_to_response("current_question.html", {"current_question": current_question, "previous_question": previous_question})
    # return HttpResponseRedirect(reverse('questions.views.current_question', args=(previous_question.id,)))

from django.forms.formsets import BaseFormSet
def submit(request):
    class BaseAnswerFormSet(BaseFormSet):
        def clean(self):
            blanks = []
            print "clean called"
            for i in range(0, self.total_form_count()):
                form = self.forms[i]
                try:
                    answer = form.cleaned_data['answer']
                    print "answer: %s" %answer
                except:
                    blanks.append(form)
                    print "found %s blanks" %len(blanks)
            if len(blanks) >= 4:
                raise forms.ValidationError("Must have at least two answer choices")


    AnswerFormSet = formset_factory(AnswerForm, max_num=5, extra = 5, formset = BaseAnswerFormSet)
    user = request.user.userprofile
    if request.method == 'POST': # If the form has been submitted...
        question_form = QuestionForm(request.POST) # A form bound to the POST data
        # Create a formset from the submitted data
        answer_formset = AnswerFormSet(request.POST, request.FILES)
        print "answer formset %s" %answer_formset
        print "non form errors %s" %answer_formset.non_form_errors()
        print "form errors %s" %answer_formset.errors
        if question_form.is_valid() and not any(answer_formset.non_form_errors()):
            question = question_form.save(commit=False)
            question.submitter = user
            question.save()
            for form in answer_formset.forms:
                try:
                    form.cleaned_data["answer"]
                    answer = form.save(commit=False)
                    answer.question = question
                    answer.save()
                    user.save()
                except:
                    pass
            return redirect('profile')
    else:
        question_form = QuestionForm()
        answer_formset = AnswerFormSet()
    c = {'question_form': question_form,
    'answer_formset': answer_formset,
    }
    c.update(csrf(request))
    return render_to_response('submit.html', c, context_instance = RequestContext(request))

@login_required
def profile(request):
    user = request.user.userprofile
    #user.populate_graph_info()
    user.save()
    uservotes = user.selections.count()
    pollcount = Question.objects.all().count()
    # for q in user.submissions.all():
    #     totalvotes += q.answer_set.get_vote_count()
    return render_to_response("profile.html", {}, context_instance = RequestContext(request))

def search_test(request):
    return render_to_response("search_test.html")

def search_results(request, searchtext):
    print "Search results"
    response_dict = {
    'results':Question.objects.filter(Q(question__icontains=searchtext)).order_by('question'),
        }
    return render_to_response("search_results.html", response_dict, context_instance=RequestContext(request))

############## THIS IS THE OLD SEARCH WITH JQUERY UI AUTOCOMPLETE#########################
# def search(request):
#     if 'searchtext' in request.GET:
#         q = request.GET.get('searchtext')
#         json = serializers.serialize('json', Question.objects.filter(Q(question__icontains=q)).order_by('question')[0:6])
#         print json
#         resp_dict=[]
#         for x in Question.objects.filter(Q(question__icontains=q)):
#             newdict=dict()
#             newdict["label"]=x.question
#             newdict["category"]="Questions"
#             resp_dict.append(newdict)
#         for y in Answer.objects.filter(Q(answer__icontains=q)):
#             newdict=dict()
#             newdict["label"]=y.answer
#             newdict["category"]="Answers"
#             resp_dict.append(newdict)
#         print resp_dict
#         # json = serializers.serialize('json', resp_dict)
#         print "attempt at split:"
#         print json
#     else:
#         resp=[]
#         for q in Question.objects.all():
#             resp.append(q.question)
#         print resp
#         json = simplejson.dumps(resp)
#         print json
#     return HttpResponse(json, mimetype='application/json')

############ THIS IS THAT NEW SHIT #######################
def typeahead_test(request):
    return render_to_response("typeahead_test.html")

def search(request):
    resp=[]
    if 'q' in request.GET:
        q=request.GET.get('q')
        queryset=Question.objects.filter(Q(question__icontains=q))
    else:
        queryset=Question.objects.all()
    for question in queryset:
        newdict=dict()
        wordlist=[]
        for word in question.question.split():
            wordlist.append(word)
        newdict["value"]=question.question
        newdict["id"]=question.id
        newdict["tokens"]=wordlist
        resp.append(newdict)
    json = simplejson.dumps(resp)
    print json
    return HttpResponse(json, mimetype='application/json')

def search_results(request):
    q=request.GET.get('q')
    response_dict = {
        'results':Question.objects.filter(Q(question__icontains=q)).order_by('question'),
        }
    return render_to_response("search_results.html", response_dict, context_instance=RequestContext(request))