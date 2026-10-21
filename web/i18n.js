let language = 'en';
export function setLanguage(value) { language = value === 'zh-CN' ? 'zh-CN' : 'en';document.documentElement.lang=language;document.title=language==='zh-CN'?'棋缘物语 · Stonebound':'Stonebound · A Go Story'; }
export function tr(en, zh, values={}) { return (language==='zh-CN'?zh:en).replace(/\{(\w+)\}/g,(_,key)=>String(values[key]??'')); }
export const getLanguage = () => language;

const rivals = {
  haru: {name:'晴',title:'河畔的老朋友',location:'河畔棋社',style:'随性而好奇',intro:[
    '嘿！你就是找到那块旧棋盘的人吧？我叫晴。',
    '爷爷以前总说，每一颗棋子都是一场对话的开始。我一直在等一位新朋友，听听不同的故事。',
    '就在河边下一盘吧。不用着急，每个人都是从第一颗棋子开始的。'],
    win:'你很有感觉嘛！去茶馆找小梅吧，她一定想认识你。就说是我介绍的。',
    lose:'这盘聊得很开心。还是老地方，再来一盘？河水又不会跑掉。',thinking:'嗯……这颗棋子，该落在哪里呢？'},
  mei: {name:'小梅',title:'茶香、脱先与一点小心思',location:'木漏日茶馆',style:'耐心而灵动',intro:[
    '晴跟我提起过你。我们这座安静的小镇，终于来了一位新棋友！',
    '以前我趁泡茶的空当下棋。现在一坐到棋盘前，连茶凉了都不知道。',
    '赢了这盘，我就介绍莲给你认识。不过先提醒你，他对棋子可是很认真的。'],
    win:'下得漂亮！下一杯茶算我的。莲常在书院练棋，我想你已经准备好了。',
    lose:'多一点耐心，总会有收获。就像泡茶一样。准备好后，随时再来。',thinking:'好棋如好茶，值得多等一会儿……'},
  ren: {name:'莲',title:'总在思考下一步',location:'青春书院',style:'专注而严谨',intro:[
    '你就是大家最近提起的棋手？我叫莲。请坐。',
    '以前我总觉得，围棋就是寻找最完美的一手。最近，我开始有些怀疑了。',
    '让我看看你眼中的棋盘吧。也许我们都能学到些什么。'],
    win:'这一手，我没想到。去山顶亭找空老师吧。他一直在等像你这样的棋手。',
    lose:'试着看看整张棋盘。有时，输掉局部的一场战斗，反而能赢下整盘棋。改天再来。',thinking:'这里一定还有什么。让我再想一想。'},
  sora: {name:'空老师',title:'旧故事的守护者',location:'山顶棋亭',style:'沉静而深远',intro:[
    '你来了以后，小镇的节奏都不一样了。连莲都开始笑了。',
    '你带着的那块旧棋盘，曾经属于我。我把它留给愿意听它讲故事的人。',
    '没有最后一课。只有下一盘棋，和坐在对面的另一个人。开始吧？'],
    win:'下得真好。棋盘现在属于你了，未来的故事也是。小镇永远为你留着一个座位。',
    lose:'每一次落败，都会留下一点智慧。收好棋盘，我们的对话才刚刚开始。',thinking:'仔细听。那些安静的棋子，也有话想说。'},
};
const items = {
  hinoki:{name:'旧桧木',tag:'最初的棋盘',description:'温润木色，等待一千个故事的开始。'},
  sakura:{name:'樱色初绽',tag:'春日藏品',description:'柔和的玫瑰木，染上初春的一抹樱色。'},
  bamboo:{name:'竹林清影',tag:'静心之选',description:'清凉竹绿，让纷乱的思绪渐渐平静。'},
  midnight:{name:'深夜靛蓝',tag:'末班车之后',description:'献给那些舍不得结束的深夜对局。'},
  classic:{name:'青石与白贝',tag:'经典之选',description:'熟悉的手感，陪你落下每一颗安心的棋子。'},
  jade:{name:'翡翠与白瓷',tag:'河畔珍藏',description:'深绿翡翠搭配温润白瓷，自有一份沉静。'},
  amber:{name:'琥珀与珍珠',tag:'流金时刻',description:'蜜色琥珀，与柔光珍珠相映成趣。'},
  obsidian:{name:'黑曜与月光',tag:'名师赠礼',description:'把一小片夜空，藏进每一步落子。'},
};
export function localizeState(data) {
  if(language==='en') return data;
  return {...data,opponents:data.opponents.map(r=>({...r,...rivals[r.id],...r.zh,rank:r.kyu>0?`${r.kyu}级`:`${1-r.kyu}段`})),items:data.items.map(i=>({...i,...items[i.id],...i.zh})),story:{...data.story,chapters:data.story.chapters.map(c=>({...c,...c.zh})),pages:data.story.pages.map(p=>({...p,panels:p.panels.map(v=>({...v,...v.zh}))}))}};
}

