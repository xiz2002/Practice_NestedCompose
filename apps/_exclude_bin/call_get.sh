#!/bin/bash
curl -f -v -X 'GET' \
    'http://localhost:8000/api/v1/todo/3' \
    -H 'accept: application/json' | 
    jq


curl -X 'GET' 'http://localhost:8000/api/v1/todo' -H 'accept: application/json' | jq