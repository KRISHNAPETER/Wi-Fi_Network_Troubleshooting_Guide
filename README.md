# Wi-Fi & Network Troubleshooting Guide

Common problems, step-by-step fixes, commands and a diagnostic flowchart.

## About

This handbook covers the most common Wi-Fi and LAN problems faced by home users and small offices, with a repeatable way to find and fix each one. It is written for desktop support and network support work.

**Contents:** `Wi-Fi_Network_Troubleshooting_Guide.pdf` (full handbook) and `network_check.py` (automated connectivity check).

## Troubleshooting method

1. Identify the problem: what exactly is not working, for whom, and since when?
2. Check the physical layer first: cables, link lights, Wi-Fi switch, router power.
3. Isolate: one device or all devices? One website or all websites?
4. Test with commands (ping, ipconfig, nslookup) and go layer by layer.
5. Fix one thing at a time, then test again.
6. Verify the fix and document what you did.

## Network basics

| Term | Meaning |
|---|---|
| IP address | Unique address of a device on the network (e.g. 192.168.1.10). |
| Subnet mask | Tells which part of the IP is the network and which is the host (e.g. 255.255.255.0). |
| Default gateway | The router's IP; the way out of the local network. |
| DNS | Converts names (google.com) into IP addresses. |
| DHCP | Automatically gives devices an IP, mask, gateway and DNS. |
| APIPA (169.254.x.x) | Self-assigned address when no DHCP server answers. |
| TCP vs UDP | TCP is reliable and connection-based (web, email). UDP is faster, no guarantee (video calls, DNS queries). |
| 2.4 GHz vs 5 GHz | 2.4 GHz has longer range but is slower and crowded. 5 GHz is faster but has shorter range. |

### OSI layers (troubleshooting view)

| Layer | Examples | Typical problems |
|---|---|---|
| 7 Application | HTTP, DNS, DHCP | Website or DNS errors |
| 4 Transport | TCP, UDP | Ports blocked by firewall |
| 3 Network | IP, ICMP (ping) | Wrong IP, gateway, routing |
| 2 Data Link | Ethernet, Wi-Fi, MAC | Wi-Fi not connecting, switch port |
| 1 Physical | Cables, radio signal | Cable fault, weak signal |

## Problems and fixes

### 1. No internet, but Wi-Fi shows connected

**Symptom:** Wi-Fi icon shows connected but websites do not open.

**Possible causes:** ISP or modem outage; Router lost its WAN connection; DNS failure; Wrong or missing gateway

**Steps to check:**
1. Check if other devices on the same Wi-Fi also have no internet.
2. Ping the gateway (router). If it fails, the problem is the local connection.
3. Ping 8.8.8.8. If it works but names fail, it is a DNS problem (see Problem 5).
4. If 8.8.8.8 fails but the gateway works, the problem is the router/ISP side.

**Fix:**
- Restart modem and router (off 30 seconds, then on).
- Check the WAN/Internet light on the router.
- Call the ISP if the WAN light is red or off.

**Commands:**
```
ping 192.168.1.1
ping 8.8.8.8
ping google.com
ipconfig /all
```

### 2. Cannot connect to Wi-Fi

**Symptom:** Network is visible but the device will not connect, or keeps asking for the password.

**Possible causes:** Wrong password; Saved profile is corrupted; Band mismatch (2.4/5 GHz); MAC filtering on the router; Router has reached its device limit

**Steps to check:**
1. Re-enter the password carefully (check Caps Lock).
2. Forget the network and connect again.
3. Try the other band (2.4 GHz or 5 GHz).
4. Check if the router has MAC filtering or a device limit.
5. Test with another device to see if the issue is the router or the device.

**Fix:**
- Forget and reconnect.
- Update or reinstall the Wi-Fi adapter driver.
- Restart the router.
- Remove MAC filter entry or raise the device limit.

**Commands:**
```
netsh wlan show profiles
netsh wlan delete profile name="WiFiName"
netsh wlan show interfaces
```

### 3. Limited connectivity / 169.254.x.x IP (APIPA)

**Symptom:** 'Limited or no connectivity' message; ipconfig shows an address starting with 169.254.

**Possible causes:** DHCP server (router) not responding; DHCP disabled on router; Bad cable or weak Wi-Fi signal; Adapter problem

