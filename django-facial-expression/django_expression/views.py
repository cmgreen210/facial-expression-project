from os.path import join as pjoin
from itertools import izip
from django.shortcuts import render, render_to_response
from django.template import RequestContext
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.conf import settings
from PIL import Image
from django.views.generic.edit import FormView
from django.contrib.staticfiles import finders
from forms import UploadImageFromURLForm
from .pipeline import run_image_classifier
from .models import add_image_models, emotion_dictionary
from validation import *


def home_page(request):
    form = UploadImageFromURLForm()
    return render(request, 'django_expression/media_upload.html',
                  {'form': form})


def example_view(request, ex_name):
    ex_name = ex_name.lower()
    url = os.path.join('django_expression', 'image', ex_name + '.jpg')
    path = finders.find(url)
    if path is None:
        return render_to_response('django_expression/image_bad.html',
                                      {'error_message':
                                      'Example image was not found!'},
                                      context_instance=RequestContext(
                                          request
                                      ))
    out = run_image_classifier(path)
    image, gray_image, class_proba = out

    best_predictions = class_proba.sort(sort_columns='score',
                                        ascending=False)
    classes = best_predictions['class']
    prob = best_predictions['score'] * 100
    scores = {}
    for c, p in izip(classes, prob):
        scores[emotion_dictionary[c]] = p

    return render_to_response('django_expression/single_image.html',
                              {'url': url,
                               'is_static': True,
                               'scores': scores},
                              context_instance=RequestContext(request))


class UploadImageFromURLView(FormView):
    template_name = 'django_expression/media_upload.html'
    form_class = UploadImageFromURLForm

    def _invalidate(self, form, message):
        form.errors['url'] = [message, ]
        return super(UploadImageFromURLView, self).form_invalid(form)

    def form_valid(self, form):
        url = form.data['url']
        domain, path = split_url(url)

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
            return render_to_response('django_expression/image_bad.html',
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
        return render_to_response('django_expression/single_image.html',
                                  {'url': image_url,
                                   'is_static': False,
                                   'scores': scores},
                                  context_instance=RequestContext(
                                      self.request))

