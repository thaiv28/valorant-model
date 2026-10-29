"""Small, injectable, rate-limited HTTP client."""

import threading
import time
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

USER_AGENT = "valorant-model/0.1 (+https://github.com/thaiv28/valorant-model)"


def http_get(url: str) -> str:
    with urlopen(
        Request(url, headers={"User-Agent": USER_AGENT}), timeout=30
    ) as response:
        return response.read().decode("utf-8")


class Fetcher:
    def __init__(
        self, get=http_get, sleep=time.sleep, clock=time.monotonic, min_interval=2.0
    ):
        if min_interval < 0:
            raise ValueError("min_interval must be nonnegative")
        self.get, self.sleep, self.clock = get, sleep, clock
        self.min_interval = min_interval
        self._last = None
        # Shared by every worker thread: one request slot per min_interval, and a
        # rate-limit or server error pauses all workers, not just the one that hit it.
        self._lock = threading.Lock()
        self._paused_until = None

    def _wait_for_slot(self):
        with self._lock:
            now = self.clock()
            start = now
            if self._last is not None:
                start = max(start, self._last + self.min_interval)
            if self._paused_until is not None:
                start = max(start, self._paused_until)
            self._last = start
        if start > now:
            self.sleep(start - now)

    def text(self, url: str) -> str:
        for attempt in range(5):
            self._wait_for_slot()
            try:
                return self.get(url)
            except (URLError, TimeoutError) as exc:
                if isinstance(exc, HTTPError) and not (
                    exc.code == 429 or 500 <= exc.code < 600
                ):
                    raise
                if attempt == 4:
                    raise
                with self._lock:
                    self._paused_until = self.clock() + 5 * 2**attempt
        raise AssertionError("unreachable")
