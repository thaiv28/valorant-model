# Deployment

## CI

`.github/workflows/ci.yml` runs ruff and pytest on pushes to main and pull requests.

## Kalshi collection

`.github/workflows/kalshi-collect.yml` runs on main at minute 23 every six hours (`23 */6 * * *`, UTC), or by manual dispatch. Runs serialize without cancellation and time out after 30 minutes.

Set repository variable `DATA_BACKUP_BUCKET` to the shared platform artifacts bucket and repository secret `AWS_ROLE_ARN` to the shared platform GitHub deployment role. It trusts `thaiv28/*` repositories on main. Authentication uses GitHub OIDC (`id-token: write`); AWS region is `us-west-2`. Storage prefix: `s3://$DATA_BACKUP_BUCKET/valorant-model/kalshi/`.

Each runner downloads only `manifest.json`. A missing manifest fails before collection unless manual dispatch supplies `allow_full: true`; otherwise it could refetch roughly 10k markets. Collection skips histories listed in the manifest. Each run uploads new trade/candle files, one book file, refreshed catalogs and the updated manifest. Zero snapshots produce no book file. Upload runs even after collection exits 1 to preserve partial progress; sync never deletes remote objects.

## Seeding and local copies

From the repository root, with a completed local backfill and AWS credentials:

```bash
export DATA_BACKUP_BUCKET=shared-artifacts-bucket-name
uv run promval kalshi manifest
scripts/kalshi_data.sh push
```

The manifest command rebuilds from histories present locally. `scripts/kalshi_data.sh pull` downloads the full archive for local use; `push` uploads the local archive. Both require `DATA_BACKUP_BUCKET`; neither deletes objects.

## Cost

A private repository spends Actions minutes: about 4 runs/day × ~2 min ≈ 240 min/month (estimate; measure after the first runs).
