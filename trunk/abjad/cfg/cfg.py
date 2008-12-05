import os


ABJADOUTPUT = os.environ.get(
   'ABJADOUTPUT', '/home/abjad/output').rstrip(os.sep)
ABJADPATH = os.environ.get(
   'ABJADPATH', '/home/abjad').rstrip(os.sep)
ABJADPERSISTENCE = os.environ.get(
   'ABJADPERSISTENCE', '/home/abjab/persistence').rstrip(os.sep)
ABJADTEMPLATES = os.environ.get(
   'ABJADTEMPLATES', '/home/abjad/templates').rstrip(os.sep)
LILYPONDINCLUDES = os.environ.get('LILYPONDINCLUDES', None)
LILYPONDLANG = os.environ.get('LILYPONDLANG', 'english')
PDFVIEWER = os.environ.get('PDFVIEWER', 'open')
VERSIONFILE = ABJADOUTPUT + '.version'
