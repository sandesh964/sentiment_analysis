"""
Test Case for checking the node, ensures the following:
1. All the Pre-requisites are installed
2. Docker, PIP and Java are installed
3. Docker service is Up and Running
"""

import os
import testinfra.utils.ansible_runner

# Set host for this test
TEST_INFRA_HOSTS = testinfra.utils.ansible_runner.AnsibleRunner(os.path.abspath('..') + os.sep + 'hosts').\
    get_hosts('docker-host')


# Scenario: Check if all the old versions of docker and its dependencies are removed
def test_old_yum_packages(host):
    """
    Test case to check if all the old versions of docker and its dependencies are removed
    :param host: reference to pytest.fixture - 'host'
    :return:
    """
    with host.sudo():
        for pkg in ['docker', 'docker-client', 'docker-client-latest', 'docker-common', 'docker-latest',
                    'docker-latest-logrotate', 'docker-logrotate', 'docker-engine']:
            assert not host.package(pkg).is_installed


# Scenario: Check if all the yum packages specified in node-setup role are installed
def test_yum_packages(host):
    """
    Test case to check if all the required yum packages are installed
    :param host: reference to pytest.fixture - 'host'
    :return:
    """
    # yum install python-pip installs pip based on the python version, since python2 is default in centos, checking
    # for python2-pip instead of python-pip
    with host.sudo():
        for pkg in ['python-devel', 'python2-pip', 'epel-release', 'java-1.8.0-openjdk.x86_64', 'yum-utils',
                    'device-mapper-persistent-data', 'lvm2', 'docker-ce', 'docker-ce-cli', 'containerd.io']:
            assert host.package(pkg).is_installed


# Scenario: Check the status of docker-ce service
def test_docker_service(host):
    """
    Test to verify docker service
    :param host: reference to pytest.fixture - 'host'
    """
    with host.sudo():
        docker_svc = host.service('docker')
        assert docker_svc.is_enabled
        assert docker_svc.is_running
