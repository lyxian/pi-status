# pi-status

Description: This app will allow devices to update their status to somewhere

Requirements:

- Client-side :
  - how to verify connectivity
  - generate unique name for devices
    > ifconfig -a wlan0 | grep 'ether ' (linux)
    > ipconfig /all >>> Wi-Fi >>> Physical Address (win)
    > netsh wlan show interfaces >>> Physical Address (win)
- Server-side :
  - create new sheet if not existing
    - use simple sheet / template
  - update summary sheet
    - collate then update
    - update individually
    - link to sheet cells
  - .
- Misc :
  - update config-init.sh to :
    - include json secrets (√)
    - ensure cryptography installed

##Packages (list required packages & run .scripts/python-init.sh)
cryptography==37.0.4
oauth2client==4.1.3
gspread==3.7.0
pendulum==2.1.2
requests==2.28.1
pyyaml==6.0
flask==2.2.2
pytest==7.1.2
##Packages
