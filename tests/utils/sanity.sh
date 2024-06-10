#!/usr/bin/env bash

set -o pipefail -eu

ANSIBLE_COLLECTIONS_PATH=$(mktemp -d)
NAMESPACE="$1"; shift
NAME="$1"; shift
TEST_DIR="${ANSIBLE_COLLECTIONS_PATH}/ansible_collections/${NAMESPACE}/${NAME}"

trap 'rm -rf ${ANSIBLE_COLLECTIONS_PATH}' err exit

rm -rf "${ANSIBLE_COLLECTIONS_PATH}"

mkdir -p "$TEST_DIR"

rsync -av . \
    --exclude tests/output \
    --exclude tools \
    --exclude ci \
    --exclude .tox \
    --exclude .git \
    "$TEST_DIR" > /dev/null|| true

if [ -f "requirements.txt" ]; then
    ansible-galaxy collection install -p ${ANSIBLE_COLLECTIONS_PATH}
    ansible-galaxy role install -p ${ANSIBLE_COLLECTIONS_PATH}
fi

cd "$TEST_DIR"
SKIP_TESTS="--skip-test import --skip-test validate-modules  --skip-test compile --python 2.7"
# Ansible-core 2.17 dropped support for the metaclass-boilerplate and future-import-boilerplate tests.
ANSIBLE_VER=$(python3 -m pip show ansible-core | awk '$1 == "Version:" { print $2 }')
ANSIBLE_MAJOR_VER=$(echo "$ANSIBLE_VER" | sed 's/^\([0-9]\)\..*/\1/g')
if [[ $ANSIBLE_MAJOR_VER -eq 2 ]]; then
    ANSIBLE_MINOR_VER=$(echo "$ANSIBLE_VER" | sed 's/^2\.\([^\.]*\)\..*/\1/g')
    if [[ $ANSIBLE_MINOR_VER -le 16 ]]; then
        SKIP_TESTS="--skip-test metaclass-boilerplate --skip-test future-import-boilerplate --skip-test import --skip-test validate-modules  --skip-test compile --python 2.7"
    fi
fi

ansible-test sanity -v \
    $SKIP_TESTS
