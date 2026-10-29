"""Network-free crawling, pacing, retry and cache tests."""

from datetime import date
from pathlib import Path
from urllib.error import HTTPError, URLError

import pytest
from typer.testing import CliRunner

from promval.vlr import cache
from promval.vlr.cli import app
from promval.vlr.crawl import crawl
from promval.vlr.http import USER_AGENT, Fetcher, http_get

FIXTURES = Path(__file__).parent / "fixtures" / "vlr"


def listing(*entries):
    return "".join(
        f'<div class="wf-label mod-large">{day.strftime("%a, %B %d, %Y")}</div><a class="match-item" href="/{id}/slug"></a>'
        for id, day in entries
    )


class FakeFetcher:
    def __init__(self, pages):
        self.pages, self.calls = pages, []

    def text(self, url):
        self.calls.append(url)
        if "page=" in url:
            return self.pages.get(
                int(url.split("page=")[1]),
                cache.load(FIXTURES / "results_p1500.html.gz"),
            )
        id = int(url.split("/")[3])
        suffix = "_economy" if "tab=economy" in url else ""
        return cache.load(FIXTURES / f"match_{id}{suffix}.html.gz")


@pytest.fixture(autouse=True)
def isolated_cache(tmp_path, monkeypatch):
    monkeypatch.setenv("PROMVAL_DATA", str(tmp_path))


def test_since_today_cached_and_empty():
    cache.save(cache.match_path(654971), "cached forever")
    cache.save(cache.economy_path(654971), "cached economy")
    fetcher = FakeFetcher(
        {
            1: listing(
                (773441, date(2026, 10, 28)),
                (654971, date(2026, 5, 6)),
                (610432, date(2026, 2, 8)),
                (163803, date(2023, 1, 8)),
            )
        }
    )
    result = crawl(fetcher, date(2026, 1, 1), today=date(2026, 10, 28))
    assert (
        result.pages_read,
        result.matches_fetched,
        result.economy_fetched,
        result.skipped,
        result.errors,
    ) == (2, 1, 1, 1, 0)
    assert cache.load(cache.match_path(654971)) == "cached forever"
    assert not cache.has(cache.match_path(773441))
    assert not cache.has(cache.match_path(163803))


def test_economy_cutoff_and_max_matches():
    fetcher = FakeFetcher(
        {1: listing((163803, date(2023, 1, 8)), (6805, date(2020, 11, 28)))}
    )
    result = crawl(fetcher, date(2020, 1, 1), today=date(2026, 10, 29))
    assert (result.matches_fetched, result.economy_fetched) == (2, 1)
    assert not cache.has(cache.economy_path(6805))
    assert cache.has(cache.economy_path(163803))
    fetcher = FakeFetcher(
        {1: listing((773441, date(2026, 10, 28)), (610432, date(2026, 2, 8)))}
    )
    result = crawl(fetcher, date(2020, 1, 1), max_matches=1, today=date(2026, 10, 29))
    assert result.matches_fetched == 1 and result.pages_read == 1
    assert not cache.has(cache.match_path(610432))
    assert crawl(fetcher, date(2020, 1, 1), max_matches=0).pages_read == 0


def test_known_page_stop_and_since_stop():
    row = listing((6805, date(2020, 11, 28)))
    cache.save(cache.match_path(6805), "known")
    fetcher = FakeFetcher(dict.fromkeys(range(1, 5), row))
    assert crawl(fetcher, date(2020, 1, 1)).pages_read == 3
    assert crawl(fetcher, date(2021, 1, 1)).pages_read == 1


def test_failures_and_missing_economy_are_retried():
    class Flaky(FakeFetcher):
        def text(self, url):
            if "page=" not in url:
                raise TimeoutError("fixture failure")
            return super().text(url)

    row = listing((773441, date(2026, 10, 28)))
    result = crawl(Flaky({1: row}), date(2026, 1, 1), today=date(2026, 10, 29))
    assert result.errors == 1 and result.matches_fetched == 0
    cache.save(cache.match_path(773441), "unchanged")
    result = crawl(Flaky({1: row}), date(2026, 1, 1), today=date(2026, 10, 29))
    assert result.errors == 1 and result.skipped == 1
    result = crawl(FakeFetcher({1: row}), date(2026, 1, 1), today=date(2026, 10, 29))
    assert result.matches_fetched == 0 and result.economy_fetched == 1
    assert cache.load(cache.match_path(773441)) == "unchanged"


