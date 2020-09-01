#!/bin/bash
# Copyright 2020 Red Hat, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

path_from_yaml() {
    python3 -c "from ruamel.yaml import YAML;\
      yaml=YAML();\
      c=yaml.load(open('galaxy.yml.in'));\
      print('%s/%s'%(c['namespace'],c['name']))"
}

TOXDIR=${1:-.}

# Detect collection namespace and name from galaxy.yml.in
collection_path=$(path_from_yaml)
ANSIBLE_COLLECTIONS_PATH=$(mktemp -d)
COLLECTION_PATH=${ANSIBLE_COLLECTIONS_PATH}/ansible_collections/${collection_path}
echo "Executing ansible-test sanity checks in ${ANSIBLE_COLLECTIONS_PATH}"

trap "rm -rf ${ANSIBLE_COLLECTIONS_PATH}" err exit

rm -rf "${ANSIBLE_COLLECTIONS_PATH}"
mkdir -p ${COLLECTION_PATH}

# Created collection x.y at z
output=$(ansible-galaxy collection build --force | sed 's,.* at ,,')
location=$(ansible-galaxy collection install ${output} \
  -p ${ANSIBLE_COLLECTIONS_PATH} --force)
#for folder in {docs,playbooks,plugins,roles,tests}; do
#  if [ -d $folder ]; then
#    cp -av ${TOXDIR}/$folder ${COLLECTION_PATH}/$folder;
#  fi
#done
#cp -av ${TOXDIR}/{plugins,docs,plugins,roles,tests} \
#  ${COLLECTION_PATH} || true
#cp ${TOXDIR}/galaxy.yml ${COLLECTION_PATH}
#mkdir ${COLLECTION_PATH}/logs
#rm -rf ${COLLECTION_PATH}/tests/output || true
cd ${COLLECTION_PATH}
#tree .
ANSIBLE_COLLECTIONS_PATH=${ANSIBLE_COLLECTIONS_PATH} && ansible-test sanity \
    --docker \
    --skip-test metaclass-boilerplate \
    --skip-test future-import-boilerplate 
#    plugins/ tests/


