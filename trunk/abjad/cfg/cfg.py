from os import environ

ABJADPERSISTENCE = environ.get('ABJADPERSISTENCE', '/home/abjab/persistence/')
ABJADOUTPUT = environ.get('ABJADOUTPUT', '/home/abjad/output/')
VERSIONFILE = ABJADOUTPUT + '.version'
PDFVIEWER = environ.get('PDFVIEWER', 'open')
