# extractor.py
from transformers import pipeline
import dateparser

ner_pipeline = pipeline("ner", grouped_entities=True)

def extract_all(text: str):
    persons, orgs, locations, entities = [], [], [], []

    ner_results = ner_pipeline(text)

    # Keep track of order of appearance
    seen = {"PER": set(), "LOC": set(), "ORG": set()}

    for ent in ner_results:
        entity_text = ent.get("word", "")
        entity_type = ent.get("entity_group", ent.get("entity", ""))
        score = ent.get("score", 0.0)

        entities.append({
            "text": entity_text,
            "type": entity_type.upper(),
            "score": float(score)
        })

        if entity_type.upper() == "PER" and entity_text not in seen["PER"]:
            persons.append(entity_text)
            seen["PER"].add(entity_text)
        elif entity_type.upper() == "LOC" and entity_text not in seen["LOC"]:
            locations.append(entity_text)
            seen["LOC"].add(entity_text)
        elif entity_type.upper() == "ORG" and entity_text not in seen["ORG"]:
            orgs.append(entity_text)
            seen["ORG"].add(entity_text)

    # Extract dates in order
    dates = []
    words = text.split()
    for word in words:
        parsed = dateparser.parse(word)
        if parsed:
            dates.append({"text": word, "normalized": parsed.date().isoformat()})

    return {
        "persons": persons,
        "orgs": orgs,
        "locations": locations,
        "entities": entities,
        "dates": dates,
        "text_length": len(text)
    }
