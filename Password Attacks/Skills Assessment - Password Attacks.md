ssh
## The Credential Theft Shuffle

[The Credential Theft Shuffle](https://adsecurity.org/?p=2362), as coined by `Sean Metcalf`, is a systematic approach attackers use to compromise Active Directory environments by exploiting `stolen credentials`. The process begins with gaining initial access, often through phishing, followed by obtaining local administrator privileges on a machine. Attackers then extract credentials from memory using tools like Mimikatz and leverage these credentials to `move laterally across the network`. Techniques such as pass-the-hash (PtH) and tools like NetExec facilitate this lateral movement and further credential harvesting. The ultimate goal is to escalate privileges and `gain control over the domain`, often by compromising Domain Admin accounts or performing DCSync attacks. Sean emphasizes the importance of implementing security measures such as the `Local Administrator Password Solution (LAPS)`, enforcing `multi-factor authentication`, and `restricting administrative privileges` to mitigate such attacks.

## Skills Assessment

`Betty Jayde` works at `Nexura LLC`. We know she uses the password `Texas123!@#` on multiple websites, and we believe she may reuse it at work. Infiltrate Nexura's network and gain command execution on the domain controller. The following hosts are in-scope for this assessment:

| Host     | IP Address                                                  |
| -------- | ----------------------------------------------------------- |
| `DMZ01`  | `10.129.*.*` **(External)**, `172.16.119.13` **(Internal)** |
| `JUMP01` | `172.16.119.7`                                              |
| `FILE01` | `172.16.119.10`                                             |
| `DC01`   | `172.16.119.11`                                             |

#### Pivoting Primer

The internal hosts (`JUMP01`, `FILE01`, `DC01`) reside on a private subnet that is not directly accessible from our attack host. The only externally reachable system is `DMZ01`, which has a second interface connected to the internal network. This segmentation reflects a classic DMZ setup, where public-facing services are isolated from internal infrastructure.

To access these internal systems, we must first gain a foothold on `DMZ01`. From there, we can `pivot` — that is, route our traffic through the compromised host into the private network. This enables our tools to communicate with internal hosts as if they were directly accessible. After compromising the DMZ, refer to the module `cheatsheet` for the necessary commands to set up the pivot and continue your assessment.

---
[ CA_default ]

dir		= ./demoCA		# Where everything is kept
certs		= $dir/certs		# Where the issued certs are kept
crl_dir		= $dir/crl		# Where the issued crl are kept
database	= $dir/index.txt	# database index file.
#unique_subject	= no			# Set to 'no' to allow creation of
					# several certs with same subject.
new_certs_dir	= $dir/newcerts		# default place for new certs.

certificate	= $dir/cacert.pem 	# The CA certificate
serial		= $dir/serial 		# The current serial number
crlnumber	= $dir/crlnumber	# the current crl number
					# must be commented out to leave a V1 CRL
crl		= $dir/crl.pem 		# The current CRL
private_key	= $dir/private/cakey.pem# The private key

x509_extensions	= usr_cert		# The extensions to add to the cert

# Comment out the following two lines for the "traditional"
# (and highly broken) format.
name_opt 	= ca_default		# Subject Name options
cert_opt 	= ca_default		# Certificate field options

jbetty@DMZ01:/$ grep -rnw "PRIVATE KEY" /* 2>/dev/null | grep ":1"
/lib/python3/dist-packages/twisted/conch/ssh/keys.py:1108:                               b' PRIVATE KEY-----'))]
/lib/python3/dist-packages/twisted/conch/ssh/keys.py:1144:                                   b' PRIVATE KEY-----')))
/lib/python3/dist-packages/twisted/conch/test/keydata.py:110:privateECDSA_openssh521 = b"""-----BEGIN EC PRIVATE KEY-----
/lib/python3/dist-packages/twisted/conch/test/keydata.py:116:-----END EC PRIVATE KEY-----"""
/lib/python3/dist-packages/twisted/conch/test/keydata.py:123:privateECDSA_openssh384 = b"""-----BEGIN EC PRIVATE KEY-----
/lib/python3/dist-packages/twisted/conch/test/keydata.py:128:-----END EC PRIVATE KEY-----"""
/lib/python3/dist-packages/twisted/conch/test/keydata.py:138:privateECDSA_openssh = b"""-----BEGIN EC PRIVATE KEY-----
/lib/python3/dist-packages/twisted/conch/test/keydata.py:142:-----END EC PRIVATE KEY-----"""
/lib/python3/dist-packages/twisted/conch/test/keydata.py:151:privateRSA_openssh = b'''-----BEGIN RSA PRIVATE KEY-----
/lib/python3/dist-packages/twisted/conch/test/keydata.py:177:-----END RSA PRIVATE KEY-----'''
/lib/python3/dist-packages/twisted/conch/test/keydata.py:183:privateRSA_openssh_alternate = b"""-----BEGIN RSA PRIVATE KEY-----
/lib/python3/dist-packages/twisted/test/key.pem.no_trailing_newline:1:-----BEGIN PRIVATE KEY-----
/lib/python3/dist-packages/jwt/utils.py:121:    b"PRIVATE KEY",
/lib/python3/dist-packages/jwt/utils.py:123:    b"ENCRYPTED PRIVATE KEY",
/lib/python3/dist-packages/jwt/utils.py:124:    b"OPENSSH PRIVATE KEY",
/lib/python3/dist-packages/jwt/utils.py:125:    b"DSA PRIVATE KEY",
/lib/python3/dist-packages/jwt/utils.py:126:    b"RSA PRIVATE KEY",
/lib/python3/dist-packages/jwt/utils.py:128:    b"EC PRIVATE KEY",
/lib/python3/dist-packages/jwt/utils.py:133:    b"SSH2 ENCRYPTED PRIVATE KEY",
/lib/python3/dist-packages/sos/report/plugins/__init__.py:1262:        "-----SCRUBBED RSA PRIVATE KEY" so that support representatives can


---

