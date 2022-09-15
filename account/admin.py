from django.contrib import admin

# Register your models here.
from ckeditor_uploader.widgets import CKEditorUploadingWidget
class NewsAdminForm(forms.ModelForm):
    content = forms.CharField(widget=CKEditorUploadingWidget())  # Поле моделей у нас назвается 'content', поэтому оставляем переменную без именений
    
    class Meta:
        model = News  # Тут нужно указать название можеди в которой мы будем использовать CKEditor
        fields = '__all__'
