#!/bin/bash

# Check if the file name is provided as a parameter
if [ $# -eq 0 ]; then
    echo "Please provide a file name as a parameter."
    exit 1
fi

# Convert the title to snake case
file_name=$(echo "$1" | tr '[:upper:]' '[:lower:]' | tr ' ' '_')

# Add the file extension
file_name="$file_name.md"

# Create the file in the _posts folder
touch "_posts/$file_name"
echo "New file created: _posts/$file_name"

# Set the current date and time
current_date=$(date +"%Y-%m-%d %H:%M:%S")

# Add a header to the new file
echo "---" >> "_posts/$file_name"
echo "layout: post" >> "_posts/$file_name"
echo "title: $file_name" >> "_posts/$file_name"
echo "date: $current_date +0700" >> "_posts/$file_name"
echo "categories: []" >> "_posts/$file_name"
echo "---" >> "_posts/$file_name"