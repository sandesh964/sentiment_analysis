# Ansible Playbooks

Playbooks to configure the hosts managing the application code components.


Requirements
------------
* Ansible should be installed on the nodes.
* Yamllint and pylint packages are installed and ready to use.


Variables
--------------
- Docker and Jenkins stable Repos are maintained by  ```docker_ce_repo```  and ```jenkins_repo`` variable.

Dependencies
------------
None

Playbooks
----------------
 *JENKINS :*
 - Installs and configures jenkins with basic security. Jenkins service will be 
   available on http://<jenkins-host-name>:8080/
 
 *TBD:*
 - LDAP Integration
 - Auto registration with master
 
 *DOCKER HOST :*
 - Installs and configures docker-ce
 - Installs Pip and default JDK as well for use by the application
 
 *RUNNING PLAYBOOKS:*
 - Set the Environment variables ``ANSIBLE_REMOTE_USER`` & ``ANSIBLE_PRIVATE_KEY_FILE``
 - Run the following command:
 
```bash
invoke play
 ``` 
 
Testing
------
 - Set the Environment variables ``ANSIBLE_REMOTE_USER`` & ``ANSIBLE_PRIVATE_KEY_FILE``
 - Run the following command:
 
```bash
invoke test
 ``` 

License
-------

Author Information
------------------
Name: Amar Sandesh Bachu
Email: sandesh964@yahoo.com