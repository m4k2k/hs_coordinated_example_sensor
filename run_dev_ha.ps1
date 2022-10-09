
$conf_folder = 'C:\Dev\Proj\ha_dev\ha_conf'


$log_filepath = "$conf_folder\home-assistant.log"
$log_file = Get-Item -Path $log_filepath
Rename-Item -Path $log_file.FullName -NewName "$($log_file.BaseName)_$(get-date -f yyyy-MM-dd_H-mm_s)$($log_file.Extension)"
New-Item -Path $log_file.Directory -Name $log_file.Name -ItemType File

docker run -it --rm `
    -e "TZ=Europe/Berlin" `
    --name "devha" `
    -p 8123:8123 `
    -p 6712:6712 `
    --mount type=bind,source="$conf_folder",target="/config" `
    homeassistant/home-assistant

# http://localhost:8123/

# usr: tempdevinstall
# pwd: §g23/(egt3253EHF


# python -m debugpy --connect 127.0.0.1:6712
