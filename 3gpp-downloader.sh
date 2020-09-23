#!/bin/bash
# A script for downloading 3gpp specifications

# Download document, unzip it and remove zip file

# Get specification to download from user
read  -p "Type the specification number that you want to download: " specification

# Get the Series of the Specification
IFS=\. read -a specarr<<<"$specification"
series=${specarr[0]}

# Download url
specification_page_url="https://www.3gpp.org/ftp/Specs/archive/${series}_series/$specification"

# Get table entries
wget -O tmp_html -q $specification_page_url

# Remove all html except the download links
sed -i '1,/tbody/d' tmp_html #remove everything before first occurance of tbody
sed -i '1,/\/tbody/!d' tmp_html #remove everything after first occurance of \tbody
sed -n -i 's/.*href="\([^"]*\).*/\1/p' tmp_html #remove everything except hrefs in html file

latest_specification_url=$(tail -n 1 tmp_html)

rm tmp_html

wget -O tmp.zip -q $latest_specification_url
unzip -q tmp.zip
rm tmp.zip

#TODO:
# * Handle bad user input
#   * Non 3gpp specifications?
#   * wget timeouts etc?
# * Some printouts about what's going on?
# * Make script more maintanable!!!!!!!!
# * Create spec number flag for user to input number, fallback to prompt if no flag is entered
# * Create a version flag for user to specify which version of the specification is desired
# * Make script properly documented (man page)
