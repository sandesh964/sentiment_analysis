"""
This is wrapper class using invoke library to expose each of the python functions which will be used by CI
tool (Jenkins) as linux functions. This class hosts a list of utility functions to run tests,
build images and lint the code etc...
"""
import glob
import os

from invoke import task


@task
def setup(ctx):
    """
    Task to configure build environment
    :param ctx: context object
    :return: None
    """
    cmd = 'sudo pip install -r requirements.txt'
    ctx.run(cmd, hide=True, warn=True)


@task
def lint(ctx):
    """
    Task to perform linting. All ansible tasks, plays and roles are tested using yamllint
    :param ctx: context object
    :return: None
    """
    ctx.run('yamllint -c .yamllint *')
    ctx.run('cd plays && yamllint -c ../.yamllint *')
    ctx.run('cd roles && yamllint -c ../.yamllint *')
    # lint tests expressed in python using pylint
    ctx.run('pylint tests/*.py')


@task
def verify(ctx):
    """
    Run syntax-check for this playbook
    :param ctx: context object
    :return: None
    """
    os.chdir('plays/')
    playbooks = glob.glob('*.yml')
    for playbook in playbooks:
        ctx.run('ansible-playbook {0} --syntax-check -i ../tests/hosts.yml'.format(playbook))


@task
def play(ctx):
    """
    Run the playbook
    :param ctx: context object
    :return: None
    """
    os.chdir('plays/')
    playbooks = glob.glob('*.yml')
    for playbook in playbooks:
        ctx.run(
            "ansible-playbook {0} --extra-vars=\"ansible_ssh_username={1}\" --extra-vars=\"ansible_ssh_private_key_file={2}\"".format(
                playbook, os.environ['ANSIBLE_REMOTE_USER'], os.environ['ANSIBLE_PRIVATE_KEY_FILE']))


@task
def test(ctx):
    """
    Run the playbook
    :param ctx: context object
    :return: None
    """
    os.chdir('tests/')
    test_case_list = glob.glob('*.py')
    for test_case in test_case_list:
        ctx.run(
            "ANSIBLE_PRIVATE_KEY_FILE={0} ANSIBLE_REMOTE_USER={1} pytest {2} -s -v --gherkin-terminal-reporter-expanded".format(
                os.environ['ANSIBLE_PRIVATE_KEY_FILE'], os.environ['ANSIBLE_REMOTE_USER'], test_case))
