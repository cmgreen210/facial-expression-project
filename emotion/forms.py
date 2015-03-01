from django import forms
from django.template.defaultfilters import filesizeformat
from django.utils.translation import ugettext_lazy as _
from django.conf import settings


class LimitedFileField(forms.FileField):
    def __init__(self, *args, **kwargs):
        self.content_types = kwargs.pop('content_types', None)
        self.max_upload_size = kwargs.pop('max_upload_size', None)
        if not self.max_upload_size:
            self.max_upload_size = settings.MAX_UPLOAD_SIZE
        if not self.content_types:
            self.content_types = set(settings.VIDEO_TYPES)

        super(LimitedFileField, self).__init__(*args, **kwargs)

    def clean(self, *args, **kwargs):
        data = super(LimitedFileField, self).clean(*args, **kwargs)
        try:
            if data.content_type in self.content_types:
                if data.size > self.max_upload_size:
                    msg = _(('File size must '
                            'be under {0}!').format(self.max_upload_size))
                    raise forms.ValidationError(msg)
            else:
                msg = _(('Video file type ({0}) is not'
                         ' supported.').format(data.content_type))
                raise forms.ValidationError(msg)
        except AttributeError:
            pass

        return data


class LimitedImageField(forms.FileField):
    def __init__(self, *args, **kwargs):
        self.max_upload_size = kwargs.pop('max_upload_size', None)
        self.content_types = kwargs.pop('content_types', None)
        if not self.max_upload_size:
            self.max_upload_size = settings.MAX_UPLOAD_SIZE
        if not self.content_types:
            self.content_types = set(settings.IMAGE_TYPES)
        super(LimitedImageField, self).__init__(*args, **kwargs)

    def clean(self, *args, **kwargs):
        data = super(LimitedImageField, self).clean(*args, **kwargs)
        try:
            if data.content_type in self.content_types:
                if data.size > self.max_upload_size:
                    msg = _(('File size must '
                             'be under {0}!').format(self.max_upload_size))
                    raise forms.ValidationError(msg)
            else:
                msg = _(('Image type ({0}) is not'
                         ' supported.').format(data.content_type))
                raise forms.ValidationError(msg)

        except AttributeError:
            pass

        return data


class VideoForm(forms.Form):
    video_file = LimitedFileField(label="Upload video for analysis",
                                  error_messages={'required':
                                                  'Please select a video'})


class ImageForm(forms.Form):
    image_file = LimitedImageField(label="Upload an image",
                                   error_messages={'required':
                                                   'Please select an image'})
