# How to install Epoch on Ubuntu

## Step 1 -- install ESL Erlang 20 on your system.

Don't use the Ubuntu-provided packages. They cause compile errors.

```wget https://packages.erlang-solutions.com/erlang-solutions_1.0_all.deb
sudo dpkg -i erlang-solutions_1.0_all.deb
sudo apt-get update
sudo apt-get install esl-erlang
rm erlang-solutions_1.0_all.deb```

## Step 2 -- get the source, and compile it

```git clone git@github.com:aeternity/epoch.git
cd epoch/
make```

## Step 3 -- edit `accounts.json`

For the Test Net, 
```{
	"BKSRJ6RvBkUhW51L15s0v1LyhbLRZndE8RNAWy3BjonpcwZv+7yRYYQ567v7y2aRMwg1Jibue8fwe5SLX3ekArc=": 100000000000001
}```

What goes in here?

## Step 3 -- setup your `epoch.yaml`

Replace the contents of `_build/local/rel/epoch/doc/examples/epoch.yaml` with the following, replacing /var/epoch with the path to your build dir, and peer_address with your external IP address.

```---
peers:
    - "http://31.13.248.108:3013/"

keys:
    dir: keys
    password: "locallocal"

http:
    external:
        peer_address: http://139.59.140.51:8095/
        port: 3003
    internal:
        port: 3103

websocket:
    internal:
        port: 3104

mining:
    autostart: true

chain:
    persist: true
    db_path: ./mydb```
	
## Step 4 -- create directories for key and db

```mkdir _build/local/rel/epoch/key _build/local/rel/epoch/mydb```

## Step 5 -- install accounts.json

The file contains the hash of the genesis block, and it is important it matches that of the peer. For the peer above, the file should contain:

```{
    "BGWkAh1FRpNiuL+v01pVjEX0AqchlwJycm53A6MILswKEwuhZqV6KkcJwc5ilxhdRnNGWlXCy+Q6EFnbPAZp8MM=": 100000000001
    
}```

If this does not match what the peer is expecting, your node will be blocked, and you'll have to change the peer's address (port number only will do) in order to connect. 

## Troubleshooting

In general, whenever a setting changes it seems that modifying the (address,port) tuple avoids weirdness. Deleting the database directory is also frequently necessary.

