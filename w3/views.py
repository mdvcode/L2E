import binascii
import requests
from django.shortcuts import render, redirect
from rest_framework.response import Response
from rest_framework.views import APIView
from web3 import Web3, HTTPProvider
from blog.models import IndexInfo, Language
from w3.forms import ConnectWallet, CreateTransForm, CreateTextTransForm, IPFSTransForm, ResultHashForm, \
    UpdateTransForm, UpdateTextTransactionForm, UpdateIPFSTransaction
from w3.models import AccountMetamask, Transaction, IPFS


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
            inst = form.save(commit=False)
            inst.user = request.user
            inst.save()
    form = ConnectWallet()
    return render(request, 'w3/connect.html', context={'form': form, 'connections': connections, 'index': index,
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
            return redirect('w3:update_trans', id_transaction=inst.id)
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
            return redirect('w3:update_texttrans', id_transaction=inst.id)
        form = CreateTextTransForm()

    return render(request, 'w3/create_text_trans.html', context={'account': account, 'transactions': transactions,
                                                                 'form': form, 'index': index,
                                                                 'languages': languages})


def ipfs(request):
    index = IndexInfo.objects.all()[0]
    languages = Language.objects.all()
    if request.method == "POST":
        form = IPFSTransForm(request.POST or None, request.FILES or None)
        if form.is_valid():
            inst = form.save(commit=False)
            inst.user = request.user
            inst.save()
            return redirect('w3:ipfs')
    form = IPFSTransForm()
    list_IPFS = IPFS.objects.filter(user=request.user)
    return render(request, 'w3/ipfs_trans.html', context={'form': form, 'list_IPFS': list_IPFS, 'index': index,
                                                          'languages': languages})


def item_ipfs(request, id_ipfs):
    index = IndexInfo.objects.all()[0]
    languages = Language.objects.all()
    item = IPFS.objects.get(id=id_ipfs)
    if request.method == "POST":
        form = IPFSTransForm(request.POST, request.FILES)
        files = {
            'file': bytes(item.file.read())
        }
        response = requests.post('https://ipfs.infura.io:5001/api/v0/add', files=files,
                                 auth=('29QAqPI0HxrbfPWaTYotMnpdyho', 'a1d30f9c414e15aa990a140ac924f33b'))
        data_url = 'https://ipfs.io/ipfs/' + response.json().get('Hash')
        IPFS.objects.filter(id=id_ipfs).update(account=form.data.get('account'),
                                               text=data_url, hash_ipfs=response.json().get('Hash'))
        ipfs = IPFS.objects.get(id=id_ipfs)
        return redirect('w3:update_ipfstrans', id_transaction=ipfs.id)
    form = IPFSTransForm
    return render(request, 'w3/item_ipfs.html', context={'item': item, 'index': index,
                                                         'languages': languages, 'form': form})


def result_ipfs_hash(request):
    index = IndexInfo.objects.all()[0]
    languages = Language.objects.all()
    result = ''
    if request.method == "POST":
        form = ResultHashForm(request.POST)
        if form.is_valid():
            params = (
                ('arg', form.data.get('hash')),
            )
            response = requests.post('https://ipfs.infura.io:5001/api/v0/cat', params=params,
                                     auth=('29QAqPI0HxrbfPWaTYotMnpdyho', 'a1d30f9c414e15aa990a140ac924f33b'))
            result = response.text
    form = ResultHashForm
    return render(request, 'w3/result_ipfs_hash.html', context={'form': form, 'result': result, 'index': index,
                                                                'languages': languages})


def update_trans(request, id_transaction):
    index = IndexInfo.objects.all()[0]
    languages = Language.objects.all()
    transactions = Transaction.objects.get(id=id_transaction)
    if request.method == 'POST':
        form = UpdateTransForm(instance=transactions, data=request.POST or None)
        if form.is_valid():
            form.save()
            return redirect('w3:update_trans', id_transaction=id_transaction)
    form = UpdateTransForm(instance=transactions)
    w3 = Web3(HTTPProvider("https://ropsten.infura.io/v3/27709d11030e4a8f8a3066732c9e6b90"))
    value = w3.toWei(transactions.value, 'ether')
    return render(request, 'w3/update_trans.html', context={'form': form, 'transactions': transactions,
                                                            'value': value, 'index': index,
                                                            'languages': languages, 'id_transaction': id_transaction})


def update_texttrans(request, id_transaction):
    index = IndexInfo.objects.all()[0]
    languages = Language.objects.all()
    transactions = Transaction.objects.get(id=id_transaction)
    if request.method == 'POST':
        form = UpdateTextTransactionForm(instance=transactions, data=request.POST or None)
        if form.is_valid():
            form.save()
            return redirect('w3:update_texttrans', id_transaction=id_transaction)
    form = UpdateTextTransactionForm(instance=transactions)
    s = transactions.data.encode('utf-8')
    data = str(s.hex())
    return render(request, 'w3/update_texttrans.html', context={'form': form, 'data': data, 'index': index,
                                                                'languages': languages, 'id_transaction': id_transaction})


def update_ipfstrans(request, id_transaction):
    index = IndexInfo.objects.all()[0]
    languages = Language.objects.all()
    item = IPFS.objects.get(id=id_transaction)
    if request.method == 'POST':
        form = UpdateIPFSTransaction(instance=item, data=request.POST or None)
        if form.is_valid():
            form.save()
            return redirect('w3:update_ipfstrans', id_transaction=id_transaction)
    form = UpdateTextTransactionForm(instance=item)
    s = item.text.encode('utf-8')
    data = str(s.hex())
    return render(request, 'w3/update_ipfstrans.html', context={'form': form,
                                                                'data': data, 'index': index, 'languages': languages,
                                                                'id_transaction': id_transaction})


class UpdateHashTransaction(APIView):
    def post(self, request, *args, **kwargs):
        transaction = Transaction.objects.get(id=request.data.get('id'))
        transaction.res_hash = request.data.get('res_hash')
        transaction.save()
        return Response(transaction.res_hash, transaction)


class UpdateIPFSHashTransaction(APIView):
    def post(self, request, *args, **kwargs):
        transaction = IPFS.objects.get(id=request.data.get('id'))
        transaction.result_hash = request.data.get('result_hash')
        transaction.save()
        return Response(transaction.result_hash, transaction)


class UpdateAccountIPFS(APIView):
    def post(self, request, *args, **kwargs):
        account = IPFS.objects.get(id=request.data.get('id'))
        account.account = request.data.get('account')
        account.save()
        return Response(account.user_wallet_address, account)

