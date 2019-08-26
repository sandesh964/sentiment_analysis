"""
Test cases to validate app base image configurations
"""
import subprocess

import pytest
import testinfra

DOCKER_IMAGE_NAME = 'publisher:latest'


# scope='session' uses the same container for all the tests;
# scope='function' uses a new container per test function.
@pytest.fixture(scope='session')
def host():
    """
    Pytest fixture to manage the lifecycle of a container of interest using the specified DOCKER_IMAGE_NAME
    :return: testinfra connection to the container
    """
    # run a container
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


# Scenario: Check if all the python packages are installed
def test_pip_packages(host):
    """
    Test case to check if all the python packages are installed as per requirements.txt
    :param host: pytest.fixture to access the docker container of our interest
    :return:
    """
    expected_python_pkg = ['google-api-python-client', 'tweepy',
                           'configparser', 'google-cloud-pubsub', 'python-dateutil']
    installed_python_pkg = (host.pip_package.get_packages()).keys()
    print installed_python_pkg
    for expected_pkg in expected_python_pkg:
        assert expected_pkg in installed_python_pkg


# Scenario: Check if the application files are copied to the docker
def test_application_artifacts(host):
    """
    Test case to verify if all the application files are copied to the image
    :param host: pytest.fixture to access the docker container of our interest
    :return:
    """
    # TEST: CHECK IF THE WORKDIR EXISTS
    application_directory = host.file('/publisher/')
    assert application_directory.exists

    # TEST: CHECK IF THE CREDENTIALS DIRECTORY EXISTS and is not empty
    credentials_directory = host.file('/publisher/credentials')
    assert credentials_directory.exists
    crendentials_dir_contents = host.run('ls /publisher/credentials').stdout
    assert crendentials_dir_contents

    # TEST: CODE ARTIFACTS ARE COPIED TO THE WORKDIR
    work_dir_contents = host.run('ls /publisher/').stdout
    expected_work_dir_contents = ['__init__.py', 'app.conf', 'requirements.txt', 'tweet_publisher.py']
    for artifact in expected_work_dir_contents:
        assert artifact in work_dir_contents


# Scenario: Check if PYTHONPATH is set in the container
def test_env_var(host):
    """
    Test case to verify if the PYTHONPATH env variable is set
    :param host: pytest.fixture to access the docker container of our interest
    :return:
    """
    python_path = host.run('echo $PYTHONPATH').stdout
    assert str(python_path).strip() == '/publisher'
