provider "google" {
  version = "3.5.0"

  credentials = file("your-project-file-from-gcp.json")

  project = "gcp-project-name"
  region = var.region
  zone = var.zone
}

resource "google_compute_network" "vpc_network" {
  name = "terraform-vpc-network"
  project = "gcp-project-name"
}

resource "google_compute_instance" "vm_instance" {
  count = 3
  name = "t-test${count.index}"
  machine_type = "e2-highcpu-2"
  metadata_startup_script = file("startup.sh")
  metadata = {
    ssh-keys = var.ssh_key
}
  tags = ["web"]
  zone = var.zone
  boot_disk {
    initialize_params {
      image = "ubuntu-1804-bionic-v20200317"
    }
  }

  network_interface {
    network = google_compute_network.vpc_network.name
    access_config {
    }
  }
}

resource "google_compute_firewall" "default" {
  name    = "test-firewall"
  network = google_compute_network.vpc_network.name

  allow {
    protocol = "icmp"
  }

  allow {
    protocol = "tcp"
    ports    = ["22", "80", "443", "8080", "1000-2000"]
  }

  source_tags = ["web"]
  source_ranges = ["0.0.0.0/0"]
}
