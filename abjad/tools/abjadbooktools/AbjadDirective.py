# -*- encoding: utf-8 -*-
import re
from docutils.parsers.rst import directives
from sphinx.util.compat import Directive
from sphinx.util.nodes import set_source_info
from docutils.nodes import literal_block


class AbjadDirective(Directive):
    r'''An abjad-book interpreter directive.

    Represents a portion of an interactive session.

    Generates a `abjad_input_block` node.
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
        'no-trim': directives.flag,
        'no-stylesheet': directives.flag,
        'pages': str,
        'strip-prompt': directives.flag,
        'stylesheet': str,
        'text-width': int,
        'with-columns': int,
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
        block['allow-exceptions'] = 'allow-exceptions' in self.options or None
        block['hide'] = 'hide' in self.options or None
        pages = self.options.get('pages', None)
        if pages is not None:
            block['pages'] = self._parse_pages_string(pages)
        else:
            block['pages'] = None
        block['no-trim'] = 'no-trim' in self.options or None
        block['no-stylesheet'] = 'no-stylesheet' in self.options or None
        block['stylesheet'] = self.options.get('stylesheet', None)
        if block['no-stylesheet']:
            block['stylesheet'] = None
        block['strip-prompt'] = 'strip-prompt' in self.options or None
        block['text-width'] = self.options.get('text-width', None)
        block['with-columns'] = self.options.get('with-columns', None)
        set_source_info(self, block)
        return [block]