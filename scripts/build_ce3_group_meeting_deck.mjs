#!/usr/bin/env node

import fs from "node:fs/promises";
import path from "node:path";
import { spawnSync } from "node:child_process";
import { fileURLToPath } from "node:url";

const ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");
const THREAD_ID = process.env.CODEX_THREAD_ID || "manual-ce3-group-meeting";
const WORKSPACE = path.join(ROOT, "outputs", THREAD_ID, "presentations", "ce3-group-meeting");
const SLIDES_DIR = path.join(WORKSPACE, "slides");
const PREVIEW_DIR = path.join(WORKSPACE, "preview");
const LAYOUT_DIR = path.join(WORKSPACE, "layout");
const QA_DIR = path.join(WORKSPACE, "qa");
const FINAL_PPTX = path.join(ROOT, "manuscript", "ce3_group_meeting_reproduction_deck.pptx");

const SKILL_DIR =
  process.env.PRESENTATIONS_SKILL_DIR ||
  "C:\\Users\\admin\\.codex\\plugins\\cache\\openai-primary-runtime\\presentations\\26.521.10419\\skills\\presentations";
const PYTHON =
  process.env.CODEX_BUNDLED_PYTHON ||
  "C:\\Users\\admin\\.cache\\codex-runtimes\\codex-primary-runtime\\dependencies\\python\\python.exe";

const helper = path.join(SKILL_DIR, "scripts", "build_artifact_deck.mjs");

function normalizeNewlines(text) {
  return text.trimStart().replace(/\r\n/g, "\n");
}

async function writeModule(name, content) {
  await fs.writeFile(path.join(SLIDES_DIR, name), normalizeNewlines(content), "utf8");
}

