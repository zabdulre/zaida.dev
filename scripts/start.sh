#!/bin/bash

if [ -z $1 ]; then
  echo "Error, usage is ./start.sh <PORT_NUMBER>"
  exit 1
fi


echo "Compiling css"
cd ../
tailwind -i style/input.css -o static/output.css
echo "Starting server on port $1"
cd ./src/
gunicorn --bind 0.0.0.0:$1 wsgi:app