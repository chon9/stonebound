"""Original spirit narrative and coaching derived from KataGo's BLACK perspective."""
import math


def bilingual(en, zh):
    return {"en": en, "zh": zh}


REFLECTIONS = [
    ("A seat by the river", "河畔一席", "I once sought an immortal move. Akari taught me to leave a seat for someone else.", "吾昔求不朽之着，明里却教吾为他人留一席。", "Your grandmother could hear me too. I have watched this board for centuries; now I will travel with you.", "你的外婆也能听见我。我守着这方棋盘数百年，如今，便随你同行。"),
    ("The missed train", "误车", "One mistaken turn need not bind a lifetime.", "一着之失，何必困其终身。", "Toma waited on the wrong platform. Review a mistake, then allow yourself a next move.", "冬真等错了月台。看清错在哪里，然后允许自己再下一手。"),
    ("A place for everyone", "容人", "To covet every corner is to lose the whole board.", "贪尽四隅者，或失全局。", "Nao cannot protect everything. Choose what matters; a sacrifice can make room for a stronger group.", "奈绪无法守住一切。先分清轻重；适当舍弃，才能照顾更重要的棋块。"),
    ("The unfinished record", "未完之谱", "A life beyond the board is also worthy of care.", "枰外亦有人间，不可不顾。", "Akari left a game to help her family. An unfinished record can still tell a complete story.", "明里离开棋局，是为了照顾家人。没有结果的棋谱，也能讲完一个故事。"),
    ("The quiet move", "静着", "First give thy stones a home; then seek distant lands.", "先安其身，而后图远。", "A weak group needs liberties and room for eyes. Before attacking, check whether your own stones can live.", "弱棋需要气，也需要做眼的空间。进攻之前，先看看自己的棋能不能活。"),
    ("Borrowed lamps", "借灯", "Many small lights together can outlast a storm.", "众灯相续，风雨何惧。", "Your friends brought the hall back to life. Connected stones can support each other too.", "朋友们让会场重新亮起来。棋子彼此联络，也能互相照应。"),
    ("An open hand", "开掌", "Victory is a moment; friendship may endure.", "胜负一时，知交可久。", "I once believed a perfect record would keep me here. Perhaps I stayed because I still had someone to teach.", "我曾以为，是未完成的名局让我留在人间。也许，我只是还想再教一个人。"),
    ("The open door", "归处", "The board returns home; the path of learning has no end.", "棋枰有归处，学道无穷期。", "Bring the board home. When another child asks how to play, leave a seat beside you. I shall be there.", "带棋盘回家吧。再有孩子问如何下棋，就在身旁留一个位置。我也会在。"),
]


def story_snapshot(defeated, seen):
    from .campaign import CHAPTERS
    from .story import completed_chapters
    complete = completed_chapters(defeated)
    reflections = []
    for chapter, row in zip(CHAPTERS, REFLECTIONS):
        n = chapter['id']
        reflections.append({"id": n, "title": bilingual(row[0], row[1]), "quote": row[3],
                            "translation": row[2], "text": bilingual(row[4], row[5]),
                            "unlocked": n == 1 or n - 1 in complete})
    pages = [
        {"id": "spirit-awakening", "title": bilingual("The board remembers", "旧枰有灵"), "unlocked": True,
         "panels": [
             ("Grandmother's old board feels strangely warm.", "外婆留下的旧棋盘，竟有一丝温度。", "Traveler", "旅人", "Who is there?", "是谁？"),
             ("Moonlight gathers into the shape of a scholar.", "月色与青雾，凝成一位古代棋士的身影。", "Yangui", "砚归", "I am Yangui, a spirit bound to this board. Akari was once my pupil.", "吾名砚归，寄此枰已久。明里，亦曾从吾学弈。"),
             ("He can see the next move, but your hand must choose it.", "他能看见下一手，却把选择留给你的手。", "Yangui", "砚归", "I shall teach; thou shalt choose. Ask me when the board grows unclear.", "吾授汝法，不代汝落子。局有不明，尽可问吾。"),
         ]},
        {"id": "spirit-homecoming", "title": bilingual("A seat for the next pupil", "为后来者留一席"), "unlocked": len(complete) == 8,
         "panels": [
             ("Eight towns later, the old board is no longer a burden.", "走过八段旅程，旧棋盘已不再是负担。", "Traveler", "旅人", "You knew Grandma all this time?", "你一直都认识外婆？"),
             ("The master's greatest lesson was never a secret winning move.", "师父最想传下来的，并不是秘密的制胜手。", "Yangui", "砚归", "A move has meaning when thou canst tell why it was played.", "知其着，更当知其所以着。"),
             ("The club opens. A child asks for a lesson. The spirit stays.", "棋社开门，孩子前来问棋，棋灵仍留在身旁。", "Yangui", "砚归", "A new pupil is at the door. Shall we begin again?", "门前又有问道者。汝我，且从第一子教起。"),
         ]},
    ]
    for page in pages:
        offset = 0 if page['id'] == 'spirit-awakening' else 3
        page['image'] = '/assets/comics/sensei.png'
        page['read'] = page['id'] in seen
        page['panels'] = [{"index": offset + i, "caption": bilingual(p[0], p[1]),
                           "speaker": bilingual(p[2], p[3]), "speech": bilingual(p[4], p[5])}
                          for i, p in enumerate(page['panels'])]
    return {"name": bilingual("Yangui", "砚归"), "pages": pages, "reflections": reflections}


