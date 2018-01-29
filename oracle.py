#!/usr/bin/python

"""
Test oracle client
Author: John Newby

(c) Ape Unit 2018
"""

import asyncio
from epoch import Epoch
import json
import os
from websocket import create_connection

class Oracle:
    def __init__(self):
        self.pub_key = os.environ['AE_PUB_KEY']
        self.url = "ws://localhost:" + os.environ['AE_WEBSOCKET'] + "/websocket"
        self.websocket = None
        self.local_port = os.environ['AE_LOCAL_PORT']
        self.local_internal_port = os.environ['AE_LOCAL_INTERNAL_PORT']
        self.epoch = Epoch()

    def connect_websocket(self):
        if not self.websocket:
            self.websocket = create_connection(self.url)

    def register(self, query_format, response_format, query_fee, ttl, fee):
        self.connect_websocket()
        query = { "target": "oracle",
                  "action": "register",
                  "payload": { "type": "OracleRegisterTxObject",
                               "vsn": 1,
                               "account": self.pub_key,
                               "query_format": query_format,
                               "response_format": response_format,
                               "query_fee": int(query_fee),
                               "ttl": {"type": "delta",
                                       "value": int(ttl)},
                               "fee": int(fee) } }
        j = json.dumps(query)
        print(j)
        self.epoch.update_top_block()
        self.websocket.send(j)
        response = json.loads(self.websocket.recv())
        if not response['payload']['result'] == "ok":
            raise RuntimeError(response)
        oracle_id = response['payload']['oracle_id']
        self.epoch.wait_for_block()
        return oracle_id

    def wait_for_block(self):
        self.epoch.update_top_block()
        self.epoch.wait_for_block()
            
    def subscribe(self, oracle_id, callback = None):
        self.connect_websocket()
        query = {"target": "oracle",
                 "action": "subscribe",
                 "payload": {"type": "query",
                             "oracle_id": oracle_id }}
        j = json.dumps(query)
        self.websocket.send(j)
        response = json.loads(self.websocket.recv())
        print(response)
        if not response['payload']['result'] == 'ok':
            raise RuntimeError(response)
        id = response['payload']['subscribed_to']['oracle_id']
        mining_events = 0
        while True:
            data = self.websocket.recv()
            j = json.loads(data)
            print(j)
            if j['action'] == 'mined_block':
                mining_events += 1
                next
            if j['action'] == 'new_oracle_query':
                if callback:
                    callback(j)
            else:
                print("Unhandled")
        if mining_events == 0:
            self.epoch.wait_for_block()
        
    def query(self, oracle_pubkey, query_fee, query_ttl, response_ttl,
              fee, query):
        self.connect_websocket()
        request = {"target": "oracle",
                   "action": "query",
                   "payload": {"type": "OracleQueryTxObject",
                               "vsn": 1,
                               "oracle_pubkey": oracle_pubkey,
                               "query_fee": int(query_fee),
                               "query_ttl": {"type": "delta",
                                             "value": int(query_ttl)},
                               "response_ttl": {"type": "delta",
                                                "value": int(response_ttl)},
                               "fee": int(fee),
                               "query": query }}
        j = json.dumps(request)
        print(j)
        self.websocket.send(j)
        response = self.websocket.recv()
        print(response)
        response = json.loads(response)
        if response['payload']['result'] == "ok":
            return response['payload']['query_id']
        self.epoch.wait_for_block()
        return False

    def subscribe_query(self, query_id, callback = None):
        self.connect_websocket()
        request = {"target": "oracle",
                   "action": "subscribe",
                   "payload": {"type": "response",
                               "query_id": query_id }}
        j = json.dumps(request)
        print(j)
        self.websocket.send(j)
        response = self.websocket.recv()
        response = json.loads(response)
        print(response)
        if not response['payload']['result'] == "ok":
            raise RuntimeError(response)
        while True:
            data = self.websocket.recv()
            data = json.loads(data)
            print(data)
            if callback:
                callback.call(data)

    def respond(self, query_id, fee, reply):
        self.connect_websocket()
        response = {"target": "oracle",
                    "action": "response",
                    "payload": {"type": "OracleResponseTxObject",
                                "vsn": 1,
                                "query_id": query_id,
                                "fee": int(fee),
                                "response": reply}}
        response = json.dumps(response)
        print(response)
        self.websocket.send(response)
        
    
    






