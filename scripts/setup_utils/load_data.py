import json

from dbmanagers.vectordbmanagers.weaviate_manager import WManager

with open("setup_data/illnesses.json", "r", encoding="utf-8") as f:
    data = json.load(f)

illnesses = data.get("illnesses", [])
input_data = []

for illness in illnesses:
    input_data.append(
        {
            "symptoms": ",".join(illness.get("symptoms", [])),
            "doctors": illness.get("doctors", []),
            "Diagnosis": illness.get("name"),
        },
    )

wm = WManager()
wm.add_data("SymptomDisease", input_data)
