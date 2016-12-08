#!/bin/sh

set -eu

cd "$(dirname "$0")"

# Edit these to configure the paths where you installed the libraries.
FOUNDATION_DIR=../foundation

# These are inside the wellylang.org repo.
SOURCE_DIR=src
BUILD_DIR=build

export PATH="tools:$PATH"

# Remove relics of previous builds.
mkdir -p $BUILD_DIR
rm -rf -- $BUILD_DIR/*
cat >$BUILD_DIR/README.txt <<EOF
These files are auto-generated by "make.sh". Do not edit them.
EOF

# Copy needed libraries into place.
mkdir -p $BUILD_DIR/js
mkdir -p $BUILD_DIR/css
mkdir -p $BUILD_DIR/logos
cp -R $FOUNDATION_DIR/js/* $BUILD_DIR/js
cp -R $FOUNDATION_DIR/css/* $BUILD_DIR/css
cp -R src/js/* $BUILD_DIR/js
cp -R src/css/* $BUILD_DIR/css
cp -R logos/WellyLogotype.svg $BUILD_DIR/logos

# Run as "./make.sh --fast" to disable the syntax highlighter.
HIGHLIGHTER=highlighter.py
if [ "$#" -gt 0 ]; then
  if [ "$1" = "--fast" ]; then
    HIGHLIGHTER=cat
  fi
fi

build () {
  local source=$1
  local target=$source.html
  mkdir -p $(dirname $BUILD_DIR/$target)
  nancy --root $SOURCE_DIR template.html $source \
    | $HIGHLIGHTER > $BUILD_DIR/$target
}


build introduction
build introduction/checklist
build introduction/project_goals
build introduction/installation
build introduction/about
build introduction/contact
build introduction/licence

build tutorial
build tutorial/first_program
build tutorial/basic_syntax
build tutorial/newlines

build reference
build reference/data_types
build reference/variables
build reference/operators

build design
build design/signedness

build history
build history/declaration
build history/dynamic
build history/field_constnesses
build history/for_array0
