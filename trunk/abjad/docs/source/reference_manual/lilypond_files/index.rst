LilyPond files
==============

Making LilyPond files
---------------------

Make a basic LilyPond input file with the ``lilypondfiletools`` package:

::

   >>> staff = Staff("c'8 d'8 e'8 f'8")
   >>> lilypond_file = lilypondfiletools.make_basic_lilypond_file(staff)


::

    >>> lilypond_file
    LilyPondFile(Staff{4})

Inspecting file output
----------------------

LilyPond input files that you create this way come equipped with many attributes
that appear in file output:

::

   >>> f(lilypond_file)
   % Abjad revision 9810:9815
   % 2013-03-24 23:47
   
   \version "2.16.1"
   \language "english"
   \include "/home/josiah/Documents/Development/abjad/trunk/abjad/cfg/abjad.scm"
   
   \score {
       \new Staff {
           c'8
           d'8
           e'8
           f'8
       }
   }


Setting default paper size
--------------------------

Set default LilyPond paper size like this:

::

   >>> lilypond_file.default_paper_size = '11x17', 'landscape'


::

   >>> f(lilypond_file)
   % Abjad revision 9810:9815
   % 2013-03-24 23:47
   
   \version "2.16.1"
   \language "english"
   \include "/home/josiah/Documents/Development/abjad/trunk/abjad/cfg/abjad.scm"
   
   #(set-default-paper-size "11x17" 'landscape)
   
   \score {
       \new Staff {
           c'8
           d'8
           e'8
           f'8
       }
   }


Setting global staff size
-------------------------

Set global staff size like this:

::

   >>> lilypond_file.global_staff_size = 16


::

   >>> f(lilypond_file)
   % Abjad revision 9810:9815
   % 2013-03-24 23:47
   
   \version "2.16.1"
   \language "english"
   \include "/home/josiah/Documents/Development/abjad/trunk/abjad/cfg/abjad.scm"
   
   #(set-default-paper-size "11x17" 'landscape)
   #(set-global-staff-size 16)
   
   \score {
       \new Staff {
           c'8
           d'8
           e'8
           f'8
       }
   }

