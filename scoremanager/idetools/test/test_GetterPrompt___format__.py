# -*- encoding: utf-8 -*-
from abjad import *
import scoremanager


def test_GetterPrompt___format___01():

    session = scoremanager.idetools.Session()
    getter = scoremanager.idetools.Getter(session=session)
    getter.append_string('value')
    prompt = getter.prompts[0]
    prompt_format = format(prompt)
    index = prompt_format.find('validation_function')
    modified_format = prompt_format[:index]
    modified_format = modified_format + ')'

    assert systemtools.TestManager.compare(
        modified_format,
        r'''
        idetools.Prompt(
            disallow_range=False,
            help_template='value must be string.',
            help_template_arguments=[],
            include_chevron=True,
            message='value',
            setup_statements=[],
            )
        '''
        )