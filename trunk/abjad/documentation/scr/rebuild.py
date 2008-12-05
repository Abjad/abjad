#! /usr/bin/env python

import os
CHAPTERSDIR = os.environ['ABJADPATH'] + '/documentation/chapters/'
chapters = os.listdir(CHAPTERSDIR)

# What's a better, nonmanual way to get rid of special directories
# from the output of os.listdir( )?
chapters.remove('.svn')

chapters.sort( )
print 'Crawling %s chapter directories ...' % len(chapters)

for i, chapter in enumerate(chapters):
   print 'Chapter %s %s:' % (i, chapter)
   print os.listdir(CHAPTERSDIR + chapter)


