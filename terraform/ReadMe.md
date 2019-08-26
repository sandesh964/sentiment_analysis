# INSTANCE CREATION ON GCE

- Install Terraform and copy the binary to `/usr/local/bin`.

- Verify Installation using the following command

```bash
$ terraform --version
Terraform v0.12.6
```

- Enable the   `Google Compute Engine API`,  `Cloud Resource Manager API`, `Identity & Access Management API`

```bash
gcloud services enable compute.googleapis.com
gcloud services enable cloudresourcemanager.googleapis.com
gcloud services enable iam.googleapis.com
gcloud services enable iamcredentials.googleapis.com
```

- Run Terraform init to initialize the configs.

```bash
$ terraform init

Initializing the backend...

Initializing provider plugins...

* provider.google: version = "~> 2.12"

Terraform has been successfully initialized!
```

- Run Terraform Validate to verify syntax and semantics of the terraform configurations

```bash
$ terraform validate
Success! The configuration is valid.
```

- Run Terraform Plan to see the changes required for the proposed instance.

```bash
$ terraform plan
Refreshing Terraform state in-memory prior to plan...
The refreshed state will be used to calculate this plan, but will not be
persisted to local or remote state storage.

data.google_compute_default_service_account.default: Refreshing state...
data.google_project.current: Refreshing state...

------------------------------------------------------------------------

An execution plan has been generated and is shown below.
Resource actions are indicated with the following symbols:
  + create

Terraform will perform the following actions:

  # google_compute_firewall.http will be created
  + resource "google_compute_firewall" "http" {
      + creation_timestamp = (known after apply)
      + destination_ranges = (known after apply)
      + direction          = (known after apply)
      + id                 = (known after apply)
      + name               = "docker-01-ssh"
      + network            = "docker-01-nw"
      + priority           = 1000
      + project            = (known after apply)
      + self_link          = (known after apply)
      + source_ranges      = (known after apply)
      + target_tags        = [
          + "docker-01-http(s)",
        ]

      + allow {
          + ports    = [
              + "80",
              + "443",
              + "8080",
              + "8443",
            ]
          + protocol = "tcp"
        }
    }

  # google_compute_firewall.ssh will be created
  + resource "google_compute_firewall" "ssh" {
      + creation_timestamp = (known after apply)
      + destination_ranges = (known after apply)
      + direction          = (known after apply)
      + id                 = (known after apply)
      + name               = "docker-01-ssh"
      + network            = "docker-01-nw"
      + priority           = 1000
      + project            = (known after apply)
      + self_link          = (known after apply)
      + source_ranges      = (known after apply)
      + target_tags        = [
          + "docker-01-ssh",
        ]

      + allow {
          + ports    = [
              + "22",
            ]
          + protocol = "tcp"
        }
    }

  # google_compute_instance.default[0] will be created
  + resource "google_compute_instance" "default" {
      + allow_stopping_for_update = true
      + can_ip_forward            = false
      + cpu_platform              = (known after apply)
      + deletion_protection       = false
      + guest_accelerator         = (known after apply)
      + id                        = (known after apply)
      + instance_id               = (known after apply)
      + label_fingerprint         = (known after apply)
      + machine_type              = "custom-8-16384-ext"
      + metadata                  = {
          + "startup-script" = "hostname -f > /test.txt"
        }
      + metadata_fingerprint      = (known after apply)
      + min_cpu_platform          = "Automatic"
      + name                      = "docker-01"
      + project                   = (known after apply)
      + self_link                 = (known after apply)
      + tags                      = [
          + "centos7",
          + "containers",
          + "docker-host",
          + "ssh",
        ]
      + tags_fingerprint          = (known after apply)
      + zone                      = "ZZZZZZZZZ"

      + boot_disk {
          + auto_delete                = true
          + device_name                = (known after apply)
          + disk_encryption_key_sha256 = (known after apply)
          + kms_key_self_link          = (known after apply)
          + source                     = (known after apply)

          + initialize_params {
              + image  = "centos-cloud/centos-7"
              + labels = (known after apply)
              + size   = 30
              + type   = "pd-standard"
            }
        }

      + network_interface {
          + address            = (known after apply)
          + name               = (known after apply)
          + network            = "docker-01-nw"
          + network_ip         = (known after apply)
          + subnetwork         = (known after apply)
          + subnetwork_project = (known after apply)
        }

      + scheduling {
          + automatic_restart   = (known after apply)
          + on_host_maintenance = (known after apply)
          + preemptible         = (known after apply)

          + node_affinities {
              + key      = (known after apply)
              + operator = (known after apply)
              + values   = (known after apply)
            }
        }

      + service_account {
          + email  = "XXXX-compute@developer.gserviceaccount.com"
          + scopes = [
              + "https://www.googleapis.com/auth/compute",
              + "https://www.googleapis.com/auth/devstorage.read_only",
              + "https://www.googleapis.com/auth/logging.write",
              + "https://www.googleapis.com/auth/monitoring.write",
              + "https://www.googleapis.com/auth/service.management.readonly",
              + "https://www.googleapis.com/auth/servicecontrol",
              + "https://www.googleapis.com/auth/trace.append",
            ]
        }
    }

  # google_compute_network.default will be created
  + resource "google_compute_network" "default" {
      + auto_create_subnetworks         = false
      + delete_default_routes_on_create = false
      + gateway_ipv4                    = (known after apply)
      + id                              = (known after apply)
      + name                            = "docker-01-nw"
      + project                         = "XXXX"
      + routing_mode                    = (known after apply)
      + self_link                       = (known after apply)
    }

Plan: 4 to add, 0 to change, 0 to destroy.

------------------------------------------------------------------------
```

