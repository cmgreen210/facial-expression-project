from django.shortcuts import render, render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.conf import settings
import os
from forms import VideoForm, ImageForm


def home_page(request):
    v_form = VideoForm()
    i_form = ImageForm()
    return render(request, 'emotion/index.html',
                  {'v_form': v_form,
                   'i_form': i_form})


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

    iform = ImageForm()

    return render_to_response('emotion/index.html', {'v_form': form,
                                                     'i_form': iform},
                              context_instance=RequestContext(request))


def get_image(request):

    if request.method == 'POST':
        form = ImageForm(request.POST, request.FILES)
        if form.is_valid():
            image_file = request.FILES['image_file']
            _, ext = os.path.splitext(image_file._name)
            path = default_storage.save('tmp_img/img' + ext,
                                        ContentFile(image_file.read()))
            # tmp_file = os.path.join(settings.MEDIA_ROOT, path)

            return HttpResponseRedirect('/')
    else:
        form = ImageForm()

    vform = VideoForm()
    return render_to_response('emotion/index.html', {'i_form': form,
                                                     'v_form': vform},
                              context_instance=RequestContext(request))
