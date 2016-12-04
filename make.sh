#!/bin/bash

set -eu

# Edit these to configure the paths where you installed the libraries.
FOUNDATION_DIR=../foundation
PRETTIFY_DIR=../code-prettify

# These are inside the wellylang.org repo.
SOURCE_DIR=src
BUILD_DIR=build

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
cp -R $PRETTIFY_DIR/src/prettify.js $BUILD_DIR/js
cp -R $PRETTIFY_DIR/src/prettify.css $BUILD_DIR/css
cp -R src/js/* $BUILD_DIR/js
cp -R src/css/* $BUILD_DIR/css
cp -R logos/WellyLogotype.svg $BUILD_DIR/logos

run_nancy () {
  local source=$1
  local target=$source.html
  mkdir -p `dirname $BUILD_DIR/$target`
  nancy --root $SOURCE_DIR template.html $source > $BUILD_DIR/$target
}


run_nancy introduction
run_nancy introduction/checklist
run_nancy introduction/project_goals
run_nancy introduction/installation
run_nancy introduction/about
run_nancy introduction/contact
run_nancy introduction/licence

run_nancy tutorial
run_nancy tutorial/first_program
run_nancy tutorial/basic_syntax
run_nancy tutorial/newlines

run_nancy reference
run_nancy reference/data_types
run_nancy reference/variables
run_nancy reference/operators

run_nancy design
run_nancy design/signedness

run_nancy history
run_nancy history/declaration
run_nancy history/dynamic
run_nancy history/field_constnesses
run_nancy history/for_array0
