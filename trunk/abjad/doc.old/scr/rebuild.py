#! /usr/bin/env python

from abjad.cfg.cfg import ABJADPATH
import os
import subprocess
import sys
import time


os.system('clear')
CHAPTERSDIR = os.path.join(ABJADPATH, 'documentation', 'chapters')
chapters = os.listdir(CHAPTERSDIR)

# What's a better, nonmanual way to get rid of special directories
# from the output of os.listdir( )?
chapters.remove('.svn')

chapters.sort( )
print 'Rebuilding %s chapters ...\n' % len(chapters)

start_time = time.time( )
#for i, chapter in enumerate(chapters[:2]):
for i, chapter in enumerate(chapters):
   status = 'Chapter %d: %s ' % (i + 1, chapter)
   print status,
   sys.stdout.flush( )
   chapter_directory = os.path.join(CHAPTERSDIR, chapter)
   chapter_files = os.listdir(chapter_directory)
   if 'text.raw' in chapter_files:
      os.chdir(chapter_directory)
      raw_chapter_file = os.path.join(chapter_directory, 'text.raw')
      p = subprocess.Popen('chapter.py', 
         shell = True, stdout = sys.stdout, stderr = subprocess.PIPE)
      out, error = p.communicate( )
      if error:
         print '\n'
         print error,
      print ''

print ''
stop_time = time.time( )
print 'Total runtime: %d seconds.\n' % (stop_time - start_time)
