USB_PATH=$(lsusb | grep -i newae | awk '{print $2 "/" $4}' | tr -d ':')

if [ -z "$USB_PATH" ]; then
    echo "Aucun périphérique USB 'newae' détecté."
    echo "Faut faire la manip bash (cf le readme)."
else
    echo "Périphérique détecté : /dev/bus/usb/$USB_PATH"
    sudo chmod 666 /dev/bus/usb/$USB_PATH
fi