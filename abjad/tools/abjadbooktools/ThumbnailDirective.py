from docutils.parsers.rst import Directive  # type: ignore
from docutils.parsers.rst import directives  # type: ignore


class ThumbnailDirective(Directive):
    r'''A thumbnail directive.
    '''

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Sphinx Internals'

    final_argument_whitespace = True
    has_content = False
    option_spec = {
        'class': directives.class_option,
        'group': directives.unchanged,
        'title': directives.unchanged,
        }
    optional_arguments = 0
    required_arguments = 1

    ### PUBLIC METHODS ###

    def run(self):
        r'''Executes the directive.
        '''
        from abjad.tools import abjadbooktools
        node = abjadbooktools.abjad_thumbnail_block()
        node['classes'] += self.options.get('class', '')
        node['group'] = self.options.get('group', '')
        node['title'] = self.options.get('title', '')
        node['uri'] = self.arguments[0]
        environment = self.state.document.settings.env
        environment.images.add_file('', node['uri'])
        return [node]
