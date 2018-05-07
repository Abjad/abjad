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
        import abjad.book
        import abjad.cli
        classes = []
        for name in sorted(dir(abjad.cli)):
            obj = getattr(abjad.cli, name)
            if not isinstance(obj, type):
                continue
            elif not issubclass(obj, CLI):
                continue
            elif issubclass(obj, type(self)):
                continue
            elif inspect.isabstract(obj):
                continue
            classes.append(obj)
        classes.append(abjad.book.AbjadBookScript)
        classes.sort(key=lambda x: x.__name__)
        return classes
