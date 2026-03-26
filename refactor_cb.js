const fs = require('fs');
const file = 'choiyeongbeen/app.js';
let code = fs.readFileSync(file, 'utf8');

// 1. Add helpers
const helpers = `
function cloneVNode(vNode) {
  return vNode == null ? vNode : JSON.parse(JSON.stringify(vNode));
}

function sourceToVNode(source) {
  const container = document.createElement("div");
  container.innerHTML = source;
  container.querySelectorAll("script").forEach((node) => node.remove());
  return domToVNode(container); // Use window.VDOM's implementation
}
`;

code = code.replace(/function diffRoot\(/g, 'function DELETED_diffRoot('); 

// Place helpers at the end since there are no bottom functions now
code += '\n' + helpers + '\n';

// 2. Rename diffRoot -> diff
code = code.replace(/\bdiffRoot\(/g, 'diff(');

// 3. Rename getMaxDepth -> calculateMaxDepth
code = code.replace(/\bgetMaxDepth\(/g, 'calculateMaxDepth(');

// 4. Update patchRoot calls
// applyPatchFromEditor()
code = code.replace(
  /patchRoot\(elements\.realDomRoot, oldVNode, nextVNode\)/g, 
  'applyPatches(elements.realDomRoot, patches, nextVNode)'
);

// moveHistory()
code = code.replace(
  /patchRoot\(elements\.realDomRoot, state\.realVNode, target\.vnode\)/g, 
  'applyPatches(elements.realDomRoot, patches, target.vnode)'
);

fs.writeFileSync(file, code);
console.log('choiyeongbeen/app.js migrated to use unified vdom.js API!');
