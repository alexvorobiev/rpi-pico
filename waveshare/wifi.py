from time import sleep
import network

# https://docs.micropython.org/en/latest/library/network.WLAN.html
netstat_err = {
    network.STAT_WRONG_PASSWORD: "STAT_WRONG_PASSWORD",
    network.STAT_NO_AP_FOUND:    "STAT_NO_AP_FOUND",
    network.STAT_CONNECT_FAIL:   "STAT_CONNECT_FAIL"
}

def connect(ssid, password):
    """
    Connect to wifi.

    Parameters
    ----------
    ssid: string
        SSID
    password: string
        password

    """
    # Network interface object
    wlan = network.WLAN(network.STA_IF)
    # Activate ("up") the interface
    wlan.active(True)

    # Try a few times to detect the SSID
    success = False
    for i in range(10):
        s = wlan.scan()
        success = ([i for i in range(len(s)) if str(s[i][0], 'utf-8') == ssid] != [])
        if success:
            print('SSID '+ssid+' detected!')
            break
        sleep(1)

    if not success:
        raise RuntimeError('SSID '+ssid+' not found!')

    # Try a few times to connect to the SSID
    success = False
    for i in range(10):
        wlan.connect(ssid, password)

        # Wait until connected
        for j in range(10):
            if wlan.status() < 0 or wlan.isconnected():
                break
            sleep(1)

    if not wlan.isconnected():
        raise RuntimeError('Connection failed: '+netstat_err[wlan.status()])

    return wlan.ifconfig()
