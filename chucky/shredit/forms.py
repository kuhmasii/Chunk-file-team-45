from django.forms import ValidationError
from django import forms
from django.conf import settings
from django.core.mail import send_mail


class ContactForm(forms.Form):

    name = forms.CharField(max_length=120, label='Name', required=True)
    email = forms.EmailField(label='Email', required=True)
    message = forms.CharField(widget=forms.Textarea,
                              label='Message', required=True)

    def get_info(self):
        """
        Method that returns formatted information
        :return: msg
        """
        # Cleaned data
        clean_data = super().clean()

        name = clean_data.get('name').strip()
        from_email = clean_data.get('email')

        msg = f'{name}, with email {from_email} says\n'
        msg += clean_data.get('message')

        return msg

    def send(self):
        msg = self.get_info()
        try:
            send_mail(
                subject="Hello :)",
                message=msg,
                from_email=settings.FROM,
                recipient_list=[settings.FROM]
            )
            return True
        except:
            return None


class UploadForm(forms.Form):
    SIZE_TYPE = (
        ("KB", "KB"),
        ("MB", "MB")
    )

    file = forms.FileField(required=False)
    size_type = forms.CharField(
        required=False,
        widget=forms.Select(choices=SIZE_TYPE)
    )
    chunk_num = forms.IntegerField(required=False)
    chunk_size_num = forms.IntegerField(required=False)

    def clean_file(self):

        file = self.cleaned_data.get('file')
        if file is not None:
            clean_file = self.cleaned_data.get('file').name.split('.')[-1]
            if not clean_file.lower() in ['json', 'csv']:
                raise ValidationError('File should be of JSON or CSV type')
        else:
            raise ValidationError('This Field is required')

        return clean_file

    def clean_chunk_num(self):
        clean_chunk_num = self.cleaned_data.get('chunk_num')

        if clean_chunk_num:
            if clean_chunk_num < 0 or clean_chunk_num == 0:
                raise ValidationError('Chunk number should be greater than 0')

        return clean_chunk_num

    def clean_size_type(self):
        clean_size_type = self.cleaned_data.get('size_type')

        if clean_size_type:
            if clean_size_type not in ['KB', 'MB']:
                raise ValidationError('Size type should be KB or MB')

        return clean_size_type

    def clean_chunk_size_num(self):
        clean_num = self.cleaned_data.get('chunk_size_num')

        if clean_num:
            if clean_num < 0 or clean_num == 0:
                raise ValidationError('Chunk number should be greater than 0')

        return clean_num
