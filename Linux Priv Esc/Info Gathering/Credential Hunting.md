
---

When enumerating a system, it is important to note down any credentials. These may be found in configuration files (`.conf`, `.config`, `.xml`, etc.), shell scripts, a user's bash history file, backup (`.bak`) files, within database files or even in text files. Credentials may be useful for escalating to other users or even root, accessing databases and other systems within the environment.

The /var directory typically contains the web root for whatever web server is running on the host. The web root may contain database credentials or other types of credentials that can be leveraged to further access. A common example is MySQL database credentials within WordPress configuration files:


```shell-session
htb_student@NIX02:~$ grep 'DB_USER\|DB_PASSWORD' wp-config.php

define( 'DB_USER', 'wordpressuser' );
define( 'DB_PASSWORD', 'WPadmin123!' );
```

The spool or mail directories, if accessible, may also contain valuable information or even credentials. It is common to find credentials stored in files in the web root (i.e. MySQL connection strings, WordPress configuration files).

```shell-session
htb_student@NIX02:~$  find / ! -path "*/proc/*" -iname "*config*" -type f 2>/dev/null

/etc/ssh/ssh_config
/etc/ssh/sshd_config
/etc/python3/debian_config
/etc/kbd/config
/etc/manpath.config
/boot/config-4.4.0-116-generic
/boot/grub/i386-pc/configfile.mod
/sys/devices/pci0000:00/0000:00:00.0/config
/sys/devices/pci0000:00/0000:00:01.0/config
<SNIP>
```

---

## SSH Keys

It is also useful to search around the system for accessible SSH private keys. We may locate a private key for another, more privileged, user that we can use to connect back to the box with additional privileges. We may also sometimes find SSH keys that can be used to access other hosts in the environment. Whenever finding SSH keys check the `known_hosts` file to find targets. This file contains a list of public keys for all the hosts which the user has connected to in the past and may be useful for lateral movement or to find data on a remote host that can be used to perform privilege escalation on our target.

  Credential Hunting

```shell-session
htb_student@NIX02:~$  ls ~/.ssh

id_rsa  id_rsa.pub  known_hosts
```

---

## Question 1

### "Find the WordPress database password."

Students first need to connect to `STMIP` with `SSH` using the credentials `htb-student:Academy_LLPE!`:

Code: shell

```shell
ssh htb-student@STMIP
```

  Credential Hunting

```shell-session
┌─[us-academy-1]─[10.10.14.118]─[htb-ac413848@pwnbox-base]─[~]
└──╼ [★]$ ssh htb-student@10.129.2.210

The authenticity of host '10.129.2.210 (10.129.2.210)' can't be established.
ECDSA key fingerprint is SHA256:jqHwbeBBQLd/z1BFRM732tTqQbhKGni0KhrGMszsiVM.
Are you sure you want to continue connecting (yes/no/[fingerprint])? Yes
Warning: Permanently added '10.129.2.210' (ECDSA) to the list of known hosts.
htb-student@10.129.2.210's password: 
Welcome to Ubuntu 16.04.4 LTS (GNU/Linux 4.4.0-116-generic x86_64)

<SNIP>

htb-student@NIX02:~$
```

Subsequently, students need to print out the contents of the `wp-config.php` file in `/var/www/html` and use `grep` to filter out the database password:

Code: shell

```shell
cat /var/www/html/wp-config.php | grep "DB_PASSWORD"
```

  Credential Hunting

```shell-session
htb-student@NIX02:~$ cat /var/www/html/wp-config.php | grep "DB_PASSWORD"

define( 'DB_PASSWORD', 'W0rdpr3ss_sekur1ty!' );
```