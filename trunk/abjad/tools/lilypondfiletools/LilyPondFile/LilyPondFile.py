from abjad.cfg.cfg import ABJADPATH
from abjad.tools.lilypondfiletools.AbjadRevisionToken import AbjadRevisionToken
from abjad.tools.lilypondfiletools.DateTimeToken import DateTimeToken
from abjad.tools.lilypondfiletools.LilyPondLanguageToken import LilyPondLanguageToken
from abjad.tools.lilypondfiletools.LilyPondVersionToken import LilyPondVersionToken
import os


class LilyPondFile(list):
    r'''.. versionadded:: 2.0

    Abjad model of LilyPond input file::

        abjad> staff = Staff("c'8 d'8 e'8 f'8")
        abjad> lilypond_file = lilypondfiletools.make_basic_lilypond_file(staff)
        abjad> lilypond_file.file_initial_user_comments.append('File construct as an example.')
        abjad> lilypond_file.file_initial_user_comments.append('Parts shown here for positioning.')
        abjad> lilypond_file.file_initial_user_includes.append('external-settings-file-1.ly')
        abjad> lilypond_file.file_initial_user_includes.append('external-settings-file-2.ly')
        abjad> lilypond_file.default_paper_size = 'letter', 'portrait'
        abjad> lilypond_file.global_staff_size = 16
        abjad> lilypond_file.header_block.composer = markuptools.Markup('Josquin')
        abjad> lilypond_file.header_block.title = markuptools.Markup('Missa sexti tonus')
        abjad> lilypond_file.layout_block.indent = 0
        abjad> lilypond_file.layout_block.left_margin = 15
        abjad> lilypond_file.paper_block.oddFooterMarkup = markuptools.Markup('The odd-page footer')
        abjad> lilypond_file.paper_block.evenFooterMarkup = markuptools.Markup('The even-page footer')

    ::

        abjad> f(lilypond_file) # doctest: +SKIP
        % Abjad revision 3719
        % 2010-09-24 09:01

        % File construct as an example.
        % Parts shown here for positioning.

        \version "2.13.32"
        \include "english.ly"
        \include "/Users/trevorbaca/Documents/abjad/trunk/abjad/cfg/abjad.scm"

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
        self._file_initial_system_comments.append(AbjadRevisionToken())
        self._file_initial_system_comments.append(DateTimeToken())
        self._file_initial_user_comments = []
        self._file_initial_system_includes = []
        self._file_initial_system_includes.append(LilyPondVersionToken())
        self._file_initial_system_includes.append(LilyPondLanguageToken())
        self._file_initial_system_includes.append(os.path.join(ABJADPATH, 'cfg', 'abjad.scm'))
        self._file_initial_user_includes = []
        self.default_paper_size = None
        self.global_staff_size = None

    ### OVERLOADS ###

    def __repr__(self):
        if hasattr(self, 'score_block') and 1 <= len(self.score_block):
            return '%s(%s)' % (type(self).__name__, self.score_block[0])
        else:
            return '%s()' % type(self).__name__

    ### PRIVATE ATTRIBUTES ###

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
            if 'format' in dir(x) and not isinstance(x, str):
                format = x.format
                if format:
                    result.append(x.format)
            else:
                result.append(str(x))
        return result

    @property
    def _formatted_file_initial_system_comments(self):
        result = []
        for x in self.file_initial_system_comments:
            if 'format' in dir(x) and not isinstance(x, str):
                format = x.format
                if format:
                    result.append('%% %s' % x.format)
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
                result.append(file_initial_include.format)
        if result:
            result = ['\n'.join(result)]
        return result

    @property
    def _formatted_file_initial_scheme_settings(self):
        result = []
        default_paper_size = self.default_paper_size
        if default_paper_size is not None:
            dimension, orientation = default_paper_size
            result.append("#(set-default-paper-size \"%s\" '%s)" % (dimension, orientation))
        global_staff_size = self.global_staff_size
        if global_staff_size is not None:
            result.append('#(set-global-staff-size %s)' % global_staff_size)
        if result:
            result = ['\n'.join(result)]
        return result

    @property
    def _formatted_file_initial_user_comments(self):
        result = []
        for x in self.file_initial_user_comments:
            if 'format' in dir(x) and not isinstance(x, str):
                format = x.format
                if format:
                    result.append('%% %s' % x.format)
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
                result.append(file_initial_include.format)
        if result:
            result = ['\n'.join(result)]
        return result

    ### PUBLIC ATTRIBUTES ###

    @apply
    def default_paper_size():
        def fget(self):
            '''LilyPond default paper size.'''
            return self._default_paper_size
        def fset(self, args):
            # #(set-default-paper-size "11x17" 'landscape)
            assert args is None or len(args) == 2
            self._default_paper_size = args
        return property(**locals())

    @apply
    def file_initial_system_comments():
        def fget(self):
            '''Read-only list of file-initial system comments.
            '''
            return self._file_initial_system_comments
        def fset(self, arg):
            if isinstance(arg, list):
                self._file_initial_system_comments = arg
            else:
                raise TypeError
        return property(**locals())

    @apply
    def file_initial_system_includes():
        def fget(self):
            '''List of file-initial system include commands.
            '''
            return self._file_initial_system_includes
        def fset(self, arg):
            if isinstance(arg, list):
                self._file_initial_system_includes = arg
            else:
                raise TypeError
        return property(**locals())

    @apply
    def file_initial_user_comments():
        def fget(self):
            '''Read-only list of file-initial user comments.
            '''
            return self._file_initial_user_comments
        def fset(self, arg):
            if isinstance(arg, list):
                self._file_initial_user_comments = arg
            else:
                raise TypeError
        return property(**locals())

    @apply
    def file_initial_user_includes():
        def fget(self):
            '''List of file-initial user include commands.
            '''
            return self._file_initial_user_includes
        def fset(self, arg):
            if isinstance(arg, list):
                self._file_initial_user_includes = arg
            else:
                raise TypeError
        return property(**locals())

    @property
    def format(self):
        '''Format-time contribution of LilyPond file.
        '''
        return '\n\n'.join(self._format_pieces)

    @apply
    def global_staff_size():
        def fget(self):
            '''LilyPond global staff size.'''
            return self._global_staff_size
        def fset(self, arg):
            assert isinstance(arg, (int, float, long, type(None)))
            self._global_staff_size = arg
        return property(**locals())
