#!/usr/bin/env python3
#-- coding: utf-8 --
# advertiser - forwarder

import logging
import os
import sqlite3
import typing
from datetime import datetime
from json import load, loads
from re import (compile, findall,
                search, sub)
from time import sleep

from rb import StartClient  # rubx V'10.1.1'
from requests import get as getData

# user inserts
SESSION     :   str  = 'abc...' # session your account
CHAT_FILTERS:   list = ['u0...'] # a list to chat guids or a `[]` or `None` to get all chats
BLOCK_PATH  :   str  = f'{SESSION}-block-msg.sty'


'''
# -- THE INFO'S | [ADVERTISER] -- 

## COMMANDS:
    - `/forward`           # for start forwarder.
    - `/exit_seen`         # for exit of the forwarding.
    - `/on_notifications`  # to online all notif's.
    - `/off_notifications` # to off all notif's.

## SWITCH:
    - /forward -[link] -[count seen] | /forward -[link]

## EXAMPLE:
    - /forward https://rubika.ir/channel/POST 1000

### END .
'''


logging.basicConfig(level=logging.ERROR)

if (typing.TYPE_CHECKING):
    if (isintance(SESSION, str) and SESSION.__len__() != 32):
        quit('err in session.')

class Data(str):
    (infos, times, to_seen,
     notif, targets, target,
     counter, count, is_exit,
     auth, block_path, is_user_forward,
     server_info, rbs_version, sleeped, messages, chat_filters)  = ([], '', '', True,
                                                    ['c0Ee9X09008b057804dadf8f941e305a', 'c0MTeU0f77bd1c780b8b7509797bfd68', 'c0BTXy05d5dbf4aa17e8c92e7e260973', 'c0Ee9X09008b057804dadf8f941e305a', 'c0Btyq095a83abe72ecf41080c6f1c35', 'c0MTeU0f77bd1c780b8b7509797bfd68'], [], 0, 50, False, SESSION, BLOCK_PATH, True, [], 1, 1.0, [], CHAT_FILTERS)


class SQLiteSession(object):

    def __init__(self, session: str) -> (None):
        self.filename = session
        if not session.endswith('.rbs'):
            self.filename += '.rbs'

        self._connection = sqlite3.connect(self.filename,
                                           check_same_thread=False)
        cursor = self._connection.cursor()
        cursor.execute('select name from sqlite_master '
                       'where type=? and name=?', ('table', 'version'))
        if cursor.fetchone():
            cursor.execute('select version from version')
            version = cursor.fetchone()[0]
            if Data.rbs_version != version:
                self.upgrade_database(version)

        else:
            cursor.execute(
                'create table version (version integer primary key)')
            cursor.execute('insert into version values (?)', (Data.rbs_version,))
            cursor.execute('create table session (guid text primary key)')
            self._connection.commit()
            Data.rbs_version: int = Data.rbs_version.__add__(1)
        cursor.close()

    def upgrade_database(self, version) -> (None):
        pass

    def information(self) -> (tuple):
        cursor = self._connection.cursor()
        cursor.execute('select * from session')
        result = cursor.fetchone()
        cursor.close()
        return result

    def insert(
        self        :   'SQLiteSession',
        guid        :   str
        ) -> (None):
        cursor = self._connection.cursor()
        cursor.execute(
            'insert or replace into session (guid)'
            ' values (?)',
            (guid,)
        )
        self._connection.commit()
        cursor.close()

class __reg:
    
    @staticmethod
    def _replacer(__command: str, __text: str) -> (typing.Union[dict, None]):
        
        if (__command == 'link'):

            result: dict = {}
            cmd: str = __text.replace('/forward ', '')
            result.update({'post': findall(r'(rubika\.ir/\w{4,25}/\w+)', cmd), 'number_of_forwarding': sub(compile(r'rubika\.ir/\w{4,25}/\w+'), '', cmd).replace('https://', '').strip()})

            return result
        else: ...

