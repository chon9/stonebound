import {tr as t} from './i18n.js';
const escape=s=>String(s??'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
export function engineSettings(state){
  const engine=state.engine,selected=engine.target||engine.backend;
  const waiting=engine.status==='starting'||state.match?.thinking;
  const label=engine.backend==='custom'?t('Custom engine','自定义引擎'):engine.backend.toUpperCase();
  return `<section class="ai-settings" aria-label="${t('AI processor','AI运算设备')}">
    <div class="ai-settings-heading"><span>${t('AI processor','AI运算设备')}<small>${t('KaTrain / KataGo · keeps your current game','KaTrain / KataGo · 保留当前棋局')}</small></span><b data-active-backend>${t('Active: {mode}','当前：{mode}',{mode:label})}</b></div>
    <div class="ai-backend-options" role="group" aria-label="${t('Choose CPU or GPU','选择CPU或GPU')}">${['cpu','gpu'].map(mode=>`<button class="${selected===mode?'selected':''}" data-ai-backend="${mode}" aria-pressed="${selected===mode}" ${waiting||!engine.available[mode]?'disabled':''}><strong>${mode.toUpperCase()}${mode==='gpu'?' · OpenCL':''}</strong><small>${mode==='cpu'?t('No dedicated GPU required','无需独立显卡'):t('Faster on a supported graphics card','支持的显卡可加速计算')}</small></button>`).join('')}</div>
    <p class="ai-switch-status" role="status">${engine.switching?t('Starting {mode}… Your board is saved.','正在启动{mode}……棋局已保存。',{mode:engine.target.toUpperCase()}):state.match?.thinking?t('Switch after your rival finishes this turn.','对手完成本回合后即可切换。'):engine.status==='starting'?t('Preparing the AI…','正在准备AI……'):t('GPU needs working OpenCL graphics drivers. First GPU startup may take a few minutes to tune.','GPU需要可用的OpenCL显卡驱动，首次启动可能需要数分钟调优。')}</p>
    ${engine.switchError?`<div class="ai-switch-error" role="alert"><p>${t('The selected engine could not start. Your previous engine and board were kept. You can try CPU or GPU again.','所选引擎未能启动，已保留原引擎与棋局。可重新选择CPU或GPU。')}</p><details><summary>${t('Details','详细信息')}</summary><pre>${escape(engine.switchError)}</pre></details></div>`:''}
  </section>`;
}
