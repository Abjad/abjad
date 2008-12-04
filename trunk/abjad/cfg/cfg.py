import os


ABJADPATH = os.environ.get('ABJADPATH', '/home/abjad/')
ABJADPERSISTENCE = os.environ.get(
   'ABJADPERSISTENCE', '/home/abjab/persistence/')
ABJADOUTPUT = os.environ.get('ABJADOUTPUT', '/home/abjad/output/')
VERSIONFILE = ABJADOUTPUT + '.version'
PDFVIEWER = os.environ.get('PDFVIEWER', 'open')
LILYPONDINCLUDES = os.environ.get('LILYPONDINCLUDES', None)
