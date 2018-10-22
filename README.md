<h3>Description</h3>

arpspoof.py is a partial clone of Dug Song's dsniff arpspoof tool which redirects packets from a target host (or all hosts) on the LAN intended for another host on the LAN by forging ARP replies.   This  is an extremely effective way of sniffing traffic on a switch.'

<h3>Files</h3>
<ul>
  <li>arpspoof.py</li>
  Primary script for launching attack. Must be run as root. Use Python3 arpspoof.py or chmod +x to run as ./arspoof.py
  Includes a help menu that can be accessed using ./arpspoof.py -h
  <li>Features_Help.png</li>
  A screenshot showing how to run the script in a UNIX terminal, and showing output of ./arpspoof.py -h
  <li>Run.png</li>
  A screenshot showing the script running with a given IP target and host. Use [ctrl+c] to quit.
  <li>Wireshark_Capture.png</li>
  A screenshot showing a packet capture in Wireshark from the attacking (man in the middle) machine which is successfully     
  intercepting ICMP packets from a PING exchange between the target and host.
</ul>
