from django.shortcuts import render, render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.conf import settings
import os
from forms import VideoForm, ImageForm


def get_video(request):

    if request.method == 'POST':
        form = VideoForm(request.POST, request.FILES)
        if form.is_valid():
            video_file = request.FILES['video_file']
            _, ext = os.path.splitext(video_file._name)
            path = default_storage.save('tmp_video/vid' + ext,
                                        ContentFile(video_file.read()))
            # tmp_file = os.path.join(settings.MEDIA_ROOT, path)

            return HttpResponseRedirect('/')
    else:
        form = VideoForm()

    return render_to_response('emotion/video.html', {'form': form},
                              context_instance=RequestContext(request))
