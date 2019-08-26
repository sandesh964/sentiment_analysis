"""
# TBD: Implement Scenario Outline with Examples so that the test can be iteratively run rather than defining
#  the scenario for each instance
"""

import os

from googleapiclient import _auth, discovery
from pytest_bdd import scenario, given, when, then, parsers


# @scenario('vm.feature',
#          'Validate Instances',
#          example_converters=dict(vm=str, flavor=str, availability_zone=str, operating_system=str))

@scenario('features/vm.feature', 'Validate GCE Instance')
def test_validate():
    """
    Validate GCE functional test
    :return:
    """
    pass


VIRTUAL_MACHINE_DEF = None

# Build and Initialize the API
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = '{0}/{1}'.format(os.environ['PWD'],
                                                                '/credentials/anz-challenge.json')
COMPUTE = discovery.build('compute', 'v1', credentials=_auth.default_credentials())


def get_instance_specs(project, zone):
    """
    Fetch the GCE instance specifications
    :param project: GCP project name
    :param zone: GCP availability zone
    :return: list of instances from the specified project and zone
    """
    result = COMPUTE.instances().list(project=project, zone=zone).execute()
    return result['items'] if 'items' in result else None


def isgoodipv4(ip_addr):
    """
    Method to check if the give ip address is a valid ipv4
    :param ip_addr: ipv4 address
    :return: Boolean
    """
    pieces = ip_addr.split('.')
    if len(pieces) != 4:
        return False
    try:
        return all(0 <= int(p) < 256 for p in pieces)
    except ValueError:
        return False


# @given('A list of instances')
# def list_instances():
#    pass
@given('A GCE instance')
def gce_instance():
    """
    Place holder to add any validation tests for the GIVEN spec
    :return: None
    """
    pass


# @when('I create each <vm>')
@when(parsers.parse('I create VM {vm_name}'))
def virtual_machine(vm_name):
    """
    Test case to validate the VM name
    :param vm_name: Host name of the GCE instance
    :return: None
    """
    global VIRTUAL_MACHINE_DEF
    VIRTUAL_MACHINE_DEF = get_instance_specs(project=os.environ['PROJECT'], zone=os.environ['ZONE'])[0]
    # print 'virtual_machine_def is:', virtual_machine_def
    # TEST: Verify Hostname
    assert vm_name == VIRTUAL_MACHINE_DEF['name']


# @then('it should have the specified <flavor>')
# def test_flavor(flavor):
@then('the spec should be custom-8-16384-ext')
def test_flavor():
    """
    Test the GCE instance flavor/spec
    Verify Flavour - 8 vcpu - 16 GiB/ custom-8-16384-ext - Flavour name specified in Terraform configuration
    :return: None
    """
    # assert flavor in virtual_machine_def['machineType']
    assert 'custom-8-16384-ext' in VIRTUAL_MACHINE_DEF['machineType']


@then('it should have a valid network network_ip and external_ip')
def test_nw_configs():
    """
    Verify the attached network interface, default network and an external IP assigned
    :return: None
    """
    nw_interface = VIRTUAL_MACHINE_DEF['networkInterfaces'][0]
    assert 'default' in nw_interface['network']
    access_configs = nw_interface['accessConfigs'][0]
    assert isgoodipv4(access_configs['natIP'])
    assert access_configs['name'] == 'External NAT'
    assert access_configs['networkTier'] == 'PREMIUM'
    assert isgoodipv4(nw_interface['networkIP'])
    assert 'default' in nw_interface['subnetwork']


# @then('it should reside in <availability_zone>')
# def test_compute_zone(availability_zone):
@then('it should reside in australia-southeast1-b')
def test_compute_zone():
    """
    Verify if the instance is created in the correct zone as specified in the terraform configuration
    :return: None
    """
    # assert availability_zone in virtual_machine_def['zone']
    assert 'ZZZZZZZZZZ' in VIRTUAL_MACHINE_DEF['zone']


# @then('its os should be <operating_system>')
# def test_os(operating_system):
@then('its os should be centos-7')
def test_os():
    """
    Verify the OS Flavour
    :return: None
    """
    # assert operating_system in virtual_machine_def['disks'][0]['licenses'][0]
    assert 'centos-7' in VIRTUAL_MACHINE_DEF['disks'][0]['licenses'][0]


@then('it should have a disk attached to it')
def test_attached_disk():
    """
    Verify the attached disk
    :return: None
    """
    disk = VIRTUAL_MACHINE_DEF['disks'][0]
    assert disk['kind'] == 'compute#attachedDisk'
    assert disk['autoDelete']
    assert disk['type'] == 'PERSISTENT'
    assert disk['mode'] == 'READ_WRITE'


@then('its metadata should match with specifications from terraform configurations')
def test_metadata():
    """
    Verify Instance Metadata - check the contents of start-up script specified in the terraform configs
    :return: None
    """
    metadata = VIRTUAL_MACHINE_DEF['metadata']['items'][0]
    assert metadata['value'] == 'hostname -f > /test.txt'
    assert metadata['key'] == 'startup-script'
