#!/bin/bash

ROOT="$(git rev-parse --show-toplevel)"
cd "${ROOT}"

# Ensure git hooks.
if [[ -d "${ROOT}/.git/hooks" && ! -L "${ROOT}/.git/hooks" ]]; then
  echo "Setup git hooks ..."
  mv "${ROOT}/.git/hooks" "${ROOT}/.git/hooks_default"
  ln -s "${ROOT}/git_hooks" "${ROOT}/.git/hooks"
fi

# Start local dev servers.
docker-compose --env-file ./.env.dev up \
  --force-recreate \
  --detach
