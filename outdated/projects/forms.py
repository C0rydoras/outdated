from django import forms
from django.forms.utils import ErrorList
from django.utils.html import format_html, format_html_join
from .models import Package, Project
import environ
import datetime

env = environ.Env()


class UiKitErrorList(ErrorList):
    def as_uikit(self):
        if not self.data:
            return ""

        return format_html(
            '<div class=" {}"  >{}</div>',
            self.error_class,
            format_html_join(
                "",
                " <p class='uk-margin-remove uk-text-danger'>{}</p>",
                ((e,) for e in self),
            ),
        )

    def __str__(self):
        return self.as_uikit()


def uikitify(fields):
    for field_name, field in fields.items():
        print(
            field.__class__.__name__,
        )
        field_supertype = field.__class__.__name__

        field_class = field.widget.attrs.get("class", "")
        if field_supertype == "DateField":
            field_class += " uk-input datepicker"
            field.widget.attrs[
                "pattern"
            ] = "[0-9]{4}-(0[1-9]|1[012])-(0[1-9]|1[0-9]|2[0-9]|3[01])"
        elif field_supertype == "TextField" or field_supertype == "CharField":
            field_class += " uk-input "
        elif field_supertype == "ModelMultipleChoiceField":
            field_class += " uk-select "

        field.widget.attrs["class"] = field_class + " uk-border-rounded"
        field.widget.attrs["placeholder"] = ""
    return fields


class PackageForm(forms.ModelForm):
    class Meta:
        model = Package
        fields = "__all__"
        override = True

    def __init__(self, *args, **kwargs):
        super(PackageForm, self).__init__(*args, **kwargs)
        self.fields = uikitify(self.fields)
        self.error_class = UiKitErrorList


class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super(ProjectForm, self).__init__(*args, **kwargs)
        self.fields = uikitify(self.fields)
        self.error_class = UiKitErrorList