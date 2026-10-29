"""Small, injectable, rate-limited HTTP client."""

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

    def text(self, url: str) -> str:
        for attempt in range(5):
            if self._last is not None:
                delay = self.min_interval - (self.clock() - self._last)
                if delay > 0:
                    self.sleep(delay)
            self._last = self.clock()
            try:
                return self.get(url)
            except (URLError, TimeoutError) as exc:
                if isinstance(exc, HTTPError) and not (
                    exc.code == 429 or 500 <= exc.code < 600
                ):
                    raise
                if attempt == 4:
                    raise
                self.sleep(5 * 2**attempt)
        raise AssertionError("unreachable")
