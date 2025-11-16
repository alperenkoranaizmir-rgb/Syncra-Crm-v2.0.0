from datetime import datetime


def generate_report_path(prefix: str = "reports/proje_assign", ext: str = "csv") -> str:
    """Return a timestamped report path string under `prefix` with extension `ext`.

    Example: generate_report_path() -> 'reports/proje_assign_20251117_143501.csv'
    """
    now = datetime.now()
    fname = f"{prefix}_{now.strftime('%Y%m%d_%H%M%S')}.{ext}"
    return fname
