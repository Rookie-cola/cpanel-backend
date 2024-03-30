import json

data = '{"images":["id_1", "id_2", "id_3"]}'

data = json.loads(data)
print(" ".join(data["images"]))
