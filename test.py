import json

level = [
    "#######################",
    "#.....................#",
    "#.#.#.#.#.#.#.#.#.#.#.#",
    "#.....................#",
    "#.#.#.#.#.#.#.#.#.#.#.#",
    "#.....................#",
    "#.#.#.#.#.#.#.#.#.#.#.#",
    "#.....................#",
    "#.#.#.#.#.#.#.#.#.#.#.#",
    "#.....................#",
    "#.#.#.#.#.#.#.#.#.#.#.#",
    "#.....................#",
    "#.#.#.#.#.#.#.#.#.#.#.#",
    "#.....................#",
    "#######################",
]


f = open("res/levels/test.lev", "w")
out = {
    "settings": {
        "width": len(level[0]) * 64,
        "height": len(level) * 64
    },
    "ui": {},
    "objects": [
        {
            "class_name": "NetworkManager",
            "properties": {
                "position": [-100, -100]
            }
        }
    ]
}

for i, line in enumerate(level):
    for j, block in enumerate(line):
        if block == "#":
            out["objects"].append({
                "class_name": "Block",
                "properties": {
                    "position": [64 * j, 64 * i],
                    "texture": "res/textures/Brick.png",
                    "collider": 0
                }
            })
        
        if block == ".":
            out["objects"].append({
                "class_name": "Blank",
                "properties": {
                    "position": [64 * j, 64 * i],
                    "texture": "res/textures/Grass.png",
                    "collider": 2
                }
            })

out_json = json.dumps(out, indent=4)

f.write(out_json)
f.close()

