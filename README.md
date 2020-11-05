# autofs-standby
Monitors the state of an autofs share and puts USB hubs into standby mode whenever possible


## Installation
### Prerequisites
1. Download and install https://github.com/mvp/uhubctl (make sure you can turn the correct USB hub on and off)
1. Install `autofs`: `sudo apt install autofs`

### Configure AutoFS
1. Create the directory where the share is mounted: `sudo mkdir /autofs`
1. Adjust the uuid of the drive to `./auto.vault.sh` (can be checked with `sudo lsblk -f`)
1. Copy the files `./auto.vault` and `./auto.vault.sh` to `/etc` and chown them to root
1. Add the following line to `/etc/auto.master`: `/autofs program:/etc/auto.vault.sh --timeout=300 --ghost` (make sure there is an empty line at the end of the config, otherwise the daemon will not load properly)
1. Restart `autofs`: `sudo service autofs restart`

### Create a Standby Watchdog Service
1. Copy `standby_watchdog.service` to `/etc/systemd/system/`: `sudo cp standby_watchdog.service /etc/systemd/system/`
1. Start the service: `sudo systemctl start standby_watchdog`
1. Start the service on boot: `sudo systemctl enable standby_watchdog`
1. Register a service to run `standby_watchdog.py` in the background


## Testing / Troubleshooting
1. Check if USB can be powered on and off using `uhubctl`:
1.1 power on: `sudo uhubctl -l 1-1 -a on`
1.1 power off: `sudo uhubctl -l 1-1 -a off`
1. Access the share: `ls -la /autofs/vault`
1. Monitor `standby_watchdog.service` to see if the mounted share is detected.
1. Wait the timeout specified in `auto.vault.sh` and try to access the share again.
1. Wait the timeout specified in `standby_watchdog.py` (`SLEEP_DURATION` * `STANDBY_COUNT` seconds) to check if USB is automatically powered off.
