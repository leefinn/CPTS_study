# 

---

There are often times during an assessment when we may be limited to a Windows network and may not be able to use SSH for pivoting. We would have to use tools available for Windows operating systems in these cases. [SocksOverRDP](https://github.com/nccgroup/SocksOverRDP) is an example of a tool that uses `Dynamic Virtual Channels` (`DVC`) from the Remote Desktop Service feature of Windows. DVC is responsible for tunneling packets over the RDP connection. Some examples of usage of this feature would be clipboard data transfer and audio sharing. However, this feature can also be used to tunnel arbitrary packets over the network. We can use `SocksOverRDP` to tunnel our custom packets and then proxy through it. We will use the tool [Proxifier](https://www.proxifier.com/) as our proxy server.

We can start by downloading the appropriate binaries to our attack host to perform this attack. Having the binaries on our attack host will allow us to transfer them to each target where needed. We will need:

1. [SocksOverRDP x64 Binaries](https://github.com/nccgroup/SocksOverRDP/releases)
    
2. [Proxifier Portable Binary](https://www.proxifier.com/download/#win-tab)
    

- We can look for `ProxifierPE.zip`

We can then connect to the target using xfreerdp and copy the `SocksOverRDPx64.zip` file to the target. From the Windows target, we will then need to load the SocksOverRDP.dll using regsvr32.exe.

#### Loading SocksOverRDP.dll using regsvr32.exe

  RDP and SOCKS Tunneling with SocksOverRDP

```cmd-session
C:\Users\htb-student\Desktop\SocksOverRDP-x64> regsvr32.exe SocksOverRDP-Plugin.dll
```

![Command Prompt showing directory listing of SocksOverRDP files. A RegSvr32 dialog confirms successful registration of SocksOverRDP-Plugin.dll.](https://academy.hackthebox.com/storage/modules/158/socksoverrdpdll.png)

Now we can connect to 172.16.5.19 over RDP using `mstsc.exe`, and we should receive a prompt that the SocksOverRDP plugin is enabled, and it will listen on 127.0.0.1:1080. We can use the credentials `victor:pass@123` to connect to 172.16.5.19.

![Command Prompt with Remote Desktop Connection to 172.16.5.19 as user 'victor'. SocksOverRDP plugin enabled, listening on 127.0.0.1:1080.](https://academy.hackthebox.com/storage/modules/158/pivotingtoDC.png)

We will need to transfer SocksOverRDPx64.zip or just the SocksOverRDP-Server.exe to 172.16.5.19. We can then start SocksOverRDP-Server.exe with Admin privileges.

![Terminal showing Socks Over RDP by Balazs Bucsay with a channel opened over RDP.](https://academy.hackthebox.com/storage/modules/158/executingsocksoverrdpserver.png)

When we go back to our foothold target and check with Netstat, we should see our SOCKS listener started on 127.0.0.1:1080.

#### Confirming the SOCKS Listener is Started

  RDP and SOCKS Tunneling with SocksOverRDP

```cmd-session
C:\Users\htb-student\Desktop\SocksOverRDP-x64> netstat -antb | findstr 1080

  TCP    127.0.0.1:1080         0.0.0.0:0              LISTENING
```

After starting our listener, we can transfer Proxifier portable to the Windows 10 target (on the 10.129.x.x network), and configure it to forward all our packets to 127.0.0.1:1080. Proxifier will route traffic through the given host and port. See the clip below for a quick walkthrough of configuring Proxifier.

#### Configuring Proxifier

![GIF showcasing the addition of a SOCKS5 server in Proxifier.](https://academy.hackthebox.com/storage/modules/158/configuringproxifier.gif)

With Proxifier configured and running, we can start mstsc.exe, and it will use Proxifier to pivot all our traffic via 127.0.0.1:1080, which will tunnel it over RDP to 172.16.5.19, which will then route it to 172.16.6.155 using SocksOverRDP-server.exe.

![Desktop with Socks Over RDP terminal, Proxifier showing connection to 172.16.6.155:3389, and Remote Desktop session to 172.16.6.155](https://academy.hackthebox.com/storage/modules/158/rdpsockspivot.png)

#### RDP Performance Considerations

When interacting with our RDP sessions on an engagement, we may find ourselves contending with slow performance in a given session, especially if we are managing multiple RDP sessions simultaneously. If this is the case, we can access the `Experience` tab in mstsc.exe and set `Performance` to `Modem`.

![Remote Desktop Connection settings window showing performance options for a 56 kbps modem. Proxifier Portable lists connections to 172.16.6.155:3389. Command Prompt displays netstat command with port 1080 listening.](https://academy.hackthebox.com/storage/modules/158/rdpexpen.png)

---

Note: When spawning your target, we ask you to wait for 3 - 5 minutes until the whole lab with all the configurations is set up so that the connection to your target works flawlessly.

---
## Question 1

### "Use the concepts taught in this section to pivot to the Windows server at 172.16.6.155 (jason:WellConnected123!). Submit the contents of Flag.txt on Jason's Desktop."

On Pwnbox/`PMVPN`, students need to download `SocksOverRDP` and `Proxifier`:

Code: shell

```shell
wget https://github.com/nccgroup/SocksOverRDP/releases/download/v1.0/SocksOverRDP-x64.zip
wget https://www.proxifier.com/download/ProxifierPE.zip
```

  RDP and SOCKS Tunneling with SocksOverRDP

```shell-session
┌─[us-academy-1]─[10.10.14.17]─[htb-ac413848@pwnbox-base]─[~]
└──╼ [★]$ wget https://github.com/nccgroup/SocksOverRDP/releases/download/v1.0/SocksOverRDP-x64.zip

--2022-08-29 18:52:57--  https://github.com/nccgroup/SocksOverRDP/releases/download/v1.0/SocksOverRDP-x64.zip
Resolving github.com (github.com)... 140.82.121.3
Connecting to github.com (github.com)|140.82.121.3|:443... connected.
HTTP request sent, awaiting response... 302 Found
<SNIP>
Saving to: ‘SocksOverRDP-x64.zip’

SocksOverRDP-x64.zip            100%[======================================================>]  43.15K  --.-KB/s    in 0.001s  

2022-08-29 18:52:58 (36.1 MB/s) - ‘SocksOverRDP-x64.zip’ saved [44183/44183]

┌─[us-academy-1]─[10.10.14.17]─[htb-ac413848@pwnbox-base]─[~]
└──╼ [★]$ wget https://www.proxifier.com/download/ProxifierPE.zip

--2022-08-29 18:53:52--  https://www.proxifier.com/download/ProxifierPE.zip
Resolving www.proxifier.com (www.proxifier.com)... 172.104.17.238
Connecting to www.proxifier.com (www.proxifier.com)|172.104.17.238|:443... connected.
HTTP request sent, awaiting response... 200 OK
Length: 3080345 (2.9M) [application/zip]
Saving to: ‘ProxifierPE.zip’

ProxifierPE.zip                 100%[======================================================>]   2.94M  4.55MB/s    in 0.6s    

2022-08-29 18:53:53 (4.55 MB/s) - ‘ProxifierPE.zip’ saved [3080345/3080345]
```

Afterward, students need to unzip the two files:

Code: shell

```shell
unzip SocksOverRDP-x64.zip
unzip ProxifierPE.zip
```

  RDP and SOCKS Tunneling with SocksOverRDP

```shell-session
┌─[us-academy-1]─[10.10.14.21]─[htb-ac413848@pwnbox-base]─[~]
└──╼ [★]$ unzip SocksOverRDP-x64.zip

Archive:  SocksOverRDP-x64.zip
  inflating: SocksOverRDP-Plugin.dll  
  inflating: SocksOverRDP-Server.exe
┌─[us-academy-1]─[10.10.14.21]─[htb-ac413848@pwnbox-base]─[~]
└──╼ [★]$ unzip ProxifierPE.zip
Archive:  ProxifierPE.zip
   creating: Proxifier PE/
  inflating: Proxifier PE/Helper64.exe  
  inflating: Proxifier PE/Proxifier.exe  
  inflating: Proxifier PE/ProxyChecker.exe  
  inflating: Proxifier PE/PrxDrvPE.dll  
  inflating: Proxifier PE/PrxDrvPE64.dll
```

Subsequently, students need to connect to the spawned Windows pivot host using `xfreerdp`, utilizing the credentials `htb-student:HTB_@cademy_stdnt!`:

Code: shell

```shell
xfreerdp /v:STMIP /u:htb-student /p:HTB_@cademy_stdnt!
```

  RDP and SOCKS Tunneling with SocksOverRDP

```shell-session
┌─[us-academy-1]─[10.10.14.17]─[htb-ac413848@pwnbox-base]─[~]
└──╼ [★]$ xfreerdp /v:10.129.113.142 /u:htb-studnet /p:HTB_@cademy_stdnt!

[18:58:58:972] [6604:6605] [INFO][com.freerdp.core] - freerdp_connect:freerdp_set_last_error_ex resetting error state

<SNIP>

Certificate details for 10.129.113.142:3389 (RDP-Server):
	Common Name: OFFICEMANAGER
	Subject:     CN = OFFICEMANAGER
	Issuer:      CN = OFFICEMANAGER
	Thumbprint:  a0:7a:87:4f:ed:ba:79:8f:54:df:d1:6b:29:64:4e:43:ad:9e:f4:b5:78:60:fa:4d:18:da:68:2e:97:5a:10:9e
The above X.509 certificate could not be verified, possibly because you do not have
the CA certificate in your certificate store, or the certificate has expired.
Please look at the OpenSSL documentation on how to add a private CA to the store.
Do you trust the above certificate? (Y/T/N) Y

<SNIP>
```

![PivotingCOMMA_TunnelingCOMMA_and_Port_Forwarding_Walkthrough_Image_21.png](https://academy.hackthebox.com/storage/walkthroughs/52/PivotingCOMMA_TunnelingCOMMA_and_Port_Forwarding_Walkthrough_Image_21.png)

After connecting successfully, and before downloading the two files and one directory, students can either uninstall or turn off Windows Defender (otherwise the DLL will not be allowed to be loaded and will get deleted automatically, and in case it does get deleted, students need to copy and paste it again), in here, it will be turned off, following the steps below:

![PivotingCOMMA_TunnelingCOMMA_and_Port_Forwarding_Walkthrough_Image_22.png](https://academy.hackthebox.com/storage/walkthroughs/52/PivotingCOMMA_TunnelingCOMMA_and_Port_Forwarding_Walkthrough_Image_22.png)

![PivotingCOMMA_TunnelingCOMMA_and_Port_Forwarding_Walkthrough_Image_23.png](https://academy.hackthebox.com/storage/walkthroughs/52/PivotingCOMMA_TunnelingCOMMA_and_Port_Forwarding_Walkthrough_Image_23.png)

![PivotingCOMMA_TunnelingCOMMA_and_Port_Forwarding_Walkthrough_Image_24.png](https://academy.hackthebox.com/storage/walkthroughs/52/PivotingCOMMA_TunnelingCOMMA_and_Port_Forwarding_Walkthrough_Image_24.png)

Thereon, students need to transfer the files `SocksOverRDP-Plugin.dll`, `SocksOverRDP-Server.exe` and the `Proxifier PE` directory, to the spawned Windows target using any file transfer technique, with the easiest being copying and pasting the two files and one folder:

![PivotingCOMMA_TunnelingCOMMA_and_Port_Forwarding_Walkthrough_Image_25.png](https://academy.hackthebox.com/storage/walkthroughs/52/PivotingCOMMA_TunnelingCOMMA_and_Port_Forwarding_Walkthrough_Image_25.png)

![PivotingCOMMA_TunnelingCOMMA_and_Port_Forwarding_Walkthrough_Image_26.png](https://academy.hackthebox.com/storage/walkthroughs/52/PivotingCOMMA_TunnelingCOMMA_and_Port_Forwarding_Walkthrough_Image_26.png)

![PivotingCOMMA_TunnelingCOMMA_and_Port_Forwarding_Walkthrough_Image_27.png](https://academy.hackthebox.com/storage/walkthroughs/52/PivotingCOMMA_TunnelingCOMMA_and_Port_Forwarding_Walkthrough_Image_27.png)

Subsequently, students then need to use `regsvr32.exe` to load `SocksOverRDP-Plugin.dll` from within a privileged (i.e., administrator) `PowerShell` session where the DLL was pasted:

Code: powershell

```powershell
regsvr32.exe SocksOverRDP-Plugin.dll
```

![PivotingCOMMA_TunnelingCOMMA_and_Port_Forwarding_Walkthrough_Image_28.png](https://academy.hackthebox.com/storage/walkthroughs/52/PivotingCOMMA_TunnelingCOMMA_and_Port_Forwarding_Walkthrough_Image_28.png)

Afterward, students need to open `mstsc.exe` from within `PowerShell` and connect to the internal DC at `172.16.5.19`, using the credentials `victor:pass@123`:

![PivotingCOMMA_TunnelingCOMMA_and_Port_Forwarding_Walkthrough_Image_29.png](https://academy.hackthebox.com/storage/walkthroughs/52/PivotingCOMMA_TunnelingCOMMA_and_Port_Forwarding_Walkthrough_Image_29.png)

![PivotingCOMMA_TunnelingCOMMA_and_Port_Forwarding_Walkthrough_Image_30.png](https://academy.hackthebox.com/storage/walkthroughs/52/PivotingCOMMA_TunnelingCOMMA_and_Port_Forwarding_Walkthrough_Image_30.png)

![PivotingCOMMA_TunnelingCOMMA_and_Port_Forwarding_Walkthrough_Image_31.png](https://academy.hackthebox.com/storage/walkthroughs/52/PivotingCOMMA_TunnelingCOMMA_and_Port_Forwarding_Walkthrough_Image_31.png)

![PivotingCOMMA_TunnelingCOMMA_and_Port_Forwarding_Walkthrough_Image_32.png](https://academy.hackthebox.com/storage/walkthroughs/52/PivotingCOMMA_TunnelingCOMMA_and_Port_Forwarding_Walkthrough_Image_32.png)

![PivotingCOMMA_TunnelingCOMMA_and_Port_Forwarding_Walkthrough_Image_33.png](https://academy.hackthebox.com/storage/walkthroughs/52/PivotingCOMMA_TunnelingCOMMA_and_Port_Forwarding_Walkthrough_Image_33.png)

Then, students need to transfer `SocksOverRDP-Server.exe` to the internal DC at `172.16.5.19`, however, before that, they need to uninstall Windows Defender (otherwise the executable will be deleted constantly):

Code: powershell

```powershell
Uninstall-WindowsFeature -Name Windows-Defender
```

  RDP and SOCKS Tunneling with SocksOverRDP

```powershell-session
PS C:\Windows\system32> Uninstall-WindowsFeature -Name Windows-Defender

Success Restart Needed Exit Code      Feature Result
------- -------------- ---------      --------------
True    No             NoChangeNeeded {}
```

Once uninstalled, students can copy and paste the executable to the DC:

![PivotingCOMMA_TunnelingCOMMA_and_Port_Forwarding_Walkthrough_Image_34.png](https://academy.hackthebox.com/storage/walkthroughs/52/PivotingCOMMA_TunnelingCOMMA_and_Port_Forwarding_Walkthrough_Image_34.png)

![PivotingCOMMA_TunnelingCOMMA_and_Port_Forwarding_Walkthrough_Image_35.png](https://academy.hackthebox.com/storage/walkthroughs/52/PivotingCOMMA_TunnelingCOMMA_and_Port_Forwarding_Walkthrough_Image_35.png)

![PivotingCOMMA_TunnelingCOMMA_and_Port_Forwarding_Walkthrough_Image_36.png](https://academy.hackthebox.com/storage/walkthroughs/52/PivotingCOMMA_TunnelingCOMMA_and_Port_Forwarding_Walkthrough_Image_36.png)

Subsequently, students need to run it as administrator:

![PivotingCOMMA_TunnelingCOMMA_and_Port_Forwarding_Walkthrough_Image_37.png](https://academy.hackthebox.com/storage/walkthroughs/52/PivotingCOMMA_TunnelingCOMMA_and_Port_Forwarding_Walkthrough_Image_37.png)

![PivotingCOMMA_TunnelingCOMMA_and_Port_Forwarding_Walkthrough_Image_38.png](https://academy.hackthebox.com/storage/walkthroughs/52/PivotingCOMMA_TunnelingCOMMA_and_Port_Forwarding_Walkthrough_Image_38.png)

Students then need to minimize this RDP connection:

![PivotingCOMMA_TunnelingCOMMA_and_Port_Forwarding_Walkthrough_Image_39.png](https://academy.hackthebox.com/storage/walkthroughs/52/PivotingCOMMA_TunnelingCOMMA_and_Port_Forwarding_Walkthrough_Image_39.png)

Thereon, students need to run the `Proxifier` executable as administrator:

![PivotingCOMMA_TunnelingCOMMA_and_Port_Forwarding_Walkthrough_Image_40.png](https://academy.hackthebox.com/storage/walkthroughs/52/PivotingCOMMA_TunnelingCOMMA_and_Port_Forwarding_Walkthrough_Image_40.png)

![PivotingCOMMA_TunnelingCOMMA_and_Port_Forwarding_Walkthrough_Image_41.png](https://academy.hackthebox.com/storage/walkthroughs/52/PivotingCOMMA_TunnelingCOMMA_and_Port_Forwarding_Walkthrough_Image_41.png)

![PivotingCOMMA_TunnelingCOMMA_and_Port_Forwarding_Walkthrough_Image_42.png](https://academy.hackthebox.com/storage/walkthroughs/52/PivotingCOMMA_TunnelingCOMMA_and_Port_Forwarding_Walkthrough_Image_42.png)

Once opened, students need to click on `Profile` --> `Proxy Servers...`:

![PivotingCOMMA_TunnelingCOMMA_and_Port_Forwarding_Walkthrough_Image_43.png](https://academy.hackthebox.com/storage/walkthroughs/52/PivotingCOMMA_TunnelingCOMMA_and_Port_Forwarding_Walkthrough_Image_43.png)

Students need to set `127.0.0.1:1080` as the proxy's socket and use `SOCKS5`:

![PivotingCOMMA_TunnelingCOMMA_and_Port_Forwarding_Walkthrough_Image_44.png](https://academy.hackthebox.com/storage/walkthroughs/52/PivotingCOMMA_TunnelingCOMMA_and_Port_Forwarding_Walkthrough_Image_44.png)

![PivotingCOMMA_TunnelingCOMMA_and_Port_Forwarding_Walkthrough_Image_45.png](https://academy.hackthebox.com/storage/walkthroughs/52/PivotingCOMMA_TunnelingCOMMA_and_Port_Forwarding_Walkthrough_Image_45.png)

At last, students need to use `mstsc.exe` to connect to the internal node at 172.16.6.155 using the credentials `jason:WellConnected123!`:

![PivotingCOMMA_TunnelingCOMMA_and_Port_Forwarding_Walkthrough_Image_46.png](https://academy.hackthebox.com/storage/walkthroughs/52/PivotingCOMMA_TunnelingCOMMA_and_Port_Forwarding_Walkthrough_Image_46.png)

![PivotingCOMMA_TunnelingCOMMA_and_Port_Forwarding_Walkthrough_Image_47.png](https://academy.hackthebox.com/storage/walkthroughs/52/PivotingCOMMA_TunnelingCOMMA_and_Port_Forwarding_Walkthrough_Image_47.png)

![PivotingCOMMA_TunnelingCOMMA_and_Port_Forwarding_Walkthrough_Image_48.png](https://academy.hackthebox.com/storage/walkthroughs/52/PivotingCOMMA_TunnelingCOMMA_and_Port_Forwarding_Walkthrough_Image_48.png)

![PivotingCOMMA_TunnelingCOMMA_and_Port_Forwarding_Walkthrough_Image_49.png](https://academy.hackthebox.com/storage/walkthroughs/52/PivotingCOMMA_TunnelingCOMMA_and_Port_Forwarding_Walkthrough_Image_49.png)

Once successfully connected, students will find the flag `H0pping@roundwithRDP!` on the desktop:

![PivotingCOMMA_TunnelingCOMMA_and_Port_Forwarding_Walkthrough_Image_50.png](https://academy.hackthebox.com/storage/walkthroughs/52/PivotingCOMMA_TunnelingCOMMA_and_Port_Forwarding_Walkthrough_Image_50.png)