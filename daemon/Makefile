
all:test status

test:
	echo "Test" | nc -u 127.0.0.1 5005 -q 0

install:
	sudo ./setup_daemon.sh

restart:
	sudo systemctl restart server

status:
	sudo systemctl status server
