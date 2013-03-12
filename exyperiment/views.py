from django.http import HttpResponse, HttpResponseRedirect, Http404, HttpResponseServerError
from django.shortcuts import render_to_response
from django.template import RequestContext
from models import Participant, ImageSet, Answer

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
        participant.num_images = 2 if participant.id % 2 is 0 else 3
        # Demographics will be set at the end.
        participant.save()
        request.session['participant_id'] = participant.id
        response = HttpResponse()
        response.status_code = 303
        response['Location'] = "/experiment/" # Get the URL and set it.
        return response


def experiment_page(request):
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
            # TODO : Randomize order of image sets.
            next_set = ImageSet.objects.order_by('id')[answers_count]
            if not next_set:
                return HttpResponseServerError(content="No image set found")
            # TODO : Add "which" parameter
            data = {"image_set": next_set,
                    "num_images": participant.num_images}
            return render_to_response("entry.html",
                                      data,
                                      context_instance=RequestContext(request))
        else:
            return HttpResponseRedirect("/survey")
    elif request.method == "POST":
        answer = Answer()
        answer.user = participant
        answer.imageSet_id=int(request.POST["image-set-id"])
        answer.value = int(request.POST["dollar-value"])
        # TODO : Add "which" parameter
        answer.save()
        return HttpResponseRedirect("/experiment")


def survey(request):
    return HttpResponse("Congartulations!")