# Platform Access Design

## Access Policy
- Bastion hosts are allowed only from office VPN CIDR blocks.
- No internet-exposed SSH endpoints are permitted.
- Artifact storage should use encryption at rest and strict access controls.
