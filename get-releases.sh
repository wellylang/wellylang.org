#!/bin/sh
# Build tarballs for all known version numbers and copy them into "releases".

set -euo pipefail

cd "$(dirname "$0")"

build() {
  local version=$1
  local tmpdir=`mktemp -d`
  hg clone -u $version ssh://goose.minworks.co.uk//home/welly "$tmpdir"
  mv `"$tmpdir"/make-dist.sh $version` ./releases
  rm -rf -- "$tmpdir"
}

# This is the definitive list of published versions.
build 0.0.0
