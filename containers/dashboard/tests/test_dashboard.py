"""
Test cases to validate dashboard base image configurations
"""

import subprocess

import pytest
import requests
import testinfra

DOCKER_IMAGE_NAME = 'dashboard:latest'


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
            '-p'
            '3527:3527',
            '-d',
            DOCKER_IMAGE_NAME,
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
    expected_python_pkg = ['requests', 'Flask']
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
    application_directory = host.file('/dashboard/')
    assert application_directory.exists

    # TEST: CODE ARTIFACTS ARE COPIED TO THE WORKDIR
    work_dir_contents = host.run('ls -R /dashboard/').stdout
    print work_dir_contents
    expected_work_dir_contents = ['static', 'templates', 'requirements.txt', 'app.py', 'Chart.js', 'chart.html']
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
    assert str(python_path).strip() == '/dashboard'


# Scenario: Check if Dashboard is Running
def test_webapp(host):
    """
    Test case to verify if the PYTHONPATH env variable is set
    :param host: pytest.fixture to access the docker container of our interest
    :return:
    """
    # TEST: Check if port 3527 is open and up for listening any requests
    # host.run('yum install -y net-tools')
    # netstat_op = host.run('netstat -anlp | grep 3527').stdout
    # assert 'tcp        0      0 0.0.0.0:3527            0.0.0.0:*               LISTEN' in netstat_op

    # TEST: Check if the application is running - Verify the page title & request is successful
    curl_op = host.run('curl -vs http://0.0.0.0:3527').stdout
    assert '<title>Sentiment Analysis Summary</title>' in curl_op
    response = requests.get('http://0.0.0.0:3527')
    assert response.status_code == 200
