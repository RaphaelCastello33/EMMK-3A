# Se connecter 

## sous winbash (admin)

```shell
usbipd list # check for busid (2-1)
usbipd detach --busid 2-1
usbipd bind --busid 2-1
usbipd attach --wsl --busid 2-1
```

## sous linux
```shell

lsusb | grep -i newae # check que t'es bien co
ls -l /dev/bus/usb/$(lsusb | grep -i newae | awk '{print $2 "/" $4}' | tr -d :)
# si c'est pas crw-rw-rw- alors faire 
sudo chmod 666 /dev/bus/usb/$(lsusb | grep -i newae | awk '{print $2 "/" $4}' | tr -d :)
ls -l /dev/bus/usb/$(lsusb | grep -i newae | awk '{print $2 "/" $4}' | tr -d :) # check que c'est passé en crw-rw-rw


```