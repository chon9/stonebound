"""Authored campaign content; existing rival/item IDs remain stable for old saves."""
import copy

CHAPTERS = [
    {"id":1,"title":"The letter by the river","region":"Riverside district","summary":"An unsigned letter and an old board bring you to a club with an uncertain future. Three new friends help you find the first trace of its owner.","rivals":["haru","mei","ren"],"zh":{"title":"河畔的来信","region":"河畔旧街","summary":"一封没有署名的信，一方旧棋盘，把你带到即将失去会所的河畔棋社。三位新朋友，帮你寻找棋盘主人留下的第一条线索。"}},
    {"id":2,"title":"The last train promise","region":"Station quarter","summary":"The next clue follows a railway line. A courier, a photographer and a station attendant remember a woman who carried this same board from town to town.","rivals":["kyo","yuna","toma"],"zh":{"title":"末班车的约定","region":"车站商区","summary":"线索沿着铁轨延伸。快递员、摄影师和站务员，都记得一位带着同样棋盘四处旅行的女士。她留下的约定，仍有人记得。"}},
    {"id":3,"title":"Stones beneath the fireworks","region":"Lantern market","summary":"A summer festival could raise the club's entry fee for the regional cup. Before anyone will join, a florist, a carpenter and an organizer need a reason to believe.","rivals":["koharu","daichi","nao"],"zh":{"title":"夏祭里的棋声","region":"灯笼市集","summary":"夏祭义演也许能筹齐地区杯的报名费。但在花店主人、木匠和祭典主持人加入之前，你得让他们相信，旧棋社值得再热闹一次。"}},
    {"id":4,"title":"What the tide leaves behind","region":"Seabreeze harbor","summary":"At the coast, a missing game record turns up in a library. It stops halfway through. Finding out why means listening to the lives outside the board.","rivals":["minato","riku","shiori"],"zh":{"title":"潮汐留下的空白","region":"海风港口","summary":"失落的棋谱在海边图书馆重现，却只记到一半。想知道那一局为什么中断，必须先听见棋盘之外的人生。"}},
    {"id":5,"title":"A joseki for the rain","region":"Mistwood foothills","summary":"Rain closes the mountain path. The people at a hillside school offer shelter, a few patient games, and the truth about the woman named Akari.","rivals":["aoi","itsuki","kaede"],"zh":{"title":"山雨里的定式","region":"雾林山麓","summary":"山雨封住了归路。山间学舍的棋友为你留宿，以几盘耐心的棋，说起那位名叫明里的女士，以及她未能完成的旅程。"}},
    {"id":6,"title":"Lanterns in the big city","region":"Lantern city","summary":"The regional qualifiers are harder than any town match. When a storm threatens the venue, your strongest rivals must decide what matters more than a bracket.","rivals":["akane","yuto","mizuki"],"zh":{"title":"灯火与棋影","region":"灯都棋院","summary":"地区预选赛比小镇的约棋严峻得多。暴雨威胁赛场时，最强的对手也必须决定：还有什么，比晋级表上的名字更重要。"}},
    {"id":7,"title":"The unfinished eighth game","region":"Regional cup pavilion","summary":"Three difficult games stand between the club and the exhibition award. The last sealed record will not tell you who was strongest, but why the eighth seat stayed empty.","rivals":["kaito","reina","hoshino"],"zh":{"title":"未完的第八局","region":"地区杯会场","summary":"三场艰难的对局，隔在棋社与展演奖金之间。最后一份封存棋谱，不会告诉你谁最强，却会说明第八个座位为何一直空着。"}},
    {"id":8,"title":"Someone across the board","region":"Homecoming riverside","summary":"The board returns home with twenty-three stories. Children are waiting to learn, the club is opening again, and Master Sora has kept one final seat for you.","rivals":["chisato","akira","sora"],"zh":{"title":"有人等你落子","region":"归途河畔","summary":"棋盘带着二十三段相遇回到家乡。孩子等着学棋，棋社准备重新开门。空老师，为你守着最后一个座位。"}},
]


