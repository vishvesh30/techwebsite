from django import forms
from django_summernote.widgets import SummernoteWidget, SummernoteInplaceWidget

from article.models import article_data


class insertarticleForm(forms.ModelForm):
    #article_text = forms.CharField(widget=SummernoteInplaceWidget())
    class Meta():
        model=article_data
        fields=['article_text']
        widgets={
            'article_text':SummernoteWidget()
        }

class updatearticleForm(forms.ModelForm):
    class Meta():
        model=article_data
        fields=['article_text']
        widgets={
            'article_text':SummernoteInplaceWidget()
        }
