locals {
  cloud-run-name = "demo-api"
}

data "google_container_registry_image" "demo-api" {
  name    = var.image-name
  project = var.project
  tag     = var.image-version
  region  = var.image-region
}

resource "google_cloud_run_service" "demo-api" {

  provider = google-beta
  name     = local.cloud-run-name
  location = var.location
  project  = var.project
  template {
    spec {
      containers {
        image = data.google_container_registry_image.demo-api.image_url
      }
    }
    dynamic "env" {
        content {
            name  = PROJECT_ID
            value = var.project-id 
        }
    }
  }
}

resource "google_cloud_run_service_iam_member" "public" {
  count    = var.public ? 1 : 0
  location = var.location
  service  = google_cloud_run_service.demo-api.name

  member = "allUsers"
  role   = "roles/run.invoker"
}