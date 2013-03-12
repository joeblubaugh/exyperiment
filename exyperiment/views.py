from django.http import HttpResponse, HttpResponseRedirect, Http404, HttpResponseServerError
from django.shortcuts import render_to_response
from django.template import RequestContext
from models import Participant, ImageSet

import random

# Create your views here.
def start_page(request):
    # For GET, display the form
    if request.method == "GET":
        return render_to_response("consent.html", context_instance=RequestContext(request))
    # For POST, create a new user and then send user to the next page, then update the session.
    elif request.method == "POST":
        participant = Participant()
        participant.save()
        participant.num_images = participant.id % 2
        # Demographics will be set at the end.
        participant.save()
        request.session['participant_id'] = participant.id
        response = HttpResponse()
        response.status_code = 303
        response['Location'] = "http://www.google.com" # Get the URL and set it.
        return response


def query_page(request):
    participant_id = request.session['participant_id']
    if not participant_id:
        return HttpResponseRedirect("/")


    # Get participant & an image set ID that we don't have yet.
    participant = Participant.objects.get(id=participant_id)
    if not participant:
        return Http404()

    if request.method == "GET":
        answers_count = participant.answer_set.count()
        if answers_count < 60:
            next_set = ImageSet.objects.order_by('id').get(answers_count)
            if not next_set:
                return HttpResponseServerError(content="No image set found")

            data = {"image_set": next_set,
                    "num_images": participant.num_images}
            return render_to_response("entry.html",
                                      data,
                                      context_instance=RequestContext(request))
        else:
            return HttpResponseRedirect("/survey")
    elif request.method == "POST":
        # TODO Process answer
        pass


def survey(request):
    pass