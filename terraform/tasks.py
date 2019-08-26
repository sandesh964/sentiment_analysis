"""
This is wrapper class using invoke library to expose each of the python functions which will be used by CI
tool (Jenkins) as linux functions. This class hosts a list of utility functions to run tests,
build images and lint the code
"""

from invoke import task


@task
def test_vm(ctx):
    """
    Task to test GCE instance
    :param ctx: context object
    :return: None
    """
    ctx.run('pytest -c pytest.ini tests/test_vm.py')


@task
def lint(ctx):
    """
    Task to perform linting.
    :param ctx: context object
    :return: None
    """
    code_dir = ['tests/*.py']
    for dir in code_dir:
        print ('Analyzing..{0}'.format(dir))
        ctx.run('pylint {0}'.format(dir))
