# Linux server / rasberry pi server:


- Connection to wifi
- Creating a ssh server
- Creating a web server
- Creating a samba share
- Creating a daemon (music player)
- Creating a git-server  
- Using the rasberry pi as an access point
- Projects:
    - Alarm clock
    - Control electrical switch




## Connect to a wireless network
edit /etc/network/interfaces

Notes:
- manual: you need to activate the connection to the accesspoint my doing ifconfig wlan0 up , try also ifdown wlan0 and ifup wlan0
- dhcp: the connection should be automatic
- static: a bit more complicated


set to

    allow-hotplug wlan0
    iface wlan0 inet dhcp
        wpa-ssid "MyNetworkName"
        wpa-psk  "MyPassword"

or 
    allow-hotplug wlan0
    iface wlan0 inet manual
        wpa-conf /etc/wpa_supplicant/wpa_supplicant.conf

where the wpa_supplicant.conf file is:
    network={
        ssid="MyNetworkName"
        psk="MyPassword"
        key_mgmt=WPA-PSK
    }

or
    allow-hotplug wlan0
    iface wlan0 inet static
        address 192.168.1.10 
        netmask 255.255.255.0
        gateway 192.168.1.1
        network 192.168.1.0
        broadcast 192.168.1.255
        wpa-conf /etc/wpa_supplicant/wpa_supplicant.conf

## Creating a ssh server 


## Creating a web server 
See webserver/ with setup script and conf files


config in /etc/nginx/ and /etc/nginx/sites-available/default

You can adapt the root, I use /www/site as a symlink to somewhere in the home directory
This forlder needs to be part of the www-data group



## Creating a samba share
see samba-server/ and setup script to automate this


## Creating a daemon
See daemon/ with setup script and conf files

## Creating a git-server
See git-server

On the server side

    apt-get install git
    mkdir /path/repository.git 
    cd /path/repository.git
    git init --bare

On the client side
    git init
    git remote add pi user@IP:/path/repositoty.git




## Using the pi as an access point

See access_point/ and setup script to automate this

    apt-get install hostapd # to create a hotspot
    apt-get install dnsmasq # easy to use DHCP and DNS server

### Configure a static IP for the wlan0 interface
    vim /etc/dhcpcd.conf

        interface wlan0
        static ip_address=192.168.0.10/24
        nohook wpa_supplicant
        #denyinterfaces eth0
        #denyinterfaces wlan0

### Configure the DHCP server (dnsmasq)
The idea of a DHCP server is to dynamically distribute network configuration parameters, such as IP addresses, for interfaces and services.

    vim /etc/dnsmasq.conf
        # providing ip addressses between 11 and 30 for the wlan0 interface
        interface=wlan0
        dhcp-range=192.168.0.11,192.168.0.30,255.255.255.0,24h

### Configure the access point host software (hoastapd)
    vim /etc/hostapd/hostapd.conf
        interface=wlan0
        driver=nl80211
        hw_mode=g
        channel=7
        wmm_enabled=0
        macaddr_acl=0
        auth_algs=1
        ignore_broadcast_ssid=0
        wpa=2
        wpa_key_mgmt=WPA-PSK
        wpa_pairwise=TKIP
        rsn_pairwise=CCMP
        ssid=NETWORK
        wpa_passphrase=PASSWORD
        #bridge=br0

    vim /etc/default/hostapd
        DEMON_CONF="/etc/hostapd/hostapd.conf"



### masquerade for outbound traffic on eth0:
Edit /etc/sysctl.conf and uncomment this line:

        net.ipv4.ip_forward=1

 sudo iptables -t nat -A  POSTROUTING -o eth0 -j MASQUERADE

 Save the iptables rule.

 sudo sh -c "iptables-save > /etc/iptables.ipv4.nat"

 Edit /etc/rc.local and add this just above "exit 0" to install these rules on boot.

 iptables-restore < /etc/iptables.ipv4.nat





### reboot
running iwconfig should show that wlan0 is in mode "Master"

### restart services
service dhcpcd restart
service hostapd restart



