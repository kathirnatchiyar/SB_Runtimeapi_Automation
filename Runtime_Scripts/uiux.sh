#!/bin/bash

sleep 20

folder_path="/opt/SB_Runtimeapi_Automation_Beta/Runtime_Scripts/"
file_name="uiux.txt"

echo "This is some content for the text file." > "$folder_path/$file_name"

echo "Text file '$file_name' created in '$folder_path'"

