#!/usr/bin/python

"""Simple post office for aeternity. Registers a free oracle which
accepts mails in the JSON format { "action": "<action>" "rcpt":
"pub_key recipient", "body": "text to send or contents" } where action
is one of 'send' or 'recv', and rcpt and body are only required
for sending.

Author: John Newby

(c) Ape Unit 2018

"""

from oracle import Oracle
import dbm.gnu
import json
import sys

oracle = Oracle()

with dbm.gnu.open('mail.gdbm', 'c') as db:

    def respond(data):
        mail = json.loads(data['payload']['query'])
        print(mail)
        action = mail['action']
        sender = data['payload']['sender']
        if action == "send":
            recipient = mail['rcpt']
            print("rcpt: " + recipient)
            body = mail['body']
            existing = []
            try:
                existing = json.loads(db[recipient])
            except KeyError:
                pass
            existing.append(json.dumps({"from": sender, "body": body}))
            db[recipient] = json.dumps(existing)
            oracle.respond(data['payload']['query_id'], 5, "Mail sent")
        else: # receive
            mail = []
            try:
                mail = json.loads(db[sender])
            except KeyError:
                pass
            oracle.respond(data['payload']['query_id'], 3, json.dumps(mail))
            db[sender] = "[]"
            db.sync
            
            
    oracle_id = oracle.register("mail2", "mail", 0, 2000, 6)
    oracle.subscribe(oracle_id, respond)
