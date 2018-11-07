# Device to Server Connection Setup

For demonstration of sending data from an IoT Gateway to on central application Server we need to setup an VPN connection from our Endpoint to and central server. 
This enables us to access our devices remotly. 
Since the 1NCE Product is offering a free of charge OpenVPN connection we are going to use this and set up an OpenVPN Client on our central server. 

## Installing OpenVPN Client

Since we are using a CentOS Server we are going to install OpenVPN by running: 

```bash
sudo yum -y install openvpn easy-rsa iptables-services
```

Next we need to download „client.conf“ from 1NCE customer portal (Configuration -> OpenVPN Configuration -> Linux/macOS -> Download client.conf).

Cody "client.conf" to /etc/openvpn

Download „credentials.txt“ from customer portal (Configuration -> OpenVPN Configuration -> Linux/macOS -> 3. Save the following file credentials.txt …).

Copy "credentials.txt" also to /etc/openvpn.

Start the OpenVPN Client by running: 
```bash
sudo openvpn --config /etc/openvpn/client.conf
```

You should see output like the following and also the required routes are added to the server automatically: 

```bash
Mon Aug 27 15:31:45 2018 TUN/TAP device tun0 opened
Mon Aug 27 15:31:45 2018 TUN/TAP TX queue length set to 100
Mon Aug 27 15:31:45 2018 do_ifconfig, tt->ipv6=0, tt->did_ifconfig_ipv6_setup=0
Mon Aug 27 15:31:45 2018 /sbin/ifconfig tun0 10.64.71.XX pointopoint 10.64.71.XX mtu 1500
Mon Aug 27 15:31:45 2018 /sbin/route add -net 10.64.X.X netmask 255.255.255.255 gw 10.64.71.XX
Mon Aug 27 15:31:45 2018 /sbin/route add -net 100.117.XXX.0 netmask 255.255.252.0 gw 10.64.71.XX
Mon Aug 27 15:31:45 2018 GID set to nogroup
Mon Aug 27 15:31:45 2018 UID set to root
Mon Aug 27 15:31:45 2018 Initialization Sequence Completed
```

Verify the setup by pinging your switched on and connected endpoint: 
```bash
ping -c 5 100.91.200.137
```
Remember to change to your IP adress and in case there are problems with the route use the `-I` paramter e.g. `-I tun0 ` to specifiy the desired network interface for the OpenVPN Tunnel. 

