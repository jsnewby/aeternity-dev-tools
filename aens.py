#!/usr/bin/python

"""
Æternity Naming System interface

Author: John Newby

Copyright (c) 2018 aeternity developers

Permission to use, copy, modify, and/or distribute this software for
any purpose with or without fee is hereby granted, provided that the
above copyright notice and this permission notice appear in all
copies.

THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL
WARRANTIES WITH REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED
WARRANTIES OF MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL THE
AUTHOR BE LIABLE FOR ANY SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL
DAMAGES OR ANY DAMAGES WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR
PROFITS, WHETHER IN AN ACTION OF CONTRACT, NEGLIGENCE OR OTHER
TORTIOUS ACTION, ARISING OUT OF OR IN CONNECTION WITH THE USE OR
PERFORMANCE OF THIS SOFTWARE.

"""

import asyncio
from epoch import Epoch
import json
import os
import requests
import urllib
from websocket import create_connection

class AENS(Epoch):

    def __init__(self):
        super().__init__()
        self.name_url = "http://localhost:" + os.environ['AE_LOCAL_PORT'] \
                        + "/v2/name"
        internal_url = "http://localhost:" + \
                         os.environ['AE_LOCAL_INTERNAL_PORT'] 
        self.pre_claim_url = internal_url + "/v2/name-preclaim-tx"
        self.claim_url = internal_url + "/v2/name-claim-tx"
        self.update_url = internal_url + "/v2/name-update-tx"
        self.transfer_url = internal_url + "/v2/name-transfer-tx"
        self.revoke_url = internal_url + "/v2/name-revoke-tx"
        
    def query(self, name):
        try:
            js = urllib.request.urlopen(self.name_url + "?name=" + name).\
                                                                 read().\
                                                                 decode("utf8")
        except urllib.error.HTTPError:
            # Name not found, not URL not found.
            return None
        
        data = json.loads(js)
        print(data)
        return data
        
    # Commitment hash needs to be passed in right now 
    def pre_claim(self, commitment, fee):
        query = { "commitment": commitment,
                  "fee": fee }
        response = json.loads(requests.post(self.pre_claim_url,
                                            json = query).text)
        try:
            return response['commitment']
        except KeyError:
            return None

    def claim(self, name, salt, fee):
        query = {"name": name,
                 "name_salt": salt,
                 "fee": fee}
        response = json.loads(requests.post(self.claim_url,
                                            json = query).text) 
        try:
            return response['name_hash']
        except KeyError:
            return None

    def update(self, target, name_hash, name_ttl, ttl, fee):
        if target.startswith("ak"):
            pointers = { "account_pubkey": target }
        else:
            pointers = { "oracle_pubkey": target }
            
        query = {"name_hash": name_hash,
                 "name_ttl": name_ttl,
                 "ttl": ttl,
                 "pointers": pointers,
                 "fee": fee }
        print(json.dumps(query))
        data = requests.post(self.update_url,
                             json = query).text
        print(data)
        response = json.loads(data) 
        try:
            return response['name_hash']
        except KeyError:
            return None

    def transfer(self, name_hash, recipient):
        query = {"name_hash": name_hash,
                 "recipient_pubkey": recipient,
                 "fee": 1 }
        response = json.loads(requests.post(self.transfer_url,
                                            json = query).text) 
        try:
            return response['name_hash']
        except KeyError:
            return None

    def revoke(self, name_hash, fee = 1):
        query = {"name_hash": name_hash,
                 "fee": fee}
        response = json.loads(requests.post(self.revoke_url,
                                            json = query).text) 
        try:
            return response['name_hash']
        except KeyError:
            return None

        
