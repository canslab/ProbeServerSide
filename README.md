# ProbeServerSide
This program enables you to receive command from the client program(ProbeController, JSON based)
and control robot body 

## Command(data) Flow
(ClientSide)--||--> JSON command --> main.py --> ControlTower.py(parse) --order behavior--> ProbeDevice.py--||--> (Control)
