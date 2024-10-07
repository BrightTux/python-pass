#!/bin/bash

base="/home/tux/.password-store/"
fzf_params="--height=50 --border=bold --margin=35%"

# Function to list possible passwords
iter_pass() {
    # Get the list of possible pass
    find "$base" -type f -name "*.gpg" | sed "s|$base||"
}

# Function to cleanup clipboard after 5 seconds
cleanup() {
    sleep 5; echo "cleared" | xclip -sel clip
}

# Get the intended item using fzf
result=$(iter_pass | fzf $fzf_params)

# Check if a result was selected
if [ -z "$result" ]; then
    cleanup
    exit 0
fi

# Now, decrypt it using gpg
decrypted_output=$(gpg --decrypt "$base$result" 2>/dev/null)

# Create an associative array to hold the results
declare -A dict_result

# Process the decrypted output
while IFS= read -r line; do
    if [[ $line == *:* ]]; then
        key="${line%%:*}"
        value="${line#*:}"
        dict_result["$key"]="$value"
    else
        dict_result["pass"]="$line"
    fi
done <<< "$decrypted_output"

# Get the target using fzf
target=$(printf "%s\n" "${!dict_result[@]}" | fzf --multi $fzf_params)

# Check if a target was selected
if [ -z "$target" ]; then
    cleanup
    exit 0
fi

# Loop through the selected targets and copy to clipboard
for t in $target; do
    echo "${dict_result[$t]}" | xclip -sel clip
done