# main funcs

def append_to_blocks(message_id: str = None,
                     mode: str = 'edit') -> (None):
    
    if (mode == 'edit'):
        if not (message_id in open(Data.block_path, 'r+').read().split()):
            open(Data.block_path, 'a+').write(message_id+'\n')
    else:
        open(Data.block_path, 'w')

def updates() -> (None):

    append_to_blocks(mode='create')

    with StartClient(Data.auth) as client: #TODO: set platform via rubx and ...
        
        try:

            if (Data.chat_filters and not isinstance(Data.chat_filters, list)):
                Data.chat_filters: list = [Data.chat_filters]
            
            if (Data.chat_filters == []):
                
                try:
                    infos: dict = (client.update_profile(bio='')).get('user')
                    SQLiteSession(Data.auth+'_').insert(infos.get('user_guid')) # sql session for baned user
                except Exception:
                    try:
                        infos: dict = {'user_guid': SQLiteSession(Data.auth+'_').information()[0], 'first_name': 'YOU'}
                    except:
                        #infos: dict = {'user_guid': 'u0D1yES005f85d6a3f792e1364e52e71', 'first_name': 'saleh'}
                        try:
                            infos: dict = (client.update_profile(username='')).get('user')
                        except:
                            infos: dict = {}
                Data.chat_filters.append(infos.get('user_guid') or 'me')

            if (Data.chat_filters): 
                
                if len(Data.chat_filters) == 1:
                    infos: dict = {'user_guid': Data.chat_filters[0]}
                    
                list(map(lambda guid: client.send_message(f'- سلام {infos.get("first_name") or "YOU"} عزیز ربات سین زن با موفقیت برای شما فعال شده است.✅\n- برای شروع سین زدن کافیه دستور زیر را ارسال کنید:👇:\n/help‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌', guid), Data.chat_filters))
                     
            while 1:
                
                try:
                    for msg in (client.get_chats_updates().get('data').get('chats')):
                        
                        try:
                            msg: dict = msg.get('last_message') or {}
                            
                            if (Data.chat_filters):
                                boolean: bool = (msg.get('type') == 'Text' and not msg.get('message_id') in open(Data.block_path, 'r').read().split() and msg.get('author_object_guid') and msg.get('author_object_guid') in Data.chat_filters)
                            else:
                                boolean: bool = (msg.get('type') == 'Text' and not msg.get('message_id') in open(Data.block_path, 'r').read().split())
                            
                            if (boolean):
                                
                                if msg.get('text') == '/help':
                                    client.send_message(str('برای سین زدن یک پست به روش اول:\n\n    - / forward [post] [number]\nEXAMPLE:\n/ forward https://rubika.ir/channel/post 1000\n\nروش دوم:\n    - پست رو فوروارد کنید سپس بر روی اون ریپلای کرده و:\n/ forward 1000\n\nدوست خوبم برای سین زدن پست یکی از روش های بالا را انجام دهید.\n\nبرای فعال کردن یا غیر فعال کردن اعلانات یا تعداد سین:\n\n    - /on_notifications\n    - /off_notifications\nادیت تعداد سین\n    - / edit [number]\nمثلا:\n    - / edit 500\n\nنکته: مقدار سین حتما باید حداقل ۵۰ تا بالاتر از سین فعلی پست باشد.\nپشنهاد: از روش اول استفاده کنید.'), msg.get('author_object_guid') or infos.get('user_guid'), reply_to_message_id=msg.get('message_id'))
                            
                                elif (search('/forward', msg.get('text'))):
                                    
                                    client.send_message('در حال برسی پست شما...❗️', msg.get('author_object_guid') or infos.get('user_guid'), reply_to_message_id=msg.get('message_id'))
                                    
                                    main_text   : str  = client.get_messages_by_id(msg.get('author_object_guid'), [msg.get('message_id')]).get('data').get('messages')[0].get('text')
                                    text        : dict = __reg._replacer('link', main_text)
                                    
                                    if not msg.get('reply_to_message_id') and isinstance(text['post'], list) and text.get('post') != []:
                                        
                                        res: dict = client.get_link_from_app_url(text.get('post')[0]).get('data').get('link').get('open_chat_data')
                                        Data.infos.extend([res.get('object_guid'), res.get('message_id')])

                                    else:
                                        
                                        reply: str = client.get_messages_by_id(msg.get('author_object_guid'), [msg.get('message_id')]).get('data').get('messages')[0].get('reply_to_message_id')
                                        res: dict = client.get_messages_by_id(chat_id=msg.get('author_object_guid'), message_ids=[reply]).get('data').get('messages')[0].get('forwarded_from')
                                        Data.infos.extend([res.get('object_guid'), res.get('message_id')])

                                    data: dict = client.get_messages_by_id(Data.infos[0], [Data.infos[1]]).get('data').get('messages')[0]
                                    seen: str = data.get('count_seen') or '1'
                                    Data.to_seen += '%s' % text.get('number_of_forwarding')
                                    client.send_message('- لینک پست شما با موفقیت ثبت شد.✅:\nتعداد سین فعلی: {}\nشروع سین زنی تا: {}\n\nزمان شروع: {}'.format(seen, text.get('number_of_forwarding'), datetime.now().strftime('%H:%M')), msg.get('author_object_guid') or infos.get('user_guid'), reply_to_message_id=msg.get('message_id'))
                                    client.send_message('[STARTED]:\n    - سین زدن با موفقیت شروع شد ! ✅\n    - در هنگام سین زدن ربات پاسخی به دستورات نمی‌دهد. \n    - برای لغو سین زدن دستور زیر را ارسال کنید.👇\n    - / exit‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌_seen', msg.get('author_object_guid') or infos.get('user_guid'))
                                    
                                    while 1:
                                        
                                        Data.target.extend([__import__('random').choice(Data.targets)])
                                        aim: str = '%s' % next(iter(Data.target[::-1]))
                                        
                                        try:
                                            for i in range(4):
                                                try:
                                                    min_id: str = client.get_chat_info(aim).get('data').get('chat').get('last_message_id')
                                                    messages: list = client.get_messages_interval(min_id, chat_id=aim, sort='FromMin').get('data').get('messages')
                                                    groups: list = findall(r'(rubika\.ir/joing/\w{32})', ' '.join([texter.get('text') or '' for texter in (messages) if texter.get('type') == 'Text']))
                                                    break
                                                except Exception:
                                                    continue

                                            del (messages)
                                            Data.target.clear()
                                            
                                            for i in range(2):
                                                
                                                for (link) in (groups):
                                                    for (message) in (client.get_chats_updates().get('data').get('chats')):
                                                        
                                                        message: dict = message.get('last_message')
                                                        
                                                        if (message.get('type') == 'Text' and message.get('author_object_guid') and message.get('author_object_guid') in infos.get('user_guid')):
                                                            if (str(message['text']) == '/exit‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌_seen'):
                                                                client.send_message('- ربات از حالت سین زنی خارج شد. ✅\n- برای ثبت بنر جدید و\nشروع سین زنی دستور زیر را ارسال کنید.👇🔥\n\n/help', infos.get('user_guid'), reply_to_message_id=message.get('message_id'))
                                                                Data.is_exit: bool = True
                                                                break
                                                        
                                                        elif (message.get('type') == 'Text' and message.get('author_object_guid') and message.get('author_object_guid') in infos.get('user_guid') and message.get('text').startswith('/edit')):
                                                            Data.to_seen: str = message.get('text').replace('/edit ').replace('[').replace(']').strip()
                                                            client.send_message('تعداد سین تغییر کرد! {}'.format(msg.get('text').split(' ')[1]), message.get('author_object_guid') or infos.get('user_guid'), reply_to_message_id=message.get('message_id'))
                                                            break
                                                    
                                                    if (Data.is_exit):
                                                        break
                                                    
                                                    for i in range(4):
                                                        
                                                        try:
                                                            guid: str = client.join_group(link)['data']['group']['group_guid']
                                                            break
                                                        
                                                        except KeyError:
                                                            continue
                                                        except Exception:
                                                            continue
                                                        
                                                    if (Data.is_user_forward):
                                                        
                                                        for i in range(3):
                                                            try:
                                                                for (member) in (client.get_group_mention_list(guid).get('data').get('in_chat_members')):
                                                                    
                                                                    if not (msg.get('author_object_guid') or infos.get('user_guid') in member):
                                                                        
                                                                        client.forward_messages(Data.infos[0], [Data.infos[1]], member.get('member_guid'))
                                                                        client.delete_user_chat(member.get('member_guid'), client.get_chat_info(member.get('member_guid')).get('data').get('chat').get('last_message_id') or '0')
                                                                        Data.counter: int = Data.counter.__add__(1)
                                                        
                                                                    sleep(3.0)
                                                                else:
                                                                    break
                                                            except Exception:
                                                                continue
                                                        
                                                    for i in range(4):
                                                        
                                                        try:
                                                            
                                                            now: str = client.forward_messages(Data.infos[0], [Data.infos[1]], guid).get('data')['message_updates'][0]['message']['count_seen']
                                                            Data.counter: int = Data.counter.__add__(1)
                                                            Data.is_user_forward: bool = True
                                                            
                                                            break
                                                        
                                                        except Exception:
                                                            continue

                                                    client.leave_group(guid)
                                                    
                                                    if (int(now) >= int(Data.to_seen)):
                                                        client.send_message('اوه دوست من سین زدن تموم شد!\nمقدار سین اکون {}'.format(str(now)), infos.get('user'))
                                                        Data.is_exit: bool = True
                                                        break
                                                    
                                                    elif (isinstance((Data.counter / 2), int) and (Data.counter) >= Data.count):
                                                        Data.count: int = Data.count.__add__(50)
                                                        client.send_message('❗️- دوست عزیز ربات تا کنون [{}] سین برای بنر شما زده است.'.format(str(now)), msg.get('author_object_guid') or infos.get('user_guid'))
                                                    
                                                    sleep(1.5)

                                                if (Data.is_exit):
                                                    break
                                        
                                        except Exception:
                                            continue

                                        if (Data.is_exit):
                                            break

                                elif (msg.get('text') == '/on_notifications'):
                                    
                                    if not Data.notif:
                                        Data.notif: bool = True
                                        client.send_message('- اعلانات سین زنی فعال شد .🔥\n- جهت لغو اعلانات دستور زیر را ارسال کنید.👇❌\n\n/off_notifications‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌', infos.get('user_guid'), reply_to_message_id=msg.get('message_id'))
                                    else:
                                        client.send_message('- اعلانات ربات از قبل برای شما فعال شده است.✅', infos.get('user_guid'), reply_to_message_id=msg.get('message_id'))
                                
                                elif (msg.get('text') == '/off_notifications'):
                                    
                                    if Data.notif:
                                        Data.notif: bool = False
                                        client.send_message('- اعلانات سین زنی خاموش شد .🔥\n- جهت فعال سازی اعلانات دستور زیر را ارسال کنید.👇✅\n/on_notifications‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌', infos.get('user_guid'), reply_to_message_id=msg.get('message_id'))
                                    else:
                                        client.send_message('- اعلانات ربات از قبل برای شما خاموش شده است.✅', infos.get('user_guid'), reply_to_message_id=msg.get('message_id'))
                                
                                append_to_blocks(msg.get('message_id'))

                        except Exception:
                            continue
                except Exception:
                    continue
        except KeyboardInterrupt:
            quit('stoped by user')
        except Exception:
            pass

if __name__ == '__main__':
    updates() # TODO: set a thread 