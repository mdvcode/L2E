import binascii

from django.shortcuts import render, redirect
from web3 import Web3, HTTPProvider

from blog.models import IndexInfo, Language
from w3.forms import ConnectWallet, CreateTransForm, RedactionForm, CreateTextTransForm
from w3.models import AccountMetamask, Transaction


def connect(request):
    index = IndexInfo.objects.all()[0]
    languages = Language.objects.all()
    connections = AccountMetamask.objects.filter(user=request.user)
    w3 = Web3(HTTPProvider("https://ropsten.infura.io/v3/27709d11030e4a8f8a3066732c9e6b90"))
    for account in connections:
        try:
            count_tran = w3.eth.getTransactionCount(w3.toChecksumAddress(account.user_wallet_address))
            balance = w3.fromWei(w3.eth.get_balance(w3.toChecksumAddress(account.user_wallet_address)), 'ether')
            AccountMetamask.objects.filter(pk=account.pk).update(balance=balance, count_trans=count_tran, active=True)
        except:
            AccountMetamask.objects.filter(pk=account.pk).update(active=False)
    connections = AccountMetamask.objects.filter(user=request.user)
    if request.method == "POST":
        form = ConnectWallet(data=request.POST)
        if form.is_valid():
            print(form.data)
            inst = form.save(commit=False)
            inst.user = request.user
            inst.save()
    form = ConnectWallet()
    return render(request, 'w3/connect.html', context={'form': form, 'connections': connections, 'index': index,
                                                       'languages': languages})


def redaction(request, id):
    index = IndexInfo.objects.all()[0]
    languages = Language.objects.all()
    redaction = AccountMetamask.objects.get(id=id)
    if request.method == "POST":
        form2 = RedactionForm(instance=redaction, data=request.POST)
        if form2.is_valid():
            form2.save()
            return redirect('w3:connect')
    form2 = RedactionForm(instance=redaction)
    return render(request, 'w3/redaction.html', context={'form2': form2, 'redaction': redaction, 'index': index,
                                                         'languages': languages})


def create_trans(request, id_acc):
    index = IndexInfo.objects.all()[0]
    languages = Language.objects.all()
    form = CreateTransForm
    account = AccountMetamask.objects.get(id=id_acc)
    transactions = Transaction.objects.filter(account__id=id_acc)
    if request.method == 'POST':
        form = CreateTransForm(request.POST)
        if form.is_valid():
            inst = form.save(commit=False)
            inst.account = AccountMetamask.objects.get(id=id_acc)
            inst.save()
            w3 = Web3(HTTPProvider("https://ropsten.infura.io/v3/27709d11030e4a8f8a3066732c9e6b90"))
            construct_txn = {
                'from': w3.toChecksumAddress(account.user_wallet_address),
                'nonce': w3.eth.getTransactionCount(w3.toChecksumAddress(account.user_wallet_address)),
                'to': w3.toChecksumAddress(inst.to_account),
                'gas': inst.gas,
                'value': w3.toWei(inst.value, 'ether'),
                'gasPrice': w3.toWei(inst.gas_price, 'gwei')}

            signed_tx = w3.eth.account.signTransaction(construct_txn, inst.account.private_key)

            tx_hash = w3.eth.sendRawTransaction(Web3.toHex(signed_tx.rawTransaction))
            Transaction.objects.filter(id=inst.id).update(res_hash=str(tx_hash.hex()))
            return redirect('w3:create_trans', id_acc=id_acc)
        form = CreateTransForm()
    return render(request, 'w3/create_trans.html', context={'account': account, 'transactions': transactions,
                                                            'form': form, 'index': index,
                                                            'languages': languages})


def hex_to_ascii(hex_str):
    hex_str = hex_str.replace(' ', '').replace('0x', '').replace('\t', '').replace('\n', '')
    ascii_str = binascii.unhexlify(hex_str.encode())
    return ascii_str


def create_text_trans(request, id_acc):
    index = IndexInfo.objects.all()[0]
    languages = Language.objects.all()
    form = CreateTextTransForm
    account = AccountMetamask.objects.get(id=id_acc)
    transactions = Transaction.objects.filter(account__id=id_acc)
    if request.method == 'POST':
        form = CreateTextTransForm(request.POST)
        if form.is_valid():
            inst = form.save(commit=False)
            inst.account = AccountMetamask.objects.get(id=id_acc)
            inst.save()
            w3 = Web3(HTTPProvider("https://ropsten.infura.io/v3/27709d11030e4a8f8a3066732c9e6b90"))

            construct_txn = {
                'from': w3.toChecksumAddress(account.user_wallet_address),
                'nonce': w3.eth.getTransactionCount(w3.toChecksumAddress(account.user_wallet_address)),
                'to': w3.toChecksumAddress(inst.to_account),
                'gas': inst.gas,
                'data': inst.data.encode('utf-8'),
                'gasPrice': w3.toWei(inst.gas_price, 'gwei')}

            signed_tx = w3.eth.account.signTransaction(construct_txn, inst.account.private_key)
            tx_hash = w3.eth.sendRawTransaction(Web3.toHex(signed_tx.rawTransaction))
            Transaction.objects.filter(id=inst.id).update(res_hash=str(tx_hash.hex()))
            transaction = w3.eth.getTransaction(tx_hash)
            Transaction.objects.filter(id=inst.id).update(data=transaction.get('input'))
            Transaction.objects.filter(id=inst.id).update(text=hex_to_ascii(transaction.get('input')).decode('utf-8'))
            return redirect('w3:create_text_trans', id_acc=id_acc)
        form = CreateTextTransForm()

    return render(request, 'w3/create_text_trans.html', context={'account': account, 'transactions': transactions,
                                                                 'form': form, 'index': index,
                                                                 'languages': languages})
