#!/bin/bash
set -euo pipefail

show_usage() {
  echo "Usage: $(basename "$0") input.pdf output_directory [dpi] [quality]"
  echo "  dpi     : Output resolution (default: 150). Higher = sharper but slower."
  echo "  quality : JPEG quality 1-100 (default: 85). Lower = smaller files."
}

if [ "$#" -lt 2 ] || [ "$#" -gt 4 ]; then
  show_usage
  exit 1
fi

input_pdf=$1
output_dir=$2
dpi=${3:-150}
quality=${4:-85}

if [ ! -f "$input_pdf" ]; then
  echo "Error: '$input_pdf' does not exist or is not a regular file."
  exit 1
fi

if ! [[ "$dpi" =~ ^[0-9]+$ ]] || [ "$dpi" -le 0 ]; then
  echo "Error: dpi must be a positive integer (got '$dpi')."
  exit 1
fi

if ! [[ "$quality" =~ ^[0-9]+$ ]] || [ "$quality" -lt 1 ] || [ "$quality" -gt 100 ]; then
  echo "Error: quality must be an integer between 1 and 100 (got '$quality')."
  exit 1
fi

if ! command -v gs >/dev/null 2>&1; then
  echo "Error: Ghostscript ('gs') is required. Install it with: brew install ghostscript"
  exit 1
fi

mkdir -p "$output_dir"

echo "Converting '$input_pdf' -> '$output_dir/page-XXX.jpg' at ${dpi}dpi, quality ${quality}..."
time gs \
  -dNOPAUSE \
  -dBATCH \
  -dSAFER \
  -sDEVICE=jpeg \
  -dJPEGQ="$quality" \
  -r"$dpi" \
  -dTextAlphaBits=4 \
  -dGraphicsAlphaBits=4 \
  -sOutputFile="$output_dir/page-%03d.jpg" \
  "$input_pdf"

echo "Done."

