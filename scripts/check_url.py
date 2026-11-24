# file: scripts/check_url.py
"""Kiểm tra danh sách URL; trả về exit code 1 nếu có URL lỗi."""
import argparse
import logging
import sys
import time
import urllib.error
import urllib.request

log = logging.getLogger("check_url")

def check(url: str, timeout: float) -> bool:
    start = time.monotonic()
    try:
        with urllib.request.urlopen(url, timeout=timeout) as resp:
            elapsed_ms = (time.monotonic() - start) * 1000
            log.info("%s -> %s (%.0f ms)", url, resp.status, elapsed_ms)
            return True
    except (urllib.error.URLError, TimeoutError) as exc:
        # HTTPError (4xx, 5xx) là lớp con của URLError nên cũng rơi vào nhánh này.
        log.error("%s -> FAIL (%s)", url, exc)
        return False

def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("urls", nargs="+", help="URL cần kiểm tra")
    parser.add_argument("--timeout", type=float, default=5.0, help="giây, mặc định 5")
    args = parser.parse_args()

    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
    results = [check(url, args.timeout) for url in args.urls]
    return 0 if all(results) else 1

if __name__ == "__main__":
    sys.exit(main())
