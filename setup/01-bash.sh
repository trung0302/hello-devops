#!/usr/bin/env bash
# file: setup/01-base.sh
# Công cụ nền tảng cho giai đoạn 1: Git, Python, công cụ dòng lệnh.
set -euo pipefail

sudo apt-get update
sudo apt-get install -y \
  git curl wget unzip jq tree make ca-certificates gnupg \
  python3 python3-venv python3-pip pipx \
  shellcheck bash-completion man-db
pipx ensurepath

git --version
python3 --version
shellcheck --version | head -2

