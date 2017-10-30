from abjad.tools.datastructuretools.TypedList import TypedList


class MarkupList(TypedList):
    '''Markup list.

    ..  container:: example

        Initializes from strings:

        ..  container:: example

            >>> markups = ['Allegro', 'assai']
            >>> markup_list = abjad.MarkupList(markups)
            >>> abjad.f(markup_list)
            abjad.MarkupList(
                items=[
                    abjad.Markup(
                        contents=['Allegro'],
                        ),
                    abjad.Markup(
                        contents=['assai'],
                        ),
                    ],
                )

            >>> abjad.show(markup_list) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(markup_list.__illustrate__().items[-1])
                \markup {
                    \column
                        {
                            Allegro
                            assai
                        }
                    }

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

                >>> markups = ['Allegro', 'assai']
                >>> markup_list = abjad.MarkupList(markups)

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


                    >>> markups = ['Allegro', 'assai']
                    >>> markup_list = abjad.MarkupList(markups)
                    >>> abjad.f(markup_list)
                    abjad.MarkupList(
                        items=[
                            abjad.Markup(
                                contents=['Allegro'],
                                ),
                            abjad.Markup(
                                contents=['assai'],
                                ),
                            ],
                        )

        Returns string.
        '''
        superclass = super(MarkupList, self)
        return superclass.__format__(format_specification=format_specification)

    def __iadd__(self, argument):
        r'''Changes items in `argument` to items and extends markup list.

        ..  container:: example

            ..  container:: example

                >>> markup_list = abjad.MarkupList()
                >>> markup_list.extend(['Allegro', 'assai'])
                >>> markup_list += ['ma', 'non', 'troppo']
                >>> abjad.f(markup_list)
                abjad.MarkupList(
                    items=[
                        abjad.Markup(
                            contents=['Allegro'],
                            ),
                        abjad.Markup(
                            contents=['assai'],
                            ),
                        abjad.Markup(
                            contents=['ma'],
                            ),
                        abjad.Markup(
                            contents=['non'],
                            ),
                        abjad.Markup(
                            contents=['troppo'],
                            ),
                        ],
                    )

                >>> abjad.show(markup_list) # doctest: +SKIP

                ..  docs::

                    >>> abjad.f(markup_list.__illustrate__().items[-1])
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

        Returns none.
        '''
        superclass = super(MarkupList, self)
        return superclass.__iadd__(argument)

    def __illustrate__(self):
        r'''Illustrates markup markup list.

        ..  container:: example

            ..  container:: example

                >>> markups = ['Allegro', 'assai']
                >>> markup_list = abjad.MarkupList(markups)
                >>> abjad.f(markup_list)
                abjad.MarkupList(
                    items=[
                        abjad.Markup(
                            contents=['Allegro'],
                            ),
                        abjad.Markup(
                            contents=['assai'],
                            ),
                        ],
                    )

                >>> abjad.show(markup_list) # doctest: +SKIP

                ..  docs::

                    >>> abjad.f(markup_list.__illustrate__().items[-1])
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

                >>> markup_list = abjad.MarkupList()
                >>> markup_list.extend(['Allegro', 'assai'])
                >>> markup_list[-1] = 'non troppo'
                >>> abjad.f(markup_list)
                abjad.MarkupList(
                    items=[
                        abjad.Markup(
                            contents=['Allegro'],
                            ),
                        abjad.Markup(
                            contents=['non troppo'],
                            ),
                        ],
                    )

                >>> abjad.show(markup_list) # doctest: +SKIP

                ..  docs::

                    >>> abjad.f(markup_list.__illustrate__().items[-1])
                    \markup {
                        \column
                            {
                                Allegro
                                "non troppo"
                            }
                        }

        Returns none.
        '''
        superclass = super(MarkupList, self)
        return superclass.__setitem__(i, argument)

    ### PRIVATE METHODS ###

    def _get_format_specification(self):
        import abjad
        agent = abjad.StorageFormatManager(self)
        names = list(agent.signature_keyword_names)
        if self.item_class is abjad.Markup:
            names.remove('item_class')
        return abjad.FormatSpecification(
            client=self,
            storage_format_kwargs_names=names,
            )

    def _update_expression(self, frame, force_return=None):
        import abjad
        callback = abjad.Expression._frame_to_callback(
            frame,
            force_return=force_return,
            )
        return self._expression.append_callback(callback)

    ### PUBLIC PROPERTIES ###

    @property
    def item_class(self):
        r'''Gets markup list item class.

        ..  container:: example

            >>> abjad.MarkupList().item_class
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

                >>> items = ['Allegro', 'assai']
                >>> markup_list = abjad.MarkupList(items)
                >>> for item in markup_list.items:
                ...     item
                ...
                Markup(contents=['Allegro'])
                Markup(contents=['assai'])

                Initializes items from keyword:

                >>> items = ['Allegro', 'assai']
                >>> markup_list = abjad.MarkupList(items=items)
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

            >>> markups = ['Allegro', 'assai']
            >>> markup_list = abjad.MarkupList(keep_sorted=True)
            >>> markup_list.append('assai')
            >>> markup_list.append('Allegro')
            >>> abjad.show(markup_list) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(markup_list.__illustrate__().items[-1])
                \markup {
                    \column
                        {
                            Allegro
                            assai
                        }
                    }

        ..  container:: example

            Does not keep markup sorted:

            >>> markups = ['Allegro', 'assai']
            >>> markup_list = abjad.MarkupList()
            >>> markup_list.append('assai')
            >>> markup_list.append('Allegro')
            >>> abjad.show(markup_list) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(markup_list.__illustrate__().items[-1])
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

                >>> markup_list = abjad.MarkupList(['Allegro'])
                >>> markup_list.append('assai')
                >>> abjad.f(markup_list)
                abjad.MarkupList(
                    items=[
                        abjad.Markup(
                            contents=['Allegro'],
                            ),
                        abjad.Markup(
                            contents=['assai'],
                            ),
                        ],
                    )

                >>> abjad.show(markup_list) # doctest: +SKIP

        Returns none.
        '''
        superclass = super(MarkupList, self)
        superclass.append(item)

    def center_column(self, direction=None):
        r'''LilyPond ``\center-column`` markup command.

        ..  container:: example

            ..  container:: example

                >>> city = abjad.Markup('Los Angeles')
                >>> date = abjad.Markup('May - August 2014')
                >>> markups = [city, date]
                >>> markup_list = abjad.MarkupList(markups)
                >>> markup = markup_list.center_column(direction=abjad.Up)
                >>> abjad.f(markup)
                ^ \markup {
                    \center-column
                        {
                            "Los Angeles"
                            "May - August 2014"
                        }
                    }

                >>> abjad.show(markup) # doctest: +SKIP

        Returns new markup.
        '''
        from abjad.tools import markuptools
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

                >>> city = abjad.Markup('Los Angeles')
                >>> date = abjad.Markup('May - August 2014')
                >>> markup_list = abjad.MarkupList([city, date])
                >>> markup = markup_list.column()
                >>> abjad.f(markup)
                \markup {
                    \column
                        {
                            "Los Angeles"
                            "May - August 2014"
                        }
                    }

                >>> abjad.show(markup) # doctest: +SKIP

        Returns new markup.
        '''
        import abjad
        contents = []
        for markup in self:
            contents.extend(markup.contents)
        command = abjad.markuptools.MarkupCommand('column', contents)
        return abjad.Markup(contents=command, direction=direction)

    def combine(self, direction=None):
        r'''LilyPond ``\combine`` markup command.

        ..  container:: example

            ..  container:: example

                >>> markup_one = abjad.Markup('Allegro assai')
                >>> markup_two = abjad.Markup.draw_line(13, 0)
                >>> markup_list = [markup_one, markup_two]
                >>> markup_list = abjad.MarkupList(markup_list)
                >>> markup = markup_list.combine(direction=abjad.Up)
                >>> abjad.f(markup)
                ^ \markup {
                    \combine
                        "Allegro assai"
                        \draw-line
                            #'(13 . 0)
                    }

                >>> abjad.show(markup) # doctest: +SKIP

        Returns new markup.
        '''
        import abjad
        if not len(self) == 2:
            message = 'markup list must be length 2: {!r}.'
            message = message.format(self)
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

                >>> downbow = abjad.Markup.musicglyph('scripts.downbow')
                >>> hspace = abjad.Markup.hspace(1)
                >>> upbow = abjad.Markup.musicglyph('scripts.upbow')
                >>> markups = [downbow, hspace, upbow]
                >>> markup_list = abjad.MarkupList(markups)
                >>> markup = markup_list.concat(direction=abjad.Up)
                >>> abjad.f(markup)
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

                >>> abjad.show(markup) # doctest: +SKIP

        Returns new markup.
        '''
        from abjad.tools import markuptools
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

            >>> markup_list = abjad.MarkupList()
            >>> markup_list.extend(['Allegro', 'assai'])

            >>> abjad.show(markup_list) # doctest: +SKIP

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

                >>> markup_list = abjad.MarkupList()
                >>> markup_list.extend(['Allegro', 'assai'])
                >>> abjad.f(markup_list)
                abjad.MarkupList(
                    items=[
                        abjad.Markup(
                            contents=['Allegro'],
                            ),
                        abjad.Markup(
                            contents=['assai'],
                            ),
                        ],
                    )

                >>> abjad.show(markup_list) # doctest: +SKIP

                ..  docs::

                    >>> abjad.f(markup_list.__illustrate__().items[-1])
                    \markup {
                        \column
                            {
                                Allegro
                                assai
                            }
                        }

        Returns none.
        '''
        superclass = super(MarkupList, self)
        superclass.extend(items)

    def index(self, item):
        r'''Gets index of `item` in markup list.

        ..  container:: example

            >>> markup_list = abjad.MarkupList()
            >>> markup_list.extend(['Allegro', 'assai'])
            >>> abjad.f(markup_list)
            abjad.MarkupList(
                items=[
                    abjad.Markup(
                        contents=['Allegro'],
                        ),
                    abjad.Markup(
                        contents=['assai'],
                        ),
                    ],
                )

            >>> abjad.show(markup_list) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(markup_list.__illustrate__().items[-1])
                \markup {
                    \column
                        {
                            Allegro
                            assai
                        }
                    }

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

                >>> markup_list = abjad.MarkupList(['assai'])
                >>> markup_list.insert(0, 'Allegro')
                >>> abjad.f(markup_list)
                abjad.MarkupList(
                    items=[
                        abjad.Markup(
                            contents=['Allegro'],
                            ),
                        abjad.Markup(
                            contents=['assai'],
                            ),
                        ],
                    )

                >>> abjad.show(markup_list) # doctest: +SKIP

        Returns markup class.
        '''
        superclass = super(MarkupList, self)
        superclass.insert(i, item)

    def left_column(self, direction=None):
        r'''LilyPond ``\left-column`` markup command.

        ..  container:: example

            ..  container:: example

                >>> city = abjad.Markup('Los Angeles')
                >>> date = abjad.Markup('May - August 2014')
                >>> markup_list = abjad.MarkupList([city, date])
                >>> markup = markup_list.left_column()
                >>> abjad.f(markup)
                \markup {
                    \left-column
                        {
                            "Los Angeles"
                            "May - August 2014"
                        }
                    }

                >>> abjad.show(markup) # doctest: +SKIP

        Returns new markup.
        '''
        import abjad
        contents = []
        for markup in self:
            contents.append(abjad.Markup._parse_markup_command_argument(markup))
        command = abjad.markuptools.MarkupCommand('left-column', contents)
        return abjad.Markup(contents=command, direction=direction)

    def line(self, direction=None):
        r'''LilyPond ``\line`` markup command.

        ..  container:: example

            ..  container:: example

                >>> markups = ['Allegro', 'assai']
                >>> markup_list = abjad.MarkupList(markups)
                >>> markup = markup_list.line()
                >>> abjad.f(markup)
                \markup {
                    \line
                        {
                            Allegro
                            assai
                        }
                    }


                >>> abjad.show(markup) # doctest: +SKIP

        Returns new markup.
        '''
        import abjad
        contents = []
        for markup in self:
            contents.extend(markup.contents)
        command = abjad.markuptools.MarkupCommand('line', contents)
        return abjad.Markup(contents=command, direction=direction)

    def overlay(self, direction=None):
        r'''LilyPond ``\overlay`` markup command.

        ..  container:: example

            ..  container:: example

                >>> city = abjad.Markup('Los Angeles')
                >>> date = abjad.Markup('May - August 2014')
                >>> markup_list = abjad.MarkupList([city, date])
                >>> markup = markup_list.overlay(direction=abjad.Up)
                >>> abjad.f(markup)
                ^ \markup {
                    \overlay
                        {
                            "Los Angeles"
                            "May - August 2014"
                        }
                    }

                >>> abjad.show(markup) # doctest: +SKIP

        Returns new markup.
        '''
        import abjad
        contents = []
        for markup in self:
            contents.append(abjad.Markup._parse_markup_command_argument(markup))
        command = abjad.markuptools.MarkupCommand('overlay', contents)
        return abjad.Markup(contents=command, direction=direction)

    def pop(self, i=-1):
        r'''Pops item `i` from markup list.

        ..  container:: example

            ..  container:: example

                >>> markup_list = abjad.MarkupList()
                >>> markup_list.extend(['Allegro', 'assai'])
                >>> markup_list.pop()
                Markup(contents=['assai'])

                >>> abjad.f(markup_list)
                abjad.MarkupList(
                    items=[
                        abjad.Markup(
                            contents=['Allegro'],
                            ),
                        ],
                    )

                >>> abjad.show(markup_list) # doctest: +SKIP

        Returns none.
        '''
        superclass = super(MarkupList, self)
        return superclass.pop(i=i)

    def remove(self, item):
        r'''Removes `item` from markup list.

        ..  container:: example

            ..  container:: example

                >>> markup_list = abjad.MarkupList()
                >>> markup_list.extend(['Allegro', 'assai'])
                >>> markup_list.remove('assai')
                >>> abjad.f(markup_list)
                abjad.MarkupList(
                    items=[
                        abjad.Markup(
                            contents=['Allegro'],
                            ),
                        ],
                    )

                >>> abjad.show(markup_list) # doctest: +SKIP

                ..  docs::

                    >>> abjad.f(markup_list.__illustrate__().items[-1])
                    \markup {
                        \column
                            {
                                Allegro
                            }
                        }

        Returns none.
        '''
        superclass = super(MarkupList, self)
        superclass.remove(item)

    def right_column(self, direction=None):
        r'''LilyPond ``\right-column`` markup command.

        ..  container:: example

            ..  container:: example

                >>> city = abjad.Markup('Los Angeles')
                >>> date = abjad.Markup('May - August 2014')
                >>> markup_list = abjad.MarkupList([city, date])
                >>> markup = markup_list.right_column()
                >>> abjad.f(markup)
                \markup {
                    \right-column
                        {
                            "Los Angeles"
                            "May - August 2014"
                        }
                    }

                >>> abjad.show(markup) # doctest: +SKIP

        Returns new markup.
        '''
        import abjad
        contents = []
        for markup in self:
            contents.append(abjad.Markup._parse_markup_command_argument(markup))
        command = abjad.markuptools.MarkupCommand('right-column', contents)
        return abjad.Markup(contents=command, direction=direction)
