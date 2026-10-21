"""Original bilingual manga script. Art contains no baked-in dialogue."""
import copy

from .campaign import CHAPTERS

# Each chapter has a three-panel arrival and a three-panel conclusion.
# (English narration, Chinese narration, speaker EN/ZH, dialogue EN/ZH)
SCRIPT = [
    [
        ('A letter without a signature. A board with eight empty inlays.', '一封没有署名的信，一方留着八处空嵌的旧棋盘。', 'The letter', '信笺', 'Bring Akari’s board to the river. Someone still remembers her next move.', '带着明里的棋盘来河边吧。还有人，记得她的下一手。'),
        ('Haru saves a seat. Mei sets down a cup. Ren looks up from his record.', '晴留下一张椅子，小梅沏好茶，莲从棋谱前抬起头。', 'Haru', '晴', 'A traveling Go player? Then your first stop is right here.', '旅行中的棋手？那第一站，就是这里。'),
        ('The old club’s lease expires before autumn. Its tables have fallen quiet.', '旧棋社的租约将在秋天到期，棋桌边早已安静下来。', 'Mei', '小梅', 'We need more than a locked door and a memory. Let’s give people a reason to return.', '不能只留下锁着的门和回忆。我们得让大家，有个回来的理由。'),
        ('Ren’s last stone connects two distant groups.', '莲的最后一手，把相隔的两块棋连在了一起。', 'Ren', '莲', 'My grandfather kept Akari’s railway ticket. Follow that route. Ask what she left behind.', '爷爷留着明里的旧车票。沿着这条线走吧，问问她留下了什么。'),
        ('A tiny river-shaped inlay fits the first empty space.', '一枚河纹嵌片，恰好填进棋盘的第一处空缺。', 'Traveler', '旅人', 'Grandma never told me she had friends in so many places.', '外婆从来没说过，她在这么多地方都有朋友。'),
        ('At dusk, a train carries the board beyond the river.', '暮色里，列车载着旧棋盘，驶出河畔。', 'Haru', '晴', 'Write to us! And keep a seat open on the way back.', '记得写信！回来的时候，也给我们留个位置。'),
    ],
    [
        ('The station clock is five minutes slow. Kyo knows every platform.', '车站的钟慢了五分钟，京却记得每一座月台。', 'Kyo', '京', 'That ticket? It’s from the year the night service stopped running.', '这张车票？是夜班车停运那年的。'),
        ('Yuna develops a photograph: a young Akari beside a station board.', '结奈洗出一张照片：年轻的明里，站在车站棋桌旁。', 'Yuna', '结奈', 'Look at the corner. That’s Toma’s tea flask. He must have been there.', '看角落，是冬真的保温壶。他当时一定在场。'),
        ('Toma places a stone before the departure bell.', '发车铃声响起前，冬真落下一子。', 'Toma', '冬真', 'I promised her one more game before the last train. We never finished.', '我答应末班车前再陪她下一盘，那局棋却没下完。'),
        ('A long connection survives by a single liberty.', '漫长的联络，靠着最后一口气活了下来。', 'Toma', '冬真', 'I waited on the wrong platform that night. For years, I called it her broken promise.', '那晚，是我等错了月台。这些年，却一直说是她失约。'),
        ('A copper station seal shines beside the faded photograph.', '褪色的照片旁，一枚铜色车站印章微微发亮。', 'Traveler', '旅人', 'Then let this game be the one you were waiting for.', '那就把今天这一局，当作迟来的赴约吧。'),
        ('Yuna’s new photograph catches all four of you laughing.', '结奈的新照片，把四个人的笑容都留了下来。', 'Kyo', '京', 'The lantern market has another of her records. I’ll deliver your letter to the club.', '灯笼市集还有她的棋谱。给棋社的信，我替你送。'),
    ],
    [
        ('Summer lanterns sway above Koharu’s flower stall.', '夏日灯笼，在小春的花摊上轻轻摇晃。', 'Koharu', '小春', 'We planned a Go exhibition. Then the table legs gave way.', '说好办围棋展演，结果棋桌的腿先散架了。'),
        ('Daichi gathers loose boards. Nao studies an empty stage.', '大地收拢松散的木板，奈绪望着空荡的舞台。', 'Daichi', '大地', 'A good joint holds because every piece carries some weight.', '接得牢，是因为每块木头都分担了一点重量。'),
        ('The crowd expects a champion. Nao hides her shaking hands.', '观众等着看冠军，奈绪却悄悄藏起发抖的手。', 'Nao', '奈绪', 'I’m afraid they’ll see how often I get it wrong.', '我怕他们发现，我也常常下错。'),
        ('Nao’s stones give up a corner and find the center.', '奈绪让出一角，棋子却走向了更宽阔的中央。', 'Nao', '奈绪', 'I kept trying to protect everything. There wasn’t room left to play.', '我一直想守住所有东西，反而没地方下棋了。'),
        ('A repaired table becomes the festival’s busiest gathering place.', '修好的棋桌，成了祭典上最热闹的一角。', 'Koharu', '小春', 'The donations are for your club. Keep the lantern board, too.', '这些捐款留给你们的棋社。这方灯影棋盘，也带上吧。'),
        ('Fireworks bloom. A child asks to place the next stone.', '烟花盛开，一个孩子问，下一子能不能让他来。', 'Traveler', '旅人', 'Maybe saving a club begins with inviting someone to sit down.', '也许，留住一间棋社，要先从请一个人坐下开始。'),
    ],
    [
        ('Salt wind lifts Minato’s charts at the harbor.', '海风翻起港边的航图，凑用棋盒压住纸角。', 'Minato', '凑', 'The tide changes every route. A Go board is no different.', '潮水一变，航路就得变。棋盘也是。'),
        ('Riku measures the waves. Shiori opens the harbor archive.', '陆记录潮位，诗织打开港口档案室的门。', 'Shiori', '诗织', 'There’s an exhibition record here. Seven games, and an eighth with no result.', '这里有一份巡回展演的记录。七局完整，第八局没有结果。'),
        ('A storm closes the ferry. The unfinished record lies between you.', '暴雨让渡轮停航，未完的棋谱摆在两人之间。', 'Traveler', '旅人', 'Was Grandma losing? Is that why she left?', '外婆当时落后了吗？所以才离开？'),
        ('Shiori turns over a page that was filed upside down.', '诗织翻过一张放反了的附页。', 'Shiori', '诗织', 'No resignation. Just a note: “My sister needs help. Please keep the board.”', '没有认输，只有一句话：妹妹需要帮忙，请替我收好棋盘。'),
        ('Sea-glass stones glow in the first clear light.', '天光初开，海玻璃般的棋子映出潮色。', 'Riku', '陆', 'A missing result doesn’t mean a missing reason.', '没有写下结果，不代表没有离开的理由。'),
        ('Beyond the harbor, the mountain bus starts its engine.', '港口之外，进山的巴士发动了。', 'Minato', '凑', 'Kaede taught beside her. She’ll know what happened next.', '枫老师曾和她一起教孩子。后来的事，她应该知道。'),
    ],
    [
        ('Rain threads through Aoi’s mountain rest stop.', '山雨细密，葵把歇脚亭的灯点亮。', 'Aoi', '葵', 'Wait out the rain with a game. The mountain will still be here.', '等雨的时候下一盘吧。山又不会跑掉。'),
        ('Itsuki’s stones gather like moss around the garden path.', '树的棋子，像庭院小路旁渐渐长起的青苔。', 'Itsuki', '树', 'You keep searching for the quickest move. Where are you trying to arrive?', '你一直在找最快的一手。到底急着去哪里？'),
        ('Kaede recognizes Akari’s photograph. Children gather at her table.', '枫老师认出照片里的明里，孩子们围到棋桌旁。', 'Kaede', '枫老师', 'She stayed to help raise her sister’s children. The exhibition could wait.', '她留下来帮妹妹照顾孩子。展演，可以以后再办。'),
        ('A quiet move gives a weak group somewhere to live.', '一手安静的棋，给孤弱的棋块留出了安身之处。', 'Kaede', '枫老师', 'She never stopped playing. She just made smaller boards for smaller hands.', '她没有停止下棋。她只是做了更小的棋盘，交给更小的手。'),
        ('A moss-green board rests beside letters from former pupils.', '苔绿色棋盘旁，堆着昔日学生寄来的信。', 'Traveler', '旅人', 'I thought I was finishing her journey. I’m finally beginning to see it.', '我以为自己在替她走完旅程。现在，才开始看见她走过的路。'),
        ('After the rain, an invitation arrives from the regional cup.', '雨停以后，地区杯的邀请函送到了山间。', 'Aoi', '葵', 'Your friends entered the club for the community exhibition grant. Go meet them.', '朋友们替棋社报名了社区展演资助。去城里和他们会合吧。'),
    ],
    [
        ('Lantern city plays quickly. Akane’s clock never seems to stop.', '灯都的棋下得很快，茜的棋钟仿佛从不停歇。', 'Akane', '茜', 'Three qualifiers, one exhibition place. Ready to be seen?', '三场选拔，一个展演名额。准备好站到大家面前了吗？'),
        ('Yuto shuts his café early to make room for practice.', '悠斗提前打烊，把咖啡馆留给练棋的人。', 'Yuto', '悠斗', 'A room earns its keep by what happens inside it.', '一间屋子的价值，要看里面发生了什么。'),
        ('A storm breaks the venue roof. Mizuki watches rain cross the floor.', '暴雨打坏赛场屋顶，瑞希望着流过地板的雨水。', 'Mizuki', '瑞希', 'If we cancel, the smaller clubs lose their only chance this year.', '要是取消，小棋社今年就再没有机会了。'),
        ('Friends arrive carrying tables, lamps, kettles, and towels.', '朋友们带着棋桌、台灯、茶壶和毛巾赶来。', 'Kyo', '京', 'You wrote to everyone. Did you think nobody would answer?', '你给每个人都写了信。难道以为，不会有人回信吗？'),
        ('Under borrowed lamps, the final qualifying game reaches its end.', '借来的灯下，最后一场选拔落下终局。', 'Mizuki', '瑞希', 'Take these stones. You earned a place, and helped everyone keep theirs.', '带上这副棋子吧。你赢得了名额，也替大家守住了机会。'),
        ('The repaired hall glows long after the storm has passed.', '雨过之后，临时会场的灯火久久未熄。', 'Traveler', '旅人', 'The club already reaches farther than its walls.', '棋社的边界，原来早就不止那几面墙。'),
    ],
    [
        ('The regional pavilion is quiet enough to hear a sleeve brush the board.', '地区杯会场很安静，衣袖掠过棋盘的声音都听得见。', 'Kaito', '海斗', 'A plan is useful until the board asks a better question.', '计划很有用，直到棋盘提出更好的问题。'),
        ('Reina, last year’s champion, sets her trophy aside.', '去年的冠军玲奈，把奖杯放到一边。', 'Reina', '玲奈', 'Don’t play the trophy. There’s only a person sitting here.', '别对着奖杯下棋。坐在这里的，只是一个人。'),
        ('Arbiter Hoshino brings a sealed wooden case from the exhibition archive.', '裁判星野，从展演档案中取出一只封存的木匣。', 'Hoshino', '星野', 'Akari’s opponent left this. The seal says: “When the board comes home.”', '这是明里的对手留下的。封条上写着：等棋盘回家的时候。'),
        ('The final exhibition game ends with an open hand across the table.', '最后一场展演结束，棋桌对面伸来一只手。', 'Reina', '玲奈', 'Your club’s proposal was selected. Children’s tables, open lessons, visiting players. Keep that promise.', '棋社的提案通过了。儿童棋桌、公开课堂、巡回棋友。记得兑现这些约定。'),
        ('Inside the case: seven records, and a letter from Sora.', '木匣里有七张棋谱，还有一封空老师的信。', 'Sora’s letter', '空老师的信', 'The eighth game was never a debt. I only hoped we would sit together again.', '第八局，从来不是欠下的债。我只是盼着，能再一起坐下来。'),
        ('On the homebound train, the board occupies the seat beside you.', '归途列车上，棋盘安静地坐在你身旁。', 'Traveler', '旅人', 'There’s one more person I need to meet.', '还有一个人，我想亲自见一面。'),
    ],
    [
        ('Chisato’s pupils have drawn a welcome banner by the river.', '千里的学生，在河边画好了欢迎回来的旗子。', 'Chisato', '千里', 'They’ve been learning from your postcards. Now they want a game with the traveler.', '孩子们一直看着你的明信片学棋。现在，都想和旅人下一盘。'),
        ('Akira lifts the repaired club sign. His handwriting matches the first letter.', '明提起修好的棋社招牌，字迹和最初那封信一模一样。', 'Akira', '明', 'Sora is my grandfather. I sent the letter. I hoped someone would bring his stories outside again.', '空老师是我爷爷。信是我寄的。我希望，有人能把他的故事重新带出门。'),
        ('Sora waits at a table with two cups and no clock.', '空老师在棋桌旁等候，桌上有两杯茶，没有棋钟。', 'Sora', '空老师', 'We needn’t recreate the old position. Tell me about the games you played on the way.', '不必摆回当年的局面。和我讲讲，你一路下过的棋吧。'),
        ('A new game ends. The eight inlays catch the afternoon light.', '新的一局走到终点，八枚嵌片映着午后的光。', 'Sora', '空老师', 'Akari would have loved these stories. Thank you for bringing everyone home.', '明里一定会喜欢这些故事。谢谢你，把大家带回家。'),
        ('The club doors open. Friends from every stop carry in their boards.', '棋社重新开门，每一站的朋友，都带着自己的棋盘来了。', 'Traveler', '旅人', 'This board isn’t a monument. Who wants the next game?', '这方棋盘，不是纪念碑。下一盘，谁来？'),
        ('A small hand places the first stone of another story.', '一只小小的手，落下另一个故事的第一颗棋子。', 'A new pupil', '新来的孩子', 'Can you teach me how to begin?', '你可以教我，怎么开始吗？'),
    ],
]


