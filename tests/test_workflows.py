"""Offline checks for the scheduled collector's storage safeguards."""

from pathlib import Path

WORKFLOW = Path(__file__).resolve().parents[1] / ".github/workflows/kalshi-collect.yml"


def test_kalshi_schedule_and_permissions():
    text = WORKFLOW.read_text()
    assert 'cron: "23 */6 * * *"' in text
    assert "workflow_dispatch:" in text
    assert "id-token: write" in text
    assert "if: github.ref == 'refs/heads/main'" in text


def test_kalshi_manifest_guard_and_upload():
    text = WORKFLOW.read_text()
    assert (
        'if [ ! -f data/kalshi/manifest.json ] && [ "$ALLOW_FULL" != "true" ]; then'
        in text
    )
    assert "github.event_name == 'workflow_dispatch' && inputs.allow_full" in text
    assert "Missing manifest.json: seed S3 first" in text
    assert "exit 1" in text
    assert "if: always() && steps.collect.outcome != 'skipped'" in text
    assert "aws s3 cp" in text
    assert "aws s3 sync data/kalshi" in text
    assert "aws s3 sync s3://" not in text
    assert "--delete" not in text


def test_site_workflow_safeguards():
    for name, cron, timeout in (
        ("refresh-db", "41 * * * *", 90),
        ("feed", "7 * * * *", 15),
    ):
        text = (WORKFLOW.parent / f"{name}.yml").read_text()
        assert f'cron: "{cron}"' in text
        assert "workflow_dispatch:" in text
        assert "contents: read" in text and "id-token: write" in text
        assert "if: github.ref == 'refs/heads/main'" in text
        assert f"group: {name}" in text
        assert "cancel-in-progress: false" in text
        assert f"timeout-minutes: {timeout}" in text
        assert "${{ vars.DATA_BACKUP_BUCKET }}" in text
        assert "${{ secrets.AWS_ROLE_ARN }}" in text
        assert "aws-region: us-west-2" in text
        assert "--delete" not in text
        assert "shell: bash" in text


def test_refresh_db_storage_and_incremental_crawl():
    text = (WORKFLOW.parent / "refresh-db.yml").read_text()
    assert "uv run promval vlr crawl --since 2021-01-01" in text
    assert "--full" not in text
    assert "bash scripts/setup_db.sh" in text
    assert "uv run promval feed-state" in text
    assert "s3://$BUCKET/valorant-model/vlr" in text
    assert "s3://$BUCKET/valorant-model/kalshi" in text
    assert "s3://$BUCKET/valorant-model/feed/state.pkl.gz" in text
    assert '--exclude "books/*"' in text
    assert "--size-only" in text
    assert "actions/cache/restore@v4" in text and "actions/cache/save@v4" in text
    # Save the raw cache before the DB build, so a slow build can't lose a seed.
    assert text.index("actions/cache/save@v4") < text.index("name: Build DB")
    assert text.count("key: raw-${{ github.run_id }}") == 2
    assert "restore-keys: raw-" in text
    assert "-newer" in text and "cache-matched-key" in text
    assert "if: steps.changed.outputs.save == 'true'" in text


def test_feed_storage_and_guarded_dispatch():
    text = (WORKFLOW.parent / "feed.yml").read_text()
    assert "PROMVAL_DATA" not in text
    assert "setup_db.sh" not in text
    assert "run refresh-db first" in text
    assert (
        "uv run promval export --state data/feed/state.pkl.gz --out data/feed/valorant.json"
        in text
    )
    for key in ("state.pkl.gz", "upcoming", "valorant.json.gz", "candidates.json"):
        assert f"s3://$BUCKET/valorant-model/feed/{key}" in text
    assert "bash scripts/feed_data.sh restore" in text
    assert "bash scripts/feed_data.sh save" in text
    assert "--content-type application/json" in text
    upload = 'aws s3 cp data/feed/candidates.json "s3://$BUCKET/valorant-model/feed/candidates.json" --content-type application/json --only-show-errors'
    assert upload in text
    assert (
        text.index("name: Upload feed")
        < text.index(upload)
        < text.index("name: Dispatch Prometheus")
    )
    assert "--acl" not in text
    assert "gzip -9 -c" in text
    assert "HAS_DISPATCH: ${{ secrets.PROMETHEUS_DISPATCH_TOKEN != '' }}" in text
    assert "if: env.HAS_DISPATCH == 'true'" in text
    assert "GH_TOKEN: ${{ secrets.PROMETHEUS_DISPATCH_TOKEN }}" in text
    assert "continue-on-error: true" in text
    assert "gh workflow run games.yml -R thaiv28/Prometheus --ref main" in text


