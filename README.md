# Probe Hunter


### Insecure usage of less common SSIDs

By using unique or unusual SSID names, we make it easier to identify our location if it has been collected by [Wigle](http://wigle.net/). This would allow an attacker to know the address or usual places of the people around. Although [Wigle](http://wigle.net/) allows you to remove the SSID from the site for privacy reasons, it is more than advisable to use common SSIDs to make it difficult to associate a device with a single location.


### What are Probe Requests?

Probe requests are an 802.11 WIFI packet type that function to automatically connect network devices to the wireless access points (APs) that they have previously associated with. Whenever a phone, computer, or other networked device has Wi-Fi enabled, but is not connected to a network, it is constantly "probing"; openly broadcating the network names (SSIDs) of previously connected APs. Because wireless access points have unique and often personal network names, it is easy to identify the device owner by recognizing the names of networks they frequently connect to.


### Enable Location tracking

1) Request your Authentication API token in Wigle: [http://wigle.net/](http://wigle.net/)

2) Add your Wigle Auth Token to `Wigle.py`


### Dependencies 

- tcpdump
- python3
	- subprocess
	- signal
	- threading
	- colorclass
	- terminatables