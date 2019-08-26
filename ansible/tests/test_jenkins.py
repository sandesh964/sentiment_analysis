"""
Test Case to verify jenkins installation:
1. Jenkins is installed
2. Java are installed
3. Jenkins service is Up and Running
"""

import os

import requests
import testinfra.utils.ansible_runner

# Set host for this test
TEST_INFRA_HOSTS = testinfra.utils.ansible_runner.AnsibleRunner(os.path.abspath('..') + os.sep + 'hosts'). \
    get_hosts('jenkins-master')


# Scenario: Check if all the yum packages specified in jenkins role are installed
def test_yum_packages(host):
    """
    Test case to check if all the required yum packages are installed i.e., jdl
    :param host: reference to pytest.fixture - 'host'
    :return: None
    """
    with host.sudo():
        assert host.package('java-1.8.0-openjdk.x86_64').is_installed


# scenario: Jenkins should be installed
def test_jenkins_installation(host):
    """
    Test case to check if jenkins is installed
    :param host: reference to pytest.fixture - 'host'
    :return: None
    """
    assert host.package('jenkins').is_installed


# scenario: Jenkins should be a systemd service, should be enabled and running
def test_jenkins_service(host):
    """
    Test case to check if jenkins is running and enabled
    :param host: reference to pytest.fixture - 'host'
    :return: None
    """
    jenkins_svc = host.service('jenkins')
    assert jenkins_svc.is_running
    assert jenkins_svc.is_enabled


# scenario: Jenkins user should exist
def test_jenkins_user(host):
    """
    Test case to check if jenkins user exists and the home directory is owned by jenkins
    :param host: reference to pytest.fixture - 'host'
    :return: None
    """
    jenkins_user = host.user('jenkins')
    assert jenkins_user.exists
    assert jenkins_user.name == 'jenkins'
    assert jenkins_user.group == 'jenkins'
    assert jenkins_user.shell == "/bin/false"
    assert jenkins_user.home == "/var/lib/jenkins"


# Scenario: Jenkins group should exist
def test_jenkins_group(host):
    """
    Test case to check if jenkins group exists
    :param host: reference to pytest.fixture - 'host'
    :return: None
    """
    assert host.group("jenkins").exists


# Scenario: Jenkins should not allow no
def test_jenkins_access_anonymous():
    """
    Test case to access jenkins UI as anonymous user
    :return: None
    """
    response = requests.get('http://localhost:8080')
    assert response.status_code == 403
    assert 'Authentication required' in response.text
