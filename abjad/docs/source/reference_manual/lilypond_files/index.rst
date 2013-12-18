LilyPond files
==============


Making LilyPond files
---------------------

Make a basic LilyPond file with the ``lilypondfiletools`` package:

::

   >>> staff = Staff("c'4 d'4 e'4 f'4")
   >>> lilypond_file = lilypondfiletools.make_basic_lilypond_file(staff)


::

   >>> lilypond_file
   LilyPondFile(Staff{4})


::

   >>> f(lilypond_file)
   % 2013-12-06 10:55
   
   \version "2.17.96"
   \language "english"
   
   \score {
       \new Staff {
           c'4
           d'4
           e'4
           f'4
       }
   }


::

   >>> show(lilypond_file)

.. image:: images/index-1.png



Getting header, layout and paper blocks
---------------------------------------

Basic LilyPond files also come equipped with header, layout and paper blocks:

::

   >>> lilypond_file.header_block
   HeaderBlock()


::

   >>> lilypond_file.layout_block
   LayoutBlock()


::

   >>> lilypond_file.paper_block
   PaperBlock()



Setting global staff size and default paper size
------------------------------------------------

Set default LilyPond global staff size and paper size like this:

::

   >>> lilypond_file.global_staff_size = 14
   >>> lilypond_file.default_paper_size = 'A7', 'portrait'


::

   >>> f(lilypond_file)
   % 2013-12-06 10:55
   
   \version "2.17.96"
   \language "english"
   
   #(set-default-paper-size "A7" 'portrait)
   #(set-global-staff-size 14)
   
   \score {
       \new Staff {
           c'4
           d'4
           e'4
           f'4
       }
   }


::

   >>> show(lilypond_file)

.. image:: images/index-2.png



Setting title, subtitle and composer information
------------------------------------------------

Use the LilyPond file header block to set title, subtitle and composer
information:

::

   >>> lilypond_file.header_block.title = markuptools.Markup('Missa sexti tonus')
   >>> lilypond_file.header_block.composer = markuptools.Markup('Josquin')


::

   >>> f(lilypond_file)
   % 2013-12-06 10:55
   
   \version "2.17.96"
   \language "english"
   
   #(set-default-paper-size "A7" 'portrait)
   #(set-global-staff-size 14)
   
   \header {
       composer = \markup { Josquin }
       title = \markup { Missa sexti tonus }
   }
   
   \score {
       \new Staff {
           c'4
           d'4
           e'4
           f'4
       }
   }


::

   >>> show(lilypond_file)

.. image:: images/index-3.png
