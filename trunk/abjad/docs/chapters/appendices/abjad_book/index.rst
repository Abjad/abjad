Using ``abjad-book``
====================

``abjad-book`` is an independent application included in every installation
of Abjad. ``abjad-book`` allows you to write Abjad code in the middle
of documents written in HTML, LaTeX or ReST. 
We created ``abjad-book`` to help us document Abjad.
Our work on ``abjad-book`` was inspired by ``lilypond-book``,
which does for LilyPond much what ``abjad-book`` does for Abjad.


HTML with embedded Abjad
------------------------

To see ``abjad-book`` in action, open a file and write some HTML by hand.
Add some Abjad code to your HTML between open and close
\<abjad\> \</abjad\> tags.

.. sourcecode:: html

   <html>

   <p>This is an <b>HTML</b> document.</p>

   <p>The code is standard hypertext mark-up.</p>

   <p>Here is some music notation generated automatically by Abjad:</p>

   <abjad>
   v = Voice(construct.scale(8))
   Beam(v)
   write_ly(v, 'abjad-book-1') <hide
   show(v)
   </abjad>

   <p>And here is more ordinary <b>HTML</b>.</p>

   </html>

Save your the file with the name ``example.html.raw``. You now have
an HTML file with embedded Abjad code.

In the terminal, call ``abjad-book`` on ``example.html.raw``. ::

   $ abjad-book example.html.raw example.html

   Parsing file...
   Rendering "abjad-book-1.ly"...
   
The application opens ``example.html.raw``, finds all Abjad code between
\<abjad\> \</abjad\> tags, executes it, and then creates and inserts 
image files of music notation accordingly.

Open ``example.html`` with your browser.

.. image:: images/browser-example-1.png

That's all there is to it. ``abjad-book`` lets you open a file and type
HTML by hand with Abjad sandwiched between the special \<abjad\> \</abjad\>
tags described here. Run ``abjad-book`` on such a hybrid file to create
pure HTML with images of music notation created by Abjad.

.. note::
   ``abjad-book`` makes use of ImageMagick's `convert <http://www.imagemagick.org/script/convert.php>`__ application to crop and scale PNG images generated for HTML and ReST documents. For LaTeX documents, ``abjad-book`` uses ``pdfcrop`` for cropping PDFs. 



LaTeX with embedded Abjad
-------------------------

You can use ``abjad-book`` to insert Abjad code and score excerpts into
any LaTeX you create. Type the sample code below into a file. ::

   \documentclass{article}
   \usepackage{graphicx}
   \usepackage{listings}
   \begin{document}

   This is a standard LaTeX document with embedded Abjad.

   The code below creates an Abjad measure and then prints the measure
   format string.

   <abjad>
   measure = RigidMeasure((5, 8), construct.scale(5))
   print measure.format
   </abjad>

   This next bit of code knows about the measure we defined earlier.
   This code renders the measure as a PDF using a template suitable
   for inclusion in LaTeX documents.

   <abjad>
   write_ly(measure, 'abjad-book-1', 'oedo') <hide
   </abjad>

   And this is the end of the our sample LaTeX document.

   \end{document}

Save your file with the name ``example.tex.raw``. You now have a LaTeX file
with embedded Abjad code.

In the terminal, call ``abjad-book`` on ``example.tex.raw``. ::

   $ abjad-book example.tex.raw example.tex

   Processing 'example.tex.raw'. Will write output to 'example.tex'...
   Parsing file...
   Rendering "abjad-book-1.ly"...

The application open ``example.tex.raw``, finds all code between Abjad tags,
executes it, and then creates and inserts Abjad interpreter output and
PDF files of music notation. You can view the contents of the next LaTeX
file ``abjad-book`` has created. ::

   \documentclass{article}
   \usepackage{graphicx}
   \usepackage{listings}
   \begin{document}

   This is a standard LaTeX document with embedded Abjad.

   The code below creates an Abjad measure and then prints the measure
   format string.

   \begin{lstlisting}[basicstyle=\footnotesize, tabsize=4, showtabs=false, showspaces=false]
      abjad> measure = RigidMeasure((5, 8), construct.scale(5))
      abjad> print measure.format
      {
         \time 5/8
         c'8
         d'8
         e'8
         f'8
         g'8
      }
   \end{lstlisting}

   This next bit of code knows about the measure we defined earlier.
   This code renders the measure as a PDF using a template suitable
   for inclusion in LaTeX documents.

   \includegraphics{images/abjad-book-1.pdf}

   And this is the end of the our sample LaTeX document.

   \end{document}

You can now process the file ``example.tex`` just like any other LaTeX file,
using ``pdflatex`` or TexShop or whatever LaTeX compilation program you
normally use on your computer. ::

   $ pdflatex example.tex

   This is pdfTeXk, Version 3.141592-1.40.3 (Web2C 7.5.6)
    %&-line parsing enabled.
   entering extended mode
   ...

And then open the resulting PDF.

Using ``abjad-book`` on ReST documents
--------------------------------------

You can call ``abjad-book`` on ReST documents, too. Follow the examples
given here for HTML and LaTeX documents and modify accordingly.


Using [hide = True]
-------------------

You can add ``[hide = True]`` to any ``abjad-book`` example to show
only music notation. ::

   <abjad>[hide = True]
   staff = Staff(construct.scale(8))
   write_ly(staff, 'staff-example', 'oedo')
   </abjad>
