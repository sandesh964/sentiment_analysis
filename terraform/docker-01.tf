provider "google" {
  region = "${var.region}"
  credentials = "${file("../credentials/anz-challenge.json")}"
}

data "google_project" "current" {
    project_id = "${var.project}"
}

data "google_compute_default_service_account" "default" {
    project = "${var.project}"
}


resource "google_compute_instance" "default" {
  project                   = "${var.project}"
  count                     = "${var.num_nodes}"
  name                      = "${var.name}"
  zone                      = "${var.zone}"
  tags                      = "${var.node_tags}"
  machine_type              = "${var.machine_type}"
  min_cpu_platform          = "${var.min_cpu_platform}"
  allow_stopping_for_update = true

  boot_disk {
    auto_delete = "${var.disk_auto_delete}"

    initialize_params {
      image = "${var.image_project}/${var.image_family}"
      size  = "${var.disk_size_gb}"
      type  = "${var.disk_type}"
    }
  }

  metadata = "${merge(
    map("startup-script", "${var.startup_script}"), var.metadata
  )}"

  service_account {
    email  = "${var.service_account_email == "" ? data.google_compute_default_service_account.default.email : var.service_account_email }"
    scopes = "${var.service_account_scopes}"
  }

  network_interface{
      network = "${var.network_name}"
  }
}

resource "google_compute_firewall" "ssh" {
  project = "${var.project}"
  name    = "allow-${var.name}-ssh"
  network = "${var.network_name}"

  allow {
    protocol = "tcp"
    ports    = ["22"]
  }

  target_tags = ["${var.name}-ssh"]
}

resource "google_compute_firewall" "http" {
  project = "${var.project}"
  name    = "allow-${var.name}-web"
  network = "${var.network_name}"

  allow {
    protocol = "tcp"
    ports    = ["80","443","8080","8443"]
  }

  target_tags = ["${var.name}-https", "${var.name}-http"]
}

resource "google_compute_firewall" "icmp" {
  project = "${var.project}"
  name    = "allow-${var.name}-icmp"
  network = "${var.network_name}"

  allow {
    protocol = "icmp"
  }

  target_tags = ["${var.name}-icmp"]
  
}
