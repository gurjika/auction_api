from celery import shared_task
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

@shared_task
def auction_timer_task(room_group_name, username, bid):
    channel_layer = get_channel_layer()
    event = {
        'type': 'finish_auction',
        'username': username,
        'bid': bid
        }
    async_to_sync(channel_layer.group_send)(group=room_group_name, message=event)


