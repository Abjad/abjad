import os


ABJADPATH = os.environ.get(
   'ABJADPATH', '/home/abjad').rstrip(os.sep)
ABJADPERSISTENCE = os.environ.get(
   'ABJADPERSISTENCE', '/home/abjab/persistence').rstrip(os.sep)
ABJADOUTPUT = os.environ.get(
   'ABJADOUTPUT', '/home/abjad/output').rstrip(os.sep)
VERSIONFILE = ABJADOUTPUT + '.version'
PDFVIEWER = os.environ.get('PDFVIEWER', 'open')
LILYPONDINCLUDES = os.environ.get('LILYPONDINCLUDES', None)
LILYPONDLANG = os.environ.get('LILYPONDLANG', 'english')
