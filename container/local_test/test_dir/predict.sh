#!/bin/bash

payload=$1
content=${2:application/json}

curl --header "Content-Type: application/json" --data '{"url":"https://img.etimg.com/thumb/msid-75093797,width-640,resizemode-4,imgsize-191560/shinzo-abe.jpg"}' -v http://localhost:8080/invocations
