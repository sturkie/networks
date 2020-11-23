README
——————
SCENARIO 1:
Running the server.py file then the client.py file will show a normal, functioning GBN protocol example.


SCENARIO 2:
Running the dropped_server.py then the client.py file will show what happens when the server drops a packet file.
	
The packet file that is dropped in dropped_server.py is different each time. The packet lost depends on the random value generated in receive(sock)