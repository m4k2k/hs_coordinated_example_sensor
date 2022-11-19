
docker stop devha

$conf_folder = "$PSScriptRoot\ha_conf"

$log_filepath = "$conf_folder\home-assistant.log"
$old_log_folder = "old_logs"
$log_file = Get-Item -Path $log_filepath
$new_log_file = "$($log_file.BaseName)_$(get-date -f yyyy-MM-dd_H-mm_s)$($log_file.Extension)"
Rename-Item -Path $log_file.FullName -NewName $new_log_file
New-Item -Path $log_file.Directory -Name $log_file.Name -ItemType File
New-Item -Path "$conf_folder\" -Name $old_log_folder -ItemType Directory -ErrorAction Ignore
Move-Item -Path "$conf_folder\$new_log_file" -Destination "$conf_folder\$old_log_folder\"

# remove db folders (delete devices and entitites)
$files_to_clear = @('core.device_registry', 'core.config_entries', 'core.entity_registry')
foreach ($_file in $files_to_clear) {
    Remove-Item -Path "$conf_folder\.storage\$_file" -Force -ErrorAction Continue
}

docker run -it --rm `
    -e "TZ=Europe/Berlin" `
    --name "devha" `
    -p 8123:8123 `
    -p 6712:6712 `
    --mount type=bind,source="$conf_folder",target="/config" `
    homeassistant/home-assistant

# Local address of homeassistant
# http://localhost:8123/

# connect to python inside docker (exposing on port 6712)
# python -m debugpy --connect 127.0.0.1:6712
