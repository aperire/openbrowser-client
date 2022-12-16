# Test Guide

1. Start main server in port 3000

`cd src/main_endpoint`

`flask run -h localhost -p 3000`

2. Start rpc server in port 8080

`cd src/server`

`flask run -h localhost -p 8080`

2. Setup test script and run

`python3 src/test.py`