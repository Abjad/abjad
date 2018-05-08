import inspect
from uqbar.cli import CLI, CLIAggregator


class AbjDevScript(CLIAggregator):
    '''
    Entry-point to the Abjad developer scripts catalog.

    Can be accessed on the commandline via `abj-dev` or `ajv`:

    ..  shell::

        ajv --help

    `ajv` supports subcommands similar to `svn`:

    ..  shell::

        ajv api --help

    '''

    ### CLASS VARIABLES ###

    config_name = '.abjadrc'
    short_description = 'Entry-point to Abjad developer scripts catalog.'

    ### SPECIAL METHODS ###

    @property
    def cli_classes(self):
        """
        Lists CLI classes for aggregation.
        """
        def scan_module(module):
            classes = []
            for name in dir(module):
                obj = getattr(module, name)
                if not isinstance(obj, type):
                    continue
                elif not issubclass(obj, CLI):
                    continue
                elif issubclass(obj, type(self)):
                    continue
                elif inspect.isabstract(obj):
                    continue
                classes.append(obj)
            return classes
        import abjad.cli
        classes = scan_module(abjad.cli)
        # TODO: Remove this once abjad.book is externalized as abjadext.book:
        try:
            import abjad.book
            classes.append(abjad.book.AbjadBookScript)
        except ImportError:
            pass
        try:
            import abjadext.book
            classes.extend(scan_module(abjadext.book))
        except ImportError:
            pass
        try:
            import abjadext.cli
            classes.extend(scan_module(abjadext.cli))
        except ImportError:
            pass
        classes.sort(key=lambda x: x.__name__)
        return classes