def character(id, name, title, location, style, intro, win, lesson):
    return {"id":id,"name":name[0],"title":title[0],"location":location[0],"style":style[0],
            "intro":[line[0] for line in intro],"win":win[0],
            "lose":lesson[0]+" Come back for another game when you're ready.","thinking":lesson[0],
            "zh":{"name":name[1],"title":title[1],"location":location[1],"style":style[1],
                  "intro":[line[1] for line in intro],"win":win[1],
                  "lose":lesson[1]+" 准备好后，再来下一盘吧。","thinking":lesson[1]}}


NEW_RIVALS = [
    character('kyo',('Kyo','京'),('Always one delivery ahead','总是快一步的信使'),('Platform bicycle stand','月台自行车棚'),('Restless & resourceful','轻快而机敏'),[
        ('Ren said you were coming. I deliver letters, but this is the first one that seems to be delivering a person.','莲说你会来。我天天送信，第一次遇到一封把人送来的信。'),
        ('That stamp on your envelope belongs to our old station club. My delivery routes all begin there.','信封上的邮戳，来自旧车站棋会。我的送件路线，也都是从那里开始的。'),
        ('One game before my next route. If you win, I will introduce you to the photographer who kept the club pictures.','下一趟出发前，来一盘吧。你赢了，我就介绍保留棋会老照片的摄影师给你。')],
        ('You caught me at the next intersection. Yuna has the photographs. Take this route card and find her on platform two.','你在下一个路口追上我了。老照片在优奈手里，拿这张路线卡去二号月台找她。'),
        ('Speed helps only after you know where you are going.','知道要去哪里，快才有意义。')),
    character('yuna',('Yuna','优奈'),('The moments between moves','收藏落子之间的瞬间'),('Platform photo booth','月台照相馆'),('Observant & unhurried','细腻而从容'),[
        ('Kyo never stops long enough for a portrait. You, at least, have brought something that stays still.','京总是快得拍不到。至少你带来的棋盘，会安安静静留在镜头里。'),
        ('I found a photograph of this board beside a train window. The woman holding it wrote eight dates on the back.','我找到一张列车窗边的照片，里面就是这方棋盘。抱着它的女士，在背面写了八个日期。'),
        ('I will show you after a game. I want to see whether you look at empty points the way she did.','下完这盘，我就给你看。我想知道，你望着空点的神情，是不是和她一样。')],
        ('You saw the quiet corner I missed. The last person in this photo still works here: station attendant Toma.','你看见了我没注意的安静角落。照片里最后一个人还在这里工作——站务员冬马。'),
        ('Sometimes the most important thing is just outside the frame.','最重要的东西，有时就在画面之外。')),
    character('toma',('Toma','冬马'),('Keeper of the last departure','守着末班车的人'),('Old station waiting room','旧站候车室'),('Steady & welcoming','稳健而温厚'),[
        ('I thought I would never see that board again. Akari carried it on the last train every summer.','我以为再也见不到这方棋盘了。明里每年夏天，都带着它赶末班车。'),
        ('She promised to reopen the riverside club when she returned. This stamp was meant for its new sign.','她答应回来后，要让河畔棋社重新开门。这枚印章，本来是留给新招牌的。'),
        ('The train can wait for one more game. Show me whether that promise has found a new traveler.','末班车还能等这一盘。让我看看，那份约定是不是找到新的旅人了。')],
        ('Take the copper stones and the club stamp. The market festival is the next stop on her old route.','带上这副铜色棋子和棋社印章。沿着她的旧路线，下一站就是市集的夏祭。'),
        ('A connection missed is not always a journey ended.','错过一次换乘，不代表旅程已经结束。')),
    character('koharu',('Koharu','小春'),('A blossom on the empty point','空点上的一枝花'),('Flower stall by the bridge','桥边花铺'),('Gentle & tenacious','温柔而坚韧'),[
        ('Mei asked me to save flowers for the old club. Are you the person trying to bring it back?','小梅让我替旧棋社留些花。想让那里再热闹起来的人，就是你吗？'),
        ('We can hold an exhibition at the summer festival, but the old table is cracked. Daichi thinks nobody needs it.','夏祭可以办棋艺展演，可旧桌子已经裂了。大地觉得，反正也没人再需要它。'),
        ('Let us put a few stones on it first. Things bloom again when someone is willing to care for them.','先在它上面落几颗棋子吧。有人愿意照顾，枯枝也会再开花。')],
        ('I will bring the flowers. Show Daichi this little blossom marker; he will know I believe in your exhibition.','花由我来准备。把这枚小花标记带给大地，他就知道，我相信你的展演。'),
        ('A small living group can become a whole garden.','一小块活棋，也能长成整座花园。')),
    character('daichi',('Daichi','大地'),('The carpenter of good shape','懂得好形的木匠'),('Market carpentry shed','市集木作坊'),('Solid & practical','厚实而务实'),[
        ('Koharu sent you? That table needs new joints, not another hopeful speech.','小春介绍你来的？那张桌子缺的是新的榫头，不是另一段热血的话。'),
        ('My father made it for the club. I kept the wood, even after everybody stopped coming.','那是父亲替棋社做的桌子。大家都不来了以后，我还是留下了那块木头。'),
        ('If your groups hold together better than these joints, I will repair it for the festival.','如果你的棋比这些榫头连得更牢，我就把桌子修好，送去夏祭。')],
        ('That shape will hold. I will repair the table tonight. Nao still has a place in the festival program.','这个形，撑得住。我今晚就修桌子。奈央那里，祭典节目还留着一个位置。'),
        ('Before you build higher, make sure the joints hold.','想盖得更高，先让连接的地方牢靠。')),
    character('nao',('Nao','奈央'),('A festival needs a heartbeat','让夏祭有心跳的人'),('Lantern festival stage','灯笼祭台'),('Bold & inviting','大胆而热情'),[
        ('You have a table and flowers. Good. Now give the crowd a story worth stopping for.','桌子有了，花也有了。很好。现在，还缺一个让人愿意停下脚步的故事。'),
        ('The regional cup accepts community clubs. Its exhibition award could pay for the riverside lease.','地区杯接受社区棋会报名。展演奖金，足够支付河畔棋社的新租约。'),
        ('Play me in front of everyone. We will show them that an old board can still make a whole street listen.','就在大家面前下一盘吧。让他们看看，旧棋盘也能让整条街安静倾听。')],
        ('Listen to that applause! We have the entry fee. A sailor in the audience recognized your unfinished record.','听见掌声了吗！报名费够了。观众里有位船员，认出了你那份没下完的棋谱。'),
        ('A brave move gives the whole board something to answer.','勇敢的一手，会让整张棋盘回应。')),
    character('minato',('Minato','凑'),('Reading currents, reading stones','读潮，也读棋'),('Harbor net house','港口网屋'),('Patient & adaptable','沉着而善变'),[
        ('I was at your festival. My grandfather knew the woman in Yuna’s photograph.','我看了夏祭展演。优奈照片里的那位女士，我祖父认识。'),
        ('Akari brought a record to our harbor library. She said the empty half belonged to somebody else.','明里曾把一份棋谱带到港口图书馆，说空着的那一半，属于另一个人。'),
        ('The tide is turning. Let us see whether your stones can turn with it.','潮水快转向了。来看看，你的棋能不能跟着转。')],
        ('You did not fight the current. Riku studies at the pier; he can help you date the paper in that record.','你没有硬拗潮流。陆在码头做研究，他能帮你辨认棋谱纸张的年代。'),
        ('The sea does not reward a boat for refusing to turn.','海不会因为一条船不肯转弯，就奖励它。')),
    character('riku',('Riku','陆'),('A question at every intersection','每个交叉点都有问题'),('Tidal research pier','潮汐观测栈桥'),('Analytical & curious','理性而好奇'),[
        ('This paper has salt in its fibers. Somebody carried the record through a coastal storm.','纸纤维里有盐。有人带着这份棋谱，穿过了海边的暴雨。'),
        ('I used to think every game had one correct answer. The tide taught me to keep better notes.','以前我以为，每一局都有唯一正确的答案。潮汐教会我，先把观察记清楚。'),
        ('Play one experiment with me. Shiori will open the archive if I can explain what we found.','陪我做一盘实验吧。把发现说清楚，诗织就会替我们打开档案柜。')],
        ('A useful result, even for the losing researcher. Shiori has the matching photograph in her archive.','对输了的研究员，也是很有用的结果。诗织的档案里，有能对上的照片。'),
        ('A pattern is a question before it becomes an answer.','规律，先是一个问题，然后才是答案。')),
    character('shiori',('Shiori','诗织'),('Archivist of unfinished things','收藏未完之事的人'),('Seaside record library','海边棋谱馆'),('Careful & far-seeing','细致而深远'),[
        ('This is the record you are looking for. Seven names are written on its cover; the eighth line is blank.','你找的就是这份棋谱。封面记着七个名字，第八行却是空白。'),
        ('Akari left during the final game. The archive says only “family emergency.” Nobody recorded a resignation.','明里在最后一局中途离开。档案只写着“家中急事”，并没有认输的记录。'),
        ('Before you call a game unfinished, consider what its players were trying to protect. Sit with me a while.','说一局棋没有完成之前，先想想下棋的人在守护什么。陪我坐一会儿吧。')],
        ('You found room for both sides to live. A teacher in Mistwood knew Akari after that interrupted game.','你找到了让双方都活下去的空间。雾林山里的老师，认识中断那局棋以后的明里。'),
        ('The missing move may have been played somewhere else.','缺少的那一手，也许落在棋盘之外。')),
    character('aoi',('Aoi','葵'),('A trail beyond the obvious path','正路之外也有风景'),('Mistwood stone steps','雾林石阶'),('Adventurous & flexible','开朗而灵活'),[
        ('The mountain path is closed by rain. You can wait under this roof, or help me find another way up.','山路被雨封住了。你可以在屋檐下等，也可以陪我找另一条上山的路。'),
        ('Kaede’s school is beyond the garden pavilion. Itsuki keeps the steps clear for the children.','枫老师的学舍在园亭后面。树伯每天替孩子们扫出一条干净的石阶。'),
        ('I have a travel board. One game while the clouds decide what to do?','我带了便携棋盘。云还没决定要往哪里走，我们先来一盘？')],
        ('You found a path I had not seen. Follow the moss wall; Itsuki is waiting at the garden gate.','你找到了我没注意的路。沿着苔墙走吧，树伯就在花园门口。'),
        ('A detour is useful if it takes you somewhere worth seeing.','能带你看见值得的风景，绕路也有意义。')),
    character('itsuki',('Itsuki','树伯'),('A garden grows in its own time','花园自有它的时辰'),('Rain garden pavilion','雨庭园亭'),('Quiet & resilient','安静而坚实'),[
        ('Do not shake the rain off too hard. The seedlings below the steps are still very small.','别把伞上的雨甩得太急，台阶下的新苗还小。'),
        ('Akari planted that tree when she came to care for her sister. She thought she would stay only a week.','明里来照顾妹妹的时候，种下了那棵树。她以为自己只会留一个星期。'),
        ('Some games grow slowly. If you have patience, I have a board that has waited longer than either of us.','有些棋，要慢慢长。你若愿意等，我这方棋盘，等得比我们都久。')],
        ('You gave the weak stones time to grow. Kaede has the letter Akari never finished sending.','你给了弱小的棋子长大的时间。明里没能寄完的信，在枫老师手里。'),
        ('Pulling at a seedling will not make it grow faster.','把苗往上拔，并不会让它长得更快。')),
    character('kaede',('Kaede','枫老师'),('Teaching the next pair of hands','把棋交给下一双手'),('Hillside learning room','山间学舍'),('Patient & encouraging','耐心而包容'),[
        ('Akari stayed to look after her sister’s children. She taught us Go between lessons and dinner.','明里留下来照顾妹妹的孩子。在上课和做饭之间，她教我们下棋。'),
        ('She did not abandon the eighth game. She found another table where somebody needed her.','她没有抛弃第八局棋。她只是找到另一张更需要她的桌子。'),
        ('The children would like to watch us. Let them see that strong players can also be gentle.','孩子们想看我们下棋。让他们看看，有力量的棋手，也可以很温柔。')],
        ('Take her letter and the garden board. The regional qualifier begins in Lantern City; your friends are already on their way.','带上她的信和雨庭棋盘吧。灯都的预选赛要开始了，你的朋友们已经在路上。'),
        ('A good lesson leaves room for somebody else to try.','好的教导，会给别人留下亲自尝试的空间。')),
    character('akane',('Akane','茜'),('A spark in the training hall','训练室里的一团火'),('Lantern City training hall','灯都训练室'),('Direct & fearless','直接而果敢'),[
        ('A community club entry? I thought they had stopped taking those. Show me your registration.','社区棋会名额？我以为他们已经不收了。把你的报名表给我看看。'),
        ('I left my hometown to train here. If I cannot win, I do not know what I will take home.','我离开家乡到这里训练。如果赢不了，我不知道该带什么回去。'),
        ('No polite warm-up. Let us both find out what our stones are worth.','不来客气的热身。让棋子告诉我们，各自走到了哪里。')],
        ('You stood your ground. Yuto runs the evening practice group; he will help you prepare for the qualifier.','你站稳了。悠人负责晚间练习组，他会帮你准备预选赛。'),
        ('If you are going to stand somewhere, stand with your whole weight.','决定站在哪里，就把全部力量放在那里。')),
    character('yuto',('Yuto','悠人'),('After the last meeting','最后一场会议之后'),('Evening Go cafe','夜灯棋咖'),('Practical & inventive','务实而多变'),[
        ('I have forty minutes before the last train. That is enough for a game, if I stop checking my phone.','末班车前还有四十分钟。只要不看手机，就够下一盘。'),
        ('I gave up my club when work got busy. Seeing you fight for yours makes that excuse sound smaller.','工作忙起来以后，我就放弃了自己的棋会。看你为棋社奔走，那理由忽然显得很小。'),
        ('Let us use the time properly. Mizuki needs one more partner for the final qualifier table.','把这段时间认真用完吧。瑞希的预选桌，还差一位练习对手。')],
        ('For once I am glad the game took all my time. Mizuki is upstairs, and I will help your club with the event accounts.','第一次觉得，时间全用在棋上也很好。瑞希在楼上，活动账目我也会帮你们整理。'),
        ('You cannot save time you never let yourself spend.','不肯花给自己的时间，也存不到哪里去。')),
    character('mizuki',('Mizuki','瑞希'),('The captain keeps a seat','替队友留座的队长'),('Regional qualifier room','地区预选室'),('Disciplined & protective','严谨而可靠'),[
        ('The forecast says heavy rain. I have checked every roof panel except the one above our board.','预报说今晚有暴雨。每块屋顶我都检查过，偏偏还没看我们棋桌上面的这一块。'),
        ('I thought a captain only needed to keep winning. Lately, keeping everyone here feels harder.','以前我以为，队长只要一直赢就好。最近才觉得，让大家都留下来更难。'),
        ('This is your last qualifier game. Whatever happens, neither of us will leave a board behind in the rain.','这是你最后一场预选。无论结果如何，我们都不会把棋盘留在雨里。')],
        ('You qualify. Now help me carry the tables: the community hall has offered its dry floor to every team.','你晋级了。现在帮我搬桌子吧，社区会堂愿意把干燥的地板借给所有队伍。'),
        ('A team is stronger when nobody has to hold the roof alone.','没有人必须独自撑住屋顶，队伍才会更强。')),
    character('kaito',('Kaito','海斗'),('Three variations ahead','总多算三种变化'),('Cup analysis lounge','地区杯研究室'),('Precise & ambitious','精密而进取'),[
        ('I studied your qualifier games. Your moves are less tidy than I expected, and harder to predict.','我看过你的预选棋谱。你的棋比我想象中不整齐，也更难预测。'),
        ('My family expects a trophy. You expect to save a club. I wonder which expectation weighs more.','家里在等我带奖杯。你在等棋社重新开门。不知道哪一种期待更重。'),
        ('Let us stop comparing the weight and put it on the board.','别再比较轻重了。把它们放到棋盘上吧。')],
        ('A variation I did not prepare. Reina is your next opponent; I will watch the game without pretending I know how it ends.','那是我没准备过的变化。下一位是玲奈，这次我会认真看，不再假装已经知道结果。'),
        ('A plan is useful until you mistake it for the whole board.','计划很有用，直到你把它当成整张棋盘。')),
    character('reina',('Reina','玲奈'),('The champion who still listens','仍愿意倾听的冠军'),('Cup main hall','地区杯主厅'),('Composed & generous','从容而大方'),[
        ('Your friends repaired the venue before they knew you would qualify. That is a rare kind of confidence.','还不知道你能否晋级，朋友们就先修好了会场。那是一种难得的信任。'),
        ('I have won this cup before. What I remember most is the person who stayed to review the game I lost.','我赢过这个杯赛。最常记起的，却是陪我复盘败局的那个人。'),
        ('Come. Give me a game I will want to remember, whatever the score.','来吧。无论比分，给我一盘值得记住的棋。')],
        ('I will remember that one. Arbiter Hoshino has the last record, and he has asked to play you himself.','这一盘，我会记得。最后的棋谱在星野裁判那里，他想亲自和你下一盘。'),
        ('Winning does not make the other person’s story disappear.','赢了，并不会让对方的故事消失。')),
    character('hoshino',('Hoshino','星野'),('Witness to the empty seat','见过那个空座位的人'),('Cup record chamber','地区杯棋谱室'),('Measured & insightful','克制而通透'),[
        ('I was the recorder of Akari’s eighth game. I kept the board position after she left.','明里第八局棋的记录员，就是我。她离开后，我一直保留着那个局面。'),
        ('Her opponent was Sora. He refused to record a forfeit. He said a game can wait for the people who matter.','她的对手是空。他不肯记弃权，说重要的人值得棋等一等。'),
        ('This exhibition award is for a living community, not an old legend. Show me the club you will build.','展演奖属于活着的社区，不是旧传说。让我看见，你想建成怎样的棋社。')],
        ('The award is yours. Take the sealed case home. Sora has been waiting to hear all the stories you gathered.','展演奖属于你们。把封好的木匣带回去吧，空一直在等你讲路上收集的故事。'),
        ('A record keeps the moves. People keep the meaning.','棋谱留下落点，人留下意义。')),
    character('chisato',('Chisato','千里'),('The first lesson after homecoming','归来后的第一课'),('Reopened club classroom','重开棋社学堂'),('Kind & tenacious','温和而执着'),[
        ('We cleaned the windows while you were away. The children drew seating plans for everyone you wrote about.','你出门以后，我们擦亮了窗户。孩子们替你信里提到的人，都画好了座位。'),
        ('I can teach the rules. I need help showing them why someone would keep coming back after losing.','规则我可以教。可为什么输了还愿意回来，我需要你帮他们看见。'),
        ('Play a game with me, with every small kindness left on the board.','陪我下一盘吧。把每一点善意，也留在棋盘上。')],
        ('They are already asking for rematches. Akira is outside fixing the sign. The club looks like itself again.','他们已经开始约下一盘了。彰在外面修招牌，棋社又有了自己的模样。'),
        ('The next generation learns from what we make room for.','下一代，会从我们愿意留出的空间里学习。')),
    character('akira',('Akira','彰'),('The sign that never came down','始终没摘下的招牌'),('Riverside club entrance','河畔棋社门口'),('Honest & determined','坦率而坚定'),[
        ('My grandmother was Akari. I wrote the unsigned letter because I did not know whether anyone would answer.','明里是我的祖母。那封没署名的信，是我写的。我不知道，会不会有人回应。'),
        ('She said the board belonged to whoever could bring its stories home. I could repair the sign, but not make that journey.','她说，谁能把棋盘的故事带回来，它就属于谁。我能修好招牌，却没能走完那段路。'),
        ('One game before Sora arrives. I would like to know the person who answered our letter.','空老师来之前，陪我下一盘吧。我想认识那个回应了来信的人。')],
        ('Thank you for answering. Grandmother’s last gift is in the case. Sora is waiting at her old seat.','谢谢你回应了这封信。祖母最后的礼物就在木匣里。空老师，在她以前的座位等你。'),
        ('Someone has to make the first move, even when the answer is uncertain.','即使不知道有没有回应，也总要有人先落下第一子。')),
]

