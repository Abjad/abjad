# -*- coding: utf-8 -*-
import re
from docutils.parsers.rst import directives
from sphinx.util.compat import Directive
from sphinx.util.nodes import set_source_info
from docutils.nodes import literal_block


class AbjadDirective(Directive):
    r'''An abjad-book interpreter directive.

    Represents a portion of an interactive session.

    Generates a ``abjad_input_block`` node.
    '''

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Sphinx Internals'

    ### CLASS VARIABLES ###

    has_content = True
    required_arguments = 0
    optional_arguments = 0
    final_argument_whitespace = True
    option_spec = {
        'allow-exceptions': directives.flag,
        'hide': directives.flag,
        'no-resize': directives.flag,
        'no-stylesheet': directives.flag,
        'no-trim': directives.flag,
        'pages': str,
        'reveal-label': str,
        'strip-prompt': directives.flag,
        'stylesheet': str,
        'text-width': int,
        'with-columns': int,
        'with-thumbnail': directives.flag,
        }

    ### PRIVATE METHODS ###

    @staticmethod
    def _parse_pages_string(pages_string):
        pattern = re.compile(r'(\d+)-(\d+)')
        page_selections = []
        for part in (_.strip() for _ in pages_string.split(',')):
            match = pattern.match(part)
            page_range = None
            if match is not None:
                start, stop = match.groups()
                start = int(start)
                stop = int(stop)
                if start == stop:
                    page_range = (start,)
                elif start < stop:
                    page_range = tuple(range(start, stop + 1))
                else:
                    page_range = tuple(range(start, stop - 1, -1))
            elif part.isdigit():
                page = int(part)
                page_range = (page,)
            else:
                continue
            if page_range:
                page_selections.extend(page_range)
        return tuple(page_selections)

    ### PUBLIC METHODS ###

    def run(self):
        r'''Executes the directive.
        '''
        from abjad.tools import abjadbooktools
        self.assert_has_content()
        code = u'\n'.join(self.content)
        literal = literal_block(code, code)
        literal.line = self.content_offset  # set the content line number
        block = abjadbooktools.abjad_input_block(code, literal)
        # Only set flags if true, for a thinner node repr.
        if 'allow-exceptions' in self.options:
            block['allow-exceptions'] = True
        if 'hide' in self.options:
            block['hide'] = True
        if 'no-resize' in self.options:
            block['no-resize'] = True
        if 'no-stylesheet' in self.options:
            block['no-stylesheet'] = True
        if 'no-trim' in self.options:
            block['no-trim'] = True
        if 'strip-prompt' in self.options:
            block['strip-prompt'] = True
        if 'with-thumbnail' in self.options:
            block['with-thumbnail'] = True
        pages = self.options.get('pages', None)
        if pages is not None:
            block['pages'] = self._parse_pages_string(pages)
        if 'reveal-label' in self.options:
            block['reveal-label'] = self.options.get('reveal-label')
        stylesheet = self.options.get('stylesheet', None)
        if block.get('no-stylesheet'):
            stylesheet = None
        if stylesheet:
            block['stylesheet'] = stylesheet
        text_width = self.options.get('text-width', None)
        if text_width is not None:
            block['text-width'] = text_width
        with_columns = self.options.get('with-columns', None)
        if with_columns is not None:
            block['with-columns'] = with_columns
        set_source_info(self, block)
        return [block]
