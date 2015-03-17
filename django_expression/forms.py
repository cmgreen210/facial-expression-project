from django import forms


class UploadImageFromURLForm(forms.Form):
    """Form to get url of image
    """
    url = forms.URLField(required=True,
                         label='',
                         error_messages={
                             "required": "Please enter a valid image URL"
                         },
                         widget=forms.TextInput(attrs={'placeholder':
                                                       'Image URL'}))