async function writeSlideModules() {
  await fs.mkdir(SLIDES_DIR, { recursive: true });
  await fs.mkdir(PREVIEW_DIR, { recursive: true });
  await fs.mkdir(LAYOUT_DIR, { recursive: true });
  await fs.mkdir(QA_DIR, { recursive: true });

  await writeModule(
    "shared.mjs",
    `
export const C = {
  bg: '#fbfaf6',
  ink: '#17212b',
  muted: '#52616b',
  line: '#d6dde1',
  blue: '#1f7a8c',
  blueSoft: '#e8f2f4',
  amber: '#d68c2f',
  amberSoft: '#fff2df',
  redSoft: '#f9e4df',
  green: '#3f7f5f',
};

export function bg(slide, ctx) {
  ctx.addShape(slide, { x: 0, y: 0, w: 1280, h: 720, fill: C.bg, line: ctx.line('#00000000', 0), name: 'background' });
}

export function kicker(slide, ctx, text, page) {
  ctx.addShape(slide, { x: 56, y: 48, w: 8, h: 24, fill: C.blue, line: ctx.line('#00000000', 0), name: 'kicker-marker-' + page });
  ctx.addText(slide, { text, x: 76, y: 43, w: 360, h: 34, size: 13, bold: true, color: C.blue, valign: 'middle', name: 'kicker-label-' + page, insets: { left: 0, right: 0, top: 2, bottom: 2 } });
  ctx.addText(slide, { text: String(page).padStart(2, '0'), x: 1168, y: 44, w: 54, h: 26, size: 13, bold: true, color: C.muted, align: 'right', valign: 'middle' });
}

export function title(slide, ctx, text, y = 88) {
  ctx.addText(slide, { text, x: 56, y, w: 1040, h: 86, size: 35, bold: true, color: C.ink, typeface: ctx.fonts.title, insets: { left: 0, right: 0, top: 2, bottom: 2 } });
}

export function subtitle(slide, ctx, text, y = 170) {
  ctx.addText(slide, { text, x: 58, y, w: 1020, h: 52, size: 18, color: C.muted, insets: { left: 0, right: 0, top: 2, bottom: 2 } });
}

export function footer(slide, ctx, page, source) {
  ctx.addShape(slide, { x: 56, y: 666, w: 1090, h: 1.2, fill: C.line, line: ctx.line('#00000000', 0) });
  ctx.addText(slide, { text: 'Source: ' + source, x: 56, y: 676, w: 1025, h: 24, size: 9.5, color: C.muted });
  ctx.addText(slide, { text: 'Ce3+ 5d1 reproduction group meeting', x: 1020, y: 676, w: 202, h: 24, size: 9.5, color: C.muted, align: 'right' });
}

export function pill(slide, ctx, text, x, y, w, fill = C.blueSoft, color = C.blue) {
  ctx.addShape(slide, { x, y, w, h: 30, fill, line: ctx.line('#00000000', 0) });
  ctx.addText(slide, { text, x: x + 12, y: y + 5, w: w - 24, h: 22, size: 12.5, bold: true, color, valign: 'middle' });
}

export function metricBox(slide, ctx, x, y, w, h, value, label, note, accent = C.blue) {
  ctx.addShape(slide, { x, y, w, h, fill: '#ffffff', line: ctx.line('#cdd7dc', 1.2) });
  ctx.addShape(slide, { x, y, w: 7, h, fill: accent, line: ctx.line('#00000000', 0) });
  ctx.addText(slide, { text: value, x: x + 22, y: y + 20, w: w - 36, h: 36, size: 27, bold: true, color: C.ink, valign: 'middle' });
  ctx.addText(slide, { text: label, x: x + 22, y: y + 64, w: w - 36, h: 26, size: 15.5, bold: true, color: C.ink, valign: 'middle' });
  ctx.addText(slide, { text: note, x: x + 22, y: y + 96, w: w - 36, h: h - 106, size: 12.8, color: C.muted });
}

export function noteBox(slide, ctx, x, y, w, h, heading, body, fill = C.amberSoft, accent = C.amber) {
  ctx.addShape(slide, { x, y, w, h, fill, line: ctx.line('#d8c5a3', 1.1) });
  ctx.addShape(slide, { x, y, w: 6, h, fill: accent, line: ctx.line('#00000000', 0) });
  ctx.addText(slide, { text: heading, x: x + 20, y: y + 14, w: w - 36, h: 24, size: 15.5, bold: true, color: C.ink, valign: 'middle' });
  ctx.addText(slide, { text: body, x: x + 20, y: y + 42, w: w - 36, h: h - 50, size: 13.5, color: C.muted });
}

export function sourceTag(slide, ctx, text, x, y, w, fill = '#f3f4f1') {
  ctx.addShape(slide, { x, y, w, h: 32, fill, line: ctx.line('#d6dde1', 0.8) });
  ctx.addText(slide, { text, x: x + 12, y: y + 6, w: w - 24, h: 22, size: 12, bold: true, color: C.muted, valign: 'middle' });
}

export function bullet(slide, ctx, text, x, y, w, color = C.blue) {
  ctx.addShape(slide, { x, y: y + 8, w: 7, h: 7, fill: color, line: ctx.line('#00000000', 0) });
  ctx.addText(slide, { text, x: x + 18, y, w, h: 42, size: 15.2, color: C.ink });
}
`,
  );

  await writeModule(
    "slide-01.mjs",
    `
import { bg, kicker, title, subtitle, footer, metricBox, noteBox, pill, C } from './shared.mjs';

export async function slide01(presentation, ctx) {
  const slide = presentation.slides.add();
  bg(slide, ctx);
  kicker(slide, ctx, 'THESIS', 1);
  title(slide, ctx, '本次完成的是 paper-aligned processed-data baseline reproduction');
  subtitle(slide, ctx, '可汇报的核心不是“完全复现”，而是把公开证据链、可重复 baseline、metric gap 和 provenance 限制讲清楚。');
  metricBox(slide, ctx, 72, 270, 330, 168, '357 x 46', 'original RFE44 workbook', 'paper-aligned public processed table; 330 composition groups', C.blue);
  metricBox(slide, ctx, 472, 270, 330, 168, '0.154993 eV', 'closest local rerun MAE', 'CPU unseeded/default; fold-mean MAE vs notebook saved 0.153388 eV', C.green);
  metricBox(slide, ctx, 872, 270, 330, 168, '0.161535 eV', 'deterministic baseline MAE', 'CPU seed=42; repeatable project baseline, not the closest notebook state', C.amber);
  noteBox(slide, ctx, 112, 500, 1030, 86, 'Reporting boundary', '可以说：完成 paper-aligned 357-row public processed-data baseline reproduction。不要说：完全复现或 provenance-faithful full reproduction。');
  pill(slide, ctx, 'Literature Fact + Model Inference + Experiment Hypothesis 分层汇报', 112, 606, 500);
  footer(slide, ctx, 1, 'reproductions/ce3_original_baseline/report.md; reproductions/ce3_original_metric_gap/report.md');
  return slide;
}
`,
  );

  await writeModule(
    "slide-02.mjs",
    `
import { bg, kicker, title, subtitle, footer, noteBox, sourceTag, C } from './shared.mjs';

export async function slide02(presentation, ctx) {
  const slide = presentation.slides.add();
  bg(slide, ctx);
  kicker(slide, ctx, 'SOURCE AUDIT', 2);
  title(slide, ctx, 'DOI/DataCite 把 paper-aligned 复现对象指向 original release');
  subtitle(slide, ctx, '先确定源头，再谈模型：DataCite related identifier 指向 NL0119/Ce_5d1_Prediction/tree/original。');
  const nodes = [
    ['arXiv:2502.18859', 'paper/source context'],
    ['MRS 2025', 'conference context'],
    ['Zenodo DOI', '10.5281/zenodo.14872504'],
    ['DataCite', 'IsSupplementTo tree/original'],
    ['GitHub original', '357-row workbook'],
    ['local audits', 'baseline + metric gap'],
  ];
  ctx.addShape(slide, { x: 105, y: 355, w: 1040, h: 4, fill: '#8aa0a9', line: ctx.line('#00000000', 0) });
  nodes.forEach((node, i) => {
    const x = 112 + i * 205;
    ctx.addShape(slide, { x, y: 330, w: 54, h: 54, fill: i < 4 ? C.blue : C.amber, line: ctx.line('#00000000', 0) });
    ctx.addText(slide, { text: String(i + 1), x, y: 342, w: 54, h: 28, size: 17, bold: true, color: '#ffffff', align: 'center', valign: 'middle' });
    ctx.addText(slide, { text: node[0], x: x - 58, y: 405, w: 170, h: 42, size: 15, bold: true, color: C.ink, align: 'center' });
    ctx.addText(slide, { text: node[1], x: x - 70, y: 462, w: 194, h: 40, size: 12.5, color: C.muted, align: 'center' });
  });
  sourceTag(slide, ctx, 'Literature Fact', 72, 240, 150, C.blueSoft);
  noteBox(slide, ctx, 250, 232, 875, 76, 'Caveat', 'Zenodo direct payload/checksum routes returned HTTP 403 locally; DOI/DataCite metadata still supports the GitHub original-release link.', C.amberSoft, C.amber);
  footer(slide, ctx, 2, 'notes/source-audit-ce3-excitation-band-baseline.md; notes/zenodo-github-version-audit.md');
  return slide;
}
`,
  );

  await writeModule(
    "slide-03.mjs",
    `
import { bg, kicker, title, subtitle, footer, noteBox, C } from './shared.mjs';

export async function slide03(presentation, ctx) {
  const slide = presentation.slides.add();
  bg(slide, ctx);
  kicker(slide, ctx, 'VERSION AUDIT', 3);
  title(slide, ctx, '357-row original 与 358-row main 是版本漂移，指标不能混用');
  subtitle(slide, ctx, '两张 workbook 不只是差一行：feature schema、row/target multiset 和 notebook code path 都不完全相同。');
  const cards = [
    ['NL0119@original', 'paper-aligned target', 'Training_Set_for_5d1.xlsx', 'RFE44', '357 rows', '46 columns', '330 unique compositions', C.blueSoft, C.blue],
    ['BrgochGroup@main', 'later public workbook', 'Training_Set_updated_for_5d1_RFE17.xlsx', 'single sheet', '358 rows', '19 columns', '330 unique compositions', C.amberSoft, C.amber],
  ];
  cards.forEach((card, i) => {
    const x = i === 0 ? 86 : 682;
    ctx.addShape(slide, { x, y: 244, w: 510, h: 300, fill: card[7], line: ctx.line('#cbd5dc', 1.2) });
    ctx.addText(slide, { text: card[0], x: x + 26, y: 270, w: 430, h: 34, size: 21, bold: true, color: C.ink });
    ctx.addText(slide, { text: card[1], x: x + 26, y: 312, w: 430, h: 24, size: 14, bold: true, color: card[8] });
    ctx.addText(slide, { text: card[2], x: x + 26, y: 354, w: 440, h: 28, size: 13.5, color: C.muted });
    ctx.addText(slide, { text: card[4] + ' / ' + card[5], x: x + 26, y: 408, w: 380, h: 38, size: 28, bold: true, color: C.ink });
    ctx.addText(slide, { text: card[3] + '; ' + card[6], x: x + 26, y: 466, w: 440, h: 32, size: 15, color: C.ink });
  });
  ctx.addShape(slide, { x: 598, y: 390, w: 80, h: 4, fill: C.ink, line: ctx.line('#00000000', 0) });
  ctx.addText(slide, { text: 'separate', x: 590, y: 350, w: 96, h: 24, size: 13.5, bold: true, color: C.ink, align: 'center' });
  noteBox(slide, ctx, 160, 568, 960, 74, 'Reporting rule', '357-row original 是 paper-aligned 复现对象；358-row main 可单独快速 rerun，但必须标注 later public workbook。');
  footer(slide, ctx, 3, 'notes/zenodo-github-version-audit.md; notes/modeling-code-audit-ce3-excitation-band-baseline.md');
  return slide;
}
`,
  );

  await writeModule(
    "slide-04.mjs",
    `
import { bg, kicker, title, subtitle, footer, noteBox, C } from './shared.mjs';

export async function slide04(presentation, ctx) {
  const slide = presentation.slides.add();
  bg(slide, ctx);
  kicker(slide, ctx, 'PIPELINE', 4);
  title(slide, ctx, '本地流程复现的是 released processed baseline，而不是 raw provenance reconstruction');
  subtitle(slide, ctx, '所有模型结论都限定在公开 processed workbook + frozen auxiliary features + composition-grouped LOGO 这个边界内。');
  const steps = [
    ['DataCite -> original', 'Zenodo DOI points to tree/original'],
    ['357-row RFE44', '5d1 target; 44 released features'],
    ['Frozen CS/RP', 'Predicted CS/RP used as released columns'],
    ['LOGO split', 'LeaveOneGroupOut by Composition'],
    ['Metric reporting', 'fold-mean and global metrics separated'],
  ];
  steps.forEach((step, i) => {
    const x = 64 + i * 242;
    ctx.addShape(slide, { x, y: 286, w: 194, h: 154, fill: '#ffffff', line: ctx.line('#b9c8ce', 1.2) });
    ctx.addShape(slide, { x, y: 286, w: 194, h: 8, fill: i < 3 ? C.blue : C.amber, line: ctx.line('#00000000', 0) });
    ctx.addText(slide, { text: step[0], x: x + 18, y: 318, w: 158, h: 44, size: 17, bold: true, color: C.ink });
    ctx.addText(slide, { text: step[1], x: x + 18, y: 376, w: 158, h: 48, size: 12.6, color: C.muted });
    if (i < steps.length - 1) {
      ctx.addShape(slide, { x: x + 198, y: 357, w: 40, h: 3, fill: C.ink, line: ctx.line('#00000000', 0) });
    }
  });
  noteBox(slide, ctx, 116, 502, 1035, 82, 'Validation boundary', 'LOGO by Composition 不是 source-aware split。公开 workbook 缺 DOI/year/source/in-house 字段，因此不能从本表单独完成 provenance-faithful full reproduction。');
  footer(slide, ctx, 4, 'reproductions/ce3_original_baseline/report.md; reproductions/ce3_original_baseline/dataset_profile.json');
  return slide;
}
`,
  );

  await writeModule(
    "slide-05.mjs",
    `
import { bg, kicker, title, subtitle, footer, metricBox, noteBox, C } from './shared.mjs';

export async function slide05(presentation, ctx) {
  const slide = presentation.slides.add();
  bg(slide, ctx);
  kicker(slide, ctx, 'BASELINE RERUN', 5);
  title(slide, ctx, 'Seed=42 CPU rerun 是可重复项目基线，且显著优于 naive baselines');
  subtitle(slide, ctx, '这里展示 deterministic baseline，不把它误写成最接近 notebook saved output 的配置。');
  metricBox(slide, ctx, 72, 252, 260, 150, '0.161535', 'XGBoost fold-mean MAE', 'eV; original params; CPU seed=42', C.blue);
  metricBox(slide, ctx, 365, 252, 260, 150, '0.160836', 'global MAE', 'eV over all held-out predictions', C.blue);
  metricBox(slide, ctx, 658, 252, 260, 150, '0.826486', 'global R2', 'unitless; eV target space', C.green);
  metricBox(slide, ctx, 951, 252, 260, 150, '~0.421', 'mean/median baseline MAE', 'fold-mean MAE eV under same split', C.amber);
  const bars = [
    ['XGBoost', 0.161535, C.blue],
    ['Train mean', 0.421168, C.amber],
    ['Train median', 0.420135, C.amber],
  ];
  bars.forEach((bar, i) => {
    const y = 475 + i * 42;
    ctx.addText(slide, { text: bar[0], x: 130, y, w: 120, h: 24, size: 14, bold: true, color: C.ink });
    ctx.addShape(slide, { x: 270, y: y + 4, w: bar[1] * 1500, h: 18, fill: bar[2], line: ctx.line('#00000000', 0) });
    ctx.addText(slide, { text: bar[1].toFixed(6) + ' eV', x: 930, y, w: 170, h: 24, size: 13, color: C.muted });
  });
  noteBox(slide, ctx, 112, 592, 1010, 62, 'Metric definition', 'All bars are fold-mean MAE in eV under LeaveOneGroupOut grouped by Composition.');
  footer(slide, ctx, 5, 'results/tables/ce3_original_baseline/summary.json; reproductions/ce3_original_baseline/report.md');
  return slide;
}
`,
  );

  await writeModule(
    "slide-06.mjs",
    `
import { bg, kicker, title, subtitle, footer, noteBox, C } from './shared.mjs';

export async function slide06(presentation, ctx) {
  const slide = presentation.slides.add();
  bg(slide, ctx);
  kicker(slide, ctx, 'METRIC GAP', 6);
  title(slide, ctx, 'Seed policy 解释了主要 metric gap，CPU unseeded/default 最接近 notebook saved');
  subtitle(slide, ctx, 'Notebook saved MAE = 0.153388 eV；closest local CPU unseeded/default MAE = 0.154993 eV。');
  const data = [
    ['notebook saved', 0.153388, C.blue],
    ['CPU unseeded', 0.154993, C.blue],
    ['seed 0', 0.154993, C.blue],
    ['seed 100', 0.156602, C.amber],
    ['seed 1', 0.158683, C.amber],
    ['seed42 n_jobs=1', 0.159381, C.amber],
    ['seed 22', 0.161379, C.amber],
    ['seed 42', 0.161535, C.amber],
  ];
  const x0 = 92, y0 = 520, h = 260, barW = 92, gap = 38, min = 0.152, max = 0.163;
  ctx.addShape(slide, { x: x0, y: y0 - h, w: 1080, h, fill: '#ffffff', line: ctx.line('#d1d5db', 1) });
  data.forEach((d, i) => {
    const x = x0 + 46 + i * (barW + gap);
    const barH = (d[1] - min) / (max - min) * h;
    ctx.addShape(slide, { x, y: y0 - barH, w: barW, h: barH, fill: d[2], line: ctx.line('#00000000', 0) });
    ctx.addText(slide, { text: d[1].toFixed(3), x: x - 4, y: y0 - barH - 28, w: barW + 8, h: 22, size: 12, bold: true, color: C.ink, align: 'center' });
    ctx.addText(slide, { text: d[0], x: x - 12, y: y0 + 18, w: barW + 24, h: 44, size: 10.5, color: C.muted, align: 'center' });
  });
  ctx.addText(slide, { text: 'fold-mean MAE (eV)', x: 88, y: 228, w: 160, h: 20, size: 12, color: C.muted });
  noteBox(slide, ctx, 140, 586, 1010, 72, 'Unresolved part', 'Residual +0.001605 eV MAE gap may reflect XGBoost version, CUDA/CPU behavior, or platform numerical differences; CUDA remains untested locally.');
  footer(slide, ctx, 6, 'results/tables/ce3_original_metric_gap/metric_gap_runs.csv; reproductions/ce3_original_metric_gap/report.md');
  return slide;
}
`,
  );

  await writeModule(
    "slide-07.mjs",
    `
import { bg, kicker, title, subtitle, footer, noteBox, bullet, C } from './shared.mjs';

export async function slide07(presentation, ctx) {
  const slide = presentation.slides.add();
  bg(slide, ctx);
  kicker(slide, ctx, 'LIMITATIONS', 7);
  title(slide, ctx, '公开 processed workbook 限制了 provenance-faithful full reproduction');
  subtitle(slide, ctx, '这些限制不是措辞问题，而是缺少必要 artifact 或 validation policy 未完全重建。');
  const cols = [
    ['Missing provenance fields', ['source_doi / source_year absent', 'measurement source metadata absent', 'in-house vs literature flag absent']],
    ['Validation caveats', ['LOGO is composition-aware only', 'Predicted CS/RP are frozen features', 'auxiliary models not nested-regenerated']],
    ['Environment gaps', ['Zenodo payload checksum blocked by 403', 'author CUDA/historical package stack not matched', 'CUDA comparison skipped locally']],
  ];
  cols.forEach((col, i) => {
    const x = 76 + i * 390;
    ctx.addShape(slide, { x, y: 246, w: 340, h: 285, fill: '#ffffff', line: ctx.line('#cdd7dc', 1.2) });
    ctx.addShape(slide, { x, y: 246, w: 340, h: 8, fill: i === 0 ? C.amber : C.blue, line: ctx.line('#00000000', 0) });
    ctx.addText(slide, { text: col[0], x: x + 20, y: 278, w: 300, h: 34, size: 18, bold: true, color: C.ink });
    col[1].forEach((item, j) => bullet(slide, ctx, item, x + 28, 338 + j * 58, 270, i === 0 ? C.amber : C.blue));
  });
  noteBox(slide, ctx, 164, 572, 950, 72, 'Conclusion boundary', 'Therefore: report completed processed-data baseline reproduction, not complete or provenance-faithful full reproduction.');
  footer(slide, ctx, 7, 'reproductions/ce3_original_baseline/report.md; reproductions/ce3_original_metric_gap/report.md');
  return slide;
}
`,
  );

  await writeModule(
    "slide-08.mjs",
    `
import { bg, kicker, title, subtitle, footer, metricBox, noteBox, C } from './shared.mjs';

export async function slide08(presentation, ctx) {
  const slide = presentation.slides.add();
  bg(slide, ctx);
  kicker(slide, ctx, 'TAKEAWAYS', 8);
  title(slide, ctx, '现在可防守的结论是 version-aware、seed-aware、provenance-aware 的有限复现');
  subtitle(slide, ctx, '组会重点应放在证据边界和下一步能提高 claim strength 的 artifact。');
  metricBox(slide, ctx, 80, 240, 335, 150, '1', 'Use original 357-row release', 'paper-aligned; metrics from later main must stay separate', C.blue);
  metricBox(slide, ctx, 472, 240, 335, 150, '2', 'Report two rerun roles', 'CPU unseeded/default for closest notebook comparison; seed=42 for deterministic baseline', C.green);
  metricBox(slide, ctx, 864, 240, 335, 150, '3', 'Name missing evidence', 'row-level provenance, nested CS/RP regeneration, CUDA/historical environment', C.amber);
  noteBox(slide, ctx, 142, 455, 996, 126, 'First next actions after group meeting', 'Recover or reconstruct row-level DOI/year/source flags; implement nested auxiliary CS/RP regeneration if strict validation is required; optionally run 358-row main only as a clearly labeled later-public-workbook track.');
  ctx.addText(slide, { text: 'Do not mix versions. Do not overclaim. Do not turn model outputs into experimental facts.', x: 170, y: 620, w: 940, h: 32, size: 20, bold: true, color: C.ink, align: 'center' });
  footer(slide, ctx, 8, 'manuscript/ce3_group_meeting_outline.md; manuscript/ce3_group_meeting_script.md');
  return slide;
}
`,
  );
}

