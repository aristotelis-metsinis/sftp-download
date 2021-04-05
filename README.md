# sftp download

A script that connects and logs into a specified host at a predefined port with a given username, and password and copies over &quot;SFTP&quot; all files from a remote source directory to a local destination directory. User can also choose to delete the remote files that have been already downloaded.

Developed by Aristotelis Metsinis [ aristotelis.metsinis@gmail.com ] in June 2020 - version 1.0
Comments and bug fixing in April 2021 - version 1.1
    
Tested with Python 2.7.6 and 3.8.7

------------

### script

* usage

<pre>
	$ ./download.py -h
	usage: download.py [-h] -H HOST [-P PORT] -s SOURCE -d DESTINATION -u USER -p PASSWORD [--delete]
	
	A script that connects and logs into a specified host at a predefined port with a given username, and password and copies over "SFTP" all files from a remote source directory to a local destination directory. User can also choose to delete the remote files that have been already downloaded.
	
	optional arguments:
	-h, --help            	show this help message and exit
	-H HOST, --host HOST  	hostname or IP address
	-P PORT, --port PORT  	server port, default = 22
	-s SOURCE, --source SOURCE
							remote directory to fetch files from
	-d DESTINATION, --destination DESTINATION
							local folder to store fetched files to
	-u USER, --user USER  	username for login
	-p PASSWORD, --password PASSWORD
							password for login
	--delete              	delete remote files
	$
</pre>

* execution

<pre>
$ ./download.py -H 's-ftp.internal.com' -s '/remote' -d 'local/' -u "username" -p 'password'
2020-06-19 09:09:13,820 - root - INFO - ---------------------------------------------------------------------------------
2020-06-19 09:09:13,821 - root - INFO - Logging to remote server 'sftp://s-ftp.internal.com:22/remote'
2020-06-19 09:09:13,830 - paramiko.transport - INFO - Connected (version 2.0, client OpenSSH_7.2p2)
2020-06-19 09:09:13,996 - paramiko.transport - INFO - Authentication (password) successful!
2020-06-19 09:09:14,147 - paramiko.transport.sftp - INFO - [chan 0] Opened sftp connection (server version 3)
2020-06-19 09:09:14,159 - root - INFO - Found 3 remote files
2020-06-19 09:09:14,159 - root - INFO - File #  1 : '4221151_2020061217.txt'
2020-06-19 09:09:14,159 - root - INFO - File #  2 : '4221151_2020061201.txt'
2020-06-19 09:09:14,159 - root - INFO - File #  3 : '4221151_2020061216.txt'
2020-06-19 09:09:14,160 - root - INFO - Downloading remote files
2020-06-19 09:09:14,198 - root - INFO - Downloading remote files completed
2020-06-19 09:09:14,198 - root - INFO - No remote files deleted
2020-06-19 09:09:14,199 - paramiko.transport.sftp - INFO - [chan 0] sftp session closed.
$
</pre>

the downloaded files are being saved under the given &apos;local/&apos; folder :

<pre>
$ ls -lt local/
total 12
-rw-rw-r-- 1 tomcat tomcat 132 Jun 19 08:18 4221151_2020061217.txt
-rw-rw-r-- 1 tomcat tomcat 132 Jun 19 08:18 4221151_2020061201.txt
-rw-rw-r-- 1 tomcat tomcat 132 Jun 19 08:18 4221151_2020061216.txt
$
</pre>

------------

### cron job

set-up a cron job in &quot;/etc/crontab&quot; file that executes the above script &quot;at every 30th minute from 10 through 59&quot;, that is every 30 minutes at hh:10 and hh:40

<pre>
$ cat /etc/crontab
# /etc/crontab: system-wide crontab
	:
	:
# download remote files on sftp server, to a local folder and remove files that have been already downloaded
10-59/30 * * * * tomcat cd /opt/ftp && ./download.py -H 's-ftp.internal.com' -s '/remote' -d 'local/' -u "username" -p 'password' --delete >/dev/null 2>&1
	:
	:
$
</pre>

* script running successfully every 5 minutes, with &quot;delete&quot; option disabled

