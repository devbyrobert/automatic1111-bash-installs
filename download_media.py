import os
import http.server
import socketserver
from pathlib import Path
import socket

# Function to get the server's IP address
def get_server_ip():
    try:
        hostname = socket.gethostname()
        ip_address = socket.gethostbyname(hostname)
        return ip_address
    except:
        return "127.0.0.1"

# Download.sh content (modified to exclude shebang line)
download_sh = """
# Install required packages
echo "Installing required packages..."
apt-get update >/dev/null
apt-get install -y bc zip >/dev/null

dir_path="/root/stable-diffusion-webui/outputs/img2img-images"
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
zip_file="/root/mp4_files.zip"
zip -j "$zip_file" "$temp_dir"/*.mp4 >/dev/null 2>&1

# Remove the temporary directory
rm -rf "$temp_dir"

# Run the download.sh content using Python
os.system("bash -c '%s'" % download_sh)

# Serve the generated zip file over HTTP
zip_file = "/root/mp4_files.zip"

if Path(zip_file).is_file():
    os.chdir(os.path.dirname(zip_file))

    PORT = 8000
    Handler = http.server.SimpleHTTPRequestHandler
    httpd = socketserver.TCPServer(("", PORT), Handler)

    server_ip = get_server_ip()

    print(f"Serving {zip_file} on port {PORT}")
    print(f"Download the file by accessing http://{server_ip}:{PORT}/{os.path.basename(zip_file)} on your local computer.")
    httpd.serve_forever()
else:
    print(f"The zip file '{zip_file}' was not found.")
