const fs = require('fs');
const path = require('path');

const srcCode = fs.readFileSync('benchmark/app.js', 'utf8');

// Extract NODE_TYPE and PATCH_TYPES
const matchConstants = srcCode.match(/const NODE_TYPE = [\s\S]*?const PATCH_TYPES = [\s\S]*?\};\n/);
const constants = matchConstants ? matchConstants[0] : '';

// Extract the rest of the VDOM core functions
// From createRootContainer down to the end of applyPatches
const vdomStart = srcCode.indexOf('function createRootContainer()');
const vdomEndMatch = srcCode.indexOf('/* 8. history manager', vdomStart);

let vdomFunctions = srcCode.substring(vdomStart, vdomEndMatch).trim();

// Strip out state.benchmark references from applyPatches
vdomFunctions = vdomFunctions.replace(/if\s*\(\s*state\.benchmark\.running\s*\|\|[\s\S]*?\}\s*\n/g, '');

const finalFileContent = `/*
  Unified Virtual DOM Engine Core
  Extracted for shared use across Patch Lab, Benchmark Engine, and Studio
*/

/* 1. Constants */
${constants}

/* 2. Virtual DOM Core & Patch Engine */
${vdomFunctions}

// Export for global access in browsers
window.VDOM = {
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
  findVNodeByPath
};
`;

fs.mkdirSync('core', { recursive: true });
fs.writeFileSync('core/vdom.js', finalFileContent);
console.log("core/vdom.js written successfully.");
