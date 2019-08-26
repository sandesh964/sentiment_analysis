Feature: GCE Instances
  Validate Compute Instances created to see if the specifications match the terraform configurations.

  Scenario Outline: Validate Instances
    Given A list of instances
    When I create each <vm>
    Then it should have the specified <flavor>
    And  it should have a valid network network_ip and external_ip
    And  its os should be <operating_system>
    And  it should reside in <availability_zone>
    And  it should have a disk attached to it
    And  its metadata should match with specifications from terraform configurations

    Examples:
      | vm        | flavor             | availability_zone      | operating_system |
      | docker-01 | custom-8-16384-ext | ZZZZZZZZZZZZZZ         | centos-7         |

  Scenario: Validate GCE Instance
    Given A GCE instance
    When I create VM docker-01
    Then the spec should be custom-8-16384-ext
    And  it should have a valid network network_ip and external_ip
    And  its os should be centos-7
    And  it should reside in ZZZZZZZZZ
    And  it should have a disk attached to it
    And  its metadata should match with specifications from terraform configurations