const errors = new Map([
  ['You have a game in progress. Resume it or leave it first.','你还有一盘未完成的对局。请先继续或离开。'],
  ['Choose a rival from the city.','请在城镇中选择一位棋友。'],
  ['Meet the previous rival on your journey first.','先战胜前一位棋友，继续你的旅程吧。'],
  ['Choose a 9×9, 13×13, or 19×19 board.','请选择9路、13路或19路棋盘。'],
  ['Start a new game in the city.','请先在城镇中开始一盘新棋。'],
  ['Your rival is thinking. Give them a moment.','对手正在思考，请稍等一下。'],
  ["Retry your rival's turn before playing.",'请先重试对手的回合。'],
  ['Choose an intersection on the board.','请在棋盘的交叉点落子。'],
  ['That point is occupied, repeats a ko, or leaves your stones with no liberties.','这里已有棋子，或涉及打劫、禁入点。请换一处落子。'],
  ['Place your first stone to begin.','请先落下第一颗棋子。'],
  ['Wait for your rival to finish thinking before leaving.','请等待对手完成思考后再离开。'],
  ["It's your turn to play.",'现在轮到你落子了。'],
  ["A hint isn't available yet. Try again in a moment.",'提示暂时还没准备好，请稍后再试。'],
  ['Complete the chapter to earn this keepsake.','完成对应章节后，即可获得这件纪念藏品。'],
  ['Complete the previous chapter to read this story.','请先完成前一章，再阅读这段故事。'],
  ['This item is not in the shop.','商店里没有这件物品。'],
  ['You already own this item.','你已经拥有这件物品了。'],
  ["You'll need a few more coins. Win a match to earn them.",'金币还不够。赢下对局就能获得金币。'],
  ['Visit the shop to unlock this item first.','请先前往商店解锁这件物品。'],
  ['KataGo is warming up. Your first game will be ready shortly.','KataGo正在准备，很快就可以开始对局了。'],
]);
export function errorText(message) {
  if(language==='en') return message;
  if(errors.has(message)) return errors.get(message);
  const locked=message.match(/^Befriend (\d+) rivals by winning to unlock this item\.$/);
  if(locked) return `战胜${locked[1]}位棋友后即可解锁这件物品。`;
  if(message.startsWith("KataGo couldn't complete this turn:")) return 'KataGo未能完成此回合。请重试，或悔棋后继续。';
  return '暂时无法完成操作，请重试。'+(message.includes('KataGo')?' 请在设置中查看引擎状态。':'');
}

export const lessons = [
  ['Your first stone','第一颗棋子','You play black and move first. Choose an empty intersection to place a stone. Your rival plays white. Stones stay where you place them unless captured.','你执黑先行。点击空的交叉点落子，对手执白。棋子落下后不能移动，除非被提走。'],
  ['Room to breathe','给棋子留一口气','Empty points directly beside a stone are its liberties. Connected stones share liberties. Surround a group on every side to capture it. Diagonals do not count.','棋子上下左右相邻的空点叫作“气”。相连的棋子共用气。围住对方棋块的全部气，就能提走它。斜角不算相连。'],
  ['A place of your own','围出属于你的天地','Enclose empty points to build territory. Two separate enclosed empty points, called eyes, keep a group safe. Connect your stones and leave space to grow.','围住空点，建立自己的地盘。棋块拥有两个独立的“眼”，就不易被提走。保持联络，也给自己的棋留出生长的空间。'],
  ['When to pass','什么时候停一手','Pass when no useful moves remain. Two consecutive passes end the game. Chinese area scoring counts living stones and enclosed empty points. White receives 6.5 komi. Play out unsettled groups before passing.','没有有用的落点时，可以停一手。双方连续停着即结束对局。中国规则计算活子与所围空点，白棋获得6.5目贴目。停着前，请先走清尚未确定死活的棋块。'],
  ['A little guidance','需要一点指引时','Ask for a hint to see KataGo’s suggested move. Undo takes back your last move and your rival’s reply. There is no time limit and no penalty for learning.','点击提示，就能看到KataGo建议的落点。悔棋会撤回你上一手和对手的应手。这里没有时间限制，也不会因为学习而受到惩罚。'],
  ['One special rule: ko','一条特别的规则：劫','You cannot immediately recapture if it repeats the previous board position. Play elsewhere first. A move with no liberties is illegal unless it captures an opposing group.','如果立即回提会让棋盘重复上一局面，就必须先在别处走一手，这叫“劫”。不能在没有气的位置落子，除非这一手能提走对方的棋子。'],
];
