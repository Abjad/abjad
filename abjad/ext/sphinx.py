from docutils.parsers.rst import Directive  # type: ignore


class HiddenDoctestDirective(Directive):
    """
    An hidden doctest directive.

    Contributes no formatting to documents built by Sphinx.
    """

    ### CLASS VARIABLES ###

    has_content = True
    required_arguments = 0
    optional_arguments = 0
    final_argument_whitespace = True
    option_spec = {}

    ### PUBLIC METHODS ###

    def run(self):
        """Executes the directive.
        """
        self.assert_has_content()
        return []


def setup(app):
    app.add_directive("docs", HiddenDoctestDirective)
