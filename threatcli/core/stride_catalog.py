"""Resource-specific STRIDE threat catalog for exhaustive analysis."""

from dataclasses import dataclass
from typing import Any

@dataclass(frozen=True)
class ThreatCheckItem:
    stride_category: str
    condition: str
    threat_description_template: str
    reference_attributes: list[str]
    severity_score: float  # 0.0-1.0

# Comprehensive catalog covering common cloud resources
STRIDE_CATALOG: dict[str, dict[str, list[ThreatCheckItem]]] = {
    "aws_s3_bucket": {
        "INFORMATION_DISCLOSURE": [
            ThreatCheckItem(
                stride_category="INFORMATION_DISCLOSURE",
                condition="acl in [public-read, public-read-write, authenticated-read]",
                threat_description_template="Public ACL ({acl}) allows unauthorized read access",
                reference_attributes=["acl"],
                severity_score=0.9
            ),
            ThreatCheckItem(
                stride_category="INFORMATION_DISCLOSURE",
                condition="server_side_encryption_configuration missing",
                threat_description_template="Data at rest is unencrypted",
                reference_attributes=["server_side_encryption_configuration"],
                severity_score=0.7
            ),
            ThreatCheckItem(
                stride_category="INFORMATION_DISCLOSURE",
                condition="ssl_only_bucket_policy missing",
                threat_description_template="Bucket does not enforce SSL/TLS for data in transit",
                reference_attributes=["policy"],
                severity_score=0.6
            ),
        ],
        "TAMPERING": [
            ThreatCheckItem(
                stride_category="TAMPERING",
                condition="versioning disabled or missing",
                threat_description_template="Lack of versioning allows permanent data destruction",
                reference_attributes=["versioning"],
                severity_score=0.6
            ),
            ThreatCheckItem(
                stride_category="TAMPERING",
                condition="object_lock_configuration missing",
                threat_description_template="No immutability guarantee for stored objects",
                reference_attributes=["object_lock_configuration"],
                severity_score=0.5
            ),
        ],
        "DENIAL_OF_SERVICE": [
            ThreatCheckItem(
                stride_category="DENIAL_OF_SERVICE",
                condition="lifecycle_rule missing",
                threat_description_template="Missing lifecycle policies may lead to unbounded storage costs (economic DoS)",
                reference_attributes=["lifecycle_rule"],
                severity_score=0.3
            ),
        ]
    },
    "aws_iam_role": {
        "ELEVATION_OF_PRIVILEGE": [
            ThreatCheckItem(
                stride_category="ELEVATION_OF_PRIVILEGE",
                condition="assume_role_policy with '*' principal",
                threat_description_template="Role is assumable by any principal, potentially leading to unauthorized access",
                reference_attributes=["assume_role_policy"],
                severity_score=0.9
            ),
            ThreatCheckItem(
                stride_category="ELEVATION_OF_PRIVILEGE",
                condition="inline_policy with broad permissions",
                threat_description_template="Role has overly broad permissions (e.g. s3:*)",
                reference_attributes=["inline_policy"],
                severity_score=0.8
            ),
        ],
        "SPOOFING": [
            ThreatCheckItem(
                stride_category="SPOOFING",
                condition="No MFA requirement in assume_role_policy",
                threat_description_template="Identity spoofing possible due to lack of MFA enforcement",
                reference_attributes=["assume_role_policy"],
                severity_score=0.7
            ),
        ]
    },
    "aws_db_instance": {
        "INFORMATION_DISCLOSURE": [
            ThreatCheckItem(
                stride_category="INFORMATION_DISCLOSURE",
                condition="publicly_accessible = true",
                threat_description_template="Database is publicly accessible from the internet",
                reference_attributes=["publicly_accessible"],
                severity_score=0.9
            ),
            ThreatCheckItem(
                stride_category="INFORMATION_DISCLOSURE",
                condition="storage_encrypted = false",
                threat_description_template="Database storage is not encrypted at rest",
                reference_attributes=["storage_encrypted"],
                severity_score=0.7
            ),
        ],
        "TAMPERING": [
             ThreatCheckItem(
                stride_category="TAMPERING",
                condition="backup_retention_period missing or 0",
                threat_description_template="Insufficient backup retention period for disaster recovery",
                reference_attributes=["backup_retention_period"],
                severity_score=0.6
            ),
        ]
    },
    "aws_security_group": {
        "INFORMATION_DISCLOSURE": [
            ThreatCheckItem(
                stride_category="INFORMATION_DISCLOSURE",
                condition="ingress rule with cidr_blocks=['0.0.0.0/0'] on sensitive ports",
                threat_description_template="Security group allows broad ingress access (0.0.0.0/0)",
                reference_attributes=["ingress"],
                severity_score=0.8
            ),
        ]
    },
    "aws_lambda_function": {
        "INFORMATION_DISCLOSURE": [
            ThreatCheckItem(
                stride_category="INFORMATION_DISCLOSURE",
                condition="vpc_config missing",
                threat_description_template="Lambda executes outside of a VPC, potentially exposing traffic",
                reference_attributes=["vpc_config"],
                severity_score=0.5
            ),
        ],
        "ELEVATION_OF_PRIVILEGE": [
            ThreatCheckItem(
                stride_category="ELEVATION_OF_PRIVILEGE",
                condition="role with excessive permissions",
                threat_description_template="Lambda execution role may have excessive permissions",
                reference_attributes=["role"],
                severity_score=0.7
            ),
        ],
        "DENIAL_OF_SERVICE": [
            ThreatCheckItem(
                stride_category="DENIAL_OF_SERVICE",
                condition="reserved_concurrent_executions missing",
                threat_description_template="Lack of concurrency limits may cause account-wide DoS",
                reference_attributes=["reserved_concurrent_executions"],
                severity_score=0.4
            ),
        ]
    },
    "aws_api_gateway_rest_api": {
        "SPOOFING": [
            ThreatCheckItem(
                stride_category="SPOOFING",
                condition="authorization = 'NONE'",
                threat_description_template="API methods lack authentication/authorization",
                reference_attributes=["authorization"],
                severity_score=0.9
            ),
        ],
        "DENIAL_OF_SERVICE": [
            ThreatCheckItem(
                stride_category="DENIAL_OF_SERVICE",
                condition="throttling settings missing",
                threat_description_template="API lacks rate limiting/throttling protection",
                reference_attributes=["settings"],
                severity_score=0.6
            ),
        ]
    },
    "aws_dynamodb_table": {
        "INFORMATION_DISCLOSURE": [
            ThreatCheckItem(
                stride_category="INFORMATION_DISCLOSURE",
                condition="server_side_encryption disabled",
                threat_description_template="DynamoDB table lacks server-side encryption",
                reference_attributes=["server_side_encryption"],
                severity_score=0.7
            ),
        ],
        "TAMPERING": [
            ThreatCheckItem(
                stride_category="TAMPERING",
                condition="point_in_time_recovery disabled",
                threat_description_template="PITR is disabled, risking data loss from accidental writes",
                reference_attributes=["point_in_time_recovery"],
                severity_score=0.6
            ),
        ]
    },
    "aws_kms_key": {
        "ELEVATION_OF_PRIVILEGE": [
            ThreatCheckItem(
                stride_category="ELEVATION_OF_PRIVILEGE",
                condition="policy with broad '*' principal",
                threat_description_template="KMS key policy allows broad access, potentially leaking secrets",
                reference_attributes=["policy"],
                severity_score=0.8
            ),
        ],
        "TAMPERING": [
            ThreatCheckItem(
                stride_category="TAMPERING",
                condition="enable_key_rotation = false",
                threat_description_template="Automatic key rotation is disabled",
                reference_attributes=["enable_key_rotation"],
                severity_score=0.4
            ),
        ]
    },
    "aws_vpc": {
        "INFORMATION_DISCLOSURE": [
            ThreatCheckItem(
                stride_category="INFORMATION_DISCLOSURE",
                condition="enable_dns_support = false",
                threat_description_template="DNS support disabled, potentially impacting security service resolution",
                reference_attributes=["enable_dns_support"],
                severity_score=0.2
            ),
        ]
    },
    "aws_elb": {
        "INFORMATION_DISCLOSURE": [
            ThreatCheckItem(
                stride_category="INFORMATION_DISCLOSURE",
                condition="listener on port 80 (HTTP)",
                threat_description_template="ELB allows unencrypted HTTP traffic",
                reference_attributes=["listener"],
                severity_score=0.7
            ),
        ],
        "DENIAL_OF_SERVICE": [
            ThreatCheckItem(
                stride_category="DENIAL_OF_SERVICE",
                condition="connection_draining disabled",
                threat_description_template="Connection draining disabled, risking dropped requests during scaling",
                reference_attributes=["connection_draining"],
                severity_score=0.3
            ),
        ]
    },
    "aws_sns_topic": {
        "INFORMATION_DISCLOSURE": [
            ThreatCheckItem(
                stride_category="INFORMATION_DISCLOSURE",
                condition="policy with broad '*' principal",
                threat_description_template="SNS topic policy allows broad access, potentially leaking alerts",
                reference_attributes=["policy"],
                severity_score=0.7
            ),
        ]
    },
    "aws_sqs_queue": {
        "TAMPERING": [
            ThreatCheckItem(
                stride_category="TAMPERING",
                condition="redrive_policy (DLQ) missing",
                threat_description_template="SQS queue lacks a Dead Letter Queue, risking message loss/tampering on failure",
                reference_attributes=["redrive_policy"],
                severity_score=0.5
            ),
        ],
        "INFORMATION_DISCLOSURE": [
            ThreatCheckItem(
                stride_category="INFORMATION_DISCLOSURE",
                condition="kms_master_key_id missing",
                threat_description_template="SQS queue messages are not encrypted at rest",
                reference_attributes=["kms_master_key_id"],
                severity_score=0.6
            ),
        ]
    },
    "aws_cloudtrail": {
        "REPUDIATION": [
            ThreatCheckItem(
                stride_category="REPUDIATION",
                condition="enable_logging = false",
                threat_description_template="CloudTrail logging is disabled, preventing audit of API calls",
                reference_attributes=["enable_logging"],
                severity_score=0.9
            ),
            ThreatCheckItem(
                stride_category="REPUDIATION",
                condition="enable_log_file_validation = false",
                threat_description_template="Log file validation disabled, allowing log tampering to go undetected",
                reference_attributes=["enable_log_file_validation"],
                severity_score=0.7
            ),
        ]
    },
    "aws_cognito_user_pool": {
        "SPOOFING": [
            ThreatCheckItem(
                stride_category="SPOOFING",
                condition="mfa_configuration = 'OFF'",
                threat_description_template="MFA is disabled for Cognito user pool, increasing account takeover risk",
                reference_attributes=["mfa_configuration"],
                severity_score=0.8
            ),
        ],
        "INFORMATION_DISCLOSURE": [
            ThreatCheckItem(
                stride_category="INFORMATION_DISCLOSURE",
                condition="allow_unauthenticated_identities = true",
                threat_description_template="Cognito identity pool allows unauthenticated access",
                reference_attributes=["allow_unauthenticated_identities"],
                severity_score=0.7
            ),
        ]
    },
    "aws_cloudwatch_log_group": {
        "INFORMATION_DISCLOSURE": [
            ThreatCheckItem(
                stride_category="INFORMATION_DISCLOSURE",
                condition="kms_key_id missing",
                threat_description_template="CloudWatch log group is not encrypted with KMS",
                reference_attributes=["kms_key_id"],
                severity_score=0.4
            ),
        ]
    },
    "aws_route53_record": {
        "TAMPERING": [
            ThreatCheckItem(
                stride_category="TAMPERING",
                condition="alias missing for sensitive endpoints",
                threat_description_template="Route53 record points to hardcoded IP instead of Alias, risking hijacking on resource replacement",
                reference_attributes=["name"],
                severity_score=0.3
            ),
        ]
    }
}
