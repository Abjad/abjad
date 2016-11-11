r'''
This empty __init__.py file is present to make py.test allow
duplicate file names.

Most Abjad score package test directories (like this one) will
contain test_materials.py, test_segments.py and other files with
generic names.

The inclusion of this empty __init__.py file allows py.test to
run over many Abjad score packages at one time, coping successfully
with the many different test_materials.py, test_segments.py and other
test files accumulated at the start of the test run.

See ...

http://stackoverflow.com/questions/12582503/py-test-test-discovery-failure-when-tests-in-different-directories-are-called

... for discussion.
'''
