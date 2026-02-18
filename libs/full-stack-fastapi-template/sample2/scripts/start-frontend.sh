#!/bin/bash -xe

cd frontend

sed -i 's/: "vite",/: "vite --host 0.0.0.0",/g' package.json
npm install

export SECRET_KEY=secretkey
export VITE_API_URL=http://192.168.10.121:8000

npm run dev