def ownership_preview(size, ownership, score=None):
    if ownership is None or len(ownership) != size * size or any(not math.isfinite(v) for v in ownership):
        raise ValueError("KataGo's territory estimate is not ready. Ask again in a moment.")
    return {"estimated": True, "scoreLead": score,
            "points": [[x, y, "B" if (v := ownership[(size - 1 - y) * size + x]) >= .65 else "W" if v <= -.65 else "N"]
                       for y in range(size) for x in range(size)]}


def review_move(before_score, after_score, played, best, move_number):
    # Both scores are BLACK's expected final lead, measured before White replies.
    if before_score is None or after_score is None or not all(math.isfinite(v) for v in (before_score, after_score)):
        return None
    loss = 0 if played.lower() == best.lower() else max(0, before_score - after_score)
    severity = 'blunder' if loss >= 6 else 'mistake' if loss >= 3 else 'calm'
    quote, translation, explanation = {
        'blunder': ("缓急不分，轻重倒置！且静心审局，勿再轻投。", "Thou hast confused the urgent with the trivial! Be still, and examine the board.", bilingual("That move lost significant ground. Compare the master's recommendation before playing on.", "这一手明显失分了。先与师父原先推荐的落点比较，再继续下。")),
        'mistake': ("此着有所失，勿逐一隅而忘全局。", "Something was lost in this move. Do not forget the whole board for one corner.", bilingual("This move appears less efficient. Review the alternative and check your groups' liberties.", "这一手的效率可能偏低。回看更好的选择，也检查各块棋的气。")),
        'calm': ("一子既落，仍须观其后势。", "Once a stone is placed, study what follows.", bilingual("No large loss detected at this search depth. Keep checking the whole board.", "本次搜索未见明显目损。仍要留意全局变化。")),
    }[severity]
    return {"severity": severity, "loss": round(loss, 1), "quote": quote, "translation": translation,
            "explanation": explanation, "played": played, "best": best, "moveNumber": move_number}


def advice(node, size, stones, move_class):
    candidates = node.candidate_moves
    if not candidates:
        raise ValueError("A hint isn't available yet. Try again in a moment.")
    best = candidates[0]
    move = move_class.from_gtp(best['move'], player=node.next_player)
    point = list(move.coords) if not move.is_pass else None
    adjacent = [c for x, y, c in stones if point and abs(x-point[0])+abs(y-point[1]) == 1]
    if point is None:
        lesson = bilingual("KataGo recommends passing. If both players pass, we count the board. Play on if a group is unsettled.", "KataGo建议停一手。双方连续停着后数目；若死活未定，应继续下清楚。")
    elif 'B' in adjacent:
        lesson = bilingual("This point touches your stones. Examine how it changes their liberties and connections; compare White's next reply.", "此点与黑棋相邻。观察落子后气和联络如何改变，再看白棋的应手。")
    elif not stones:
        lesson = bilingual("Corners are easier to enclose than the center. Compare the suggested opening with the amount of space it can influence.", "角上较容易围地。观察推荐的开局点，以及它能照顾到的空间。")
    else:
        lesson = bilingual("Compare this point with your plan: check weak groups, urgent replies, and the largest open areas before choosing.", "把此点与你的计划比较：先看弱棋、必须应对之处，再找最大的空地。")
    return {"point": point, "gtp": move.gtp(), "lesson": lesson,
            "quote": "知其着，更当知其所以着。", "translation": "Learn the move, then learn the reason.",
            "visits": node.analysis['root'].get('visits', 0),
            "preview": ownership_preview(size, node.ownership, node.score)}
