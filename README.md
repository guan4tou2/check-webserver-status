# check-webserver-status
use python to check webserver status and send result from email

useage. 
`git clone https://github.com/guan4tou2/check-webserver-status.git` then fill in mail server, username, password, webserver in pingtest.py. 

```shell
apt install -y screen
screen -S pingtest
python pingtest.py
```
then keep press Ctrl+A, and D to exit  
`screen -ls` to check  
