import socket, os

#host to listen on
host = "192.168.2.14"

#create a new socket and bind it to the public interface
if os.name == "nt":
	socket_protocol = socket.IPPROTO_IP
else:
	socket_protocol = socket.IPPROTO_ICMP

with socket.socket(socket.AF_INET, socket.SOCK_RAW, socket_protocol) as sniffer:
	sniffer.bind((host, 0))

	#we want the IP headers included in the capture
	sniffer.setsockopt(socket.IPPROTO_IP, socket.IP_HDRINCL, 1)

	#if we're using Windows, we need to send an IOCTL to set up promiscuous mode
	if os.name == "nt":
		sniffer.ioctl(socket.SIO_RCVALL, socket.RCVALL_ON)
		
	#read a single packet
	for i in range(10): print(sniffer.recvfrom(65565), end='\n\n')

	#if we're using Windows, turn off promiscuous mode
	if os.name == "nt":
		sniffer.ioctl(socket.SIO_RCVALL, socket.RCVALL_OFF)

#--------------------------------------------------------------------------------------#
'''
The difference between Windowsand Linux is that Windows will allow us tosniff
all incoming packets regardless of protocol,whereas Linux forces us to specify 
that we are sniffing ICMP.

Promiscuousmode requires administrative privileges on Windows and root on Linux.

If we are using Windows, we perform the additional step of sending an IOCTL to the 
network card driver to enable promiscuous mode.
'''