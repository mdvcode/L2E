from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render, redirect
from web3 import Web3, HTTPProvider

from blog.models import IndexInfo, Language
from message.forms import CreateMessageForm, SendForm, UpdateMessageForm, UpdateInfoMessageForm
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
            return redirect('message:update_createmessage')
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
    index = IndexInfo.objects.all()[0]
    languages = Language.objects.all()
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
            return redirect('message:update_infomessage', message_id=message.id)
            # w3 = Web3(HTTPProvider("https://ropsten.infura.io/v3/27709d11030e4a8f8a3066732c9e6b90"))
            # construct_txn = {
            #     'from': w3.toChecksumAddress(inst.metamask.user_wallet_address),
            #     'nonce': w3.eth.getTransactionCount(w3.toChecksumAddress(inst.metamask.user_wallet_address)),
            #     'to': w3.toChecksumAddress(inst.metamask_to),
            #     'gas': inst.gas,
            #     'data': base64.b64encode(inst.text.encode('utf-8')),
            #     'gasPrice': w3.toWei(inst.gas_price, 'gwei')}
            #
            # signed_tx = w3.eth.account.signTransaction(construct_txn, inst.metamask.private_key)
            # tx_hash = w3.eth.sendRawTransaction(Web3.toHex(signed_tx.rawTransaction))
            # Message.objects.filter(id=inst.id).update(res_hash=str(tx_hash.hex()))
    form = SendForm
    return render(request, 'message/infomessage.html', context={'message': message, 'form': form, 'index': index,
                                                                'languages': languages})


def update_createmessage(request):
    index = IndexInfo.objects.all()[0]
    languages = Language.objects.all()
    messages = Message.objects.filter(user=request.user)[0]
    if request.method == "POST":
        form = UpdateMessageForm(instance=messages, data=request.POST or None)
        if form.is_valid():
            inst = form.save(commit=False)
            inst.user = request.user
            inst.save()
            return redirect('message/update_createmessage')
    form = UpdateMessageForm(instance=messages)
    w3 = Web3(HTTPProvider("https://ropsten.infura.io/v3/27709d11030e4a8f8a3066732c9e6b90"))
    gasprice = w3.toWei(messages.gas_price, 'gwei')
    gas = messages.gas
    s = base64.b64encode(messages.text.encode('utf-8'))
    text = str(s.hex())
    return render(request, 'message/update_createmessage.html', context={'form': form, 'gasprice': gasprice,
                                                                         'gas': gas, 'text': text, 'index': index,
                                                                         'languages': languages})


def update_infomessage(request, message_id):
    index = IndexInfo.objects.all()[0]
    languages = Language.objects.all()
    message = Message.objects.filter(id=message_id)[0]
    if request.method == "POST":
        form = UpdateInfoMessageForm(instance=message, data=request.POST or None)
        if form.is_valid():
            inst = form.save(commit=False)
            inst.user = request.user
            inst.metamask_to = message.metamask.user_wallet_address
            inst.metamask = AccountMetamask.objects.get(user_wallet_address=message.metamask_to)
            inst.save()
            return redirect('message/update_infomessage', message_id=message_id)
    form = UpdateInfoMessageForm(instance=message)
    w3 = Web3(HTTPProvider("https://ropsten.infura.io/v3/27709d11030e4a8f8a3066732c9e6b90"))
    from_acc = message.metamask_to
    print(from_acc)
    to_acc = message.metamask.user_wallet_address
    gasprice = w3.toWei(message.gas_price, 'gwei')
    gas = message.gas
    s = base64.b64encode(message.text.encode('utf-8'))
    text = str(s.hex())
    return render(request, 'message/update_infomessage.html', context={'form': form, 'gas': gas, 'gasprice': gasprice,
                                                                       'text': text, 'index': index,
                                                                       'languages': languages, 'from_acc': from_acc,
                                                                       'to_acc': to_acc})
