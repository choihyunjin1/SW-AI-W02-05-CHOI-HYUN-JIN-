const fs = require('fs');
const execSync = require('child_process').execSync;

let srcCode = execSync('git show HEAD:benchmark/app.js').toString('utf8');

const matchConstants = srcCode.match(/const NODE_TYPE = [\s\S]*?const PATCH_TYPES = [\s\S]*?\};\n/);
const constants = matchConstants ? matchConstants[0] : '';

const vdomStart = srcCode.indexOf('function createRootContainer()');
const vdomEndMatch = srcCode.indexOf('/* 8. history manager', vdomStart);

let vdomFunctions = srcCode.substring(vdomStart, vdomEndMatch).trim();

// Remove state.benchmark tracking code
vdomFunctions = vdomFunctions.replace(/if\s*\(\s*state\.benchmark\.running\s*\|\|[\s\S]*?\}\s*\n/g, '');

// Remove setManualStatus from vdom.js since it interacts with state.ui and belongs in benchmark/app.js
vdomFunctions = vdomFunctions.replace(/function setManualStatus\([\s\S]*?\n\}\n/, '');

const sanitizeHelper = `
function sanitizeText(text) {
  return typeof text === 'string' ? text.replace(/\\s+/g, ' ').trim() : '';
}
`;

const finalFileContent = `/*
  Unified Virtual DOM Engine Core
  Extracted for shared use across Patch Lab, Benchmark Engine, and Studio
*/

/* 1. Constants */
${constants}

/* 2. Virtual DOM Core & Patch Engine */
${sanitizeHelper}

${vdomFunctions}

// Export for global access in browsers
Object.assign(window, {
  NODE_TYPE,
  PATCH_TYPES,
  createRootContainer,
  createElementVNode,
  createTextVNode,
  domNodeToVNode,
  domToVNode,
  createDOMFromVNode,
  diff,
  applyPatches,
  isComparableDomNode,
  getComparableChildNodes,
  getDomKey,
  serializeHTML,
  safelyParseHTML,
  renderHTMLIntoTarget,
  countNodes,
  calculateMaxDepth,
  getNodeDescriptor,
  getReadableNodeSummary,
  findVNodeByPath,
  sanitizeText
});
`;

fs.writeFileSync('core/vdom.js', finalFileContent);
console.log('core/vdom.js successfully rebuilt from pristine git source!');
