# incident_response

In the pcap file, I found payload which used to attack the target web server.
I extracted the shellcode and made dummy binary to disassemble shellcode with IDA.

Shellcode used a custom stream cipher to communicate with the attacker.

I made a python script to decrypt the communication data.