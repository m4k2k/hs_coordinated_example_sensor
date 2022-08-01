
$conf_folder = 'C:\Dev\Proj\ha_dev\ha_conf'

docker run -it --rm `
    -e "TZ=Europe/Berlin" `
    --name "devha" `
    -p 8123:8123 `
    --mount type=bind,source="$conf_folder",target="/config" `
    homeassistant/home-assistant

# http://localhost:8123/

# usr: tempdevinstall
# pwd: §g23/(egt3253EHF