async function main() {
  await writeSlideModules();
  await fs.mkdir(path.dirname(FINAL_PPTX), { recursive: true });

  const args = [
    helper,
    "--workspace",
    WORKSPACE,
    "--slides-dir",
    SLIDES_DIR,
    "--out",
    FINAL_PPTX,
    "--preview-dir",
    PREVIEW_DIR,
    "--layout-dir",
    LAYOUT_DIR,
    "--contact-sheet",
    path.join(PREVIEW_DIR, "contact-sheet.png"),
    "--manifest",
    path.join(QA_DIR, "artifact-build-manifest.json"),
    "--slide-count",
    "8",
    "--slide-size",
    "1280x720",
    "--scale",
    "1",
  ];
  const env = {
    ...process.env,
    HOME: process.env.HOME || "C:\\Users\\admin",
    PYTHON,
    PYTHONIOENCODING: "utf-8",
    PYTHONUTF8: "1",
  };
  const result = spawnSync(process.execPath, args, {
    cwd: ROOT,
    env,
    encoding: "utf8",
  });
  if (result.status !== 0) {
    const finalExists = await fs
      .stat(FINAL_PPTX)
      .then((stat) => stat.size > 0)
      .catch(() => false);
    const contactSheetExists = await fs
      .stat(path.join(PREVIEW_DIR, "contact-sheet.png"))
      .then((stat) => stat.size > 0)
      .catch(() => false);
    const previewEntries = await fs
      .readdir(PREVIEW_DIR)
      .then((entries) => entries.filter((entry) => /^slide-\d+\.png$/i.test(entry)).length)
      .catch(() => 0);
    if (!finalExists || !contactSheetExists || previewEntries !== 8) {
      throw new Error(["Deck build failed.", result.stdout, result.stderr].filter(Boolean).join("\n"));
    }
    console.warn(
      [
        "Deck helper returned a non-zero status after writing required outputs.",
        `status=${result.status}; signal=${result.signal || "none"}`,
        "Continuing because final PPTX, 8 previews, and contact sheet are present.",
      ].join("\n"),
    );
  }
  const stat = await fs.stat(FINAL_PPTX);
  console.log(
    JSON.stringify(
      {
        ok: true,
        pptx: path.relative(ROOT, FINAL_PPTX).replaceAll(path.sep, "/"),
        bytes: stat.size,
        workspace: path.relative(ROOT, WORKSPACE).replaceAll(path.sep, "/"),
        previewDir: path.relative(ROOT, PREVIEW_DIR).replaceAll(path.sep, "/"),
      },
      null,
      2,
    ),
  );
}

main().catch((error) => {
  console.error(error.stack || error.message || String(error));
  process.exit(1);
});
