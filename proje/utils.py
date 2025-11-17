"""Utility helpers for `proje` app.

Small helpers for generating report paths and uploading files to S3.
"""

import re
from datetime import datetime
from typing import Optional


def upload_file_to_s3(
    path,
    bucket: Optional[str] = None,
    key: Optional[str] = None,
    public: bool = False,
    expire_seconds: int = 3600,
):
    """Upload a local file to S3 and return a dict with keys: bucket, key, url.

    - `bucket`: S3 bucket name. If None, caller must provide via settings or boto3 default.
    - `key`: object key in S3. If None, the filename will be used.
    - `public`: if True, the object will be uploaded with public-read ACL and returned URL is the public URL.
      Otherwise a presigned URL is returned (valid for `expire_seconds`).
    """
    import os

    import boto3

    s3 = boto3.client("s3")
    bucket_name = bucket
    if not bucket_name:
        # let boto3 fail if no default bucket provided
        raise ValueError("S3 bucket must be provided to upload reports")

    path = str(path)
    filename = os.path.basename(path)
    object_key = key or filename

    extra_args = {}
    if public:
        extra_args["ACL"] = "public-read"

    s3.upload_file(path, bucket_name, object_key, ExtraArgs=extra_args or None)

    if public:
        # Construct public URL using virtual-hosted-style URL; let caller override if needed.
        url = f"https://{bucket_name}.s3.amazonaws.com/{object_key}"
    else:
        url = s3.generate_presigned_url(
            "get_object",
            Params={"Bucket": bucket_name, "Key": object_key},
            ExpiresIn=expire_seconds,
        )

    return {"bucket": bucket_name, "key": object_key, "url": url}


def _sanitize_label(label: str) -> str:
    # keep only alphanumerics, dash and underscore
    return re.sub(r"[^A-Za-z0-9_-]", "_", (label or "").strip())


def generate_report_path(
    prefix: str = "reports/proje_assign",
    ext: str = "csv",
    label: str | None = None,
) -> str:
    """Return a timestamped report path string under `prefix` with extension `ext`.

    If `label` is provided it will be included in the filename (sanitized).
    Example: generate_report_path(label='ali') -> 'reports/proje_assign_ali_20251117_143501.csv'
    """
    now = datetime.now()
    parts = [prefix]
    if label:
        parts.append(_sanitize_label(label))
    parts.append(now.strftime("%Y%m%d_%H%M%S"))
    fname = "_".join(parts) + f".{ext}"
    return fname
