from django.forms import ModelForm, DateInput
from .models import Content

class ContentForm(ModelForm):
  class Meta:
    model = Content
    # datetime-local is a HTML5 input type, format to make date time show on fields
    widgets = {
      'start_time': DateInput(attrs={'type': 'date-local'}, format='%Y-%m-%d'),
      'end_time': DateInput(attrs={'type': 'date-local'}, format='%Y-%m-%d'),
    }
    fields = ['owner', 'title', 'content', 'start_time', 'end_time']

  def __init__(self, *args, **kwargs):
    super(ContentForm, self).__init__(*args, **kwargs)
    # input_formats parses HTML5 datetime-local input to datetime field
    self.fields['start_time'].input_formats = ('%Y-%m-%d',)
    self.fields['end_time'].input_formats = ('%Y-%m-%d',)
