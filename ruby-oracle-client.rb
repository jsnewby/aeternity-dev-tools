#!/usr/bin/env ruby
require 'rubygems'
require 'eventmachine'
require 'json'
require 'ws_sync_client'

# General purpose script to interact with oracles. Where possible we use the 
# simple synchronous 'ws_sync_client' library. When we're in server mode,
# waiting for events, we use the event machine based library. 
#
# This script relies on the AE_PUB_KEY, AE_LOCAL_PORT and AE_WEBSOCKET
# environment variables set by the script aeternity-functions.sh
#
# (c) 2018 Ape Unit
# Author: John Newby

class Oracle
  
  def initialize
    @pub_key = ENV['AE_PUB_KEY']
    @url = "ws://localhost:#{ENV['AE_WEBSOCKET']}/websocket"
    @ws_sync = nil
    @local_port = ENV['AE_LOCAL_PORT']
    @local_internal_port = ENV['AE_LOCAL_INTERNAL_PORT']
    @websocket = ENV['AE_WEBSOCKET']
  end

  def connect_sync
    @ws_sync = WsSyncClient.new @url unless @ws_sync
  end

  def register(query_format, response_format, query_fee, ttl, fee)
    connect_sync
    query = { "target" => "oracle",
              "action" => "register",
              "payload" => { "type" => "OracleRegisterTxObject",
                             "vsn" => 1,
                             "account" => @pub_key,
                             "query_format" => query_format,
                             "response_format" => "the response spec",
                             "query_fee" => query_fee.to_i,
                             "ttl" => {"type" => "delta",
                                       "value" => ttl.to_i},
                             "fee" => fee.to_i } }.to_json
    puts query
    @ws_sync.send_frame query
    response = JSON.parse(@ws_sync.recv_frame)
    puts response
    unless response['payload']['result'].eql? "ok"
      throw response
    end
    oracle_id = response['payload']['oracle_id']
    wait_for_mining_event
    return oracle_id
  end

  def wait_for_mining_event
    loop do
      # now wait for a block to be mined, to ensure that the xaction is
      # written
      puts "Waiting for block to be mined"
      response = @ws_sync.recv_frame
      puts response
      response = JSON.parse response
      break if response['action'].eql? "mined_block"
    end
  end

  # subscripe to events (queries) to created oracle.
  def subscribe(oracle_id)
    connect_sync
    query = {"target" => "oracle",
             "action" => "subscribe",
             "payload" => {"type" =>"query",
                           "oracle_id" => oracle_id }}.to_json
    
    @ws_sync.send_frame query
    response = JSON.parse @ws_sync.recv_frame
    puts response.to_s
    throw response unless response['payload']['result'].eql? "ok"
    id = response['payload']['subscribed_to']['oracle_id']
    wait_for_mining_event
    loop do
      data = @ws_sync.recv_frame
      json = JSON.parse data
      p data
    end
  end

  def query(oracle_pubkey, query_fee, query_ttl, response_ttl, fee, query)
    connect_sync
    request = {"target" => "oracle",
               "action" => "query",
               "payload" => {"type" => "OracleQueryTxObject",
                             "vsn" => 1,
                             "oracle_pubkey" => oracle_pubkey,
                             "query_fee" => query_fee.to_i,
                             "query_ttl" => {"type" => "delta",
                                             "value" => query_ttl.to_i},
                             "response_ttl" => {"type" => "delta",
                                                "value" => response_ttl.to_i},
                             "fee" => fee.to_i,
                             "query" => query }}.to_json
    puts request
    @ws_sync.send_frame request
    response = @ws_sync.recv_frame
    puts response
    response = JSON.parse response
    if response['payload']['result'].eql? "ok"
      return response['payload']['query_id']
    end
    return nil
  end

  def subscribe_query(query_id)
    connect_sync
    request = {"target" => "oracle",
               "action" => "subscribe",
               "payload" => {"type" => "response",
                             "query_id" => query_id }}.to_json
    puts request
    @ws_sync.send_frame request
    response = @ws_sync.recv_frame
    puts response
    response = JSON.parse response
    throw response unless response['payload']['result'].eql? "ok"
    loop do
      data = @ws_sync.recv_frame
      json = JSON.parse data
      p data
    end
  end

  def respond(query_id, fee, response)
    connect_sync
    response = {"target" => "oracle",
                "action" => "response",
                "payload" => {"type" => "OracleResponseTxObject",
                              "vsn" => 1,
                              "query_id" => query_id,
                              "fee" => fee.to_i,
                              "response" => response}}.to_json
    puts response
    @ws_sync.send_frame response
    response = @ws_sync.recv_frame
    puts response
    response = JSON.parse response
    throw response unless response['payload']['result'].eql? "ok"
    return response['payload']['query_id']
                              
  end
end

oracle = Oracle.new
action = ARGV.shift

case action
when "register"
  (query_format, response_format, query_fee, ttl, fee) = ARGV
  oracle_id = oracle.register(query_format, response_format, query_fee, ttl, fee)
  if oracle_id
    puts "Registered, id : #{oracle_id}"
  else
    puts "Registration failed"
  end
when "subscribe"
  oracle_id = ARGV.shift
  id = oracle.subscribe(oracle_id)
when "register-and-subscribe"
  (query_format, response_format, query_fee, ttl, fee) = ARGV
  oracle_id = oracle.register(query_format, response_format, query_fee, ttl, fee)
  oracle.subscribe oracle_id
when "query"
  (oracle_pubkey, query_fee, query_ttl, response_ttl, fee, query) = ARGV
  result = oracle.query(oracle_pubkey, query_fee, query_ttl, response_ttl,
                        fee, query)
  puts "Query made, id is #{result}"
when "subscribe_query"
  query_id = ARGV.shift
  oracle.subscribe_query query_id
when "query-and-subscribe"
  (oracle_pubkey, query_fee, query_ttl, response_ttl, fee, query) = ARGV
  query_id = oracle.query(oracle_pubkey, query_fee, query_ttl, response_ttl,
                        fee, query)
  oracle.subscribe_query query_id
when "respond"
  (query_id, fee, response) = ARGV
  oracle.respond(query_id, fee, response)
else
  puts "Usage: aeoracle [register|subscribe|query|subscribe_query|respond] args..."
  exit
end

