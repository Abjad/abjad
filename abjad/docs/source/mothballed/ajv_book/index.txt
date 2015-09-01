Using ``ajv book``
==================

``ajv book`` is an independent application included in every installation of
Abjad. ``ajv book`` allows you to write Abjad code in the middle of documents
written in HTML, LaTeX or ReST.  We created ``ajv book`` to help us document
Abjad.  Our work on ``ajv book`` was inspired by ``lilypond-book``, which does
for LilyPond much what ``ajv book`` does for Abjad.

``ajv book`` can be accessed on the commandline either via ``ajv book`` or
through Abjad's ``ajv`` tool collection.  For the most up-to-date documentation
on ``ajv book``, always consult ``ajv book --help``:

.. shell::

   ajv book --help


HTML with embedded Abjad
------------------------

To see ``ajv book`` in action, open a file and write some HTML by hand.  Add
some Abjad code to your HTML between open and close \<abjad\> \</abjad\> tags.

.. sourcecode:: html

   <html>

   <p>This is an <b>HTML</b> document.</p>

   <p>The code is standard hypertext mark-up.</p>

   <p>Here is some music notation generated automatically by Abjad:</p>

   <abjad>
   v = Voice("c'8 d' e' f' g' a' b' c''")
   beam = spannertools.Beam(v)
   show(v)
   </abjad>

   <p>And here is more ordinary <b>HTML</b>.</p>

   </html>

Save your the file with the name ``example.html.raw``. You now have an HTML
file with embedded Abjad code.

In the terminal, call ``ajv book`` in the directory:

..  code-block:: bash

   $ ajv book

   Parsing file...
   Rendering "ajv book-1.ly"...
   
The application opens ``example.html.raw``, finds all Abjad code between
\<abjad\> \</abjad\> tags, executes it, and then creates and inserts image
files of music notation accordingly.

Open ``example.html`` with your browser.

.. image:: images/browser-example-1.png

That's all there is to it. ``ajv book`` lets you open a file and type HTML by
hand with Abjad sandwiched between the special \<abjad\> \</abjad\> tags
described here. Run ``ajv book`` on such a hybrid file to create pure HTML with
images of music notation created by Abjad.

Note that ``ajv book`` makes use of ImageMagick's `convert
<http://www.imagemagick.org/script/convert.php>`__ application to crop and
scale PNG images generated for HTML and ReST documents. For LaTeX documents,
``ajv book`` uses ``pdfcrop`` for cropping PDFs. 


LaTeX with embedded Abjad
-------------------------

You can use ``ajv book`` to insert Abjad code and score excerpts into
any LaTeX you create. Type the sample code below into a file:

..  code-block:: latex

   \documentclass{article}
   \usepackage{graphicx}
   \usepackage{listings}
   \begin{document}

   This is a standard LaTeX document with embedded Abjad.

   The code below creates an Abjad measure and then prints the measure
   format string.

   <abjad>
   measure = Measure((5, 8), "c'8 d'8 e'8 f'8 g'8")
   f(measure)
   </abjad>

   This next bit of code knows about the measure we defined earlier.

   <abjad>
   show(measure)
   </abjad>

   And this is the end of the our sample LaTeX document.

   \end{document}

Save your file with the name ``example.tex.raw``. You now have a LaTeX file
with embedded Abjad code.

In the terminal, call ``ajv book`` on ``example.tex.raw``:

..  code-block:: bash

   $ ajv book example.tex.raw example.tex

   Processing 'example.tex.raw'. Will write output to 'example.tex'...
   Parsing file...
   Rendering "ajv book-1.ly"...

The application open ``example.tex.raw``, finds all code between Abjad tags,
executes it, and then creates and inserts Abjad interpreter output and
PDF files of music notation. You can view the contents of the next LaTeX
file ``ajv book`` has created:

..  code-block:: latex

   \documentclass{article}
   \usepackage{graphicx}
   \usepackage{listings}
   \begin{document}

   This is a standard LaTeX document with embedded Abjad.

   The code below creates an Abjad measure and then prints the measure
   format string.

   \begin{lstlisting}[basicstyle=\footnotesize, tabsize=4, showtabs=false, showspaces=false]
      >>> measure = Measure((5, 8), "c'8 d'8 e'8 f'8 g'8")
      >>> f(measure)
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

   \includegraphics{images/ajv book-1.pdf}

   And this is the end of the our sample LaTeX document.

   \end{document}

You can now process the file ``example.tex`` just like any other LaTeX file,
using ``pdflatex`` or TexShop or whatever LaTeX compilation program you
normally use on your computer:

..  code-block:: bash

   $ pdflatex example.tex

   This is pdfTeXk, Version 3.141592-1.40.3 (Web2C 7.5.6)
    %&-line parsing enabled.
   entering extended mode
   ...

And then open the resulting PDF.


Using ``ajv book`` on ReST documents
--------------------------------------

You can call ``ajv book`` on ReST documents, too. Follow the examples
given here for HTML and LaTeX documents and modify accordingly.


Using ``[hide=true]``
---------------------

You can add ``[hide=true]`` to any ``ajv book`` example to show
only music notation:

..  code-block:: latex

   <abjad>[hide=true]
   staff = Staff("c'8 d'8 e'8 f'8 g'8 a'8 b''8")
   show(staff)
   </abjad>
