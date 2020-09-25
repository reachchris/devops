variable "project" {
  description = "Project name"
}
variable "project-id" {
  description = "Project ID"
}
variable "region" {
  description = "Geographic region this project will run in"
}
variable "zone" {
  description = "Zone within the region this project will run in"
}
variable "service-accounts" {
  description = "A list of accounts that will be allowed to invoke the service"
  default     = {}
}
variable "image-version" {
  description = "The container version, maps to a tag in GCR"
}
variable "image-region" {
  description = "Region where the container image is found"
  default     = "eu"
}
variable "public" {
  description = "To make endpoint public set to true"
  default     = false
}
variable "image-name" {
  description = "Name of the service, maps to a GCR container"
}
variable "location" {
  description = "The location where the service is to be deployed"
}