# id, English, Chinese, pattern, color, accent, unique victories, source rival (gift)
BOARD_ROWS = [
    ('cedar','Cedar Morning','杉木晨光','wood','#c38e58','#f0c783',2,None),
    ('walnut','Walnut Study','胡桃书斋','wood','#927253','#d9c49b',3,None),
    ('maple','Maple Honey','枫糖暖木','wood','#dfbc82','#a66c3f',4,None),
    ('ebony','Ebony Quiet','乌木静室','wood','#4c504e','#b4bfab',5,None),
    ('washi','Washi Letter','和纸来信','paper','#e6dec5','#b7a47b',2,None),
    ('river_map','River Route','河川路图','ripple','#b8c8ad','#6b968b',3,'ren'),
    ('station_oak','Platform Oak','月台橡木','rail','#c39d6d','#796e56',5,None),
    ('railway_night','Last Train Indigo','末班车靛蓝','rail','#455975','#a4bbc9',6,None),
    ('festival_ink','Festival Lanterns','夏祭灯影','lantern','#bd8872','#f3ce85',9,'nao'),
    ('blue_porcelain','Blue Porcelain','青花白瓷','porcelain','#c6dce1','#6e99b6',7,None),
    ('tidal_glass','Tidal Glass','潮汐海玻璃','ripple','#8fbebc','#e5e5bd',10,None),
    ('shore_stone','Shore Slate','海岸岩灰','marble','#a8b4af','#e1ded0',11,None),
    ('storm_slate','Storm Slate','雨云青石','rain','#798b9a','#c4d5d7',12,None),
    ('moss_garden','Rain Garden','雨庭苔影','garden','#9fae86','#d8d4a9',15,'kaede'),
    ('autumn_leaf','Maple Letter','红叶书简','leaves','#c29d75','#8a6251',14,None),
    ('city_brass','City Brass','灯都黄铜','metal','#c5aa69','#ede2b3',16,None),
    ('neon_grid','Neon Intersections','霓虹交点','circuit','#435f65','#93c7b3',18,None),
    ('star_chart','Night Star Chart','夜航星图','stars','#3b4868','#c7d3c3',20,None),
    ('ink_mountain','Ink Mountains','水墨群山','ink','#c1c3ae','#7c8e88',21,None),
    ('homecoming','The Open Door','归来之门','kintsugi','#d4b781','#f8dc8d',24,'sora'),
]
STONE_ROWS = [
    ('tea_cream','Tea & Cream','红茶与奶霜','smooth','#755844','#f5e6c9',1,None),
    ('charcoal_chalk','Charcoal & Chalk','炭墨与粉笔','matte','#434c4b','#e3e6da',2,None),
    ('river_pebble','River Pebble & Foam','河卵石与浪花','speckle','#65796f','#dce5d6',3,None),
    ('station_copper','Copper & Glass','站灯铜与玻璃','metal','#9d6946','#d8e7dc',6,'toma'),
    ('sakura_opal','Sakura & Opal','樱石与欧泊','vein','#9c5e70','#f3e0db',5,None),
    ('festival_glass','Lantern & Glass','灯火与流璃','glow','#af683c','#e8dcae',7,None),
    ('sea_salt','Tide & Salt','潮声与海盐','wave','#326f80','#dfedeb',12,'shiori'),
    ('deep_sea','Deep Sea & Sand','深海与细砂','wave','#315769','#e3d1a8',10,None),
    ('moss_agate','Moss Agate & Ivory','苔玛瑙与象牙','vein','#55765e','#eee6cf',11,None),
    ('autumn_garnet','Garnet & Moonlight','秋榴石与月色','vein','#854b4e','#e7e5d4',13,None),
    ('rain_crystal','Rain & Crystal','雨石与水晶','speckle','#576f87','#dce5e6',14,None),
    ('sunrise_gold','Sunrise & Gold','朝霞与金砂','metal','#a77348','#eee0b8',15,None),
    ('city_neon','Neon & Frost','霓虹与霜白','glow','#476e76','#dce9df',18,'mizuki'),
    ('violet_amethyst','Amethyst & Pearl','紫晶与白珠','vein','#67567f','#eee4e5',17,None),
    ('meteor_iron','Meteor & Ice','陨铁与冰魄','speckle','#535967','#dce8ee',18,None),
    ('star_silver','Starlight & Silver','星辉与银砂','galaxy','#3e4b70','#e3e5db',20,None),
    ('champion_seal','Champion’s Seal','杯赛印玺','seal','#6c5240','#e4d9b6',21,'hoshino'),
    ('kintsugi_stones','Mended Gold & Clay','金缮与陶白','crack','#645346','#e5dac0',22,None),
    ('ink_jade','Inkstone & Jade','砚墨与青玉','wave','#3e5c56','#dce9d1',23,None),
    ('warm_home','Hearth & Milk','炉火与乳白','glow','#a56544','#f5e6cf',24,None),
]


