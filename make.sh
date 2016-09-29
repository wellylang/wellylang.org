#!/bin/sh

# Edit these to configure the paths where you installed the libraries.
export FOUNDATION_DIR=../foundation-6.2.3-complete

# These are inside the wellylang.org repo.
export SOURCE_DIR=src
export BUILD_DIR=build
export NANCY_COMMAND="nancy --root $SOURCE_DIR"

# Remove relics of previous builds.
mkdir -p $BUILD_DIR
rm -r $BUILD_DIR/*

# Copy needed libraries into place.
cp -R $FOUNDATION_DIR/js build
cp -R $FOUNDATION_DIR/css build

# Main directory.
$NANCY_COMMAND template.html index >$BUILD_DIR/index.html
$NANCY_COMMAND template.html project_goals >$BUILD_DIR/project_goals.html
$NANCY_COMMAND template.html installation >$BUILD_DIR/installation.html
$NANCY_COMMAND template.html basic_syntax >$BUILD_DIR/basic_syntax.html
$NANCY_COMMAND template.html basic_syntax/newlines >$BUILD_DIR/newlines.html
$NANCY_COMMAND template.html first_program >$BUILD_DIR/first-program.html
$NANCY_COMMAND template.html question_answer >$BUILD_DIR/question_answer.html
$NANCY_COMMAND template.html data_types >$BUILD_DIR/data_types.html
$NANCY_COMMAND template.html variables>$BUILD_DIR/variables.html
$NANCY_COMMAND template.html operators >$BUILD_DIR/operators.html
$NANCY_COMMAND template.html language_comparison >$BUILD_DIR/language_comparison.html
$NANCY_COMMAND template.html about >$BUILD_DIR/about.html
$NANCY_COMMAND template.html contact >$BUILD_DIR/contact.html

# History directory.
$NANCY_COMMAND template.html history >$BUILD_DIR/history.html
$NANCY_COMMAND template.html history/declaration >$BUILD_DIR/history_declaration.html
$NANCY_COMMAND template.html history/dynamic >$BUILD_DIR/history_dynamic.html
$NANCY_COMMAND template.html history/field_constnesses >$BUILD_DIR/history_field_constnesses.html
$NANCY_COMMAND template.html history/for_array0 >$BUILD_DIR/history_for_array0.html
