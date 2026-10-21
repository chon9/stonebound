OPPONENTS = [
    {
        "id": "haru", "name": "Haru", "title": "The riverside regular", "rank": "15 kyu",
        "kyu": 15, "portrait": 0, "location": "Riverside Go Club", "requires": None,
        "reward": 250, "xp": 100, "chapter": 1, "style": "Curious & easygoing",
        "intro": [
            "Hey! You're the one who found that old Go board, right? I'm Haru.",
            "My grandfather used to say every stone is the beginning of a conversation. I've been waiting for someone new to talk to.",
            "Let's play a little game by the river. Take your time. We all start with one stone."
        ],
        "win": "You've got a feel for this! Mei at the tea shop will want to meet you. Tell her I sent you.",
        "lose": "That was a good conversation. Same spot, another game? The river isn't going anywhere.",
        "thinking": "Hmm… where does this little stone want to go?",
    },
    {
        "id": "mei", "name": "Mei", "title": "Tea, tenuki & a little mischief", "rank": "10 kyu",
        "kyu": 10, "portrait": 1, "location": "Komorebi Tea House", "requires": "haru",
        "reward": 350, "xp": 150, "chapter": 1, "style": "Patient & inventive",
        "intro": [
            "Haru told me about you. A new player in our sleepy little town—finally!",
            "I used to play between tea orders. Now the tea goes cold because I forget everything else.",
            "Win this one and I'll introduce you to Ren. Fair warning: he takes his stones very seriously."
        ],
        "win": "Well played! Your next cup is on me. Ren practices at the academy. I think you're ready.",
        "lose": "A little patience goes a long way. Like brewing tea, really. Come back when you're ready.",
        "thinking": "A good move needs a moment to steep…",
    },
    {
        "id": "ren", "name": "Ren", "title": "One move ahead", "rank": "6 kyu",
        "kyu": 6, "portrait": 2, "location": "Aoharu Academy", "requires": "mei",
        "reward": 450, "xp": 200, "chapter": 2, "style": "Focused & precise",
        "intro": [
            "So you're the player everyone's talking about. I'm Ren. Sit down.",
            "I used to think Go was about finding the perfect move. Lately, I'm not so sure.",
            "Show me what you see on this board. Maybe we'll both learn something."
        ],
        "win": "I didn't see that coming. You should visit Master Sora at the hilltop pavilion. He's been waiting for someone like you.",
        "lose": "Look at the whole board. A stone can lose a battle and still win the game. Let's try again sometime.",
        "thinking": "There is something here. Give me a moment.",
    },
    {
        "id": "sora", "name": "Master Sora", "title": "The keeper of old stories", "rank": "2 kyu",
        "kyu": 2, "portrait": 3, "location": "Hilltop Pavilion", "requires": "ren",
        "reward": 650, "xp": 300, "chapter": 2, "style": "Calm & far-seeing",
        "intro": [
            "The town has a different rhythm since you arrived. Even Ren has been smiling.",
            "That old board you carry was mine, once. I left it for someone who would listen to what it had to say.",
            "There is no final lesson. Only another game, and another person across the board. Shall we?"
        ],
        "win": "Beautifully played. The board is yours now. So are all the stories you'll make with it. Our little town will always have a seat for you.",
        "lose": "Every loss leaves a little wisdom behind. Keep the board. Our conversation has only just begun.",
        "thinking": "Listen closely. The quiet stones have something to say.",
    },
]

ITEMS = [
    {"id": "hinoki", "name": "Old Hinoki", "type": "board", "price": 0, "wins": 0, "tag": "Your first board", "description": "Warm wood. A thousand stories waiting to happen.", "color": "#dcb676"},
    {"id": "sakura", "name": "Sakura Blossom", "type": "board", "price": 300, "wins": 1, "tag": "Spring collection", "description": "Soft rosewood, touched by the first blush of spring.", "color": "#d9a59b"},
    {"id": "bamboo", "name": "Bamboo Grove", "type": "board", "price": 450, "wins": 2, "tag": "The quiet collection", "description": "A cool green playing field for a clear mind.", "color": "#aabd9d"},
    {"id": "midnight", "name": "Midnight Indigo", "type": "board", "price": 650, "wins": 3, "tag": "After hours", "description": "For the games that keep you up past the last train.", "color": "#3e5268"},
    {"id": "classic", "name": "Slate & Shell", "type": "stones", "price": 0, "wins": 0, "tag": "The essentials", "description": "The familiar weight of a well-loved stone.", "color": "#2f3537"},
    {"id": "jade", "name": "Jade & Porcelain", "type": "stones", "price": 250, "wins": 1, "tag": "River treasures", "description": "Deep green jade and milky porcelain. Naturally calming.", "color": "#326f60"},
    {"id": "amber", "name": "Amber & Pearl", "type": "stones", "price": 400, "wins": 2, "tag": "Golden hour", "description": "Honey-colored amber with a soft pearlescent partner.", "color": "#9c5f2d"},
    {"id": "obsidian", "name": "Obsidian & Moonstone", "type": "stones", "price": 600, "wins": 4, "tag": "A master's keepsake", "description": "A little piece of the night sky in every move.", "color": "#30334d"},
]

from .campaign import expand_catalog
OPPONENTS, ITEMS = expand_catalog(OPPONENTS, ITEMS)
OPPONENT_BY_ID = {r["id"]: r for r in OPPONENTS}
ITEM_BY_ID = {r["id"]: r for r in ITEMS}
