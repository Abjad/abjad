# -*- encoding: utf-8 -*-
from abjad.tools.abctools.AbjadObject import AbjadObject
from abjad.tools.lilypondfiletools.DateTimeToken import DateTimeToken
from abjad.tools.lilypondfiletools.LilyPondLanguageToken \
    import LilyPondLanguageToken
from abjad.tools.lilypondfiletools.LilyPondVersionToken \
    import LilyPondVersionToken


class LilyPondFile(AbjadObject, list):
    r'''A LilyPond input file.

    ::

        >>> staff = Staff("c'8 d'8 e'8 f'8")
        >>> lilypond_file = lilypondfiletools.make_basic_lilypond_file(staff)
        >>> lilypond_file.file_initial_user_comments.append(
        ...     'File construct as an example.')
        >>> lilypond_file.file_initial_user_comments.append(
        ...     'Parts shown here for positioning.')
        >>> lilypond_file.file_initial_user_includes.append(
        ...     'external-settings-file-1.ly')
        >>> lilypond_file.file_initial_user_includes.append(
        ...     'external-settings-file-2.ly')
        >>> lilypond_file.default_paper_size = 'letter', 'portrait'
        >>> lilypond_file.global_staff_size = 16
        >>> lilypond_file.header_block.composer = \
        ...     markuptools.Markup('Josquin')
        >>> lilypond_file.header_block.title = \
        ...     markuptools.Markup('Missa sexti tonus')
        >>> lilypond_file.layout_block.indent = 0
        >>> lilypond_file.layout_block.left_margin = 15
        >>> lilypond_file.paper_block.oddFooterMarkup = \
        ...     markuptools.Markup('The odd-page footer')
        >>> lilypond_file.paper_block.evenFooterMarkup = \
        ...     markuptools.Markup('The even-page footer')

    ..  doctest::

        >>> print format(lilypond_file)
        % ...

        % File construct as an example.
        % Parts shown here for positioning.

        \version "2..."
        \include "english.ly"

        \include "external-settings-file-1.ly"
        \include "external-settings-file-2.ly"

        #(set-default-paper-size "letter" 'portrait)
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
            evenFooterMarkup = \markup { The even-page footer }
            oddFooterMarkup = \markup { The odd-page footer }
        }

        \new Staff {
            c'8
            d'8
            e'8
            f'8
        }

    '''

    def __init__(self):
        list.__init__(self)
        self._file_initial_system_comments = []
        self._file_initial_system_comments.append(DateTimeToken())
        self._file_initial_user_comments = []
        self._file_initial_system_includes = []
        self._file_initial_system_includes.append(LilyPondVersionToken())
        self._file_initial_system_includes.append(LilyPondLanguageToken())
        self._file_initial_user_includes = []
        self.default_paper_size = None
        self.global_staff_size = None

    ### SPECIAL METHODS ###

    def __format__(self, format_specification=''):
        r'''Formats LilyPond file.

        Returns string.
        '''
        if format_specification in ('', 'lilypond'):
            return self._lilypond_format
        return str(self)

    def __illustrate__(self):
        r'''Illustrates LilyPond file.

        Returns LilyPond file unchanged.
        '''
        return self

    def __repr__(self):
        r'''Gets interpreter representation of LilyPond file.

        Returns string.
        '''
        if hasattr(self, 'score_block') and 1 <= len(self.score_block):
            return '%s(%s)' % (type(self).__name__, self.score_block[0])
        else:
            return '%s()' % type(self).__name__

    ### PRIVATE PROPERTIES ###

    @property
    def _format_pieces(self):
        result = []
        result.extend(self._formatted_file_initial_system_comments)
        result.extend(self._formatted_file_initial_user_comments)
        result.extend(self._formatted_file_initial_system_includes)
        result.extend(self._formatted_file_initial_user_includes)
        result.extend(self._formatted_file_initial_scheme_settings)
        result.extend(self._formatted_blocks)
        return result

    @property
    def _formatted_blocks(self):
        result = []
        for x in self:
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
            result.append("#(set-default-paper-size \"%s\" '%s)" % (
                dimension, orientation))
        global_staff_size = self.global_staff_size
        if global_staff_size is not None:
            result.append('#(set-global-staff-size %s)' % global_staff_size)
        if result:
            result = ['\n'.join(result)]
        return result

    @property
    def _formatted_file_initial_system_comments(self):
        result = []
        for x in self.file_initial_system_comments:
            if '_lilypond_format' in dir(x) and not isinstance(x, str):
                lilypond_format = format(x)
                if lilypond_format:
                    result.append('%% %s' % format(x))
            else:
                result.append('%% %s' % str(x))
        if result:
            result = ['\n'.join(result)]
        return result

    @property
    def _formatted_file_initial_system_includes(self):
        result = []
        for file_initial_include in self.file_initial_system_includes:
            if isinstance(file_initial_include, str):
                result.append(r'\include "%s"' % file_initial_include)
            else:
                result.append(format(file_initial_include))
        if result:
            result = ['\n'.join(result)]
        return result

    @property
    def _formatted_file_initial_user_comments(self):
        result = []
        for x in self.file_initial_user_comments:
            if '_lilypond_format' in dir(x) and not isinstance(x, str):
                lilypond_format = format(x)
                if lilypond_format:
                    result.append('%% %s' % format(x))
            else:
                result.append('%% %s' % str(x))
        if result:
            result = ['\n'.join(result)]
        return result

    @property
    def _formatted_file_initial_user_includes(self):
        result = []
        for file_initial_include in self.file_initial_user_includes:
            if isinstance(file_initial_include, str):
                result.append(r'\include "%s"' % file_initial_include)
            else:
                result.append(format(file_initial_include))
        if result:
            result = ['\n'.join(result)]
        return result

    @property
    def _lilypond_format(self):
        return '\n\n'.join(self._format_pieces)
        
    ### PUBLIC PROPERTIES ###

    @property
    def default_paper_size(self):
        r'''LilyPond default paper size.
        '''
        return self._default_paper_size


    @default_paper_size.setter
    def default_paper_size(self, args):
        # #(set-default-paper-size "11x17" 'landscape)
        assert args is None or len(args) == 2
        self._default_paper_size = args


    @property
    def file_initial_system_comments(self):
        r'''List of file-initial system comments.
        '''
        return self._file_initial_system_comments


    @file_initial_system_comments.setter
    def file_initial_system_comments(self, arg):
        if isinstance(arg, list):
            self._file_initial_system_comments = arg
        else:
            raise TypeError


    @property
    def file_initial_system_includes(self):
        r'''List of file-initial system include commands.
        '''
        return self._file_initial_system_includes


    @file_initial_system_includes.setter
    def file_initial_system_includes(self, arg):
        if isinstance(arg, list):
            self._file_initial_system_includes = arg
        else:
            raise TypeError


    @property
    def file_initial_user_comments(self):
        r'''List of file-initial user comments.
        '''
        return self._file_initial_user_comments


    @file_initial_user_comments.setter
    def file_initial_user_comments(self, arg):
        if isinstance(arg, list):
            self._file_initial_user_comments = arg
        else:
            raise TypeError


    @property
    def file_initial_user_includes(self):
        r'''List of file-initial user include commands.
        '''
        return self._file_initial_user_includes


    @file_initial_user_includes.setter
    def file_initial_user_includes(self, arg):
        if isinstance(arg, list):
            self._file_initial_user_includes = arg
        else:
            raise TypeError


    @property
    def global_staff_size(self):
        r'''LilyPond global staff size.
        '''
        return self._global_staff_size


    @global_staff_size.setter
    def global_staff_size(self, arg):
        assert isinstance(arg, (int, float, long, type(None)))
        self._global_staff_size = arg
