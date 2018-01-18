#!/usr/bin/env ruby
require 'rubygems'
require 'websocket-client-simple'


require 'json'
require 'ws_sync_client'

(pub_key, url) = ARGV

class Oracle
  
  def initialize(pub_key, url)
    @pub_key = pub_key
    @url = url
    @ws = WsSyncClient.new url 
  end

  def register(query_format, response_format, query_fee, ttl, fee)
    query = { "target" => "oracle",
              "action" => "register",
              "payload" => { "type" => "OracleRegisterTxObject",
                             "vsn" => 1,
                             "account" => @pub_key,
                             "query_format" => query_format,
                             "response_format" => "the response spec",
                             "query_fee" => query_fee,
                             "ttl" => {"type" => "delta",
                                       "value" => ttl},
                             "fee" => fee } }.to_json
    puts query
    @ws.send_frame query
    response = JSON.parse(@ws.recv_frame)
    puts response
    if response['payload']['result'].eql? "ok"
      @oracle_id = response['payload']['oracle_id']
      return @oracle_id
    end
    return nil
  end

  def subscribe
    query = {"target" => "oracle",
             "action" => "subscribe",
             "payload" => {"type" =>"query",
                           "oracle_id" => @oracle_id }}.to_json
    puts query
    @ws.send_frame query
    response = JSON.parse @ws.recv_frame
    puts response.to_s
    if response['payload']['result'].eql? "ok"
      id = response['payload']['subscribed_to']['oracle_id']
      return id
    end
    return nil
  end

  def query(oracle_pubkey, query_fee, query_ttl, response_ttl, fee, query)
    request = {"target" => "oracle",
               "action" => "query",
               "payload" => {"type" => "OracleQueryTxObject",
                             "vsn" => 1,
                             "oracle_pubkey" => oracle_pubkey,
                             "query_fee" => query_fee,
                             "query_ttl" => {"type" => "delta",
                                             "value" => query_ttl},
                             "response_ttl" => {"type" => "delta",
                                                "value" => response_ttl},
                             "fee" => fee,
                             "query" => query }}.to_json
    puts request
    @ws.send_frame query
    response = JSON.parse @ws.recv_frame
    if response['payload']['result'].eql? "ok"
      return response['payload']['query_id']
    end
    return nil
  end
end

oracle = Oracle.new(pub_key, url)
oracle_id = oracle.register("query_format", "response_format", 4, 50, 5)
puts "Oracle created, id: #{oracle_id}"
id = oracle.subscribe
puts "Subscribed to: #{id}"
oracle.query(oracle_id, 4, 10, 10, 7, "query")