**Steps to check:**
1. Run ipconfig /all and confirm the 169.254 address.
2. Check the cable or Wi-Fi signal.
3. Release and renew the IP.
4. Log in to the router and confirm DHCP is enabled and has free addresses.

**Fix:**
- ipconfig /release then ipconfig /renew.
- Restart the router.
- Enable DHCP on the router, or set a static IP temporarily.

**Commands:**
```
ipconfig /all
ipconfig /release
ipconfig /renew
```

### 4. IP address conflict

**Symptom:** 'Another device on the network has the same IP address'; connection drops now and then.

**Possible causes:** Two devices with the same static IP; A static IP inside the DHCP range; Old DHCP lease

**Steps to check:**
1. Note the IP address shown in the error.
2. Run arp -a to see which MAC addresses are using it.
3. Identify the other device and check whether it uses a static IP.

**Fix:**
- Set the PC to obtain an IP automatically.
- Give static devices addresses outside the DHCP range.
- Release and renew, or use DHCP reservation on the router.

**Commands:**
```
arp -a
ipconfig /all
ipconfig /release
ipconfig /renew
```

### 5. DNS error: sites do not open but ping works

**Symptom:** 'DNS_PROBE_FINISHED_NO_INTERNET' or 'server not found'; ping 8.8.8.8 works but ping google.com fails.

**Possible causes:** ISP DNS server down; Wrong DNS settings; Corrupt DNS cache

**Steps to check:**
1. Ping 8.8.8.8 (works) and ping google.com (fails): confirms DNS.
2. Run nslookup google.com and see if a server answers.
3. Check which DNS server the PC is using in ipconfig /all.

**Fix:**
- ipconfig /flushdns.
- Set DNS manually to 8.8.8.8 and 1.1.1.1.
- Restart the router.

**Commands:**
```
nslookup google.com
ipconfig /flushdns
ipconfig /all
```

### 6. Slow internet

**Symptom:** Pages load slowly, videos buffer, downloads are slow.

**Possible causes:** Weak Wi-Fi signal; Too many devices connected; Channel interference; Background downloads or updates; ISP speed problem

**Steps to check:**
1. Run a speed test on a wired and a Wi-Fi device and compare.
2. Check signal strength and distance from the router.
3. See how many devices are connected and what is using bandwidth.
4. Look at the Wi-Fi channel; crowded channels cause interference.

**Fix:**
- Move closer to the router or use 5 GHz.
- Change the Wi-Fi channel (1, 6 or 11 on 2.4 GHz).
- Disconnect unused devices.
- Restart the router; contact the ISP if the wired speed is also low.

**Commands:**
```
ping -t 8.8.8.8 (watch time=)
netsh wlan show interfaces (signal %)
netstat -e
```

### 7. Cannot reach the default gateway

**Symptom:** Ping to the router fails or times out; no access to the router page.

**Possible causes:** Wrong gateway setting; Wrong subnet mask; Cable/port fault; Router down

**Steps to check:**
1. Run ipconfig /all and compare the IP, mask and gateway: they must be in the same network.
2. Ping the gateway; if it fails, check the cable or Wi-Fi.
3. Run tracert 8.8.8.8 and see where the first hop fails.

**Fix:**
- Switch the adapter back to automatic (DHCP) settings.
- Correct the static gateway or subnet mask.
- Replace the cable or try another router port.

**Commands:**
```
ipconfig /all
ping <gateway IP>
tracert 8.8.8.8
route print
```

### 8. Network cable or switch port not working

**Symptom:** No link light, 'Network cable unplugged' message, or connection that keeps dropping.

**Possible causes:** Damaged or loose cable; Faulty port on switch/router; Faulty network card; Duplex or speed mismatch

**Steps to check:**
1. Check that the cable is firmly seated at both ends and the link lights are on.
2. Swap the cable with a known good one.
3. Try a different port on the switch or router.
4. Test the cable on another PC to isolate PC versus cable.

**Fix:**
- Replace the cable or re-crimp the connector.
- Move to a working port.
- Update or reinstall the NIC driver.
- Reset adapter speed/duplex to Auto.

**Commands:**
```
ipconfig /all
netsh interface show interface
Device Manager > Network adapters
```

### 9. Printer or shared folder not reachable on the LAN

**Symptom:** Cannot print to a network printer or open \\PC-NAME shared folders.

