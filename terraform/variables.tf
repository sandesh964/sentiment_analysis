variable "region" {
  default = "YYYYYYYYY"
}

variable "zone" {
  default = "ZZZZZZZZZ"
}

variable "network_cidr" {
  default = "10.127.0.0/20"
}

variable "network_name" {
  default = "default"
}

variable "machine_type" {
  # Memory should be a multiple of 256MiB in zone australia-southeast1-b for custom machine type. So to create an instance
  # with 16GiB we specify multiple of 256MiB, which is approx 16384 MiB
  description = "In the form of custom-CPUS-MEM, number of CPUs and memory for custom machine. https://cloud.google.com/compute/docs/instances/creating-instance-with-custom-machine-type#specifications"
  default     = "custom-8-16384-ext"
}

variable "min_cpu_platform" {
  description = "Specifies a minimum CPU platform for the VM instance. Applicable values are the friendly names of CPU platforms, such as Intel Haswell or Intel Skylake. https://cloud.google.com/compute/docs/instances/specify-min-cpu-platform"
  default     = "Automatic"
}

variable "name" {
  description = "Name prefix for the nodes"
  default     = "docker-01"
}

variable "num_nodes" {
  description = "Number of nodes to create"
  default     = 1
}

variable "image_family" {
  default = "centos-7"
}

variable "image_project" {
  default = "centos-cloud"
}

variable "disk_auto_delete" {
  description = "Whether or not the disk should be auto-deleted."
  default     = true
}

variable "disk_type" {
  description = "The GCE disk type. Can be either pd-ssd, local-ssd, or pd-standard."
  default     = "pd-standard"
}

variable "disk_size_gb" {
  description = "The size of the image in gigabytes."
  default     = 30
}

variable "node_tags" {
  description = "Additional compute instance network tags for the nodes."
  type        = "list"
  default     = ["ssh", "containers", "centos7", "docker-host"]
}

variable "startup_script" {
  description = "Content of startup-script metadata passed to the instance template."
  default     = "hostname -f > /test.txt"
}

variable "metadata" {
  description = "Map of metadata values to pass to instances."
  type        = "map"
  default     = {}
}

variable "service_account_email" {
  description = "The email of the service account for the instance template."
  default     = ""
}

variable "service_account_scopes" {
  description = "List of scopes for the instance template service account"
  type        = "list"
  default     = [
    "https://www.googleapis.com/auth/compute",
    "https://www.googleapis.com/auth/devstorage.read_only",
    "https://www.googleapis.com/auth/logging.write",
    "https://www.googleapis.com/auth/monitoring.write",
    "https://www.googleapis.com/auth/servicecontrol",
    "https://www.googleapis.com/auth/service.management.readonly",
    "https://www.googleapis.com/auth/trace.append"
  ]
}

variable "project" {
  description = "The project ID"
  default = "XXXXXXXX"
}
