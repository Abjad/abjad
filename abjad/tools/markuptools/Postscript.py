# -*- encoding: utf-8 -*-
from abjad.tools.abctools import AbjadValueObject


class Postscript(AbjadValueObject):
    r'''A Postscript session.

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
                1.0 1.0 moveto
                2.5 setlinewidth
                [ 2.0 1.0 ] 0.0 setdash
                3.0 -4.0 lineto
                stroke

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

    def __str__(self):
        r'''Gets string representation of Postscript.

        Return string.
        '''
        if not self.operators:
            return ''
        return '\n'.join(str(_) for _ in self.operators)

    ### PRIVATE METHODS ###

    def _with_operator(self, operator):
        operators = self.operators or ()
        operators = operators + (operator,)
        return type(self)(operators)

    ### PUBLIC METHODS ###

    def lineto(self, x, y):
        r'''Postscript ``lineto`` operator.

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

        Returns new Postscript.
        '''
        from abjad.tools import markuptools
        x = float(x)
        y = float(y)
        operator = markuptools.PostscriptOperator('moveto', x, y)
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

        Returns new Postscript.
        '''
        from abjad.tools import markuptools
        dx = float(dx)
        dy = float(dy)
        operator = markuptools.PostscriptOperator('rmoveto', dx, dy)
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

        ..  container:: example

            ::

                >>> postscript = markuptools.Postscript().setdash()
                >>> print(format(postscript))
                markuptools.Postscript(
                    operators=(
                        markuptools.PostscriptOperator('setdash', (), 0.0),
                        ),
                    )

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

        Returns new Postscript.
        Returns new Postscript.
        '''
        from abjad.tools import markuptools
        width = float(width)
        operator = markuptools.PostscriptOperator('setlinewidth', width)
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

        Returns new Postscript.
        Returns new Postscript.
        '''
        from abjad.tools import markuptools
        operator = markuptools.PostscriptOperator('stroke')
        return self._with_operator(operator)

    ### PUBLIC PROPERTIES ###

    @property
    def operators(self):
        r'''Gets Postscript operators.

        Returns tuple or none.
        '''
        return self._operators