from django import forms
from ads.humanize import naturalsize
from django.core.files.uploadedfile import InMemoryUploadedFile


from ads.models import Ads

class CreateForm(forms.ModelForm):

    max_upload_limit = 2 * 1024 * 1024
    max_upload_limit_text = naturalsize(max_upload_limit)

    picture = forms.FileField(required=False, label='File to Upload <= '+max_upload_limit_text)
    upload_file_name = 'picture'

    class Meta:

        fields = ['title', 'text', 'price', 'picture','tags']
        model = Ads

    def clean(self):

        cleaned_data = super().clean()
        pic = cleaned_data.get('picture')
        if pic is None:
            return
        if len(pic) > self.max_upload_limit:
            self.add_error('picture','File must be < '+self.max_upload_limit_text+' bytes')


    def save(self, commit=True):

        instance = super(CreateForm, self).save(commit=False)
        f = instance.picture

        if isinstance(f, InMemoryUploadedFile):
            bytearray = f.read()
            instance.content_type = f.content_type
            instance.picture = bytearray

        if commit:
            instance.save()
            self.save_m2m()

        return instance



class CommentForm(forms.Form):
    comment = forms.CharField(max_length=500, min_length=5, strip=True, required=True)

# def get_form_class(view_fields=None, *args, **kwargs):
#     class AdsForm(forms.ModelForm):
#         def __init__(self, *args, **kwargs):
#             super(AdsForm,self).__init__(*args, **kwargs)
#         class Meta:
#             model = Ads

#             if view_fields is not None:

#                 fields = view_fields
            
#             else:
#                 fields = '__all__'

#     return AdsForm
