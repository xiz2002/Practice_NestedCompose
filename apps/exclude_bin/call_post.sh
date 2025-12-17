#!/bin/bash
curl -f -v -X 'POST' \
    'http://localhost:8000/api/v1/todo' \
    -H 'accept: application/json' \
    -H 'Content-Type: application/json' \
    -d '{"id": 1,"item": "First Route is to finish this book!"}'

curl -X 'POST' 'http://localhost:8000/api/v1/todo' -H 'accept: application/json' -H 'Content-Type: application/json' -d '{"id": 2,"item": "Validation models help with input types"}'

curl -X 'POST' \
    'http://localhost:8000/api/v1/todo' \
    -H 'accept: application/json' \
    -H 'Content-Type: application/json' \
    -d '{"id": 3,"item": {"item": "Nested models are powerful", "status": "in-progress"}}'

curl -X 'POST' \
    'http://localhost:8000/api/v1/todo' \
    -H 'accept: application/json' \
    -H 'Content-Type: application/json' \
    -d '{"id": 3,"item": "Example Schema in Pydantic Models"}'    


curl -X 'PUT' \
    'http://localhost:8000/api/v1/todo/3' \
    -H 'accept: application/json' \
    -H 'Content-Type: application/json' \
    -d '{"item": "Example Schema in Pydantic Models Tset UPDATE!"}'

curl -X 'POST' \
    'http://localhost:8000/api/v1/todo' \
    -H 'accept: application/json' \
    -H 'Content-Type: application/json' \
    -d '{"id": 1, "item": "This todo will be retrievd without exposing my ID"}'