def completed_chapters(defeated):
    return [c['id'] for c in CHAPTERS if set(c['rivals']).issubset(defeated)]


def story_snapshot(defeated, seen=()):
    chapters, pages = [], []
    previous_complete = True
    for chapter, script in zip(CHAPTERS, SCRIPT):
        c = copy.deepcopy(chapter)
        complete = set(c['rivals']).issubset(defeated)
        c.update(unlocked=previous_complete, completed=complete,
                 progress=sum(r in defeated for r in c['rivals']))
        chapters.append(c)
        for half, kind in enumerate(('open', 'close')):
            page_id = f'ch{c["id"]:02d}-{kind}'
            unlocked = previous_complete and (half == 0 or complete)
            panels = []
            if unlocked:
                for index, (en, zh, speaker, zh_speaker, speech, zh_speech) in enumerate(script[half*3:half*3+3]):
                    panels.append({'index':half*3+index, 'caption':en, 'speaker':speaker, 'speech':speech,
                                   'zh':{'caption':zh,'speaker':zh_speaker,'speech':zh_speech}})
            pages.append({'id':page_id, 'chapter':c['id'], 'kind':kind, 'unlocked':unlocked,
                          'read':page_id in seen, 'image':f'/assets/comics/chapter-{c["id"]:02d}.png',
                          'panels':panels})
        previous_complete = previous_complete and complete
    return {'chapters':chapters, 'pages':pages}
