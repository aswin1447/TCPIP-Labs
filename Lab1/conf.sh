# ===== PC1 =====
ip link set PC1-eth0 up
su
ip addr add 10.10.14.1/24 dev PC1-eth0
ip -6 addr add fd24:ec43:12ca:c001:14::1/80 dev PC1-eth0
ip addr del 10.0.0.1 dev PC1-eth0
ip route add default via 10.10.14.4
ip -6 route add default via fd24:ec43:12ca:c001:14::4
## MITM


# ===== PC2 =====
ip link set PC2-eth0 up
su
ip addr add 10.10.24.1/24 dev PC2-eth0
ip -6 addr add fd24:ec43:12ca:c001:24::2/80 dev PC2-eth0
ip addr del 10.0.0.2 dev PC2-eth0
ip route add default via 10.10.24.4
ip -6 route add default via fd24:ec43:12ca:c001:24::4
## MITM

# ===== PC3 =====
ip link set PC3-eth0 up
su
ip addr add 10.10.34.3/24 dev PC3-eth0
ip -6 addr add fd24:ec43:12ca:c001:34::3/80 dev PC3-eth0
ip addr del 10.0.0.3 dev PC3-eth0
		ip route add default via 10.10.34.4
ip -6 route add default via fd24:ec43:12ca:c001:34::4
## MITM
echo 1 > /proc/sys/net/ipv4/ip_forward
iptables -t nat -A PREROUTING -p icmp -s 10.10.24.2 -d 10.10.34.3 -j
DNAT --to-destination 10.10.14.1
iptables -t nat -A POSTROUTING -o PC3-eth0 -s 10.10.24.2 -d
10.10.14.1 -j MASQUERADE

# ===== PC4 =====
ip link set PC4-eth0 up
ip link set PC4-eth1 up
ip link set PC4-eth2 up
su
ip addr del 10.0.0.4 dev PC4-eth0
ip addr add 10.10.14.4/24 dev PC4-eth0   # pas trop compris pourquoi /24
ip addr add 10.10.24.4/24 dev PC4-eth1
ip addr add 10.10.34.4/24 dev PC4-eth2
ip -6 addr add fd24:ec43:12ca:c001:14::4/80 dev PC4-eth0
ip -6 addr add fd24:ec43:12ca:c001:24::4/80 dev PC4-eth1
ip -6 addr add fd24:ec43:12ca:c001:34::4/80 dev PC4-eth2
echo 1 > /proc/sys/net/ipv4/ip_forward
echo 1 > /proc/sys/net/ipv6/conf/all/forwarding
## MITM
sudo bash mitmConfig.sh
iptables -t nat -A POSTROUTING -o PC4-eth2 -j MASQUERADE
iptable -F
iptables -t nat -F
iptables -t nat -A PREROUTING -d 10.10.14.1 -j DNAT --to-destination
10.10.34.3
iptable -F
iptables -t nat -F
iptables -t nat -A PREROUTING -p icmp -s 10.10.24.2 -d 10.10.14.1 -j
DNAT --to-destination 10.10.34.3
