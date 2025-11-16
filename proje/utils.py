import re
from datetime import datetime


def _sanitize_label(label: str) -> str:
    # keep only alphanumerics, dash and underscore
    return re.sub(r"[^A-Za-z0-9_-]", "_", (label or "").strip())


def generate_report_path(
    prefix: str = "reports/proje_assign", ext: str = "csv", label: str | None = None
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
