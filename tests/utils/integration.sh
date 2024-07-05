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
    ansible-galaxy collection install -r requirements.txt -p ${ANSIBLE_COLLECTIONS_PATH}
    ansible-galaxy role install -r requirements.txt -p ${ANSIBLE_COLLECTIONS_PATH}
fi

# Initialize PYTHONPATH and ANSIBLE_COLLECTIONS_PATHS if not set
export PYTHONPATH=${ANSIBLE_COLLECTIONS_PATH}:${PYTHONPATH:-""}
export ANSIBLE_COLLECTIONS_PATHS=${ANSIBLE_COLLECTIONS_PATH}:${ANSIBLE_COLLECTIONS_PATHS:-""}

# Install the necessary openstack.cloud collection explicitly
ansible-galaxy collection install openstack.cloud -f -p ${ANSIBLE_COLLECTIONS_PATH}

# Verify that the collection is installed
if [ ! -d "${ANSIBLE_COLLECTIONS_PATH}/ansible_collections/openstack/cloud" ]; then
    echo "Error: openstack.cloud collection is not installed correctly."
    exit 1
fi

cd "$TEST_DIR"
ansible-test integration --no-temp-unicode
