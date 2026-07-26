#!/usr/bin/env bash

git pull
docker compose down
sleep 1
docker compose up --build
