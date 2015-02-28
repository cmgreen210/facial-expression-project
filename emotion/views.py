from django.shortcuts import render, render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect
from forms import VideoForm, ImageForm


def get_video(request):

    if request.method == 'POST':
        form = VideoForm(request.POST, request.FILES)
        if form.is_valid():
            return HttpResponseRedirect('/')
    else:
        form = VideoForm()

    return render_to_response('emotion/video.html', {'form': form},
                              context_instance=RequestContext(request))
