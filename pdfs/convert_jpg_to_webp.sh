#!/bin/bash
set -euo pipefail

show_usage() {
  echo "Usage: $(basename "$0") input_path output_directory [quality]"
  echo "  input_path      : JPEG file or directory containing .jpg/.jpeg files."
  echo "  output_directory: Destination directory for generated .webp files."
  echo "  quality         : Optional quality (1-100). Default: 80."
}

if [ "$#" -lt 2 ] || [ "$#" -gt 3 ]; then
  show_usage
  exit 1
fi

input_path=$1
output_dir=$2
quality=${3:-80}

if ! [[ "$quality" =~ ^[0-9]+$ ]] || [ "$quality" -lt 1 ] || [ "$quality" -gt 100 ]; then
  echo "Error: quality must be an integer between 1 and 100 (got '$quality')."
  exit 1
fi

if ! command -v magick >/dev/null 2>&1 && ! command -v cwebp >/dev/null 2>&1; then
  echo "Error: Requires ImageMagick (magick) or libwebp (cwebp). Install with:"
  echo "  brew install imagemagick    # preferred"
  echo "  brew install webp           # provides cwebp"
  exit 1
fi

if [ ! -e "$input_path" ]; then
  echo "Error: '$input_path' does not exist."
  exit 1
fi

mkdir -p "$output_dir"

files=()

if [ -f "$input_path" ]; then
  ext=${input_path##*.}
  ext_lower=$(printf '%s' "$ext" | tr '[:upper:]' '[:lower:]')
  if [ "$ext_lower" != "jpg" ] && [ "$ext_lower" != "jpeg" ]; then
    echo "Error: input file must have .jpg or .jpeg extension."
    exit 1
  fi
  files+=("$input_path")
elif [ -d "$input_path" ]; then
  while IFS= read -r -d '' file; do
    files+=("$file")
  done < <(find "$input_path" \( -iname '*.jpg' -o -iname '*.jpeg' \) -type f -print0)
else
  echo "Error: '$input_path' is neither a file nor a directory."
  exit 1
fi

if [ "${#files[@]}" -eq 0 ]; then
  echo "No JPEG files found in '$input_path'."
  exit 0
fi

convert_with_magick() {
  local src=$1
  local dst=$2
  magick "$src" -auto-orient -quality "$quality" -define webp:method=6 -define webp:auto-filter=true "$dst"
}

convert_with_cwebp() {
  local src=$1
  local dst=$2
  cwebp -quiet -q "$quality" "$src" -o "$dst"
}

converted=0

for src in "${files[@]}"; do
  filename=$(basename "$src")
  name_without_ext=${filename%.*}
  dst="$output_dir/$name_without_ext.webp"

  if command -v magick >/dev/null 2>&1; then
    convert_with_magick "$src" "$dst"
  else
    convert_with_cwebp "$src" "$dst"
  fi
  converted=$((converted + 1))
done

echo "Converted $converted file(s) to WebP in '$output_dir' (quality=$quality)."