<pre>
* Found remote files | No remote files deleted

2020-06-19 13:55:01,867 - root - INFO - ---------------------------------------------------------------------------------
2020-06-19 13:55:01,867 - root - INFO - Logging to remote server 'sftp://s-ftp.internal.com:22/remote'
2020-06-19 13:55:01,876 - paramiko.transport - INFO - Connected (version 2.0, client OpenSSH_7.2p2)
2020-06-19 13:55:02,487 - paramiko.transport - INFO - Authentication (password) successful!
2020-06-19 13:55:02,626 - paramiko.transport.sftp - INFO - [chan 0] Opened sftp connection (server version 3)
2020-06-19 13:55:02,635 - root - INFO - Found 1 remote files
2020-06-19 13:55:02,636 - root - INFO - File #  1 : '4221151_2020061913.txt'
2020-06-19 13:55:02,636 - root - INFO - Downloading remote files
2020-06-19 13:55:02,657 - root - INFO - Downloading remote files completed
2020-06-19 13:55:02,658 - root - INFO - No remote files deleted
2020-06-19 13:55:02,658 - paramiko.transport.sftp - INFO - [chan 0] sftp session closed.

* Found remote files | No remote files deleted

2020-06-19 14:00:01,786 - root - INFO - ---------------------------------------------------------------------------------
2020-06-19 14:00:01,787 - root - INFO - Logging to remote server 'sftp://s-ftp.internal.com:22/remote'
2020-06-19 14:00:01,797 - paramiko.transport - INFO - Connected (version 2.0, client OpenSSH_7.2p2)
2020-06-19 14:00:03,113 - paramiko.transport - INFO - Authentication (password) successful!
2020-06-19 14:00:03,239 - paramiko.transport.sftp - INFO - [chan 0] Opened sftp connection (server version 3)
2020-06-19 14:00:03,250 - root - INFO - Found 1 remote files
2020-06-19 14:00:03,250 - root - INFO - File #  1 : '4221151_2020061913.txt'
2020-06-19 14:00:03,251 - root - INFO - Downloading remote files
2020-06-19 14:00:03,275 - root - INFO - Downloading remote files completed
2020-06-19 14:00:03,275 - root - INFO - No remote files deleted
2020-06-19 14:00:03,275 - paramiko.transport.sftp - INFO - [chan 0] sftp session closed.

* Found remote files | No remote files deleted

2020-06-19 14:05:01,401 - root - INFO - ---------------------------------------------------------------------------------
2020-06-19 14:05:01,401 - root - INFO - Logging to remote server 'sftp://s-ftp.internal.com:22/remote'
2020-06-19 14:05:01,412 - paramiko.transport - INFO - Connected (version 2.0, client OpenSSH_7.2p2)
2020-06-19 14:05:02,054 - paramiko.transport - INFO - Authentication (password) successful!
2020-06-19 14:05:02,186 - paramiko.transport.sftp - INFO - [chan 0] Opened sftp connection (server version 3)
2020-06-19 14:05:02,196 - root - INFO - Found 1 remote files
2020-06-19 14:05:02,196 - root - INFO - File #  1 : '4221151_2020061913.txt'
2020-06-19 14:05:02,196 - root - INFO - Downloading remote files
2020-06-19 14:05:02,219 - root - INFO - Downloading remote files completed
2020-06-19 14:05:02,219 - root - INFO - No remote files deleted
2020-06-19 14:05:02,219 - paramiko.transport.sftp - INFO - [chan 0] sftp session closed.
</pre>

* script running successfully every 5 minutes, with &quot;delete&quot; option enabled

<pre>
* Found remote files | Deleting remote files

