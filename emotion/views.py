from django.shortcuts import render, render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect, HttpResponse
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.conf import settings
import os
from os.path import join as pjoin
from forms import VideoForm, ImageForm
from emotion.pipeline import run_video_classifier, run_image_classifier
from emotion.models import add_video_image_models, add_image_models


def home_page(request):
    v_form = VideoForm()
    i_form = ImageForm()
    return render(request, 'emotion/media_upload.html',
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
            path = pjoin(settings.MEDIA_ROOT, path)
            classifications, images = run_video_classifier(path, frame_skip=1)
            _, image_clfs = \
                add_video_image_models(classifications, images)

            if os.path.exists(path):
                os.remove(path)

            return render_to_response('emotion/image_array.html',
                                      {'images': image_clfs},
                                      context_instance=RequestContext(request))
    else:
        form = VideoForm()

    iform = ImageForm()

    return render_to_response('emotion/media_upload.html', {'v_form': form,
                                                            'i_form': iform},
                              context_instance=RequestContext(request))


def get_image(request):

    if request.method == 'POST':
        form = ImageForm(request.POST, request.FILES)
        if form.is_valid():
            image_file = request.FILES['image_file']
            _, ext = os.path.splitext(image_file. _name)
            path = default_storage.save('tmp_img/img' + ext,
                                        ContentFile(image_file.read()))
            path = pjoin(settings.MEDIA_ROOT, path)
            out = run_image_classifier(path)
            if out is None:
                # TODO: No face found so alert the user
                pass
            image, gray_image, class_proba = out
            _, image_url, scores = add_image_models(class_proba,
                                                           image,
                                                           gray_image)
            if os.path.exists(path):
                os.remove(path)
            return render_to_response('emotion/single_image.html',
                                      {'url': image_url,
                                       'scores': scores},
                                      context_instance=RequestContext(request))
    else:
        form = ImageForm()

    vform = VideoForm()
    return render_to_response('emotion/index.html', {'i_form': form,
                                                     'v_form': vform},
                              context_instance=RequestContext(request))
