#!/bin/sh

# Run this in the project directory on a fresh installation
# this will clear the Downloads/ folder and reset the Downloads/downloads.json file

cd Downloads/ && rm -rf *
echo "Downloads Cleared"
echo [] > downloads.json
echo "Created downloads.json"