from django.shortcuts import render
from django.http import HttpResponseRedirect
from forms import LimitedImageField, LimitedFileField


def get_video(request):

    if request.method == 'POST':
        form = LimitedFileField(request.POST)

        if form.is_valid():
            return HttpResponseRedirect('/success/')
    else:
        form = LimitedFileField()

    return render(request, 'emotion/video.html', {'form': form})
