#!/usr/bin/env bash
# file: scripts/backup.sh
# Nén một thư mục thành file .tar.gz có timestamp, chỉ giữ lại N bản mới nhất.
set -euo pipefail

usage() {
  echo "Usage: $0 <source_dir> <backup_dir> [keep=7]" >&2
  exit 1
}

if [[ $# -lt 2 ]]; then
  usage
fi

src="${1%/}"
dest="$2"
keep="${3:-7}"
name="$(basename "$src")"

if [[ ! -d "$src" ]]; then
  echo "Source directory not found: $src" >&2
  exit 2
fi

mkdir -p "$dest"
archive="$dest/${name}-$(date +%Y%m%d-%H%M%S).tar.gz"
tar -czf "$archive" -C "$(dirname "$src")" "$name"
echo "Created $archive"

# Sắp xếp các bản backup theo thời gian sửa đổi, mới nhất trước, rồi xoá các bản vượt quá $keep.
mapfile -t old < <(
  find "$dest" -maxdepth 1 -type f -name "${name}-*.tar.gz" -printf '%T@ %p\n' \
    | sort -rn | tail -n +"$((keep + 1))" | cut -d' ' -f2-
)
if ((${#old[@]} > 0)); then
  rm -- "${old[@]}"
  echo "Removed ${#old[@]} old backup(s)"
fi
