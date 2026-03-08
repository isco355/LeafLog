# Farmer-friendly dashboards project

## Zigbee2MQTT server portal http://10.0.0.31:8080

## ssh config
```ssh-config
Host pi
  HostName pi.local
  User mdelgado9286
  IdentityFile ~/.ssh/id_ed25519
  ForwardAgent yes
```
# Docker cheatsheet
Build images
```bash
docker compose build
```
Run docker containers in the background
```bash
docker compose up -d
```
Watch containers
```bash 
watch -n 0.1 docker ps
```
Monitor a container like zigbee2mqtt
```bash
docker compose logs -f zigbee2mqtt
```

# Misc useful commands
restart ssh agent
```bash
eval "$(ssh-agent -s)"
```
