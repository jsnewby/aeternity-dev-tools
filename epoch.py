#!/usr/bin/python

"""Class encapsulating epoch calls
Author: John Newby

Copyright (c) 2018 aeternity developers

Permission to use, copy, modify, and/or distribute this software for
any purpose with or without fee is hereby granted, provided that the
above copyright notice and this permission notice appear in allqq
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

import json
import os
import time
import urllib.request
from websocket import create_connection

class Epoch:
    def __init__(self):
        self.pub_key = os.environ['AE_PUB_KEY']
        self.url = "ws://localhost:" + os.environ['AE_WEBSOCKET'] + "/websocket"
        self.websocket = None
        self.local_port = os.environ['AE_LOCAL_PORT']
        self.local_internal_port = os.environ['AE_LOCAL_INTERNAL_PORT']
        self.top_block_url = "http://localhost:" + os.environ['AE_LOCAL_PORT'] \
                             + "/v2/top"
        self.top_block = None
        self.sleep_period = 10

    def connect_websocket(self):
        if not self.websocket:
            self.websocket = create_connection(self.url)

    def get_top_block(self):
        js = urllib.request.urlopen(self.top_block_url).read().\
               decode("utf8")
        data = json.loads(js)
        print(data)
        return int(data['height'])

    def update_top_block(self):
        self.top_block = self.get_top_block()        
    
    def wait_for_block(self):
        while True:
            time.sleep(self.sleep_period)
            new_block = self.get_top_block()
            if(new_block > self.top_block):
                self.top_block = new_block
                break