@pytest.mark.parametrize(
    "failure",
    [
        HTTPError("url", 429, "slow", {}, None),
        HTTPError("url", 503, "unavailable", {}, None),
        URLError("offline"),
        TimeoutError(),
    ],
)
def test_pacing_retry_and_exhaustion(failure):
    now, starts, sleeps = [0.0], [], []

    def sleep(seconds):
        sleeps.append(seconds)
        now[0] += seconds

    def get(url):
        starts.append(now[0])
        if len(starts) == 2:
            raise failure
        return "ok"

    f = Fetcher(get=get, sleep=sleep, clock=lambda: now[0])
    assert f.text("one") == f.text("two") == "ok"
    assert starts == [0, 2, 7] and sleeps == [2, 5]
    starts.clear()
    sleeps.clear()

    def broken(url):
        starts.append(now[0])
        raise failure

    f = Fetcher(get=broken, sleep=sleep, clock=lambda: now[0])
    with pytest.raises(type(failure)):
        f.text("broken")
    assert len(starts) == 5 and sleeps == [5, 10, 20, 40]


def test_http_headers_timeout_and_no_404_retry(monkeypatch):
    class Response:
        def __enter__(self):
            return self

        def __exit__(self, *args):
            pass

        def read(self):
            return "KRÜ".encode()

    def open_(request, timeout):
        assert request.get_header("User-agent") == USER_AGENT
        assert timeout == 30
        return Response()

    monkeypatch.setattr("promval.vlr.http.urlopen", open_)
    assert http_get("https://example.invalid") == "KRÜ"

    def missing(url):
        raise HTTPError(url, 404, "missing", {}, None)

    with pytest.raises(HTTPError):
        Fetcher(get=missing, sleep=lambda _: pytest.fail("404 retried")).text(
            "https://example.invalid"
        )


def test_atomic_cache_and_cli(monkeypatch):
    p = cache.match_path(1)
    cache.save(p, "first")

    def fail(*args):
        raise OSError("replace failed")

    monkeypatch.setattr("promval.vlr.cache.os.replace", fail)
    with pytest.raises(OSError):
        cache.save(p, "second")
    assert cache.load(p) == "first"
    assert list(p.parent.glob("*.tmp")) == []
    from promval.vlr.crawl import Summary

    def fake(
        fetcher, since, economy_since, max_matches, stop_after_known_pages, workers
    ):
        assert since == date(2023, 1, 1) and economy_since == date(2023, 1, 1)
        assert max_matches == 0 and fetcher.min_interval == 2
        assert stop_after_known_pages == 3
        return Summary()

    monkeypatch.setattr("promval.vlr.cli.crawl_pages", fake)
    result = CliRunner().invoke(
        app, ["crawl", "--since", "2023-01-01", "--max-matches", "0"]
    )
    assert result.exit_code == 0, result.output
    assert "~2 requests per new match at 2 s" in result.output
    assert "pages=0 matches=0 economy=0 skipped=0 errors=0" in result.output
    assert CliRunner().invoke(app, ["crawl", "--since", "bad"]).exit_code != 0


def test_saved_results_page_with_fixture_fetcher():
    fetcher = FakeFetcher({1: cache.load(FIXTURES / "results_p1.html.gz")})
    result = crawl(fetcher, date(2026, 1, 1), max_matches=1, today=date(2026, 10, 29))
    assert (
        result.pages_read,
        result.matches_fetched,
        result.economy_fetched,
        result.errors,
    ) == (1, 1, 1, 0)
    assert cache.load(cache.match_path(773441)) == cache.load(
        FIXTURES / "match_773441.html.gz"
    )


def test_parallel_workers_fetch_every_page_once(tmp_path, monkeypatch):
    import threading
    from datetime import date

    from promval.vlr.crawl import crawl
    from promval.vlr.http import Fetcher

    monkeypatch.setenv("PROMVAL_DATA", str(tmp_path))
    results = cache.load(FIXTURES / "results_p1.html.gz")
    seen, lock = [], threading.Lock()

    def get(url):
        with lock:
            seen.append(url)
        if "results" in url:
            return results if url.endswith("page=1") else "<html></html>"
        return "<html>match</html>"

    fetcher = Fetcher(get=get, sleep=lambda s: None, min_interval=0)
    summary = crawl(fetcher, date(2026, 10, 1), today=date(2026, 10, 29), workers=4)
    pages = [u for u in seen if "results" not in u]
    assert len(pages) == len(set(pages))  # no page fetched twice
    assert summary.matches_fetched == len([u for u in pages if "economy" not in u])
    assert summary.errors == 0


def test_rate_limit_pauses_all_workers():
    from urllib.error import HTTPError

    from promval.vlr.http import Fetcher

    clock = [0.0]
    sleeps = []
    calls = []

    def get(url):
        calls.append(url)
        if len(calls) == 1:
            raise HTTPError(url, 429, "slow down", None, None)
        return "ok"

    def sleep(seconds):
        sleeps.append(seconds)
        clock[0] += seconds

    fetcher = Fetcher(get=get, sleep=sleep, clock=lambda: clock[0], min_interval=0.25)
    assert fetcher.text("a") == "ok"
    # The retry waited out the shared pause, and so does the next caller.
    assert sum(sleeps) >= 5
    assert fetcher._paused_until <= clock[0]
