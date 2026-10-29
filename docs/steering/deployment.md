# Deployment

## CI

`.github/workflows/ci.yml` runs ruff and pytest on pushes to main and pull requests.

## Kalshi collection

`.github/workflows/kalshi-collect.yml` runs on main at minute 23 every six hours (`23 */6 * * *`, UTC), or by manual dispatch. Runs serialize without cancellation and time out after 30 minutes.

Repository variable `DATA_BACKUP_BUCKET` and secret `AWS_ROLE_ARN` are set to the shared artifacts bucket and GitHub deployment role. It trusts `thaiv28/*` repositories on main. Authentication uses GitHub OIDC (`id-token: write`); AWS region is `us-west-2`. Storage prefix: `s3://$DATA_BACKUP_BUCKET/valorant-model/kalshi/`.

Each runner downloads only `manifest.json`. A missing manifest fails before collection unless manual dispatch supplies `allow_full: true`; otherwise it could refetch roughly 10k markets. Collection skips histories listed in the manifest. Each run uploads new trade/candle files, one book file, refreshed catalogs and the updated manifest. Zero snapshots produce no book file. Upload runs even after collection exits 1 to preserve partial progress; sync never deletes remote objects.

## Seeding and local copies

From the repository root, with a completed local backfill and AWS credentials:

```bash
export DATA_BACKUP_BUCKET=shared-artifacts-bucket-name
uv run promval kalshi manifest
scripts/kalshi_data.sh push
```

The manifest command rebuilds from histories present locally. `scripts/kalshi_data.sh pull` downloads the full archive for local use; `push` uploads the local archive. Both require `DATA_BACKUP_BUCKET`; neither deletes objects.

## Site feed

`refresh-db.yml` crawls incrementally, rebuilds SQLite and uploads a ratings snapshot hourly. `feed.yml` loads it without a DB, refreshes schedule/prices and publishes the feed. cron-job.org dispatches refresh-db hourly and feed every 10 minutes; GitHub schedules (`41 * * * *`, `7 * * * *`, UTC) are backups. Both allow manual dispatch, run only on main and serialize without cancellation.

S3 keys: `valorant-model/feed/{state.pkl.gz,predictions.json,valorant.json.gz,upcoming/}`; `valorant-model/feed/candidates.json` is private, read by Prometheus's execution Lambda; raw inputs: `valorant-model/vlr/` and `valorant-model/kalshi/` (books excluded on download). Seed the raw cache in S3 once before running refresh-db. The Actions cache accelerates raw downloads. Prediction-log writes require an unchanged ETag; races warn and skip the save. Snapshots are trusted gzip pickles, version checked on load.

Set `PROMETHEUS_DISPATCH_TOKEN` to enable dispatching `thaiv28/Prometheus`'s `games.yml` on main after publication; dispatch failure is nonfatal. `DATA_BACKUP_BUCKET`/`AWS_ROLE_ARN` are already set. Workflows have not yet run on GitHub; runner times are unmeasured.

## Cost

Actions minutes now include up to 24 refreshes/day and 144 feed runs/day, plus four Kalshi collections. Runner durations and monthly cost remain unmeasured.
