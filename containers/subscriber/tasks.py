"""
This is wrapper class using invoke library to expose each of the python functions which will be used by CI
tool (Jenkins) as linux functions. This class hosts a list of utility functions to run tests,
build images and lint the code
"""

from invoke import task


@task(help={'dockerfile': "Dockerfile path to build the image"})
def build_image(ctx, dockerfile, tag):
    """
    Task to build docker image
    :param ctx: context object
    :param dockerfile: Dockerfile path
    :return: None
    """
    ctx.run('docker build --rm -t {0} -f {1}/Dockerfile .'.format(tag, dockerfile))


@task
def test_subscriber_image(ctx):
    """
    Task to test dashboard docker container
    :param ctx: context object
    :return: None
    """
    ctx.run('pytest -c pytest.ini tests/test_subscriber_image.py')


@task
def lint(ctx):
    """
    Task to perform linting.
    :param ctx: context object
    :return: None
    """
    code_dir = ['tests/*.py', 'app/*.py']
    for dir in code_dir:
        print ('Analyzing..{0}'.format(dir))
        ctx.run('pylint {0}'.format(dir))


@task
def test_subscriber(ctx):
    """
    Task to validate subscriber functionality.
    :param ctx: context object
    :return: None
    """
    ctx.run('pytest -c pytest.ini tests/test_subscriber.py --cov app/')
