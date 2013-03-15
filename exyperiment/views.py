from django.http import HttpResponse, HttpResponseRedirect, Http404, HttpResponseServerError
from django.shortcuts import render_to_response
from django.template import RequestContext
from models import Participant, ImageSet, Answer
from forms import DemographicsForm, remove_holddown
import random

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
        image_sets = {x.imageSet_id for x in participant.answer_set.all()}
        total_set = {x for x in range(1, 61)}
        allowed = total_set.difference(image_sets)
        if len(allowed) > 0:
            random.seed()
            idx = random.sample(allowed, 1)[0]
            next_set = ImageSet.objects.get(id=idx)

            if not next_set:
                return HttpResponseServerError(content="No image set found")
            # TODO : Add "which" parameter
            data = {"image_set": next_set,
                    "num_images": "two" if participant.num_images is 2 else "three"}
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
    participant_id = request.session['participant_id']
    if not participant_id:
        return HttpResponseRedirect("/")

    # Get participant & an image set ID that we don't have yet.
    participant = Participant.objects.get(id=participant_id)
    if not participant:
        return Http404()

    if request.method == "GET":
        form = DemographicsForm()
        return render_to_response("demographics.html", {"form" : form}, context_instance=RequestContext(request))
    elif request.method == "POST":
        # Create and link demographics object
        request.session.clear()
        # Save the form
        return HttpResponseRedirect("/thankyou/")

def thank_you(request):
    return render_to_response("thankyou.html", context_instance=RequestContext(request))