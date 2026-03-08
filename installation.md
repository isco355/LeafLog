OS image Ubuntu Server LTS

## Step 1 Update system
```bash
sudo apt update && sudo apt upgrade -y```
## Step 2 Install Docker
Install required dependencies, add Docker's official GPG key and repository, then install Docker:
```bash 
# Install prerequisites
sudo apt install -y ca-certificates curl gnupg

# Add Docker's GPG key
sudo install -m 0755 -d /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | \
  sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg

# Add the Docker repository
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] \
  https://download.docker.com/linux/ubuntu \
  $(lsb_release -cs) stable" | \
  sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

# Install Docker Engine
sudo apt update
sudo apt install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
```
Enable and start Docker
```bash 
sudo systemctl start docker
sudo systemctl enable docker
```
(Optional) Run Docker without sudo
```bash
sudo gpasswd -a $USER docker
newgrp docker
```
Then verify: ```bash docker --version```


# Step 3: Identify Your Zigbee Adapter

Plug in your Zigbee USB adapter and run the following to find its device path:​

```bash
ls /dev/tty*
```
Look for something like /dev/ttyUSB0 or /dev/ttyACM0. Unplug and re-plug the adapter while watching dmesg to confirm the exact path.

# Step 4: Create the Docker Compose Setup

Create a working directory and the Compose file:​

```bash
mkdir -p ~/zigbee2mqtt && cd ~/zigbee2mqtt
mkdir -p zigbee2mqtt-data mosquitto-data
nano docker-compose.yml```

Paste the following into docker-compose.yml, replacing <DEVICENAME>, <ADAPTERTYPE>, and <TIMEZONE> with your values:​
```yaml
services:
  mqtt:
    image: eclipse-mosquitto:2
    restart: unless-stopped
    volumes:
      - "./mosquitto-data:/mosquitto"
    ports:
      - "1883:1883"
      - "9001:9001"
    command: "mosquitto -c /mosquitto-no-auth.conf"

  zigbee2mqtt:
    container_name: zigbee2mqtt
    restart: unless-stopped
    image: koenkk/zigbee2mqtt
    volumes:
      - ./zigbee2mqtt-data:/app/data
      - /run/udev:/run/udev:ro
    ports:
      - 8080:8080
    environment:
      - TZ=America/Los_Angeles
    devices:
      - /dev/ttyUSB0:/dev/ttyUSB0   # ← change to your device
```

# Step 5: Configure Zigbee2MQTT

Create the configuration file:
```bash
nano zigbee2mqtt-data/configuration.yaml
```
```yaml
permit_join: true

mqtt:
  base_topic: zigbee2mqtt
  server: mqtt://mqtt

serial:
  port: /dev/ttyUSB0          # ← your device path
  adapter: zstack             # ← your adapter type

frontend:
  port: 8080

advanced:
  network_key: GENERATE

homeassistant:
  enabled: false              # set true if using Home Assistant
```
