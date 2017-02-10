import json

from django.shortcuts import render

from .models import ChatAndReply, Notice, Poll
from manage_room.models import Room

# Create your views here.
def get_chat_list(request):
    # request is room's label
    room = Room.objects.get(label=request)

    chats = ChatAndReply.objects.filter(room=room, is_reply=False).order_by('time')
    replies = ChatAndReply.objects.filter(room=room, is_reply=True).order_by('time')

    return (chats, replies)

def get_notice_list(request):
    # request is room's label
    room = Room.objects.get(label=request)

    notices = Notice.objects.filter(room=room).order_by('time')

    return notices

def get_poll_list(request):
    #request is room's label
    room = Room.objects.get(label=request)

    polls = Poll.objects.filter(room=room).order_by('time')
    json_polls = []
    for poll in polls:
        temp = {
                'result_poll': room.label,
                'question': poll.question,
                'hash_value': poll.hash_value,
                'answer': poll.answer,
                'answer_count': poll.answer_count
            }
        json_polls.append(json.dumps(temp))

    return json_polls
