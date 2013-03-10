from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.http import HttpResponseRedirect, HttpResponse
from django.db.models import Q
from django.views.decorators.csrf import csrf_exempt
from django.core.urlresolvers import reverse
from django.utils import simplejson
from questions.models import Question, Answer
from questions.forms import QuestionForm, AnswerForm
from questions.utils import *

def index(request):
    current_question = Question.objects.all().order_by('?')[:1].get()
    return render_to_response("index.html", {"current_question": current_question,})


def current_question(request, current_question_id):
    current_question = get_object_or_404(Question, pk=current_question_id)
    print request
    next_question = Question.objects.filter(~Q(id = current_question.id)).order_by('?')[:1].get()
    if request.is_ajax():
        print "vote is ajax"
        return render_to_response("view_question.html", {"current_question":current_question})
    return render_to_response("current_question.html", {"current_question": current_question, "next_question": next_question})


def previous_question(request, previous_question_id):
    previous_question = get_object_or_404(Question, pk=previous_question_id)
    return render_to_response("previous_question.html", {"previous_question":previous_question})
    # return render_to_response("previous_question.html", {"previous_question": previous_question})


def vote(request, answer_id):
    # previous_question = get_object_or_404(Question, pk=request.POST["current_question_pk"])
    selected_answer = Answer.objects.get(pk=answer_id)
    previous_question = get_object_or_404(Question, pk=selected_answer.question.id)
    selected_answer.votes += 1
    selected_answer.save()
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
    return HttpResponseRedirect(reverse('questions.views.current_question', args=(previous_question.id,)))


def search(request):
	return HttpResponse("hi")