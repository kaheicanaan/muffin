#!/bin/bash

docker-compose --env-file ./.env.dev up \
  --force-recreate \
  --detach
