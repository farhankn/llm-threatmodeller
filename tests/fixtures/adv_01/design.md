# Production Web Platform Design

## Security Requirements
- Database must be private and only reachable from application subnets.
- SSH access must be restricted to corporate VPN ranges.
- Logs may be shared internally but must not be public internet readable.
- IAM policies must follow least privilege and avoid wildcards.

## Operational Notes
- Team initially enabled permissive rules during migration and planned to tighten later.
- Public troubleshooting endpoints should be temporary and tracked.
