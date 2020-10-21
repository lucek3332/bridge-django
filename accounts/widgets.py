from django.forms.widgets import ClearableFileInput

class CustomClearableFileInput(ClearableFileInput):
    template_name = 'forms/widgets/custom_clearable_file_input.html'