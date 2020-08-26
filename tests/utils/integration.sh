#!/usr/bin/env bash

set -o pipefail -eu

function render_config()
{
  readonly template="tests/integration/integration_config.yml.template"
  readonly content="$(cat "$template")"

  eval "echo \"$content\"" > tests/integration/integration_config.yml
}

render_config

ANSIBLE_COLLECTIONS_PATH=$(mktemp -d)
NAMESPACE="$1"; shift
NAME="$1"; shift
TEST_DIR="${ANSIBLE_COLLECTIONS_PATH}/ansible_collections/${NAMESPACE}/${NAME}"

trap 'rm -rf ${ANSIBLE_COLLECTIONS_PATH}' err exit

rm -rf "${ANSIBLE_COLLECTIONS_PATH}"

mkdir -p "$TEST_DIR"

rsync -av . \
    --exclude tests/output \
    --exclude .tox \
    --exclude .git \
    "$TEST_DIR" > /dev/null|| true

if [ -f "requirements.txt" ]; then
    ansible-galaxy collection install -p "${ANSIBLE_COLLECTIONS_PATH}"
    ansible-galaxy role install -p "${ANSIBLE_COLLECTIONS_PATH}"
fi

cd "$TEST_DIR"
ansible-test integration --no-temp-unicode
