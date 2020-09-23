provider "google" {
  project = var.project
  region  = var.region
  zone    = "${var.region}-${var.zone}"
}

terraform {
  required_version = ">= 0.13"
  backend "gcs" {
    bucket  = "deployer-demo"
    prefix    = "terraform-state/terraform.tfstate"
  }
}