2020-06-19 14:10:01,466 - root - INFO - ---------------------------------------------------------------------------------
2020-06-19 14:10:01,466 - root - INFO - Logging to remote server 'sftp://s-ftp.internal.com:22/remote'
2020-06-19 14:10:01,475 - paramiko.transport - INFO - Connected (version 2.0, client OpenSSH_7.2p2)
2020-06-19 14:10:02,501 - paramiko.transport - INFO - Authentication (password) successful!
2020-06-19 14:10:02,640 - paramiko.transport.sftp - INFO - [chan 0] Opened sftp connection (server version 3)
2020-06-19 14:10:02,649 - root - INFO - Found 1 remote files
2020-06-19 14:10:02,649 - root - INFO - File #  1 : '4221151_2020061913.txt'
2020-06-19 14:10:02,649 - root - INFO - Downloading remote files
2020-06-19 14:10:02,669 - root - INFO - Downloading remote files completed
2020-06-19 14:10:02,672 - root - INFO - Deleting remote file '4221151_2020061913.txt'
2020-06-19 14:10:02,672 - paramiko.transport.sftp - INFO - [chan 0] sftp session closed.

* No remote files found

2020-06-19 14:15:01,796 - root - INFO - ---------------------------------------------------------------------------------
2020-06-19 14:15:01,797 - root - INFO - Logging to remote server 'sftp://s-ftp.internal.com:22/remote'
2020-06-19 14:15:01,806 - paramiko.transport - INFO - Connected (version 2.0, client OpenSSH_7.2p2)
2020-06-19 14:15:02,235 - paramiko.transport - INFO - Authentication (password) successful!
2020-06-19 14:15:02,377 - paramiko.transport.sftp - INFO - [chan 0] Opened sftp connection (server version 3)
2020-06-19 14:15:02,385 - root - CRITICAL - No remote files found
2020-06-19 14:15:02,504 - paramiko.transport.sftp - INFO - [chan 0] sftp session closed.

* Found remote files | Deleting remote files

2020-06-19 14:20:01,624 - root - INFO - ---------------------------------------------------------------------------------
2020-06-19 14:20:01,624 - root - INFO - Logging to remote server 'sftp://s-ftp.internal.com:22/remote'
2020-06-19 14:20:01,634 - paramiko.transport - INFO - Connected (version 2.0, client OpenSSH_7.2p2)
2020-06-19 14:20:02,213 - paramiko.transport - INFO - Authentication (password) successful!
2020-06-19 14:20:02,352 - paramiko.transport.sftp - INFO - [chan 0] Opened sftp connection (server version 3)
2020-06-19 14:20:02,362 - root - INFO - Found 1 remote files
2020-06-19 14:20:02,363 - root - INFO - File #  1 : '4221151_2020061917.txt'
2020-06-19 14:20:02,363 - root - INFO - Downloading remote files
2020-06-19 14:20:02,386 - root - INFO - Downloading remote files completed
2020-06-19 14:20:02,389 - root - INFO - Deleting remote file '4221151_2020061917.txt'
2020-06-19 14:20:02,389 - paramiko.transport.sftp - INFO - [chan 0] sftp session closed.

* No remote files found

2020-06-19 14:25:01,513 - root - INFO - ---------------------------------------------------------------------------------
2020-06-19 14:25:01,513 - root - INFO - Logging to remote server 'sftp://s-ftp.internal.com:22/remote'
2020-06-19 14:25:01,522 - paramiko.transport - INFO - Connected (version 2.0, client OpenSSH_7.2p2)
2020-06-19 14:25:02,092 - paramiko.transport - INFO - Authentication (password) successful!
2020-06-19 14:25:02,224 - paramiko.transport.sftp - INFO - [chan 0] Opened sftp connection (server version 3)
2020-06-19 14:25:02,232 - root - CRITICAL - No remote files found
2020-06-19 14:25:02,351 - paramiko.transport.sftp - INFO - [chan 0] sftp session closed.

* No remote files found

2020-06-19 14:30:01,466 - root - INFO - ---------------------------------------------------------------------------------
2020-06-19 14:30:01,466 - root - INFO - Logging to remote server 'sftp://s-ftp.internal.com:22/remote'
2020-06-19 14:30:01,477 - paramiko.transport - INFO - Connected (version 2.0, client OpenSSH_7.2p2)
2020-06-19 14:30:02,523 - paramiko.transport - INFO - Authentication (password) successful!
2020-06-19 14:30:02,667 - paramiko.transport.sftp - INFO - [chan 0] Opened sftp connection (server version 3)
2020-06-19 14:30:02,675 - root - CRITICAL - No remote files found
2020-06-19 14:30:02,794 - paramiko.transport.sftp - INFO - [chan 0] sftp session closed.
</pre>

