from django import forms

from message.models import Message


class CreateMessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ('metamask', 'metamask_to', 'text', 'gas', 'gas_price', )


class SendForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ('text', 'gas', 'gas_price',)


class UpdateMessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ('metamask_to', 'text', 'gas', 'gas_price',)


class UpdateInfoMessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ('text', 'gas', 'gas_price', )
