# -*- coding: utf-8 -*-
import inspect
from abjad.tools import expressiontools
from abjad.tools.datastructuretools.TypedList import TypedList
from abjad.tools.markuptools.Markup import Markup


class MarkupList(TypedList):
    '''Markup list.

    ..  container:: example

        Initializes from strings:

        ..  container:: example

            ::

                >>> markups = ['Allegro', 'assai']
                >>> markup_list = MarkupList(markups)
                >>> f(markup_list)
                markuptools.MarkupList(
                    items=[
                        markuptools.Markup(
                            contents=['Allegro'],
                            ),
                        markuptools.Markup(
                            contents=['assai'],
                            ),
                        ],
                    )

            ::

                >>> show(markup_list) # doctest: +SKIP

            ..  doctest::

                >>> f(markup_list.__illustrate__().items[-1])
                \markup {
                    \column
                        {
                            Allegro
                            assai
                        }
                    }

        ..  container:: example expression

            ::

                >>> expression = Expression().markup_list()
                >>> markup_list = expression(['Allegro', 'assai'])
                >>> f(markup_list)
                markuptools.MarkupList(
                    items=[
                        markuptools.Markup(
                            contents=['Allegro'],
                            ),
                        markuptools.Markup(
                            contents=['assai'],
                            ),
                        ],
                    )

            ::

                >>> show(markup_list) # doctest: +SKIP

            ..  doctest::

                >>> f(markup_list.__illustrate__().items[-1])
                \markup {
                    \column
                        {
                            Allegro
                            assai
                        }
                    }

    Markup list implement the list interface and are mutable.
    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        '_expression',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        items=None,
        item_class=None,
        keep_sorted=None,
        ):
        from abjad.tools import markuptools
        self._expression = None
        item_class = item_class or markuptools.Markup
        TypedList.__init__(
            self,
            item_class=item_class,
            items=items,
            keep_sorted=keep_sorted,
            )

    ### SPECIAL METHODS ###

    def __contains__(self, item):
        r'''Is true when markup markup list contains `item`.
        Otherwise false.

        ..  container:: example

            ..  container:: example

                ::

                    >>> markups = ['Allegro', 'assai']
                    >>> markup_list = MarkupList(markups)

                ::

                    >>> 'assai' in markup_list
                    True

            ..  container:: example expression

                ::

                    >>> expression = Expression().markup_list()
                    >>> markup_list = expression(['Allegro', 'assai'])

                ::

                    >>> 'assai' in markup_list
                    True

        Returns true or false.
        '''
        superclass = super(MarkupList, self)
        return superclass.__contains__(item)

    def __format__(self, format_specification=''):
        r'''Formats markup list.

        ..  container:: example

            ..  container:: example

                Formats markup list:

                ::


                    >>> markups = ['Allegro', 'assai']
                    >>> markup_list = MarkupList(markups)
                    >>> f(markup_list)
                    markuptools.MarkupList(
                        items=[
                            markuptools.Markup(
                                contents=['Allegro'],
                                ),
                            markuptools.Markup(
                                contents=['assai'],
                                ),
                            ],
                        )

            ..  container:: example expression

                Formats markup list expression:

                ::

                    >>> expression = Expression().markup_list()
                    >>> f(expression)
                    expressiontools.Expression(
                        callbacks=[
                            expressiontools.Expression(
                                evaluation_template='abjad.markuptools.MarkupList',
                                is_initializer=True,
                                ),
                            ],
                        proxy_class=markuptools.MarkupList,
                        )

        Returns string.
        '''
        superclass = super(MarkupList, self)
        return superclass.__format__(format_specification=format_specification)

    def __iadd__(self, argument):
        r'''Changes items in `argument` to items and extends markup list.

        ..  container:: example

            ..  container:: example

                ::

                    >>> markup_list = MarkupList()
                    >>> markup_list.extend(['Allegro', 'assai'])
                    >>> markup_list += ['ma', 'non', 'troppo']
                    >>> f(markup_list)
                    markuptools.MarkupList(
                        items=[
                            markuptools.Markup(
                                contents=['Allegro'],
                                ),
                            markuptools.Markup(
                                contents=['assai'],
                                ),
                            markuptools.Markup(
                                contents=['ma'],
                                ),
                            markuptools.Markup(
                                contents=['non'],
                                ),
                            markuptools.Markup(
                                contents=['troppo'],
                                ),
                            ],
                        )

                ::

                    >>> show(markup_list) # doctest: +SKIP

                ..  doctest::

                    >>> f(markup_list.__illustrate__().items[-1])
                    \markup {
                        \column
                            {
                                Allegro
                                assai
                                ma
                                non
                                troppo
                            }
                        }

            ..  container:: example expression

                ::

                    >>> expression = Expression().markup_list()
                    >>> expression += ['ma', 'non', 'troppo']
                    >>> markup_list = expression(['Allegro', 'assai'])
                    >>> f(markup_list)
                    markuptools.MarkupList(
                        items=[
                            markuptools.Markup(
                                contents=['Allegro'],
                                ),
                            markuptools.Markup(
                                contents=['assai'],
                                ),
                            markuptools.Markup(
                                contents=['ma'],
                                ),
                            markuptools.Markup(
                                contents=['non'],
                                ),
                            markuptools.Markup(
                                contents=['troppo'],
                                ),
                            ],
                        )

                ::

                    >>> show(markup_list) # doctest: +SKIP

        Returns none.
        '''
        if self._expression:
            return self._update_expression(
                inspect.currentframe(),
                force_return=True,
                )
        superclass = super(MarkupList, self)
        return superclass.__iadd__(argument)

    def __illustrate__(self):
        r'''Illustrates markup markup list.

        ..  container:: example

            ..  container:: example

                ::

                    >>> markups = ['Allegro', 'assai']
                    >>> markup_list = MarkupList(markups)
                    >>> f(markup_list)
                    markuptools.MarkupList(
                        items=[
                            markuptools.Markup(
                                contents=['Allegro'],
                                ),
                            markuptools.Markup(
                                contents=['assai'],
                                ),
                            ],
                        )

                ::

                    >>> show(markup_list) # doctest: +SKIP

                ..  doctest::

                    >>> f(markup_list.__illustrate__().items[-1])
                    \markup {
                        \column
                            {
                                Allegro
                                assai
                            }
                        }

            ..  container:: example expression

                ::

                    >>> expression = Expression().markup_list()
                    >>> markup_list = expression(['Allegro', 'assai'])
                    >>> f(markup_list)
                    markuptools.MarkupList(
                        items=[
                            markuptools.Markup(
                                contents=['Allegro'],
                                ),
                            markuptools.Markup(
                                contents=['assai'],
                                ),
                            ],
                        )

                ::

                    >>> show(markup_list) # doctest: +SKIP

                ..  doctest::

                    >>> f(markup_list.__illustrate__().items[-1])
                    \markup {
                        \column
                            {
                                Allegro
                                assai
                            }
                        }

        Returns LilyPond file.
        '''
        import abjad
        lilypond_file = abjad.LilyPondFile.new()
        for name in ('layout', 'paper', 'score'):
            block = lilypond_file[name]
            lilypond_file.items.remove(block)
        lilypond_file.header_block.tagline = False
        markup = abjad.Markup.column(list(self))
        lilypond_file.items.append(markup)
        return lilypond_file

    def __setitem__(self, i, argument):
        r'''Sets item `i` equal to `argument`.

        ..  container:: example

            ..  container:: example

                ::

                    >>> markup_list = MarkupList()
                    >>> markup_list.extend(['Allegro', 'assai'])
                    >>> markup_list[-1] = 'non troppo'
                    >>> f(markup_list)
                    markuptools.MarkupList(
                        items=[
                            markuptools.Markup(
                                contents=['Allegro'],
                                ),
                            markuptools.Markup(
                                contents=['non troppo'],
                                ),
                            ],
                        )

                ::

                    >>> show(markup_list) # doctest: +SKIP

                ..  doctest::

                    >>> f(markup_list.__illustrate__().items[-1])
                    \markup {
                        \column
                            {
                                Allegro
                                "non troppo"
                            }
                        }

            ..  container:: example expression

                ::

                    >>> expression = Expression().markup_list()
                    >>> expression = expression.__setitem__(-1, 'non troppo')
                    >>> markup_list = expression(['Allegro', 'assai'])
                    >>> f(markup_list)
                    markuptools.MarkupList(
                        items=[
                            markuptools.Markup(
                                contents=['Allegro'],
                                ),
                            markuptools.Markup(
                                contents=['non troppo'],
                                ),
                            ],
                        )

                ::

                    >>> show(markup_list) # doctest: +SKIP

                ..  doctest::

                    >>> f(markup_list.__illustrate__().items[-1])
                    \markup {
                        \column
                            {
                                Allegro
                                "non troppo"
                            }
                        }

        Returns none.
        '''
        if self._expression:
            return self._update_expression(
                inspect.currentframe(),
                force_return=True,
                )
        superclass = super(MarkupList, self)
        return superclass.__setitem__(i, argument)

    ### PRIVATE METHODS ###

    def _get_format_specification(self):
        import abjad
        agent = abjad.systemtools.StorageFormatAgent(self)
        names = list(agent.signature_keyword_names)
        if self.item_class is abjad.Markup:
            names.remove('item_class')
        return abjad.systemtools.FormatSpecification(
            client=self,
            storage_format_kwargs_names=names,
            )

    def _update_expression(self, frame, force_return=None):
        #import abjad
        from abjad.tools import expressiontools
        callback = expressiontools.Expression._frame_to_callback(
            frame,
            force_return=force_return,
            )
        return self._expression.append_callback(callback)

    ### PUBLIC PROPERTIES ###

    @property
    def item_class(self):
        r'''Gets markup list item class.

        ..  container:: example

            ::

                >>> MarkupList().item_class
                <class 'abjad.tools.markuptools.Markup.Markup'>

        Returns markup class.
        '''
        superclass = super(MarkupList, self)
        return superclass.item_class

    @property
    def items(self):
        r'''Gets markup list items.

        ..  container:: example

            ..  container:: example

                Initializes items positionally:

                ::

                    >>> items = ['Allegro', 'assai']
                    >>> markup_list = MarkupList(items)
                    >>> for item in markup_list.items:
                    ...     item
                    ...
                    Markup(contents=['Allegro'])
                    Markup(contents=['assai'])

                Initializes items from keyword:

                ::

                    >>> items = ['Allegro', 'assai']
                    >>> markup_list = MarkupList(items=items)
                    >>> for item in markup_list.items:
                    ...     item
                    ...
                    Markup(contents=['Allegro'])
                    Markup(contents=['assai'])

            ..  container:: example expression

                Initializes items positionally:

                ::

                    >>> items = ['Allegro', 'assai']
                    >>> expression = Expression().markup_list()
                    >>> markup_list = expression(items)
                    >>> for item in markup_list.items:
                    ...     item
                    ...
                    Markup(contents=['Allegro'])
                    Markup(contents=['assai'])

                Initializes items from keyword:

                ::

                    >>> items = ['Allegro', 'assai']
                    >>> expression = Expression().markup_list()
                    >>> markup_list = expression(items=items)
                    >>> for item in markup_list.items:
                    ...     item
                    ...
                    Markup(contents=['Allegro'])
                    Markup(contents=['assai'])

        Returns tuple.
        '''
        superclass = super(MarkupList, self)
        return superclass.items

    @property
    def keep_sorted(self):
        r'''Is true when markup list keeps markups sorted.
        Otherwise false.

        ..  container:: example

            Keeps markup sorted:

            ::

                >>> markups = ['Allegro', 'assai']
                >>> markup_list = MarkupList(keep_sorted=True)
                >>> markup_list.append('assai')
                >>> markup_list.append('Allegro')
                >>> show(markup_list) # doctest: +SKIP

            ..  doctest::

                >>> f(markup_list.__illustrate__().items[-1])
                \markup {
                    \column
                        {
                            Allegro
                            assai
                        }
                    }

        ..  container:: example

            Does not keep markup sorted:

            ::

                >>> markups = ['Allegro', 'assai']
                >>> markup_list = MarkupList()
                >>> markup_list.append('assai')
                >>> markup_list.append('Allegro')
                >>> show(markup_list) # doctest: +SKIP

            ..  doctest::

                >>> f(markup_list.__illustrate__().items[-1])
                \markup {
                    \column
                        {
                            assai
                            Allegro
                        }
                    }

        Defaults to none.

        Set to true, false or none.

        Returns true, false or none.
        '''
        superclass = super(MarkupList, self)
        return superclass.keep_sorted

    ### PUBLIC METHODS ###

    def append(self, item):
        r'''Appends `item` to markup list.

        ..  container:: example

            ..  container:: example

                ::

                    >>> markup_list = MarkupList(['Allegro'])
                    >>> markup_list.append('assai')
                    >>> f(markup_list)
                    markuptools.MarkupList(
                        items=[
                            markuptools.Markup(
                                contents=['Allegro'],
                                ),
                            markuptools.Markup(
                                contents=['assai'],
                                ),
                            ],
                        )

                ::

                    >>> show(markup_list) # doctest: +SKIP

            ..  container:: example expression

                ::

                    >>> expression = Expression().markup_list()
                    >>> expression = expression.append('assai')
                    >>> markup_list = expression(['Allegro'])
                    >>> f(markup_list)
                    markuptools.MarkupList(
                        items=[
                            markuptools.Markup(
                                contents=['Allegro'],
                                ),
                            markuptools.Markup(
                                contents=['assai'],
                                ),
                            ],
                        )

                ::

                    >>> show(markup_list) # doctest: +SKIP

        Returns none.
        '''
        if self._expression:
            return self._update_expression(
                inspect.currentframe(),
                force_return=True,
                )
        superclass = super(MarkupList, self)
        superclass.append(item)

    def center_column(self, direction=None):
        r'''LilyPond ``\center-column`` markup command.

        ..  container:: example

            ..  container:: example

                ::

                    >>> city = Markup('Los Angeles')
                    >>> date = Markup('May - August 2014')
                    >>> markups = [city, date]
                    >>> markup_list = MarkupList(markups)
                    >>> markup = markup_list.center_column(direction=Up)
                    >>> f(markup)
                    ^ \markup {
                        \center-column
                            {
                                "Los Angeles"
                                "May - August 2014"
                            }
                        }

                ::

                    >>> show(markup) # doctest: +SKIP

            ..  container:: example expression

                ::

                    >>> expression = Expression().markup_list()
                    >>> expression = expression.center_column(direction=Up)
                    >>> city = Markup('Los Angeles')
                    >>> date = Markup('May - August 2014')
                    >>> markups = [city, date]
                    >>> markup = expression(markups)
                    >>> f(markup)
                    ^ \markup {
                        \center-column
                            {
                                "Los Angeles"
                                "May - August 2014"
                            }
                        }

                ::

                    >>> show(markup) # doctest: +SKIP

        Returns new markup.
        '''
        from abjad.tools import markuptools
        if self._expression:
            return self._update_expression(inspect.currentframe())
        contents = []
        for markup in self:
            string = markuptools.Markup._parse_markup_command_argument(markup)
            contents.append(string)
        command = markuptools.MarkupCommand('center-column', contents)
        return markuptools.Markup(contents=command, direction=direction)

    def column(self, direction=None):
        r'''LilyPond ``\column`` markup command.

        ..  container:: example

            ..  container:: example

                ::

                    >>> city = Markup('Los Angeles')
                    >>> date = Markup('May - August 2014')
                    >>> markup_list = MarkupList([city, date])
                    >>> markup = markup_list.column()
                    >>> f(markup)
                    \markup {
                        \column
                            {
                                "Los Angeles"
                                "May - August 2014"
                            }
                        }

                ::

                    >>> show(markup) # doctest: +SKIP

            ..  container:: example expression

                ::

                    >>> expression = Expression().markup_list()
                    >>> expression = expression.column()
                    >>> city = Markup('Los Angeles')
                    >>> date = Markup('May - August 2014')
                    >>> markup = expression([city, date])
                    >>> f(markup)
                    \markup {
                        \column
                            {
                                "Los Angeles"
                                "May - August 2014"
                            }
                        }

                ::

                    >>> show(markup) # doctest: +SKIP

        Returns new markup.
        '''
        import abjad
        if self._expression:
            return self._update_expression(inspect.currentframe())
        contents = []
        for markup in self:
            contents.extend(markup.contents)
        command = abjad.markuptools.MarkupCommand('column', contents)
        return abjad.Markup(contents=command, direction=direction)

    def combine(self, direction=None):
        r'''LilyPond ``\combine`` markup command.

        ..  container:: example

            ..  container:: example

                ::

                    >>> markup_one = Markup('Allegro assai')
                    >>> markup_two = Markup.draw_line(13, 0)
                    >>> markup_list = [markup_one, markup_two]
                    >>> markup_list = MarkupList(markup_list)
                    >>> markup = markup_list.combine(direction=Up)
                    >>> f(markup)
                    ^ \markup {
                        \combine
                            "Allegro assai"
                            \draw-line
                                #'(13 . 0)
                        }

                ::

                    >>> show(markup) # doctest: +SKIP

            ..  container:: example expression

                ::

                    >>> expression = Expression().markup_list()
                    >>> expression = expression.combine(direction=Up)
                    >>> markup_1 = Markup('Allegro assai')
                    >>> markup_2 = Markup.draw_line(13, 0)
                    >>> markup_list = [markup_1, markup_2]
                    >>> markup = expression(markup_list)
                    >>> f(markup)
                    ^ \markup {
                        \combine
                            "Allegro assai"
                            \draw-line
                                #'(13 . 0)
                        }

                ::

                    >>> show(markup) # doctest: +SKIP

        Returns new markup.
        '''
        import abjad
        if self._expression:
            return self._update_expression(inspect.currentframe())
        if not len(self) == 2:
            message = 'markup list must be length 2: {!r}.'
            message = message.format(markup_list)
            raise Exception(message)
        markup_1, markup_2 = self.items
        contents_1 = abjad.Markup._parse_markup_command_argument(markup_1)
        contents_2 = abjad.Markup._parse_markup_command_argument(markup_2)
        command = abjad.markuptools.MarkupCommand(
            'combine', contents_1, contents_2)
        return abjad.Markup(contents=command, direction=direction)

    def concat(self, direction=None):
        r'''LilyPond ``\concat`` markup command.

        ..  container:: example

            ..  container:: example

                ::

                    >>> downbow = Markup.musicglyph('scripts.downbow')
                    >>> hspace = Markup.hspace(1)
                    >>> upbow = Markup.musicglyph('scripts.upbow')
                    >>> markups = [downbow, hspace, upbow]
                    >>> markup_list = MarkupList(markups)
                    >>> markup = markup_list.concat(direction=Up)
                    >>> f(markup)
                    ^ \markup {
                        \concat
                            {
                                \musicglyph
                                    #"scripts.downbow"
                                \hspace
                                    #1
                                \musicglyph
                                    #"scripts.upbow"
                            }
                        }

                ::

                    >>> show(markup) # doctest: +SKIP

            ..  container:: example expression

                ::

                    >>> expression = Expression().markup_list()
                    >>> expression = expression.concat(direction=Up)
                    >>> downbow = Markup.musicglyph('scripts.downbow')
                    >>> hspace = Markup.hspace(1)
                    >>> upbow = Markup.musicglyph('scripts.upbow')
                    >>> markups = [downbow, hspace, upbow]
                    >>> markup = expression(markups)
                    >>> f(markup)
                    ^ \markup {
                        \concat
                            {
                                \musicglyph
                                    #"scripts.downbow"
                                \hspace
                                    #1
                                \musicglyph
                                    #"scripts.upbow"
                            }
                        }

                ::

                    >>> show(markup) # doctest: +SKIP

        Returns new markup.
        '''
        from abjad.tools import markuptools
        if self._expression:
            return self._update_expression(inspect.currentframe())
        result = []
        for markup in self:
            contents = markuptools.Markup._parse_markup_command_argument(
                markup)
            result.append(contents)
        command = markuptools.MarkupCommand('concat', result)
        return markuptools.Markup(contents=command, direction=direction)

    def count(self, item):
        r'''Counts `item` in markup list.

        ..  container:: example

            ::

                >>> markup_list = MarkupList()
                >>> markup_list.extend(['Allegro', 'assai'])

            ::

                >>> show(markup_list) # doctest: +SKIP

            ::

                >>> markup_list.count('Allegro')
                1
                >>> markup_list.count('assai')
                1
                >>> markup_list.count('ma non troppo')
                0

        Returns none.
        '''
        superclass = super(MarkupList, self)
        return superclass.count(item)

    def extend(self, items):
        r'''Extends markup list with `items`.

        ..  container:: example

            ..  container:: example

                ::

                    >>> markup_list = MarkupList()
                    >>> markup_list.extend(['Allegro', 'assai'])
                    >>> f(markup_list)
                    markuptools.MarkupList(
                        items=[
                            markuptools.Markup(
                                contents=['Allegro'],
                                ),
                            markuptools.Markup(
                                contents=['assai'],
                                ),
                            ],
                        )

                ::

                    >>> show(markup_list) # doctest: +SKIP

                ..  doctest::
            
                    >>> f(markup_list.__illustrate__().items[-1])
                    \markup {
                        \column
                            {
                                Allegro
                                assai
                            }
                        }

            ..  container:: example expression

                ::

                    >>> expression = Expression().markup_list()
                    >>> expression = expression.extend(['assai'])
                    >>> markup_list = expression(['Allegro'])
                    >>> f(markup_list)
                    markuptools.MarkupList(
                        items=[
                            markuptools.Markup(
                                contents=['Allegro'],
                                ),
                            markuptools.Markup(
                                contents=['assai'],
                                ),
                            ],
                        )

                ::

                    >>> show(markup_list) # doctest: +SKIP

                ..  doctest::

                    >>> f(markup_list.__illustrate__().items[-1])
                    \markup {
                        \column
                            {
                                Allegro
                                assai
                            }
                        }

        Returns none.
        '''
        if self._expression:
            return self._update_expression(
                inspect.currentframe(),
                force_return=True,
                )
        superclass = super(MarkupList, self)
        superclass.extend(items)

    def index(self, item):
        r'''Gets index of `item` in markup list.

        ..  container:: example

            ::

                >>> markup_list = MarkupList()
                >>> markup_list.extend(['Allegro', 'assai'])
                >>> f(markup_list)
                markuptools.MarkupList(
                    items=[
                        markuptools.Markup(
                            contents=['Allegro'],
                            ),
                        markuptools.Markup(
                            contents=['assai'],
                            ),
                        ],
                    )

            ::

                >>> show(markup_list) # doctest: +SKIP

            ..  doctest::

                >>> f(markup_list.__illustrate__().items[-1])
                \markup {
                    \column
                        {
                            Allegro
                            assai
                        }
                    }

            ::

                >>> markup_list.index('Allegro')
                0
                >>> markup_list.index('assai')
                1

        Returns none.
        '''
        superclass = super(MarkupList, self)
        return superclass.index(item)

    def insert(self, i, item):
        r'''Inserts `item` in markup markup list.

        ..  container:: example

            ..  container:: example

                ::

                    >>> markup_list = MarkupList(['assai'])
                    >>> markup_list.insert(0, 'Allegro')
                    >>> f(markup_list)
                    markuptools.MarkupList(
                        items=[
                            markuptools.Markup(
                                contents=['Allegro'],
                                ),
                            markuptools.Markup(
                                contents=['assai'],
                                ),
                            ],
                        )

                ::

                    >>> show(markup_list) # doctest: +SKIP

            ..  container:: example expression

                ::

                    >>> expression = Expression().markup_list()
                    >>> expression = expression.insert(0, 'Allegro')
                    >>> markup_list = expression(['assai'])
                    >>> f(markup_list)
                    markuptools.MarkupList(
                        items=[
                            markuptools.Markup(
                                contents=['Allegro'],
                                ),
                            markuptools.Markup(
                                contents=['assai'],
                                ),
                            ],
                        )

                ::

                    >>> show(markup_list) # doctest: +SKIP

        Returns markup class.
        '''
        if self._expression:
            return self._update_expression(
                inspect.currentframe(),
                force_return=True,
                )
        superclass = super(MarkupList, self)
        superclass.insert(i, item)

    def left_column(self, direction=None):
        r'''LilyPond ``\left-column`` markup command.

        ..  container:: example

            ..  container:: example

                ::

                    >>> city = Markup('Los Angeles')
                    >>> date = Markup('May - August 2014')
                    >>> markup_list = MarkupList([city, date])
                    >>> markup = markup_list.left_column()
                    >>> f(markup)
                    \markup {
                        \left-column
                            {
                                "Los Angeles"
                                "May - August 2014"
                            }
                        }

                ::

                    >>> show(markup) # doctest: +SKIP

            ..  container:: example expression

                ::

                    >>> expression = Expression().markup_list()
                    >>> expression = expression.left_column()
                    >>> city = Markup('Los Angeles')
                    >>> date = Markup('May - August 2014')
                    >>> markup = expression([city, date])
                    >>> f(markup)
                    \markup {
                        \left-column
                            {
                                "Los Angeles"
                                "May - August 2014"
                            }
                        }

                ::

                    >>> show(markup) # doctest: +SKIP

        Returns new markup.
        '''
        import abjad
        if self._expression:
            return self._update_expression(inspect.currentframe())
        contents = []
        for markup in self:
            contents.append(abjad.Markup._parse_markup_command_argument(markup))
        command = abjad.markuptools.MarkupCommand('left-column', contents)
        return abjad.Markup(contents=command, direction=direction)

    def line(self, direction=None):
        r'''LilyPond ``\line`` markup command.

        ..  container:: example

            ..  container:: example

                ::

                    >>> markups = ['Allegro', 'assai']
                    >>> markup_list = MarkupList(markups)
                    >>> markup = markup_list.line()
                    >>> f(markup)
                    \markup {
                        \line
                            {
                                Allegro
                                assai
                            }
                        }


                ::

                    >>> show(markup) # doctest: +SKIP

            ..  container:: example expression

                ::

                    >>> expression = Expression().markup_list()
                    >>> expression = expression.line()
                    >>> markup = expression(['Allegro', 'assai'])
                    >>> f(markup)
                    \markup {
                        \line
                            {
                                Allegro
                                assai
                            }
                        }


                ::

                    >>> show(markup) # doctest: +SKIP

        Returns new markup.
        '''
        import abjad
        if self._expression:
            return self._update_expression(inspect.currentframe())
        contents = []
        for markup in self:
            contents.extend(markup.contents)
        command = abjad.markuptools.MarkupCommand('line', contents)
        return abjad.Markup(contents=command, direction=direction)

    def overlay(self, direction=None):
        r'''LilyPond ``\overlay`` markup command.

        ..  container:: example

            ..  container:: example

                ::

                    >>> city = Markup('Los Angeles')
                    >>> date = Markup('May - August 2014')
                    >>> markup_list = MarkupList([city, date])
                    >>> markup = markup_list.overlay(direction=Up)
                    >>> f(markup)
                    ^ \markup {
                        \overlay
                            {
                                "Los Angeles"
                                "May - August 2014"
                            }
                        }

                ::

                    >>> show(markup) # doctest: +SKIP

            ..  container:: example expression

                ::

                    >>> expression = Expression().markup_list()
                    >>> expression = expression.overlay(direction=Up)
                    >>> city = Markup('Los Angeles')
                    >>> date = Markup('May - August 2014')
                    >>> markup = expression([city, date])
                    >>> f(markup)
                    ^ \markup {
                        \overlay
                            {
                                "Los Angeles"
                                "May - August 2014"
                            }
                        }

                ::

                    >>> show(markup) # doctest: +SKIP

        Returns new markup.
        '''
        import abjad
        if self._expression:
            return self._update_expression(inspect.currentframe())
        contents = []
        for markup in self:
            contents.append(abjad.Markup._parse_markup_command_argument(markup))
        command = abjad.markuptools.MarkupCommand('overlay', contents)
        return abjad.Markup(contents=command, direction=direction)

    def pop(self, i=-1):
        r'''Pops item `i` from markup list.

        ..  container:: example

            ..  container:: example

                ::

                    >>> markup_list = MarkupList()
                    >>> markup_list.extend(['Allegro', 'assai'])
                    >>> markup_list.pop()
                    Markup(contents=['assai'])

                ::

                    >>> f(markup_list)
                    markuptools.MarkupList(
                        items=[
                            markuptools.Markup(
                                contents=['Allegro'],
                                ),
                            ],
                        )

                ::

                    >>> show(markup_list) # doctest: +SKIP

            ..  container:: example expression

                ::

                    >>> expression = Expression().markup_list()
                    >>> expression = expression.pop()
                    >>> markup_list = expression(['Allegro', 'assai'])

                ::

                    >>> f(markup_list)
                    markuptools.MarkupList(
                        items=[
                            markuptools.Markup(
                                contents=['Allegro'],
                                ),
                            ],
                        )

                ::

                    >>> show(markup_list) # doctest: +SKIP

        Returns none.
        '''
        if self._expression:
            return self._update_expression(
                inspect.currentframe(),
                force_return=True,
                )
        superclass = super(MarkupList, self)
        return superclass.pop(i=i)

    def remove(self, item):
        r'''Removes `item` from markup list.

        ..  container:: example

            ..  container:: example

                ::

                    >>> markup_list = MarkupList()
                    >>> markup_list.extend(['Allegro', 'assai'])
                    >>> markup_list.remove('assai')
                    >>> f(markup_list)
                    markuptools.MarkupList(
                        items=[
                            markuptools.Markup(
                                contents=['Allegro'],
                                ),
                            ],
                        )

                ::

                    >>> show(markup_list) # doctest: +SKIP

                ..  doctest::

                    >>> f(markup_list.__illustrate__().items[-1])
                    \markup {
                        \column
                            {
                                Allegro
                            }
                        }

            ..  container:: example expression

                ::

                    >>> expression = Expression().markup_list()
                    >>> expression = expression.remove('assai')
                    >>> markup_list = expression(['Allegro', 'assai'])
                    >>> f(markup_list)
                    markuptools.MarkupList(
                        items=[
                            markuptools.Markup(
                                contents=['Allegro'],
                                ),
                            ],
                        )

                ::

                    >>> show(markup_list) # doctest: +SKIP

                ..  doctest::

                    >>> f(markup_list.__illustrate__().items[-1])
                    \markup {
                        \column
                            {
                                Allegro
                            }
                        }

        Returns none.
        '''
        if self._expression:
            return self._update_expression(
                inspect.currentframe(),
                force_return=True,
                )
        superclass = super(MarkupList, self)
        superclass.remove(item)

    def right_column(self, direction=None):
        r'''LilyPond ``\right-column`` markup command.

        ..  container:: example

            ..  container:: example

                ::

                    >>> city = Markup('Los Angeles')
                    >>> date = Markup('May - August 2014')
                    >>> markup_list = MarkupList([city, date])
                    >>> markup = markup_list.right_column()
                    >>> f(markup)
                    \markup {
                        \right-column
                            {
                                "Los Angeles"
                                "May - August 2014"
                            }
                        }

                ::

                    >>> show(markup) # doctest: +SKIP

            ..  container:: example expression

                ::

                    >>> expression = Expression().markup_list()
                    >>> expression = expression.right_column()
                    >>> city = Markup('Los Angeles')
                    >>> date = Markup('May - August 2014')
                    >>> markup = expression([city, date])
                    >>> f(markup)
                    \markup {
                        \right-column
                            {
                                "Los Angeles"
                                "May - August 2014"
                            }
                        }

                ::

                    >>> show(markup) # doctest: +SKIP

        Returns new markup.
        '''
        import abjad
        if self._expression:
            return self._update_expression(inspect.currentframe())
        contents = []
        for markup in self:
            contents.append(abjad.Markup._parse_markup_command_argument(markup))
        command = abjad.markuptools.MarkupCommand('right-column', contents)
        return abjad.Markup(contents=command, direction=direction)