- Run Terraform Apply to create the instance as per the configuration.

```bash
Do you want to perform these actions?
  Terraform will perform the actions described above.
  Only 'yes' will be accepted to approve.

  Enter a value: yes

google_compute_firewall.http: Creating...
google_compute_firewall.icmp: Creating...
google_compute_firewall.ssh: Creating...
google_compute_instance.default[0]: Modifying... [id=docker-01]
google_compute_firewall.icmp: Still creating... [10s elapsed]
google_compute_firewall.ssh: Still creating... [10s elapsed]
google_compute_firewall.http: Still creating... [10s elapsed]
google_compute_instance.default[0]: Still modifying... [id=docker-01, 10s elapsed]
google_compute_firewall.icmp: Creation complete after 18s [id=allow-docker-01-icmp]
google_compute_firewall.ssh: Creation complete after 18s [id=allow-docker-01-ssh]
google_compute_firewall.http: Creation complete after 18s [id=allow-docker-01-web]
google_compute_instance.default[0]: Still modifying... [id=docker-01, 20s elapsed]
google_compute_instance.default[0]: Still modifying... [id=docker-01, 30s elapsed]
google_compute_instance.default[0]: Still modifying... [id=docker-01, 40s elapsed]
google_compute_instance.default[0]: Modifications complete after 47s [id=docker-01]
```

- Verify the instance and firewall rules from the console
![Image](screenshots/vm_instances.png?raw=true)
![Image](screenshots/firewall_rules.png?raw=true)

- Logon to the VM instance using gcloud or other options available:

```bash
gcloud beta compute --project <project-name> ssh --zone <zone-name> <username>@<hostname>
```

## Running Automated Tests

The tests specified for instance creation uses `pytest_bdd` and `pytest` packages. The test scenario is experssed in `Gherkin` langugage.

- All the test configs are specified in `pytest.ini`, this file needs to be updated with the relevant settings so that tests can access the right credentials file to access the project to test the instance.

```Gherkin
Scenario: Validate GCE Instance
    Given A GCE instance
    When I create VM docker-01
    Then the spec should be custom-8-16384-ext
    And  it should have a valid network network_ip and external_ip
    And  its os should be centos-7
    And  it should reside in ZZZZZZ
    And  it should have a disk attached to it
    And  its metadata should match with specifications from terraform configurations
```

**TBD:** The above mentioned scenario can be replaced with `Scenario Outline`, so that the test can be iteratively executed on any number of instances using the `Examples` dictionary as an input to the test.

```Gherkin
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
    | docker-01 | custom-8-16384-ext | ZZZZZZZ                | centos-7         |
```

- To execute the tests, run the following command:

```bash
pytest -c pytest.ini terraform/tests/ --cov terraform/
```

![Image](screenshots/test_execution.png?raw=true)

- The tests use `pytest-cov` plugin to print the coverage report.

```bash
---------- coverage: platform darwin, python 2.7.10-final-0 ----------
Name         Stmts   Miss  Cover
--------------------------------
test_vm.py      48      1    98%

```

# CI PIPELINE
The project is enabled with gitlab-ci pipeline and below is the pipeline summary and description:
![Alt](screenshots/ci-pipeline.png?raw=true)

![Alt](screenshots/ci-pipeline-expanded.png?raw=true)