import json

level = [
    "#############",
    "#...........#",
    "#...........#",
    "#...........#",
    "#...........#",
    "#...........#",
    "#...........#",
    "#...........#",
]


f = open("test_level.json", "w")
out = []

for i, line in enumerate(level):
    for j, block in enumerate(line):
        if block == "#":
            out.append({
                "class_name": "Block",
                "properties": {
                    "position": [64 * j, 64 * i],
                    "texture": "res/textures/Brick.png"
                }
            })

out_json = json.dumps(out, indent=4)

f.write(out_json)
f.close()