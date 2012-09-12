from experimental.interpretertools.DivisionCommand import DivisionCommand


class RegionDivisionCommand(DivisionCommand):
    r'''.. versionadded:: 1.0

    Command indicating durated period of time over which a division payload will apply.

    How do region division commands and (unqualified) division commands differ?

    Region division commands represent a more refined product of interpretation.

    (Unqualified) division commands may or may not glue together to create region division commands. 

    Region division commands never glue together.

    Region division commands represent an absolute command to create divisions over a given duration.
    '''

    pass
