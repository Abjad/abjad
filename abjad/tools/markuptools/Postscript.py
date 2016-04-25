# -*- coding: utf-8 -*-
import collections
from abjad.tools import mathtools
from abjad.tools.abctools import AbjadValueObject


class Postscript(AbjadValueObject):
    r'''A Postscript session.

    ..  note::

        The markup resulting from the ``\postscript`` markup command is both
        0-height and 0-width. Make sure to wrap the ``\postscript`` command
        with a ``\pad-to-box`` or ``\with-dimensions`` markup command to give
        it explicit height and width. Likewise, use only positive coordinates
        in your postscript markup if at all possible. When specifying explicit
        extents with ``\pad-to-box`` or ``\with-dimensions``, negative extents
        will *not* be interpreted by LilyPond as resulting in positive height
        or width, and may have unexpected behavior.

    ..  note::

        LilyPond will fail to render if *any* of the font commands are used. To
        create text, use ``.show('text')`` preceded by ``.scale()`` or
        ``.rotate()`` to provide the appropriate transformation.
        ``.charpath()`` is also useable. However, ``.findfont()``,
        ``.scalefont()``, ``.setfont()`` will cause LilyPond to error.

    ..  container:: example

        ::

            >>> postscript = markuptools.Postscript()
            >>> postscript = postscript.moveto(1, 1)
            >>> postscript = postscript.setlinewidth(2.5)
            >>> postscript = postscript.setdash((2, 1))
            >>> postscript = postscript.lineto(3, -4)
            >>> postscript = postscript.stroke()
            >>> print(format(postscript))
            markuptools.Postscript(
                operators=(
                    markuptools.PostscriptOperator('moveto', 1.0, 1.0),
                    markuptools.PostscriptOperator('setlinewidth', 2.5),
                    markuptools.PostscriptOperator('setdash', (2.0, 1.0), 0.0),
                    markuptools.PostscriptOperator('lineto', 3.0, -4.0),
                    markuptools.PostscriptOperator('stroke'),
                    ),
                )

        ::

            >>> print(str(postscript))
            1 1 moveto
            2.5 setlinewidth
            [ 2 1 ] 0 setdash
            3 -4 lineto
            stroke

        ::

            >>> postscript = markuptools.Postscript()
            >>> postscript = postscript.newpath()
            >>> postscript = postscript.moveto(0, 0)
            >>> postscript = postscript.rlineto(0, -10)
            >>> postscript = postscript.rlineto(10, 0)
            >>> postscript = postscript.rlineto(0, 10)
            >>> postscript = postscript.rlineto(-10, 0)
            >>> postscript = postscript.closepath()
            >>> postscript = postscript.gsave()
            >>> postscript = postscript.setrgbcolor(0.5, 1, 0.5)
            >>> postscript = postscript.fill()
            >>> postscript = postscript.grestore()
            >>> postscript = postscript.setrgbcolor(1, 0, 0)
            >>> postscript = postscript.setlinewidth(1)
            >>> postscript = postscript.stroke()
            >>> show(postscript) # doctest: +SKIP

    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        '_operators',
        )

    ### INITIALIZER ###

    def __init__(self, operators=None):
        from abjad.tools import markuptools
        prototype = markuptools.PostscriptOperator
        if operators is not None:
            assert all(isinstance(_, prototype) for _ in operators)
            operators = tuple(operators)
        self._operators = operators

    ### SPECIAL METHODS ###

    def __add__(self, expr):
        r'''Adds postscript to `expr`.

        Returns new postscript.
        '''
        assert isinstance(expr, type(self))
        self_operators = self.operators or ()
        expr_operators = expr.operators or ()
        operators = self_operators + expr_operators
        operators = operators or None
        return type(self)(operators)

    def __illustrate__(self):
        r'''Illustrates Postscript.

        Returns LilyPond file.
        '''
        from abjad.tools import markuptools
        markup = markuptools.Markup.postscript(self)
        return markup.__illustrate__()

    def __str__(self):
        r'''Gets string representation of Postscript.

        Return string.
        '''
        if not self.operators:
            return ''
        return '\n'.join(str(_) for _ in self.operators)

    ### PRIVATE METHODS ###

    @staticmethod
    def _format_argument(argument):
        if isinstance(argument, str):
            if argument.startswith('/'):
                return argument
            return '({})'.format(argument)
        elif isinstance(argument, collections.Sequence):
            if not argument:
                return '[ ]'
            contents = ' '.join(
                Postscript._format_argument(_) for _ in argument
                )
            return '[ {} ]'.format(contents)
        elif isinstance(argument, bool):
            return str(argument).lower()
        elif isinstance(argument, (int, float)):
            argument = mathtools.integer_equivalent_number_to_integer(argument)
            return str(argument)
        return str(argument)

    def _with_operator(self, operator):
        operators = self.operators or ()
        operators = operators + (operator,)
        return type(self)(operators)

    ### PUBLIC METHODS ###

    def as_markup(self):
        r'''Converts postscript to markup.

        ..  container:: example

            ::

                >>> postscript = markuptools.Postscript()
                >>> postscript = postscript.newpath()
                >>> postscript = postscript.moveto(100, 200)
                >>> postscript = postscript.lineto(200, 250)
                >>> postscript = postscript.lineto(100, 300)
                >>> postscript = postscript.closepath()
                >>> postscript = postscript.gsave()
                >>> postscript = postscript.setgray(0.5)
                >>> postscript = postscript.fill()
                >>> postscript = postscript.grestore()
                >>> postscript = postscript.setlinewidth(4)
                >>> postscript = postscript.setgray(0.75)
                >>> postscript = postscript.stroke()

            ::

                >>> markup = postscript.as_markup()
                >>> print(format(markup))
                \markup {
                    \postscript
                        #"
                        newpath
                        100 200 moveto
                        200 250 lineto
                        100 300 lineto
                        closepath
                        gsave
                        0.5 setgray
                        fill
                        grestore
                        4 setlinewidth
                        0.75 setgray
                        stroke
                        "
                    }

        Returns new markup.
        '''
        from abjad.tools import markuptools
        return markuptools.Markup.postscript(self)

    def charpath(self, text, modify_font=True):
        r'''Postscript ``charpath`` operator.

        ..  container:: example

            ::

                >>> postscript = markuptools.Postscript()
                >>> postscript = postscript.findfont('Times Roman')
                >>> postscript = postscript.scalefont(32)
                >>> postscript = postscript.setfont()
                >>> postscript = postscript.translate(100, 200)
                >>> postscript = postscript.rotate(45)
                >>> postscript = postscript.scale(2, 1)
                >>> postscript = postscript.newpath()
                >>> postscript = postscript.moveto(0, 0)
                >>> postscript = postscript.charpath('This is text.', True)
                >>> postscript = postscript.setlinewidth(0.5)
                >>> postscript = postscript.setgray(0.25)
                >>> postscript = postscript.stroke()
                >>> print(str(postscript))
                /Times-Roman findfont
                32 scalefont
                setfont
                100 200 translate
                45 rotate
                2 1 scale
                newpath
                0 0 moveto
                (This is text.) true charpath
                0.5 setlinewidth
                0.25 setgray
                stroke

        Returns new Postscript.
        '''
        from abjad.tools import markuptools
        text = str(text)
        modify_font = bool(modify_font)
        operator = markuptools.PostscriptOperator(
            'charpath',
            text,
            modify_font,
            )
        return self._with_operator(operator)

    def closepath(self):
        r'''Postscript ``closepath`` operator.

        ..  container:: example

            ::

                >>> postscript = markuptools.Postscript()
                >>> postscript = postscript.newpath()
                >>> postscript = postscript.moveto(100, 200)
                >>> postscript = postscript.lineto(200, 250)
                >>> postscript = postscript.lineto(100, 300)
                >>> postscript = postscript.closepath()
                >>> postscript = postscript.gsave()
                >>> postscript = postscript.setgray(0.5)
                >>> postscript = postscript.fill()
                >>> postscript = postscript.grestore()
                >>> postscript = postscript.setlinewidth(4)
                >>> postscript = postscript.setgray(0.75)
                >>> postscript = postscript.stroke()
                >>> print(str(postscript))
                newpath
                100 200 moveto
                200 250 lineto
                100 300 lineto
                closepath
                gsave
                0.5 setgray
                fill
                grestore
                4 setlinewidth
                0.75 setgray
                stroke

        Returns new Postscript.
        '''
        from abjad.tools import markuptools
        operator = markuptools.PostscriptOperator('closepath')
        return self._with_operator(operator)

    def curveto(self, x1, y1, x2, y2, x3, y3):
        r'''Postscript ``curveto`` operator.

        ..  container:: example

            ::

                >>> postscript = markuptools.Postscript()
                >>> postscript = postscript.curveto(0, 1, 1.5, 2, 3, 6)
                >>> print(str(postscript))
                0 1 1.5 2 3 6 curveto

        Returns new Postscript.
        '''
        from abjad.tools import markuptools
        x1 = float(x1)
        x2 = float(x2)
        x3 = float(x3)
        y1 = float(y1)
        y2 = float(y2)
        y3 = float(y3)
        operator = markuptools.PostscriptOperator(
            'curveto',
            x1, y1,
            x2, y2,
            x3, y3,
            )
        return self._with_operator(operator)

    def fill(self):
        r'''Postscript ``fill`` operator.

        ..  container:: example

            ::

                >>> postscript = markuptools.Postscript()
                >>> postscript = postscript.newpath()
                >>> postscript = postscript.moveto(100, 200)
                >>> postscript = postscript.lineto(200, 250)
                >>> postscript = postscript.lineto(100, 300)
                >>> postscript = postscript.closepath()
                >>> postscript = postscript.gsave()
                >>> postscript = postscript.setgray(0.5)
                >>> postscript = postscript.fill()
                >>> postscript = postscript.grestore()
                >>> postscript = postscript.setlinewidth(4)
                >>> postscript = postscript.setgray(0.75)
                >>> postscript = postscript.stroke()
                >>> print(str(postscript))
                newpath
                100 200 moveto
                200 250 lineto
                100 300 lineto
                closepath
                gsave
                0.5 setgray
                fill
                grestore
                4 setlinewidth
                0.75 setgray
                stroke

        Returns new Postscript.
        '''
        from abjad.tools import markuptools
        operator = markuptools.PostscriptOperator('fill')
        return self._with_operator(operator)

    def findfont(self, font_name):
        r'''Postscript ``findfont`` operator.

        ..  container:: example

            ::

                >>> postscript = markuptools.Postscript()
                >>> postscript = postscript.findfont('Times Roman')
                >>> postscript = postscript.scalefont(12)
                >>> postscript = postscript.setfont()
                >>> postscript = postscript.newpath()
                >>> postscript = postscript.moveto(100, 200)
                >>> postscript = postscript.show('This is text.')
                >>> print(str(postscript))
                /Times-Roman findfont
                12 scalefont
                setfont
                newpath
                100 200 moveto
                (This is text.) show

        Returns new Postscript.
        '''
        from abjad.tools import markuptools
        font_name = str(font_name)
        font_name = font_name.replace(' ', '-')
        font_name = '/{}'.format(font_name)
        operator = markuptools.PostscriptOperator('findfont', font_name)
        return self._with_operator(operator)

    def grestore(self):
        r'''Postscript ``grestore`` operator.

        ..  container:: example

            ::

                >>> postscript = markuptools.Postscript()
                >>> postscript = postscript.newpath()
                >>> postscript = postscript.moveto(100, 200)
                >>> postscript = postscript.lineto(200, 250)
                >>> postscript = postscript.lineto(100, 300)
                >>> postscript = postscript.closepath()
                >>> postscript = postscript.gsave()
                >>> postscript = postscript.setgray(0.5)
                >>> postscript = postscript.fill()
                >>> postscript = postscript.grestore()
                >>> postscript = postscript.setlinewidth(4)
                >>> postscript = postscript.setgray(0.75)
                >>> postscript = postscript.stroke()
                >>> print(str(postscript))
                newpath
                100 200 moveto
                200 250 lineto
                100 300 lineto
                closepath
                gsave
                0.5 setgray
                fill
                grestore
                4 setlinewidth
                0.75 setgray
                stroke

        Returns new Postscript.
        '''
        from abjad.tools import markuptools
        operator = markuptools.PostscriptOperator('grestore')
        return self._with_operator(operator)

    def gsave(self):
        r'''Postscript ``gsave`` operator.

        ..  container:: example

            ::

                >>> postscript = markuptools.Postscript()
                >>> postscript = postscript.newpath()
                >>> postscript = postscript.moveto(100, 200)
                >>> postscript = postscript.lineto(200, 250)
                >>> postscript = postscript.lineto(100, 300)
                >>> postscript = postscript.closepath()
                >>> postscript = postscript.gsave()
                >>> postscript = postscript.setgray(0.5)
                >>> postscript = postscript.fill()
                >>> postscript = postscript.grestore()
                >>> postscript = postscript.setlinewidth(4)
                >>> postscript = postscript.setgray(0.75)
                >>> postscript = postscript.stroke()
                >>> print(str(postscript))
                newpath
                100 200 moveto
                200 250 lineto
                100 300 lineto
                closepath
                gsave
                0.5 setgray
                fill
                grestore
                4 setlinewidth
                0.75 setgray
                stroke

        Returns new Postscript.
        '''
        from abjad.tools import markuptools
        operator = markuptools.PostscriptOperator('gsave')
        return self._with_operator(operator)

    def lineto(self, x, y):
        r'''Postscript ``lineto`` operator.

        ..  container:: example

            ::

                >>> postscript = markuptools.Postscript()
                >>> postscript = postscript.moveto(1, 1)
                >>> postscript = postscript.lineto(3, -4)
                >>> postscript = postscript.stroke()
                >>> print(str(postscript))
                1 1 moveto
                3 -4 lineto
                stroke

        Returns new Postscript.
        '''
        from abjad.tools import markuptools
        x = float(x)
        y = float(y)
        operator = markuptools.PostscriptOperator('lineto', x, y)
        return self._with_operator(operator)

    def moveto(self, x, y):
        r'''Postscript ``moveto`` operator.

        ..  container:: example

            ::

                >>> postscript = markuptools.Postscript()
                >>> postscript = postscript.moveto(1, 1)
                >>> postscript = postscript.lineto(3, -4)
                >>> postscript = postscript.stroke()
                >>> print(format(postscript))
                markuptools.Postscript(
                    operators=(
                        markuptools.PostscriptOperator('moveto', 1.0, 1.0),
                        markuptools.PostscriptOperator('lineto', 3.0, -4.0),
                        markuptools.PostscriptOperator('stroke'),
                        ),
                    )

            ::

                >>> print(str(postscript))
                1 1 moveto
                3 -4 lineto
                stroke

        Returns new Postscript.
        '''
        from abjad.tools import markuptools
        x = float(x)
        y = float(y)
        operator = markuptools.PostscriptOperator('moveto', x, y)
        return self._with_operator(operator)

    def newpath(self):
        r'''Postscript ``newpath`` operator.

        ..  container:: example

            ::

                >>> postscript = markuptools.Postscript()
                >>> postscript = postscript.newpath()
                >>> postscript = postscript.moveto(100, 200)
                >>> postscript = postscript.lineto(200, 250)
                >>> postscript = postscript.lineto(100, 300)
                >>> postscript = postscript.closepath()
                >>> postscript = postscript.gsave()
                >>> postscript = postscript.setgray(0.5)
                >>> postscript = postscript.fill()
                >>> postscript = postscript.grestore()
                >>> postscript = postscript.setlinewidth(4)
                >>> postscript = postscript.setgray(0.75)
                >>> postscript = postscript.stroke()
                >>> print(str(postscript))
                newpath
                100 200 moveto
                200 250 lineto
                100 300 lineto
                closepath
                gsave
                0.5 setgray
                fill
                grestore
                4 setlinewidth
                0.75 setgray
                stroke

        Returns new Postscript.
        '''
        from abjad.tools import markuptools
        operator = markuptools.PostscriptOperator('newpath')
        return self._with_operator(operator)

    def rcurveto(self, dx1, dy1, dx2, dy2, dx3, dy3):
        r'''Postscript ``rcurveto`` operator.

        ..  container:: edxample

            ::

                >>> postscript = markuptools.Postscript()
                >>> postscript = postscript.rcurveto(0, 1, 1.5, 2, 3, 6)
                >>> print(str(postscript))
                0 1 1.5 2 3 6 rcurveto

        Returns new Postscript.
        '''
        from abjad.tools import markuptools
        dx1 = float(dx1)
        dx2 = float(dx2)
        dx3 = float(dx3)
        dy1 = float(dy1)
        dy2 = float(dy2)
        dy3 = float(dy3)
        operator = markuptools.PostscriptOperator(
            'rcurveto',
            dx1, dy1,
            dx2, dy2,
            dx3, dy3,
            )
        return self._with_operator(operator)

    def rlineto(self, dx, dy):
        r'''Postscript ``rlineto`` operator.

        ..  container:: example

            ::

                >>> postscript = markuptools.Postscript()
                >>> postscript = postscript.rmoveto(1, 1)
                >>> postscript = postscript.rlineto(3, -4)
                >>> postscript = postscript.stroke()
                >>> print(format(postscript))
                markuptools.Postscript(
                    operators=(
                        markuptools.PostscriptOperator('rmoveto', 1.0, 1.0),
                        markuptools.PostscriptOperator('rlineto', 3.0, -4.0),
                        markuptools.PostscriptOperator('stroke'),
                        ),
                    )

            ::

                >>> print(str(postscript))
                1 1 rmoveto
                3 -4 rlineto
                stroke

        Returns new Postscript.
        '''
        from abjad.tools import markuptools
        dx = float(dx)
        dy = float(dy)
        operator = markuptools.PostscriptOperator('rlineto', dx, dy)
        return self._with_operator(operator)

    def rmoveto(self, dx, dy):
        r'''Postscript ``rmoveto`` operator.

        ..  container:: example

            ::

                >>> postscript = markuptools.Postscript()
                >>> postscript = postscript.rmoveto(1, 1)
                >>> postscript = postscript.rlineto(3, -4)
                >>> postscript = postscript.stroke()
                >>> print(format(postscript))
                markuptools.Postscript(
                    operators=(
                        markuptools.PostscriptOperator('rmoveto', 1.0, 1.0),
                        markuptools.PostscriptOperator('rlineto', 3.0, -4.0),
                        markuptools.PostscriptOperator('stroke'),
                        ),
                    )

            ::

                >>> print(str(postscript))
                1 1 rmoveto
                3 -4 rlineto
                stroke

        Returns new Postscript.
        '''
        from abjad.tools import markuptools
        dx = float(dx)
        dy = float(dy)
        operator = markuptools.PostscriptOperator('rmoveto', dx, dy)
        return self._with_operator(operator)

    def rotate(self, degrees):
        r'''Postscript ``restore`` operator.

        ..  container:: example

            ::

                >>> postscript = markuptools.Postscript()
                >>> postscript = postscript.findfont('Times Roman')
                >>> postscript = postscript.scalefont(32)
                >>> postscript = postscript.setfont()
                >>> postscript = postscript.translate(100, 200)
                >>> postscript = postscript.rotate(45)
                >>> postscript = postscript.scale(2, 1)
                >>> postscript = postscript.newpath()
                >>> postscript = postscript.moveto(0, 0)
                >>> postscript = postscript.charpath('This is text.', True)
                >>> postscript = postscript.setlinewidth(0.5)
                >>> postscript = postscript.setgray(0.25)
                >>> postscript = postscript.stroke()
                >>> print(str(postscript))
                /Times-Roman findfont
                32 scalefont
                setfont
                100 200 translate
                45 rotate
                2 1 scale
                newpath
                0 0 moveto
                (This is text.) true charpath
                0.5 setlinewidth
                0.25 setgray
                stroke

        Returns new Postscript.
        '''
        from abjad.tools import markuptools
        degrees = float(degrees)
        operator = markuptools.PostscriptOperator('rotate', degrees)
        return self._with_operator(operator)

    def scale(self, dx, dy):
        r'''Postscript ``scale`` operator.

        ..  container:: example

            ::

                >>> postscript = markuptools.Postscript()
                >>> postscript = postscript.findfont('Times Roman')
                >>> postscript = postscript.scalefont(32)
                >>> postscript = postscript.setfont()
                >>> postscript = postscript.translate(100, 200)
                >>> postscript = postscript.rotate(45)
                >>> postscript = postscript.scale(2, 1)
                >>> postscript = postscript.newpath()
                >>> postscript = postscript.moveto(0, 0)
                >>> postscript = postscript.charpath('This is text.', True)
                >>> postscript = postscript.setlinewidth(0.5)
                >>> postscript = postscript.setgray(0.25)
                >>> postscript = postscript.stroke()
                >>> print(str(postscript))
                /Times-Roman findfont
                32 scalefont
                setfont
                100 200 translate
                45 rotate
                2 1 scale
                newpath
                0 0 moveto
                (This is text.) true charpath
                0.5 setlinewidth
                0.25 setgray
                stroke

        Returns new Postscript.
        '''
        from abjad.tools import markuptools
        dx = float(dx)
        dy = float(dy)
        operator = markuptools.PostscriptOperator('scale', dx, dy)
        return self._with_operator(operator)

    def scalefont(self, font_size):
        r'''Postscript ``scalefont`` operator.

        ..  container:: example

            ::

                >>> postscript = markuptools.Postscript()
                >>> postscript = postscript.findfont('Times Roman')
                >>> postscript = postscript.scalefont(12)
                >>> postscript = postscript.setfont()
                >>> postscript = postscript.newpath()
                >>> postscript = postscript.moveto(100, 200)
                >>> postscript = postscript.show('This is text.')
                >>> print(str(postscript))
                /Times-Roman findfont
                12 scalefont
                setfont
                newpath
                100 200 moveto
                (This is text.) show

        Returns new Postscript.
        '''
        from abjad.tools import markuptools
        font_size = float(font_size)
        operator = markuptools.PostscriptOperator('scalefont', font_size)
        return self._with_operator(operator)

    def setdash(self, array=None, offset=0):
        r'''Postscript ``setdash`` operator.

        ..  container:: example

            ::

                >>> postscript = markuptools.Postscript().setdash([2, 1], 3)
                >>> print(format(postscript))
                markuptools.Postscript(
                    operators=(
                        markuptools.PostscriptOperator('setdash', (2.0, 1.0), 3.0),
                        ),
                    )

            ::

                >>> print(str(postscript))
                [ 2 1 ] 3 setdash

        ..  container:: example

            ::

                >>> postscript = markuptools.Postscript().setdash()
                >>> print(format(postscript))
                markuptools.Postscript(
                    operators=(
                        markuptools.PostscriptOperator('setdash', (), 0.0),
                        ),
                    )

            ::

                >>> print(str(postscript))
                [ ] 0 setdash

        Returns new Postscript.
        '''
        from abjad.tools import markuptools
        if array is None:
            array = ()
        else:
            array = tuple(float(_) for _ in array)
        offset = float(offset)
        operator = markuptools.PostscriptOperator('setdash', array, offset)
        return self._with_operator(operator)

    def setfont(self):
        r'''Postscript ``setfont`` operator.

        ..  container:: example

            ::

                >>> postscript = markuptools.Postscript()
                >>> postscript = postscript.findfont('Times Roman')
                >>> postscript = postscript.scalefont(12)
                >>> postscript = postscript.setfont()
                >>> postscript = postscript.newpath()
                >>> postscript = postscript.moveto(100, 200)
                >>> postscript = postscript.show('This is text.')
                >>> print(str(postscript))
                /Times-Roman findfont
                12 scalefont
                setfont
                newpath
                100 200 moveto
                (This is text.) show

        Returns new Postscript.
        '''
        from abjad.tools import markuptools
        operator = markuptools.PostscriptOperator('setfont')
        return self._with_operator(operator)

    def setgray(self, gray_value):
        r'''Postscript ``setgray`` operator.

        ..  container:: example

            ::

                >>> postscript = markuptools.Postscript()
                >>> postscript = postscript.newpath()
                >>> postscript = postscript.moveto(100, 200)
                >>> postscript = postscript.lineto(200, 250)
                >>> postscript = postscript.lineto(100, 300)
                >>> postscript = postscript.closepath()
                >>> postscript = postscript.gsave()
                >>> postscript = postscript.setgray(0.5)
                >>> postscript = postscript.fill()
                >>> postscript = postscript.grestore()
                >>> postscript = postscript.setlinewidth(4)
                >>> postscript = postscript.setgray(0.75)
                >>> postscript = postscript.stroke()
                >>> print(str(postscript))
                newpath
                100 200 moveto
                200 250 lineto
                100 300 lineto
                closepath
                gsave
                0.5 setgray
                fill
                grestore
                4 setlinewidth
                0.75 setgray
                stroke

        Returns new Postscript.
        '''
        from abjad.tools import markuptools
        gray_value = float(gray_value)
        assert 0 <= gray_value <= 1
        operator = markuptools.PostscriptOperator('setgray', gray_value)
        return self._with_operator(operator)

    def setlinewidth(self, width):
        r'''Postscript ``setlinewidth`` operator.

        ..  container:: example

            ::

                >>> postscript = markuptools.Postscript()
                >>> postscript = postscript.moveto(1, 1)
                >>> postscript = postscript.setlinewidth(2.5)
                >>> postscript = postscript.lineto(3, -4)
                >>> postscript = postscript.stroke()
                >>> print(format(postscript))
                markuptools.Postscript(
                    operators=(
                        markuptools.PostscriptOperator('moveto', 1.0, 1.0),
                        markuptools.PostscriptOperator('setlinewidth', 2.5),
                        markuptools.PostscriptOperator('lineto', 3.0, -4.0),
                        markuptools.PostscriptOperator('stroke'),
                        ),
                    )

            ::

                >>> print(str(postscript))
                1 1 moveto
                2.5 setlinewidth
                3 -4 lineto
                stroke

        Returns new Postscript.
        '''
        from abjad.tools import markuptools
        width = float(width)
        operator = markuptools.PostscriptOperator('setlinewidth', width)
        return self._with_operator(operator)

    def setrgbcolor(self, red, green, blue):
        r'''Postscript ``setrgb`` operator.

        ..  container:: example

            ::

                >>> postscript = markuptools.Postscript()
                >>> postscript = postscript.newpath()
                >>> postscript = postscript.moveto(100, 100)
                >>> postscript = postscript.rlineto(0, 100)
                >>> postscript = postscript.rlineto(100, 0)
                >>> postscript = postscript.rlineto(0, -100)
                >>> postscript = postscript.rlineto(-100, 0)
                >>> postscript = postscript.closepath()
                >>> postscript = postscript.gsave()
                >>> postscript = postscript.setrgbcolor(0.5, 1, 0.5)
                >>> postscript = postscript.fill()
                >>> postscript = postscript.grestore()
                >>> postscript = postscript.setrgbcolor(1, 0, 0)
                >>> postscript = postscript.setlinewidth(4)
                >>> postscript = postscript.stroke()

            ::

                >>> print(str(postscript))
                newpath
                100 100 moveto
                0 100 rlineto
                100 0 rlineto
                0 -100 rlineto
                -100 0 rlineto
                closepath
                gsave
                0.5 1 0.5 setrgbcolor
                fill
                grestore
                1 0 0 setrgbcolor
                4 setlinewidth
                stroke

        Returns new Postscript.
        '''
        from abjad.tools import markuptools
        red = float(red)
        green = float(green)
        blue = float(blue)
        assert 0 <= red <= 1
        assert 0 <= green <= 1
        assert 0 <= blue <= 1
        operator = markuptools.PostscriptOperator(
            'setrgbcolor',
            red,
            green,
            blue,
            )
        return self._with_operator(operator)

    def show(self, text):
        r'''Postscript ``show`` operator.

        ..  container:: example

            ::

                >>> postscript = markuptools.Postscript()
                >>> postscript = postscript.findfont('Times Roman')
                >>> postscript = postscript.scalefont(12)
                >>> postscript = postscript.setfont()
                >>> postscript = postscript.newpath()
                >>> postscript = postscript.moveto(100, 200)
                >>> postscript = postscript.show('This is text.')
                >>> print(str(postscript))
                /Times-Roman findfont
                12 scalefont
                setfont
                newpath
                100 200 moveto
                (This is text.) show

        Returns new Postscript.
        '''
        from abjad.tools import markuptools
        text = str(text)
        operator = markuptools.PostscriptOperator('show', text)
        return self._with_operator(operator)

    def stroke(self):
        r'''Postscript ``stroke`` operator.

        ..  container:: example

            ::

                >>> postscript = markuptools.Postscript()
                >>> postscript = postscript.lineto(3, -4)
                >>> postscript = postscript.stroke()
                >>> print(format(postscript))
                markuptools.Postscript(
                    operators=(
                        markuptools.PostscriptOperator('lineto', 3.0, -4.0),
                        markuptools.PostscriptOperator('stroke'),
                        ),
                    )

            ::

                >>> print(str(postscript))
                3 -4 lineto
                stroke

        Returns new Postscript.
        '''
        from abjad.tools import markuptools
        operator = markuptools.PostscriptOperator('stroke')
        return self._with_operator(operator)

    def translate(self, dx, dy):
        r'''Postscript ``translate`` operator.

        ..  container:: example

            ::

                >>> postscript = markuptools.Postscript()
                >>> postscript = postscript.findfont('Times Roman')
                >>> postscript = postscript.scalefont(32)
                >>> postscript = postscript.setfont()
                >>> postscript = postscript.translate(100, 200)
                >>> postscript = postscript.rotate(45)
                >>> postscript = postscript.scale(2, 1)
                >>> postscript = postscript.newpath()
                >>> postscript = postscript.moveto(0, 0)
                >>> postscript = postscript.charpath('This is text.', True)
                >>> postscript = postscript.setlinewidth(0.5)
                >>> postscript = postscript.setgray(0.25)
                >>> postscript = postscript.stroke()
                >>> print(str(postscript))
                /Times-Roman findfont
                32 scalefont
                setfont
                100 200 translate
                45 rotate
                2 1 scale
                newpath
                0 0 moveto
                (This is text.) true charpath
                0.5 setlinewidth
                0.25 setgray
                stroke

        Returns new Postscript.
        '''
        from abjad.tools import markuptools
        dx = float(dx)
        dy = float(dy)
        operator = markuptools.PostscriptOperator('translate', dx, dy)
        return self._with_operator(operator)

    ### PUBLIC PROPERTIES ###

    @property
    def operators(self):
        r'''Gets Postscript operators.

        Returns tuple or none.
        '''
        return self._operators
