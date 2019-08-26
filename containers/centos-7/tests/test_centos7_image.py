"""
Test cases to validate centos7 base image configurations
"""

import subprocess

import pytest
import testinfra

DOCKER_IMAGE_NAME = 'python:latest'


# scope='session' uses the same container for all the tests;
# scope='function' uses a new container per test function.
@pytest.fixture(scope='session')
def host():
    """
    Pytest fixture to manage the lifecycle of a container of interest using the specified DOCKER_IMAGE_NAME
    :return: testinfra connection to the container
    """
    docker_id = subprocess.check_output(
        [
            'docker',
            'run',
            '-d',
            '-t',
            '-i',
            DOCKER_IMAGE_NAME,
            '/bin/bash'
        ]
    ).decode().strip()

    # return a testinfra connection to the container
    yield testinfra.get_host("docker://" + docker_id)
    # at the end of the test suite, destroy the container
    subprocess.check_call(['docker', 'rm', '-f', docker_id])


# Scenario: pip should be installed
def test_pip(host):
    """
    Test case to check if pip is installed
    :param host: reference to pytest.fixture - 'host'
    :return: None
    """
    pip = host.file('/usr/lib/python2.7/site-packages/pip')
    assert pip.exists


# Scenario: Check Timezone
def test_tz(host):
    """
    Test case to check if the time zone is AEST
    :param host: reference to pytest.fixture - 'host'
    :return: None
    """
    actual_output = host.run('date +"%Z %z"').stdout
    assert 'AEST' in actual_output


# Scenario: Check if all the yum packages in Dockerfile are installed
def test_yum_packages(host):
    """
    Test case to check if all the required yum packages are installed
    :param host: reference to pytest.fixture - 'host'
    :return:
    """
    # yum install python-pip installs pip based on the python version, since python2 is default in centos, checking
    # for python2-pip instead of python-pip
    for pkg in ['python-devel', 'python2-pip', 'epel-release']:
        assert host.package(pkg).is_installed