def test_feed_data_shell_syntax():
    import subprocess

    script = WORKFLOW.parents[2] / "scripts/feed_data.sh"
    subprocess.run(["bash", "-n", str(script)], check=True)
    text = script.read_text()
    assert "valorant-model/feed/predictions.json" in text
    assert "--if-match" in text and "--if-none-match" in text


def test_refresh_db_input_hash_and_exact_cache():
    text = (WORKFLOW.parent / "refresh-db.yml").read_text()
    assert "hashFiles('scripts/**', 'promval/**', 'uv.lock')" in text
    assert (
        "find data/vlr data/kalshi -type f -not -path '*/books/*' "
        "-not -path 'data/vlr/parsed/*' -print0 | LC_ALL=C sort -z | xargs -0 sha256sum"
        in text
    )
    assert "xargs -0 sha256sum; printf" in text
    assert "sha256sum" in text
    assert text.count("key: db-${{ steps.inputs.outputs.hash }}") == 2
    restore = text.split("id: db\n", 1)[1].split("      - name:", 1)[0]
    assert "path: db" in restore
    assert "restore-keys:" not in restore
    assert text.index("name: Crawl") < text.index("name: Hash DB inputs")


def test_refresh_db_skip_requires_cache_and_matching_state():
    text = (WORKFLOW.parent / "refresh-db.yml").read_text()
    assert "DB_CACHE_HIT: ${{ steps.db.outputs.cache-hit }}" in text
    guard = text.split("name: Check rebuild", 1)[1].split("name: Build DB", 1)[0]
    assert 'if [ "$DB_CACHE_HIT" = "true" ]; then' in guard
    assert "--key valorant-model/feed/state.pkl.gz --query Metadata.inputs" in guard
    assert 'if [ "$state_inputs" = "$INPUTS" ]; then' in guard
    assert 'echo "skip=true" >> "$GITHUB_OUTPUT"' in guard
    assert "Unchanged inputs; skipped rebuild" in guard
    for step in ("Build DB", "Save ratings snapshot", "Publish blend artifact"):
        block = text.split(f"name: {step}\n", 1)[1].split("      - ", 1)[0]
        assert "if: steps.rebuild.outputs.skip != 'true'" in block
    save = text.rsplit("uses: actions/cache/save@v4", 1)[1]
    assert "if: steps.rebuild.outputs.skip != 'true'" in save
    assert '--metadata inputs="$INPUTS"' in text
    assert "uv run promval blend-artifact --out data/feed/blend_artifact.json" in text
    assert (
        'aws s3 cp data/feed/blend_artifact.json "s3://$BUCKET/valorant-model/feed/blend_artifact.json" --content-type application/json --only-show-errors'
        in text
    )
    assert "promval/blend_artifact.json" not in text


def test_refresh_db_cold_and_weekly_seeds():
    text = (WORKFLOW.parent / "refresh-db.yml").read_text()
    seed = text.split("name: Seed cold raw cache\n", 1)[1].split("      - name:", 1)[0]
    assert "if: steps.raw.outputs.cache-matched-key == ''" in seed
    assert "continue-on-error: true" in seed
    assert (
        'aws s3 cp "s3://$BUCKET/valorant-model/seed/raw.tar.zst" - | tar -I zstd -xf -'
        in seed
    )
    assert text.index("name: Seed cold raw cache") < text.index(
        "name: Top up raw cache"
    )
    assert text.index("name: Top up raw cache") < text.index("find data/vlr/parsed")
    weekly = text.split("name: Refresh weekly raw seed\n", 1)[1].split(
        "      - name:", 1
    )[0]
    assert "if: steps.raw_save.outcome == 'success'" in weekly
    assert "id: raw_save" in text
    assert "continue-on-error: true" in weekly
    assert "--query LastModified" in weekly
    assert '[ -z "$modified" ]' in weekly
    assert "-gt 604800" in weekly
    assert (
        "tar -I 'zstd -T0 -3' -cf - --exclude='*/books/*' data/vlr data/kalshi"
        in weekly
    )
    assert "--expected-size 3000000000" in weekly
    assert text.index("id: raw_save") < text.index("name: Build DB")
