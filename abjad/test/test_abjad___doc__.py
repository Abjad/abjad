import abjad
import inspect
import pytest


ignored_names = (
    '__dict__',
    '__init__',
    '__new__',
    '__weakref__',
    'lilypond_type',
    'denominator',
    'duration',
    'multiplier',
    'music',
    'numerator',
    'optional_id',
    'optional_context_mod',
    'push_signature',
    'type',
    'value',
    )

ignored_classes = (
    abjad.parser.LilyPondLexicalDefinition,
    abjad.parser.LilyPondSyntacticalDefinition,
    abjad.parser.ReducedLyParser,
    abjad.parser.SchemeParser,
    abjad.rhythmtree.RhythmTreeParser,
    abjad.StorageFormatManager,
    abjad.FormatSpecification,
    )

classes = abjad.documentationtools.list_all_abjad_classes(
    ignored_classes=ignored_classes,
    )

@pytest.mark.parametrize('class_', classes)
def test_abjad___doc___01(class_):
    """
    All classes have a docstring. All class methods have a docstring.
    """
    missing_doc_names = []
    if class_.__doc__ is None:
        missing_doc_names.append(class_.__name__)
    for attribute in inspect.classify_class_attrs(class_):
        if attribute.name in ignored_names:
            continue
        elif attribute.defining_class is not class_:
            continue
        if attribute.name[0].isalpha() or attribute.name.startswith('__'):
            if getattr(class_, attribute.name).__doc__ is None:
                missing_doc_names.append(attribute.name)
    if missing_doc_names:
        names = [class_.__name__ + '.' + _ for _ in missing_doc_names]
        names = ', '.join(names)
        message = 'Missing docstrings for: {}'
        message = message.format(names)
        raise Exception(message)


functions = abjad.documentationtools.list_all_abjad_functions()
if functions:
    @pytest.mark.parametrize('function', functions)
    def test_abjad___doc___02(function):
        """
        All old functions had a docstring.
        """
        assert function.__doc__ is not None
