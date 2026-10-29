#!/usr/bin/env bash
# Preserve frozen predictions with conditional S3 writes.
set -euo pipefail
root="${PROMVAL_DATA:-data}"
LOG="$root/predictions.json"
STATE="$root/.predictions-etag"
bucket="${DATA_BACKUP_BUCKET:?set DATA_BACKUP_BUCKET}"
key=valorant-model/feed/predictions.json

etag() {
    local out
    if out=$(aws s3api head-object --bucket "$bucket" --key "$key" --query ETag --output text 2>&1); then
        echo "$out"
    elif grep -q '(404)' <<<"$out"; then
        echo ""
    else
        echo "::error::Can't read s3://$bucket/$key: $out" >&2
        return 1
    fi
}

case "${1:-}" in
restore)
    mkdir -p "$root"
    tag=$(etag)
    if [ -z "$tag" ]; then
        rm -f "$LOG"
        : >"$STATE"
        echo "No saved prediction log yet."
        exit 0
    fi
    aws s3api get-object --bucket "$bucket" --key "$key" --if-match "$tag" "$LOG" >/dev/null
    echo "$tag" >"$STATE"
    echo "Restored prediction log."
    ;;
save)
    [ -f "$LOG" ] || { echo "No prediction log to save."; exit 0; }
    [ -f "$STATE" ] || { echo "::error::Restore the prediction log before saving." >&2; exit 1; }
    restored=$(cat "$STATE")
    current=$(etag)
    if [ "$current" != "$restored" ]; then
        echo "::warning::Prediction log changed since restore; skipping save."
        exit 0
    fi
    condition=(--if-none-match '*')
    [ -z "$current" ] || condition=(--if-match "$current")
    if out=$(aws s3api put-object --bucket "$bucket" --key "$key" --body "$LOG" \
        --content-type application/json "${condition[@]}" 2>&1); then
        echo "Saved prediction log."
    elif grep -Eq 'PreconditionFailed|ConditionalRequestConflict|\(412\)|\(409\)' <<<"$out"; then
        echo "::warning::Prediction log changed during save; skipping write."
    else
        echo "::error::Can't save prediction log: $out" >&2
        exit 1
    fi
    ;;
*) echo "usage: $0 restore|save" >&2; exit 2 ;;
esac
