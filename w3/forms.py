from django import forms

from w3.models import AccountMetamask, Transaction, IPFS


class ConnectWallet(forms.ModelForm):
    class Meta:
        model = AccountMetamask
        fields = ('user_wallet_address',)


class CreateTransForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ('to_account', 'gas', 'value', 'gas_price',)


class CreateTextTransForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ('to_account', 'gas', 'data', 'gas_price',)


class IPFSTransForm(forms.ModelForm):
    class Meta:
        model = IPFS
        fields = '__all__'


class ResultHashForm(forms.Form):
    hash = forms.CharField(max_length=250)


class UpdateTransForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ('to_account', 'gas', 'value', 'gas_price',)


class UpdateTextTransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ('to_account', 'gas', 'data', 'gas_price',)



