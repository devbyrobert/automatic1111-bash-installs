import os
import subprocess
import tempfile
from pathlib import Path

download_sh = """
# Install required packages
echo "Installing required packages..."
apt-get update >/dev/null
apt-get install -y bc zip >/dev/null

if [ -d "/root/stable-diffusion-webui/outputs/img2img-images" ]; then
  dir_path="/root/stable-diffusion-webui/outputs/img2img-images"
elif [ -d "/root/img2img-images" ]; then
  dir_path="/root/img2img-images"
else
  echo "img2img-images directory not found."
  exit 1
fi

file_counts=()
max_files=0

echo "Analyzing subdirectories..."
# Loop through subdirectories
for subdir in "$dir_path"/*/; do
  # Ensure the entry is a directory
  if [ -d "$subdir" ]; then
    # Count the number of files in the subdirectory
    file_count=$(find "$subdir" -type f | wc -l)

    # Add the file count to the array
    file_counts+=("$file_count")

    # Update the maximum file count
    if [ $file_count -gt $max_files ]; then
      max_files=$file_count
    fi
  fi
done

# Sort the file counts array
IFS=$'\n' sorted_file_counts=($(sort -n <<<"${file_counts[*]}"))

# Calculate the median
array_length=${#sorted_file_counts[@]}

if [ $array_length -eq 0 ]; then
  median=0
else
  middle_index=$((array_length / 2))

  if [ $((array_length % 2)) -eq 0 ]; then
    median=$(bc <<< "scale=2; (${sorted_file_counts[middle_index - 1]} + ${sorted_file_counts[middle_index]}) / 2")
  else
    median=${sorted_file_counts[middle_index]}
  fi
fi

# Calculate the average
if [ $array_length -gt 0 ]; then
  total_files=$(IFS=+; bc <<< "${file_counts[*]}")
  average_files=$(bc <<< "scale=2; $total_files / $array_length")
else
  average_files=0
fi

# Calculate the threshold
threshold=$((max_files - 20))
if [ $(bc <<< "$threshold > $median") -eq 1 ] && [ $(bc <<< "$threshold > $average_files") -eq 1 ]; then
  min_files=$threshold
else
  min_files=0
fi

# Create a temporary directory to store the selected .mp4 files
temp_dir=$(mktemp -d)

echo "Copying selected .mp4 files..."
# Copy .mp4 files from the selected directories to the temporary directory
for subdir in "$dir_path"/*/; do
  # Ensure the entry is a directory
  if [ -d "$subdir" ]; then
    # Count the number of files in the subdirectory
    file_count=$(find "$subdir" -type f | wc -l)

    if [ $file_count -ge $min_files ]; then
      # Copy all .mp4 files in the subdirectory to the temporary directory
      find "$subdir" -type f -iname "*.mp4" -exec cp {} "$temp_dir" \; >/dev/null 2>&1
    fi
  fi
done

# Create a .zip file containing the .mp4 files
echo "Compressing .mp4 files into a zip file..."
mkdir -p /root/log  # <-- This line has been added to create the log directory if it doesn't exist.
zip_file="/root/log/mp4_files.zip"
zip -j "$zip_file" "$temp_dir"/*.mp4 >/dev/null 2>&1

# Remove the temporary directory
rm -rf "$temp_dir"
"""

# Run the download.sh content using Python
with tempfile.NamedTemporaryFile(mode="w", delete=False) as temp_script_file:
    temp_script_file.write(download_sh)
    temp_script_file.flush()

subprocess.run(["bash", temp_script_file.name])

os.remove(temp_script_file.name)

# Upload the generated zip file to transfer.sh
zip_file = "/root/log/mp4_files.zip"

if Path(zip_file).is_file():
    print(f"Uploading {zip_file} to transfer.sh...")

    try:
        result = subprocess.run(["curl", "--upload-file", zip_file, "https://transfer.sh/mp4_files.zip"], capture_output=True, text=True)
        download_link = result.stdout.strip()

        print(f"Download the file by accessing the following link:")
        print(download_link)
    except Exception as e:
        print("An error occurred while uploading the file to transfer.sh:")
        print(e)

else:
    print(f"The zip file {zip_file} was not found.")
