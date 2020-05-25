variable "project" {
  default = "kuldip-p4"
}

variable "creds" {
  default =  "kuldip-p3-277321-1273b0d61a5b.json"
}

variable "region" {
  default = "us-central1" 
}

variable "zone"  {
  default = "us-central1-c"
}

variable "cidr_ip" {
  default = ["10.0.0.0/16"]
}

variable "ssh_key" {
  default = "your-public-ssh-key"
}

