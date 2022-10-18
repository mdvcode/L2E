from django import forms

from w3.models import AccountMetamask, Transaction, IPFS


class ConnectWallet(forms.ModelForm):
    class Meta:
        model = AccountMetamask
        fields = ('user_wallet_address',)


class CreateTransForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ('value',)


class CreateTextTransForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ('data',)


class IPFSTransForm(forms.ModelForm):
    class Meta:
        model = IPFS
        fields = '__all__'


class ResultHashForm(forms.Form):
    hash = forms.CharField(max_length=250)


class UpdateTransForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ('value',)


class UpdateTextTransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ('data',)


class UpdateIPFSTransaction(forms.ModelForm):
    class Meta:
        model = IPFS
        fields = '__all__'



