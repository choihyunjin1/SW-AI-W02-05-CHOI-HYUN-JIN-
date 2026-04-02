const fs = require('fs');

function processFile(file, isCb) {
  let code = fs.readFileSync(file, 'utf8');
  
  // Remove constants
  code = code.replace(/const NODE_TYPE = [\s\S]*?};\n/, '');
  code = code.replace(/const PATCH_TYPES = [\s\S]*?};\n/, '');

  if (isCb) {
    // choiyeongbeen specific (remove from ROOT_TYPE up to describeVNode)
    const pStart = code.indexOf('const ROOT_TYPE');
    const pEnd = code.indexOf('function describeVNode');
    if (pStart !== -1 && pEnd !== -1) {
      code = code.substring(0, pStart) + code.substring(pEnd);
    }
    // Rename patchRoot to applyPatches etc
    const helpers = `
function cloneVNode(vNode) {
  return vNode == null ? vNode : JSON.parse(JSON.stringify(vNode));
}
function sourceToVNode(source) {
  const container = document.createElement("div");
  container.innerHTML = source;
  container.querySelectorAll("script").forEach((node) => node.remove());
  return domToVNode(container); 
}
`;
    // Add helpers at the bottom
    code += helpers;
    
    code = code.replace(/\bdiffRoot\(/g, 'diff(');
    code = code.replace(/\bgetMaxDepth\(/g, 'calculateMaxDepth(');
    code = code.replace(/patchRoot\(elements\.realDomRoot, oldVNode, nextVNode\)/g, 'applyPatches(elements.realDomRoot, patches, nextVNode)');
    code = code.replace(/patchRoot\(elements\.realDomRoot, state\.realVNode, target\.vnode\)/g, 'applyPatches(elements.realDomRoot, patches, target.vnode)');

  } else {
    // benchmark/jungchanbin
    // From: function createRootContainer() down to end of applyPatches()
    const blockStart = code.indexOf('function createRootContainer()');
    const blockEndMatchStr = '/* 8. history manager';
    const blockEnd = code.indexOf(blockEndMatchStr);
    
    if (blockStart !== -1 && blockEnd !== -1) {
      code = code.substring(0, blockStart) + code.substring(blockEnd);
    }

    // Since benchmark tracked patches in applyPatches, let's inject tracking into benchmark's runBenchmarkTick
    if (file.includes('benchmark')) {
      code = code.replace(
        'applyPatches(state.ui.benchmarkVdomRoot, patches, nextVNode);',
        'applyPatches(state.ui.benchmarkVdomRoot, patches, nextVNode);\n  if (state.benchmark.running || state.benchmark.burstRemaining > 0) { state.benchmark.mutationTotals.vdom += patches.length; }'
      );
      code = code.replace(
        'applyPatches(state.ui.benchmarkVdomRoot, patches, nextVNode); // update with toggle',
        'applyPatches(state.ui.benchmarkVdomRoot, patches, nextVNode);\n  if (state.benchmark.running || state.benchmark.burstRemaining > 0) { state.benchmark.mutationTotals.vdom += patches.length; }'
      );
    }
  }

  fs.writeFileSync(file, code);
  console.log(`Cleaned ${file}`);
}

processFile('benchmark/app.js', false);
processFile('jungchanbin/app.js', false);
processFile('choiyeongbeen/app.js', true);
