#!/bin/bash
set -euo pipefail

if [ "$#" -ne 2 ]; then
  echo "Usage: $(basename "$0") input.pdf output_directory"
  exit 1
fi

input_pdf=$1
output_dir=$2

if ! command -v magick >/dev/null 2>&1 && ! command -v convert >/dev/null 2>&1; then
  echo "Error: ImageMagick is required. Install it with Homebrew: brew install imagemagick"
  exit 1
fi

if ! command -v gs >/dev/null 2>&1; then
  echo "Error: Ghostscript ('gs') is required by ImageMagick to read PDFs. Install it with Homebrew: brew install ghostscript"
  exit 1
fi

mkdir -p "$output_dir"

if command -v magick >/dev/null 2>&1; then
  magick -density 300 "$input_pdf" -quality 90 "$output_dir/page-%03d.jpg"
else
  # Fallback for older ImageMagick versions
  convert -density 300 "$input_pdf" -quality 90 "$output_dir/page-%03d.jpg"
fi

