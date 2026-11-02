# levels.py

TOTAL_MISSIONS = 50

CHAPTERS = [
    {
        "name": "The Forgotten Forest",
        "start": 1,
        "end": 10,
        "difficulty": "Easy"
    },
    {
        "name": "The Ancient Dungeon",
        "start": 11,
        "end": 20,
        "difficulty": "Normal"
    },
    {
        "name": "The Shadow Castle",
        "start": 21,
        "end": 30,
        "difficulty": "Medium"
    },
    {
        "name": "The Fire Kingdom",
        "start": 31,
        "end": 40,
        "difficulty": "Hard"
    },
    {
        "name": "The Final Darkness",
        "start": 41,
        "end": 50,
        "difficulty": "Expert"
    }
]


def get_level_info(level_number):
    for chapter in CHAPTERS:
        if chapter["start"] <= level_number <= chapter["end"]:
            return {
                "mission": level_number,
                "chapter": chapter["name"],
                "difficulty": chapter["difficulty"]
            }

    return None



