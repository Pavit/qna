from django.shortcuts import render_to_response, redirect, get_object_or_404
from django.template import RequestContext
from django.http import HttpResponseRedirect, HttpResponse
from django.db.models import Q
from django import forms
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.core.urlresolvers import reverse
from django.utils import simplejson
from django.forms.formsets import formset_factory, BaseFormSet
from django.core.context_processors import csrf
from questions.models import Question, Answer
from questions.forms import QuestionForm, AnswerForm
from questions.utils import *

def index(request):
    if request.user.is_authenticated():
        current_question = Question.objects.all().order_by('?')[:1].get()
        return HttpResponseRedirect(reverse('questions.views.current_question', args=(current_question.id,)))
    else:
        current_question = Question.objects.all().order_by('?')[:1].get()
        return render_to_response("index.html", {"current_question": current_question,}, context_instance = RequestContext(request))

def sunburstplay(request):
    return render_to_response("sunburstplay.html")

def current_question(request, current_question_id):
    current_question = get_object_or_404(Question, pk=current_question_id)
    next_question = Question.objects.filter(~Q(id = current_question.id)).order_by('?')[:1].get()
    if request.is_ajax():
        print "vote is ajax"
        return render_to_response("view_question.html", {"current_question":current_question}, context_instance = RequestContext(request))
    return render_to_response("current_question.html", {"current_question": current_question, "next_question": next_question}, context_instance = RequestContext(request))


def previous_question(request, previous_question_id):
    previous_question = get_object_or_404(Question, pk=previous_question_id)
    return render_to_response("previous_question.html", {"previous_question":previous_question})

def question_details(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    resp_dict=dict()
    resp_dict["name"] = question.question
    resp_dict["children"]=[]
    for answer in question.answer_set.all():
        resp_dict["children"].append( {"name": answer.answer,
                                    "size": answer.votes,
                                    "children": [
                                    { 
                                    "name": "males",
                                    "size": answer.selected_by.filter(gender="M").count(),
                                    "children":[
                                        {"name":"< 15", "size": answer.selected_by.filter(gender="M").filter(age__lt=16).count() },
                                        {"name": "16 - 25", "size": answer.selected_by.filter(gender="M").filter(age__gte=16).filter(age__lte=25).count()},
                                        {"name": "26 - 35", "size": answer.selected_by.filter(gender="M").filter(age__gt=26).filter(age__lte=35).count()},
                                        {"name": "36+", "size": answer.selected_by.filter(gender="M").filter(age__gt=35).count()}
                                        ]
                                    }, 
                                    {
                                    "name": "females",
                                    "size": answer.selected_by.filter(gender="F").count(),
                                    "children": [
                                        {"name":"< 15", "size": answer.selected_by.filter(gender="F").filter(age__lt=16).count() },
                                        {"name": "16 - 25", "size": answer.selected_by.filter(gender="F").filter(age__gte=16).filter(age__lte=25).count()},
                                        {"name": "26 - 35", "size": answer.selected_by.filter(gender="F").filter(age__gt=26).filter(age__lte=35).count()},
                                        {"name": "36+", "size": answer.selected_by.filter(gender="F").filter(age__gt=35).count()}
                                        ]
                                    }]
                                    })
    json = simplejson.dumps(resp_dict).replace("'", r"\'")
    # return HttpResponse(json)
    return render_to_response("question_details.html", {"question":question, "json":json})
    

def vote(request, answer_id):
    selected_answer = Answer.objects.get(pk=answer_id)
    selected_answer.votes += 1
    previous_question = selected_answer.question
    if request.user.is_authenticated():
        userprofile = request.user.userprofile
        previous_question.answered_by.add(userprofile)
        selected_answer.selected_by.add(userprofile)
        selected_answer.save()
        previous_question.save()
        userprofile.save()
        print selected_answer.selected_by.all()
        print userprofile.answered.all()
        print userprofile.selections.all()
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
    totalvotes = 0
    # for q in user.submissions.all():
    #     totalvotes += q.answer_set.get_vote_count()
    return render_to_response("profile.html", {}, context_instance = RequestContext(request))

def search(request):
	return HttpResponse("hi")