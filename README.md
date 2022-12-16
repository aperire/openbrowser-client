# OpenBrowser Test Guide
## RPC Side
1. Access server directory

`cd src/server/app.py`

2. Start server

`python3 app.py`


## RPC Registry Side
1. Access main endpoint directory

`cd src/main_endpoint`

2. Update `rpc_array`

3. Start server
`python3 app.py`

## Client Side
1. Access source directory

`cd src`

2. Initialize client `client = Client(rpc_registry_endpoint)`

3. Select image `img_path = "path to image"`

4. Run

`python3 test.py`