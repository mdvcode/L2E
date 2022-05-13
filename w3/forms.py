from django import forms

from w3.models import AccountMetamask, Transaction


class ConnectWallet(forms.ModelForm):
    class Meta:
        model = AccountMetamask
        fields = ('user_wallet_address', 'private_key',)


class RedactionForm(forms.ModelForm):
    class Meta:
        model = AccountMetamask
        fields = ('private_key',)


class CreateTransForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ('to_account', 'gas', 'value', 'gas_price',)


class CreateTextTransForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ('to_account', 'gas', 'data', 'gas_price',)