* script running successfully every 30 minutes at hh:10 and hh:40, with &quot;delete&quot; option enabled

<pre>
* No remote files found

2020-06-19 14:40:02,353 - root - INFO - ---------------------------------------------------------------------------------
2020-06-19 14:40:02,353 - root - INFO - Logging to remote server 'sftp://s-ftp.internal.com:22/remote'
2020-06-19 14:40:02,364 - paramiko.transport - INFO - Connected (version 2.0, client OpenSSH_7.2p2)
2020-06-19 14:40:03,026 - paramiko.transport - INFO - Authentication (password) successful!
2020-06-19 14:40:03,159 - paramiko.transport.sftp - INFO - [chan 0] Opened sftp connection (server version 3)
2020-06-19 14:40:03,167 - root - CRITICAL - No remote files found
2020-06-19 14:40:03,286 - paramiko.transport.sftp - INFO - [chan 0] sftp session closed.

* No remote files found

2020-06-19 15:10:01,677 - root - INFO - ---------------------------------------------------------------------------------
2020-06-19 15:10:01,677 - root - INFO - Logging to remote server 'sftp://s-ftp.internal.com:22/remote'
2020-06-19 15:10:01,687 - paramiko.transport - INFO - Connected (version 2.0, client OpenSSH_7.2p2)
2020-06-19 15:10:02,416 - paramiko.transport - INFO - Authentication (password) successful!
2020-06-19 15:10:02,590 - paramiko.transport.sftp - INFO - [chan 0] Opened sftp connection (server version 3)
2020-06-19 15:10:02,598 - root - CRITICAL - No remote files found
2020-06-19 15:10:02,717 - paramiko.transport.sftp - INFO - [chan 0] sftp session closed.

* Found remote files | Deleting remote files

2020-06-19 15:40:02,480 - root - INFO - ---------------------------------------------------------------------------------
2020-06-19 15:40:02,481 - root - INFO - Logging to remote server 'sftp://s-ftp.internal.com:22/remote'
2020-06-19 15:40:02,490 - paramiko.transport - INFO - Connected (version 2.0, client OpenSSH_7.2p2)
2020-06-19 15:40:03,422 - paramiko.transport - INFO - Authentication (password) successful!
2020-06-19 15:40:03,549 - paramiko.transport.sftp - INFO - [chan 0] Opened sftp connection (server version 3)
2020-06-19 15:40:03,559 - root - INFO - Found 1 remote files
2020-06-19 15:40:03,559 - root - INFO - File #  1 : '4221151_2020061918.txt'
2020-06-19 15:40:03,559 - root - INFO - Downloading remote files
2020-06-19 15:40:03,579 - root - INFO - Downloading remote files completed
2020-06-19 15:40:03,582 - root - INFO - Deleting remote file '4221151_2020061918.txt'
2020-06-19 15:40:03,582 - paramiko.transport.sftp - INFO - [chan 0] sftp session closed.

* No remote files found

2020-06-19 16:10:01,907 - root - INFO - ---------------------------------------------------------------------------------
2020-06-19 16:10:01,907 - root - INFO - Logging to remote server 'sftp://s-ftp.internal.com:22/remote'
2020-06-19 16:10:01,917 - paramiko.transport - INFO - Connected (version 2.0, client OpenSSH_7.2p2)
2020-06-19 16:10:02,471 - paramiko.transport - INFO - Authentication (password) successful!
2020-06-19 16:10:02,610 - paramiko.transport.sftp - INFO - [chan 0] Opened sftp connection (server version 3)
2020-06-19 16:10:02,619 - root - CRITICAL - No remote files found
2020-06-19 16:10:02,738 - paramiko.transport.sftp - INFO - [chan 0] sftp session closed.
</pre>

------------
