#!/bin/sh

rm -r ../build/*

~/Desktop/nancy/nancy template.html index >../build/index.html
~/Desktop/nancy/nancy template.html project_goals >../build/project_goals.html
~/Desktop/nancy/nancy template.html Installation >../build/installation.html
~/Desktop/nancy/nancy template.html basic_syntax >../build/basic_syntax.html
~/Desktop/nancy/nancy template.html basic_syntax/newlines >../build/newlines.html
~/Desktop/nancy/nancy template.html first-program >../build/first-program.html
~/Desktop/nancy/nancy template.html question_answer >../build/question_answer.html
~/Desktop/nancy/nancy template.html data_types >../build/data_types.html
~/Desktop/nancy/nancy template.html variables>../build/variables.html
~/Desktop/nancy/nancy template.html operators >../build/operators.html
~/Desktop/nancy/nancy template.html language_comparison >../build/language_comparison.html
~/Desktop/nancy/nancy template.html about >../build/about.html
~/Desktop/nancy/nancy template.html contact >../build/contact.html
~/Desktop/nancy/nancy searchresult.html . >../build/searchresult.html

~/Desktop/nancy/nancy template.html history >../build/history.html
~/Desktop/nancy/nancy template.html history/declaration >../build/history_declaration.html
~/Desktop/nancy/nancy template.html history/dynamic >../build/history_dynamic.html
~/Desktop/nancy/nancy template.html history/field_constnesses >../build/history_field_constnesses.html
~/Desktop/nancy/nancy template.html history/for_array0 >../build/history_for_array0.html
