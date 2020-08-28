#!/bin/bash -eu

set -o pipefail

function main()
{
  readonly template="$1"; shift
  readonly content="$(cat "$template")"

  eval "echo \"$content\""
}

main tests/integration/integration_config.yml.template > tests/integration/integration_config.yml