def expand_catalog(opponents, items):
    legacy = {r['id']:copy.deepcopy(r) for r in opponents}
    legacy['ren']['win'] = 'Your stones have a voice of their own. Take this railway ticket: somebody at the station knew the owner of your board.'
    legacy['ren']['zh'] = {'win':'你的棋子，有自己的声音。拿着这张旧车票吧，车站有人认识这方棋盘以前的主人。'}
    legacy['sora'].update(intro=[
        'Your postcards have made this old room feel wide as the world.',
        'Akari left to care for her family. I kept the board until she could return. It found its way to you instead.',
        'We need not finish our old game. Let us begin a new conversation, with all the stories you brought home.'],
        win='Akari would have loved these stories. Open the doors. Someone is waiting for their first game.',
        zh={'intro':['你的明信片，让这间老屋像整个世界一样宽广。','明里为了照顾家人离开了。我替她收着棋盘，等她回来。后来，棋盘到了你手中。','不必续完当年的旧局。带着你一路的故事，和我下一盘新的棋吧。'],
            'win':'明里一定会喜欢这些故事。把门打开吧，还有人在等着自己的第一盘棋。'})
    all_rivals = {**legacy, **{r['id']:copy.deepcopy(r) for r in NEW_RIVALS}}
    order = [id for chapter in CHAPTERS for id in chapter['rivals']]
    ranks = list(range(15,0,-1)) + [1,0,0,-1,-1,-2,-2,-3,-3]
    new_ids = [r['id'] for r in NEW_RIVALS]
    result = []
    for index,id in enumerate(order):
        rival = all_rivals[id]
        chapter = index//3+1
        rival.update({'chapter':chapter,'kyu':ranks[index], 'rank':f'{ranks[index]} kyu' if ranks[index]>0 else f'{1-ranks[index]} dan',
                      'requires':order[index-1] if index else None,'order':index+1,'boss':index%3==2,
                      'reward':[250,350,450][index] if index<3 else 300+chapter*95+index*15,
                      'xp':100+index*30})
        if id in new_ids:
            portrait_index = new_ids.index(id)
            rival.update({'portrait':portrait_index%4,'portrait_sheet':2+portrait_index//4})
        else:
            rival['portrait_sheet']=1
        result.append(rival)
    treasures=copy.deepcopy(items)
    for existing in treasures:
        existing.update({'pattern':'wood' if existing['type']=='board' else 'smooth','white_color':'#f0efe3','rarity':'common','source':'shop','accent':'#c6b98c'})
    for type,rows in [('board',BOARD_ROWS),('stones',STONE_ROWS)]:
        for id,en,zh,pattern,color,accent,wins,gift in rows:
            chapter=min(8,max(1,(wins+2)//3))
            c=CHAPTERS[chapter-1]
            tag='Chapter keepsake' if gift else c['region']+' collection'
            description=(f'A keepsake of {c["title"].lower()}, awarded for completing the chapter.' if gift else
                         f'Crafted along the route through {c["region"].lower()}. Its {pattern} finish carries a small memory of that place.')
            zhdesc=f'完成「{c["zh"]["title"]}」后获得的纪念藏品。' if gift else f'来自{c["zh"]["region"]}的手作珍藏，把旅途中一小段风景留在每次落子之间。'
            treasures.append({'id':id,'name':en,'type':type,'price':0 if gift else 180+wins*42,'wins':wins,
                              'tag':tag,'description':description,'color':color,'accent':accent,'white_color':accent if type=='stones' else '#f0efe3',
                              'pattern':pattern,'rarity':'legendary' if gift else 'epic' if wins>=16 else 'rare' if wins>=7 else 'common',
                              'source':'story' if gift else 'shop','gift_from':gift,
                              'zh':{'name':zh,'tag':'章节纪念' if gift else c['zh']['region']+'藏品','description':zhdesc}})
    return result,treasures
