# -*- encoding: utf-8 -*-
from abjad.tools.abctools.AbjadObject import AbjadObject


class LilyPondFile(AbjadObject):
    r'''A LilyPond file.

    ..  container:: example

        ::

            >>> staff = Staff("c'8 d'8 e'8 f'8")
            >>> lilypond_file = lilypondfiletools.make_basic_lilypond_file(staff)
            >>> comment = 'File construct as an example.'
            >>> lilypond_file.file_initial_user_comments.append(comment)
            >>> comment = 'Parts shown here for positioning.'
            >>> lilypond_file.file_initial_user_comments.append(comment)
            >>> file_name = 'external-settings-file-1.ly'
            >>> lilypond_file.file_initial_user_includes.append(file_name)
            >>> file_name = 'external-settings-file-2.ly'
            >>> lilypond_file.file_initial_user_includes.append(file_name)
            >>> lilypond_file.default_paper_size = 'a5', 'portrait'
            >>> lilypond_file.global_staff_size = 16
            >>> lilypond_file.header_block.composer = Markup('Josquin')
            >>> lilypond_file.header_block.title = Markup('Missa sexti tonus')
            >>> lilypond_file.layout_block.indent = 0
            >>> lilypond_file.layout_block.left_margin = 15
            >>> lilypond_file
            <LilyPondFile(4)>

        ::

            >>> print(format(lilypond_file)) # doctest: +SKIP
            % 2004-01-14 17:29

            % File construct as an example.
            % Parts shown here for positioning.

            \version "2.19.0"
            \language "english"

            \include "external-settings-file-1.ly"
            \include "external-settings-file-2.ly"

            #(set-default-paper-size "a5" 'portrait)
            #(set-global-staff-size 16)

            \header {
                composer = \markup { Josquin }
                title = \markup { Missa sexti tonus }
            }

            \layout {
                indent = #0
                left-margin = #15
            }

            \paper {
            }

            \new Staff {
                c'8
                d'8
                e'8
                f'8
            }

        ::

            >>> show(lilypond_file) # doctest: +SKIP

    '''

    def __init__(self):
        from abjad.tools import lilypondfiletools
        self._items = []
        self._file_initial_system_comments = []
        token = lilypondfiletools.DateTimeToken()
        self._file_initial_system_comments.append(token)
        self._file_initial_user_comments = []
        self._file_initial_system_includes = []
        token = lilypondfiletools.LilyPondVersionToken()
        self._file_initial_system_includes.append(token)
        token = lilypondfiletools.LilyPondLanguageToken()
        self._file_initial_system_includes.append(token)
        self._file_initial_user_includes = []
        self.default_paper_size = None
        self.global_staff_size = None
        self.use_relative_includes = False

    ### SPECIAL METHODS ###

    def __format__(self, format_specification=''):
        r'''Formats LilyPond file.

        Returns string.
        '''
        from abjad.tools import systemtools
        if format_specification in ('', 'lilypond'):
            return self._lilypond_format
        elif format_specification == 'storage':
            return systemtools.StorageFormatManager.get_storage_format(self)
        return str(self)

    def __getitem__(self, name):
        r'''Gets LilyPond file item with `name`.

        ..  container:: example

            ::

                >>> lilypond_file['header']
                <Block(name='header')>

        Raises key error when no item with `name` is found.
        '''
        for item in self.items:
            if getattr(item, 'name', None) == name:
                return item
        raise KeyError

    def __illustrate__(self):
        r'''Illustrates LilyPond file.

        Returns LilyPond file unchanged.
        '''
        return self

    def __repr__(self):
        r'''Gets interpreter representation of LilyPond file.

        ..  container:: example

            ::

                >>> lilypond_file
                <LilyPondFile(4)>

        Returns string.
        '''
        from abjad.tools import systemtools
        return systemtools.StorageFormatManager.get_repr_format(self)

    ### PRIVATE PROPERTIES ###

    @property
    def _format_pieces(self):
        result = []
        result.extend(self._formatted_file_initial_system_comments)
        result.extend(self._formatted_file_initial_user_comments)
        result.extend(self._formatted_file_initial_system_includes)
        if self.use_relative_includes:
            string = "#(ly:set-option 'relative-includes #t)"
            result.append(string)
        result.extend(self._formatted_file_initial_user_includes)
        result.extend(self._formatted_file_initial_scheme_settings)
        result.extend(self._formatted_blocks)
        return result

    @property
    def _formatted_blocks(self):
        result = []
        for x in self.items:
            if '_lilypond_format' in dir(x) and not isinstance(x, str):
                lilypond_format = format(x)
                if lilypond_format:
                    result.append(lilypond_format)
            else:
                result.append(str(x))
        return result

    @property
    def _formatted_file_initial_scheme_settings(self):
        result = []
        default_paper_size = self.default_paper_size
        if default_paper_size is not None:
            dimension, orientation = default_paper_size
            string = "#(set-default-paper-size \"{}\" '{})"
            string = string.format(dimension, orientation)
            result.append(string)
        global_staff_size = self.global_staff_size
        if global_staff_size is not None:
            string = '#(set-global-staff-size {})'
            string = string.format(global_staff_size)
            result.append(string)
        if result:
            result = ['\n'.join(result)]
        return result

    @property
    def _formatted_file_initial_system_comments(self):
        result = []
        for comment in self.file_initial_system_comments:
            if '_lilypond_format' in dir(comment) and \
                not isinstance(comment, str):
                lilypond_format = format(comment)
                if lilypond_format:
                    string = '% {}'.format(comment)
                    result.append(string)
            else:
                string = '% {!s}'.format(comment)
                result.append(string)
        if result:
            result = ['\n'.join(result)]
        return result

    @property
    def _formatted_file_initial_system_includes(self):
        result = []
        for file_initial_include in self.file_initial_system_includes:
            if isinstance(file_initial_include, str):
                string = r'\include "{}"'.format(file_initial_include)
                result.append(string)
            else:
                result.append(format(file_initial_include))
        if result:
            result = ['\n'.join(result)]
        return result

    @property
    def _formatted_file_initial_user_comments(self):
        result = []
        for comment in self.file_initial_user_comments:
            if '_lilypond_format' in dir(comment) and \
                not isinstance(comment, str):
                lilypond_format = format(comment)
                if lilypond_format:
                    string = '% {}'.format(comment)
                    result.append(string)
            else:
                string = '% {!s}'.format(comment)
                result.append(string)
        if result:
            result = ['\n'.join(result)]
        return result

    @property
    def _formatted_file_initial_user_includes(self):
        result = []
        for file_initial_include in self.file_initial_user_includes:
            if isinstance(file_initial_include, str):
                string = r'\include "{}"'.format(file_initial_include)
                result.append(string)
            else:
                result.append(format(file_initial_include))
        if result:
            result = ['\n'.join(result)]
        return result

    @property
    def _lilypond_format(self):
        return '\n\n'.join(self._format_pieces)

    @property
    def _repr_specification(self):
        from abjad.tools import systemtools
        positional_argument_values = []
        if self.items:
            positional_argument_values.append(len(self.items))
        positional_argument_values = tuple(positional_argument_values)
        return systemtools.StorageFormatSpecification(
            self,
            is_bracketed=True,
            is_indented=False,
            positional_argument_values=positional_argument_values,
            )

    ### PUBLIC PROPERTIES ###

    @property
    def default_paper_size(self):
        r'''Gets default paper size of LilyPond file.

        ..  container:: example

            ::

                >>> lilypond_file.default_paper_size
                ('a5', 'portrait')

        Returns pair or none.
        '''
        return self._default_paper_size

    @default_paper_size.setter
    def default_paper_size(self, args):
        assert args is None or len(args) == 2
        self._default_paper_size = args

    @property
    def file_initial_system_comments(self):
        r'''Gets file-initial system comments of LilyPond file.

        ..  container:: example

            ::

                >>> for x in lilypond_file.file_initial_system_comments: # doctest: +SKIP
                ...     x
                ...
                DateTimeToken('2014-01-04 17:16')

        Returns list.
        '''
        return self._file_initial_system_comments

    @property
    def file_initial_system_includes(self):
        r'''Gets file-initial system include commands of LilyPond file.

        ..  container:: example

            ::

                >>> for x in lilypond_file.file_initial_system_includes:
                ...     x
                ...
                LilyPondVersionToken('...')
                LilyPondLanguageToken()

        Returns list.
        '''
        return self._file_initial_system_includes

    @property
    def file_initial_user_comments(self):
        r'''Gets file-initial user comments of Lilypond file.

        ..  container:: example

            ::

                >>> for x in lilypond_file.file_initial_user_comments:
                ...     x
                ...
                'File construct as an example.'
                'Parts shown here for positioning.'

        Returns list.
        '''
        return self._file_initial_user_comments

    @property
    def file_initial_user_includes(self):
        r'''Gets file-initial user include commands of LilyPond file.

        ..  container:: example

            ::

                >>> for x in lilypond_file.file_initial_user_includes:
                ...     x
                ...
                'external-settings-file-1.ly'
                'external-settings-file-2.ly'

        Returns list.
        '''
        return self._file_initial_user_includes

    @property
    def global_staff_size(self):
        r'''Gets global staff size of LilyPond file.

        ..  container:: example

            ::

                >>> lilypond_file.global_staff_size
                16

        Returns number.
        '''
        return self._global_staff_size

    @global_staff_size.setter
    def global_staff_size(self, arg):
        assert isinstance(arg, (int, float, int, type(None)))
        self._global_staff_size = arg

    @property
    def items(self):
        r'''Gets items in LilyPond file.

        ..  container:: example

            ::

                >>> for item in lilypond_file.items:
                ...     item
                ...
                <Block(name='header')>
                <Block(name='layout')>
                <Block(name='paper')>
                <Block(name='score')>

        Returns list.
        '''
        return self._items

    @property
    def use_relative_includes(self):
        r'''Gets boolean flag to use relative include paths.

        ..  container:: example

            ::

                >>> lilypond_file.use_relative_includes
                False

        Returns boolean.
        '''
        return self._use_relative_includes

    @use_relative_includes.setter
    def use_relative_includes(self, arg):
        self._use_relative_includes = bool(arg)