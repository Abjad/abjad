# -*- encoding: utf-8 -*-
import collections
import filecmp
import copy
import os
import shutil
import scoremanager
import score_manager_library
from scoremanager import idetools
from experimental import *
configuration = scoremanager.idetools.Configuration()
session = scoremanager.idetools.Session(is_test=True)

ide = scoremanager.idetools.AbjadIDE(is_test=True)
#input_ = 'red~example m tempo da add ((1, 8), 136) q'
#ide._run(input_=input_)
#transcript = ide._transcript
#contents = transcript.contents
#
#for title in transcript.titles:
#    print repr(title)
#for entry in transcript.entries:
#    print entry
#
#for entry in transcript.entries:
#    for line in entry.lines:
#        print(repr(line))
#    print
#    print