import json

req = "[{'id': '3998198f-7560-4496-bb07-cca6623d18f8', 'mapNumber': 1, 'mapName': 'Eden Prime'}, {'id': '95fddff0-5030-4b59-9671-11474048f464', 'mapNumber': 2, 'mapName': 'Noveria'}, {'id': '35090e96-b0da-4d08-b580-09b314e454f4', 'mapNumber': 3, 'mapName': 'Hyperion'}]"
req = req.replace("\'", "\"")

print(json.loads(req)[0]['id'])