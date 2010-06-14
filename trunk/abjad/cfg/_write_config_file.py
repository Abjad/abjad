from abjad.cfg.cfg import ABJADPATH, HOME
import os
import time

def _write_config_file(path):
   
   preamble = '# -*- coding: utf-8 -*-\n'
   preamble += '# \n'
   preamble += '# Abjad configuration file, created by Abjad on %s.\n' % \
      time.strftime("%d %B %Y %H:%M:%S")
   preamble += '#\n'
   preamble += '# This file is Python execfile( )d and should thus follow\n'
   preamble += "# Python's syntax.\n"
   preamble += '\n\n'

   ## write file
   f = open(path, 'w')

   f.write(preamble)

   f.write("# Configuration Variables ---------------------------------\n\n")

   f.write("# Live debugging. Set for live debugging during development.\n")  
   f.write("DEBUG = False\n\n")

   f.write("# Set to the one directory you wish all Abjad generate files\n")
   f.write("# (such as PDFs, LilyPond, MIDI or log files) to be saved.\n") 
   f.write("abjad_output = '%s'\n\n" % \
      os.path.join(HOME, '.abjad', 'output'))

   f.write("# List of directories where Abjad will look for LilyPond\n")
   f.write("# templates.\n")
   f.write("abjad_templates = ['%s',]\n\n" % \
      os.path.join(ABJADPATH, 'templates'))

   f.write("# Default accidental spelling.\n")
   f.write("accidental_spelling = 'mixed'\n\n")

   f.write("# List of LilyPond files that Abjad will '\include' in all \n")
   f.write("# generated *.ly files.\n")
   f.write("lilypond_includes = None\n\n")

   f.write("# Language to use in all generated LilyPond files.\n")
   f.write("lilypond_lang = 'english'\n\n")

   f.write("# PDF viewer to use to view generated PDF files.\n")
   f.write("# When None your environment should know how to open PDFs.\n")
   f.write("pdf_viewer = None \n\n")

   f.write("# MIDI player to play MIDI files.\n")
   f.write("# When None your environment should know how to open MIDIs.\n")
   f.write("midi_player = None\n\n")

   f.close( ) 
