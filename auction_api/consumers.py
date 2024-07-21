import json
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import async_to_sync
from core.models import User
from .models import Auction
from asgiref.sync import async_to_sync
from .tasks import auction_timer_task
from auction.celery  import app
from channels.db import database_sync_to_async
from datetime import timedelta
from django.core.cache import cache


class AuctionConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        
        self.auction_pk = self.scope['url_route']['kwargs']['pk']
        self.room_group_name = f'auction_{self.auction_pk}'
        self.task_id = None
        auction = await database_sync_to_async(Auction.objects.get)(id=self.auction_pk)
        self.starting_bid = auction.starting_bid

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

      
        await self.accept()


    async def disconnect(self, code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )


    async def receive(self, text_data=None, bytes_data=None):
        text_data_json = json.loads(text_data)
        bid = text_data_json['bid']

        task_id = cache.get(self.room_group_name)
        prev_bid = cache.get(f'{self.room_group_name}_bid')

        if not prev_bid:
            prev_bid = self.starting_bid

        if float(prev_bid) < float(bid): 
        
            if task_id:
                app.control.revoke(task_id, terminate=True)

            new_task_id = auction_timer_task.apply_async(
                args=[self.room_group_name, self.scope['user'].username, bid, self.auction_pk], countdown=60).id
            
            
            cache.set(f'{self.room_group_name}_bid', bid)
            cache.set(self.room_group_name, new_task_id)
            

            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'update_bid',
                    'bid': bid,
                    'username': self.scope['user'].username
                }
            )
            
    

    async def update_bid(self, event):

        bid = event['bid']

        await self.send(text_data=json.dumps(
            {
                'username': event['username'],
                'bid': bid,
                'protocol': 'UPDATE'
            }
        ))


    async def finish_auction(self, event):

        await self.send(text_data=json.dumps(
            {
                'bid': event['bid'],
                'username': event['username'],
                'protocol': 'FINISHED'

            }
        ))