from django.shortcuts import render, render_to_response
from django.template import RequestContext
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.conf import settings
from PIL import Image
from os.path import join as pjoin
from forms import VideoForm, ImageForm, UploadImageFromURLForm
from emotion.pipeline import run_video_classifier, run_image_classifier
from emotion.models import add_video_image_models, add_image_models
from django.views.generic.edit import FormView
from validation import *
import StringIO


def home_page(request):
    form = UploadImageFromURLForm()
    return render(request, 'emotion/media_upload.html',
                  {'form': form})


def get_video(request):

    if request.method == 'POST':
        form = VideoForm(request.POST, request.FILES)
        if form.is_valid():
            try:
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

                if image_clfs[0] is None:
                    return render_to_response('emotion/image_bad.html',
                                              {'error_message':
                                              "Didn't find any faces! Try"
                                              " another clip."},
                                              context_instance=RequestContext(
                                                  request
                                              ))

                return render_to_response('emotion/image_array.html',
                                          {'images': image_clfs},
                                          context_instance=RequestContext(
                                              request))
            except:
                return render_to_response('emotion/image_bad.html',
                                              {'error_message':
                                              'Unexpected error!'},
                                              context_instance=RequestContext(
                                                  request
                                              ))
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
            try:
                image_file = request.FILES['image_file']
                _, ext = os.path.splitext(image_file. _name)
                path = default_storage.save('tmp_img/img' + ext,
                                            ContentFile(image_file.read()))
                path = pjoin(settings.MEDIA_ROOT, path)
                out = run_image_classifier(path)
                if out is None:
                    if os.path.exists(path):
                        os.remove(path)
                    return render_to_response('emotion/image_bad.html',
                                              {'error_message':
                                              'No faces were found in the '
                                              'image. Please try another!'},
                                              context_instance=RequestContext(
                                                  request
                                              ))

                image, gray_image, class_proba = out
                _, image_url, scores = add_image_models(class_proba,
                                                               image,
                                                               gray_image)
                if os.path.exists(path):
                    os.remove(path)
                return render_to_response('emotion/single_image.html',
                                          {'url': image_url,
                                           'scores': scores},
                                          context_instance=RequestContext(
                                              request))
            except:
                return render_to_response('emotion/image_bad.html',
                                              {'error_message':
                                              'Unexpected error!'},
                                              context_instance=RequestContext(
                                                  request
                                              ))
    else:
        form = ImageForm()

    vform = VideoForm()
    return render_to_response('emotion/index.html', {'i_form': form,
                                                     'v_form': vform},
                              context_instance=RequestContext(request))


class UploadImageFromURLView(FormView):
    template_name = 'emotion/media_upload.html'
    form_class = UploadImageFromURLForm

    def _invalidate(self, form, message):
        form.errors['url'] = [message, ]
        return super(UploadImageFromURLView, self).form_invalid(form)

    def form_valid(self, form):
        url = form.data['url']
        domain, path = split_url(url)
        filename = get_url_tail(path)

        if not image_exists(domain, path):
            return self._invalidate(form,
                                    "Image not found at specified url.")

        f = retrieve_image(url)
        if not valid_image_mimetype(f):
            return self._invalidate(form, "Downloaded file not a valid image.")

        image = Image.open(f)
        if not valid_image_size(image)[0]:
            return self._invalidate(form, "Image is too large (>4mb)")

        image_io = StringIO.StringIO()
        image.save(image_io, format="JPEG")

        path = default_storage.save('tmp_img/img.jpeg',
                                    ContentFile(image_io.getvalue()))

        path = pjoin(settings.MEDIA_ROOT, path)
        out = run_image_classifier(path)
        if out is None:
            if os.path.exists(path):
                os.remove(path)
            return render_to_response('emotion/image_bad.html',
                                      {'error_message':
                                      'No faces were found in the '
                                      'image. Please try another!'},
                                      context_instance=RequestContext(
                                          self.request
                                      ))

        image, gray_image, class_proba = out
        _, image_url, scores = add_image_models(class_proba,
                                                image,
                                                gray_image)
        if os.path.exists(path):
            os.remove(path)
        return render_to_response('emotion/single_image.html',
                                  {'url': image_url,
                                   'scores': scores},
                                  context_instance=RequestContext(
                                      self.request))

