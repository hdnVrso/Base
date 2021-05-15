#!/usr/bin/env python
# -*- coding: utf-8 -*-

import configparser
from telethon.errors import SessionPasswordNeededError
from telethon.sync import TelegramClient
from telethon import functions


class TelegramApiWrapper:
    def __init__(self):
        config = configparser.ConfigParser()
        config.read("telegram_api_wrapper/config.ini")
        api_id = config['Telegram']['api_id']
        api_hash = config['Telegram']['api_hash']
        self.phone = config['Telegram']['phone']
        username = config['Telegram']['username']
        self.client = TelegramClient(username, api_id, api_hash)

    def check_auth(self, user):
        if not user.is_user_authorized():
            user.send_code_request(self.phone)
            try:
                user.sign_in(self.phone, input('Enter the code: '))
            except SessionPasswordNeededError:
                user.sign_in(password=input('Password: '))

    def search_channels(self, search_query):
        self.client.start()
        self.check_auth(self.client)
        result = self.client(functions.contacts.SearchRequest(
            q=search_query,
            limit=4
        ))
        channels_dicts = []
        links = ""
        counter = 0
        for channel in result.chats:
            if counter == 3:
                break
            full_result = self.client(functions.channels.GetFullChannelRequest(
                channel=channel.id
            ))
            channel_dict = self.create_dict(channel,
                                            full_result.full_chat.about)
            links += "\n" + channel_dict['link']
            channels_dicts.append(channel_dict)
            counter += 1
        # self.send_messages("@marshaldub", links)#Изменить
        return channels_dicts

    def send_messages(self, username, message):
        result = self.client(functions.messages.SendMessageRequest(
            peer=username,
            message=message
        ))
        return result

    def create_dict(self, channel, channel_info):
        result_dict = {}
        result_dict.setdefault("title", channel.title)
        result_dict.setdefault("members", channel.participants_count)
        result_dict.setdefault("link", "t.me/" + channel.username)
        result_dict.setdefault("channel_info", channel_info)
        return result_dict
