from django.contrib.auth import logout
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.shortcuts import render_to_response, redirect, get_object_or_404
from django.template import RequestContext

def logout_view(request):
    logout(request)
    print "logged out"
    return HttpResponseRedirect(reverse('questions.views.index'))
    # return render_to_response("index.html", {}, context_instance=RequestContext(request))