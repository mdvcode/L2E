from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render, redirect
from web3 import Web3, HTTPProvider

from blog.models import IndexInfo, Language
from message.forms import CreateMessageForm, SendForm
from message.models import Message
import base64

from w3.models import AccountMetamask


def create_message(request):
    index = IndexInfo.objects.all()[0]
    languages = Language.objects.all()
    if str(request.user) == 'AnonymousUser':
        return redirect('/users/login/')
    messages = Message.objects.filter(user=request.user).order_by('-id')
    paginator = Paginator(messages, 10)
    page_num = request.GET.get('page')
    try:
        messages = paginator.page(page_num)
    except PageNotAnInteger:
        messages = paginator.page(1)
    except EmptyPage:
        messages = paginator.page(paginator.num_pages)
    if request.method == "POST":
        form = CreateMessageForm(request.POST)
        if form.is_valid():
            inst = form.save(commit=False)
            inst.user = request.user
            inst.save()

            w3 = Web3(HTTPProvider("https://ropsten.infura.io/v3/27709d11030e4a8f8a3066732c9e6b90"))
            construct_txn = {
                'from': w3.toChecksumAddress(inst.metamask.user_wallet_address),
                'nonce': w3.eth.getTransactionCount(w3.toChecksumAddress(inst.metamask.user_wallet_address)),
                'to': w3.toChecksumAddress(inst.metamask_to),
                'gas': inst.gas,
                'data': base64.b64encode(inst.text.encode('utf-8')),
                'gasPrice': w3.toWei(inst.gas_price, 'gwei')}

            signed_tx = w3.eth.account.signTransaction(construct_txn, inst.metamask.private_key)
            tx_hash = w3.eth.sendRawTransaction(Web3.toHex(signed_tx.rawTransaction))
            Message.objects.filter(id=inst.id).update(res_hash=str(tx_hash.hex()))
    form = CreateMessageForm
    return render(request, 'message/create_message.html', context={'form': form, 'index': index,
                                                                   'languages': languages, 'messages': messages})


def my_messages(request):
    index = IndexInfo.objects.all()[0]
    languages = Language.objects.all()
    list_metamask_to = []
    for item in AccountMetamask.objects.filter(user=request.user):
        list_metamask_to.append(item.user_wallet_address)
    messages = Message.objects.filter(metamask_to__in=list_metamask_to).order_by('-id')
    paginator = Paginator(messages, 10)
    page_num = request.GET.get('page')
    try:
        messages = paginator.page(page_num)
    except PageNotAnInteger:
        messages = paginator.page(1)
    except EmptyPage:
        messages = paginator.page(paginator.num_pages)
    return render(request, 'message/mymessages.html', context={'index': index, 'messages': messages,
                                                               'languages': languages})


def info_message(request, message_id):
    message = Message.objects.get(id=message_id)
    if message.show is False:
        message.show = True
        message.save()
    if request.method == "POST":
        form = SendForm(request.POST)
        if form.is_valid():
            inst = form.save(commit=False)
            inst.user = request.user
            inst.metamask_to = message.metamask.user_wallet_address
            inst.metamask = AccountMetamask.objects.get(user_wallet_address=message.metamask_to)
            inst.save()
            w3 = Web3(HTTPProvider("https://ropsten.infura.io/v3/27709d11030e4a8f8a3066732c9e6b90"))
            construct_txn = {
                'from': w3.toChecksumAddress(inst.metamask.user_wallet_address),
                'nonce': w3.eth.getTransactionCount(w3.toChecksumAddress(inst.metamask.user_wallet_address)),
                'to': w3.toChecksumAddress(inst.metamask_to),
                'gas': inst.gas,
                'data': base64.b64encode(inst.text.encode('utf-8')),
                'gasPrice': w3.toWei(inst.gas_price, 'gwei')}

            signed_tx = w3.eth.account.signTransaction(construct_txn, inst.metamask.private_key)
            tx_hash = w3.eth.sendRawTransaction(Web3.toHex(signed_tx.rawTransaction))
            Message.objects.filter(id=inst.id).update(res_hash=str(tx_hash.hex()))
    form = SendForm
    return render(request, 'message/infomessage.html', context={'message': message, 'form': form})
