#! /usr/bin/env python

import os
from abjad.cfg.cfg import ABJADPATH

CHAPTERSDIR = os.path.join(ABJADPATH, 'documentation', 'chapters')
chapters = os.listdir(CHAPTERSDIR)

# What's a better, nonmanual way to get rid of special directories
# from the output of os.listdir( )?
chapters.remove('.svn')

chapters.sort( )
print 'Crawling %s chapter directories ...' % len(chapters)

for i, chapter in enumerate(chapters[:2]):
   status = 'Chapter %s %s ...' % (i + 1, chapter)
   print status,
   chapter_directory = os.path.join(CHAPTERSDIR, chapter)
   chapter_files = os.listdir(chapter_directory)
   if 'text.raw' in chapter_files:
      os.chdir(chapter_directory)
      raw_chapter_file = os.path.join(chapter_directory, 'text.raw')
      os.system('chapter.py %s' % raw_chapter_file)
      print 'done.'
