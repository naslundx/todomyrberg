#!/usr/bin/env bash

git pull
docker compose -p todomyrberg down
sleep 1
docker compose -p todomyrberg up --build