**Possible causes:** Devices on different subnets; Firewall blocking file/printer sharing; Network profile set to Public; Printer IP changed

**Steps to check:**
1. Ping the printer or PC by IP address.
2. If the IP works but the name does not, it is a name resolution problem.
3. Check that the network profile is Private and file/printer sharing is on.
4. Check whether the printer got a new IP from DHCP.

**Fix:**
- Set the network profile to Private.
- Allow File and Printer Sharing in the firewall.
- Give the printer a static IP or a DHCP reservation.
- Re-add the printer using its IP address.

**Commands:**
```
ping <printer IP>
ping <PC-NAME>
net view
arp -a
```

### 10. VPN not connecting

**Symptom:** VPN client shows 'connecting' forever or fails with an error.

**Possible causes:** No base internet connection; Wrong credentials or expired password; Firewall or ISP blocking VPN ports; Outdated VPN client

**Steps to check:**
1. Confirm normal internet works first (ping 8.8.8.8).
2. Check username, password and server address.
3. Try another network (for example a mobile hotspot) to see if the current network blocks the VPN.
4. Check the client version and the logs for the exact error.

**Fix:**
- Fix credentials or reset the password.
- Update or reinstall the VPN client.
- Allow the VPN in the firewall.
- Contact the network admin if the server side is down.

**Commands:**
```
ping 8.8.8.8
nslookup <vpn server name>
tracert <vpn server>
```

## Command cheat sheet

| Windows | Linux | Purpose |
|---|---|---|
| `ping <host>` | `ping <host>` | Test whether a host replies |
| `ipconfig /all` | `ip a  /  ifconfig` | Show IP, mask, gateway, DNS, MAC |
| `ipconfig /release, /renew` | `sudo dhclient -r / sudo dhclient` | Get a new IP from DHCP |
| `ipconfig /flushdns` | `resolvectl flush-caches` | Clear the DNS cache |
| `nslookup <name>` | `dig <name>` | Test DNS resolution |
| `tracert <host>` | `traceroute <host>` | Show the path and where it breaks |
| `netstat -an` | `ss -tuln` | Show open ports and connections |
| `arp -a` | `ip neigh` | Show IP-to-MAC mappings on the LAN |
| `route print` | `ip route` | Show the routing table and gateway |
| `netsh wlan show interfaces` | `iwconfig / nmcli dev wifi` | Wi-Fi signal, channel, SSID |

## Diagnostic flowchart (the ping ladder)

Work from top to bottom. The first step that fails shows where the problem is.

1. **Ping 127.0.0.1**: FAIL: network adapter / TCP-IP stack problem. Reinstall driver, netsh int ip reset.
2. **Ping default gateway**: FAIL: local link problem. Check Wi-Fi/cable, IP settings, DHCP.
3. **Ping 8.8.8.8**: FAIL: router/ISP problem. Check WAN light, restart modem, call ISP.
4. **Ping google.com**: FAIL: DNS problem. Flush DNS, change DNS servers.

If all four pass, the network is fine; check the website or application itself.

## Router basics

- Find the router address: it is the default gateway in ipconfig /all (often 192.168.1.1 or 192.168.0.1).
- Open it in a browser and log in. Change the default admin password straight away.
- Change the Wi-Fi name (SSID) and set a strong WPA2 or WPA3 password.
- Check the DHCP range and keep static devices outside it.
- Choose a less crowded Wi-Fi channel (1, 6 or 11 for 2.4 GHz).
- Update the firmware regularly; back up the settings before a factory reset.

## Automated check

```
python network_check.py
```

Sample output:

```
=== Network Check ===

  [PASS] Loopback (127.0.0.1) - TCP/IP stack on this PC
  [PASS] Default gateway (192.168.1.1) - your router
  [PASS] Public IP (8.8.8.8) - internet reachable
  [FAIL] DNS lookup (google.com) - name resolution

--- Diagnosis ---
Internet works but names do not resolve. This is a DNS problem.
```

## Screenshots

Add your own screenshots to a `screenshots/` folder (ipconfig /all, ping tests, tracert, the script output) and link them here.

## Author

Krishnakumar C | [GitHub](https://github.com/KRISHNAPETER) | [LinkedIn](https://www.linkedin.com/in/krishna-kumar-c-43722a3b9)
