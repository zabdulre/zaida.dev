#!/bin/bash

curl -sLO https://github.com/tailwindlabs/tailwindcss/releases/download/v4.1.12/tailwindcss-linux-x64
chmod +x tailwindcss-linux-x64
mv tailwindcss-linux-x64 /bin/tailwindcss

pip install -r ../requirements.txt