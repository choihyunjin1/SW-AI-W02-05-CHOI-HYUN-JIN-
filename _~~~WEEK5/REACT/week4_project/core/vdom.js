/*
  Unified Virtual DOM Engine Core
  Extracted for shared use across Patch Lab, Benchmark Engine, and Studio
*/

/* 1. Constants */
const NODE_TYPE = {
  ELEMENT: 1,
  TEXT: 3,
  COMMENT: 8
};

const PATCH_TYPES = {
  CREATE: "CREATE",
  REMOVE: "REMOVE",
  REPLACE: "REPLACE",
  TEXT: "TEXT",
  ATTR_SET: "ATTR_SET",
  ATTR_REMOVE: "ATTR_REMOVE",
  REORDER_CHILDREN: "REORDER_CHILDREN"
};


/* 2. Virtual DOM Core & Patch Engine */

function sanitizeText(text) {
  return typeof text === 'string' ? text.replace(/\s+/g, ' ').trim() : '';
}


function createRootContainer() {
  return {
    type: "element",
    tag: "div",
    attrs: { "data-virtual-root": "true" },
    children: [],
    text: "",
    key: "__root__",
    path: "0",
    depth: 0
  };
}

function buildKey(attrs, fallbackKey) {
  if (!attrs) {
    return fallbackKey;
  }
  return attrs["data-key"] || attrs.key || attrs.id || fallbackKey;
}

function serializeHTML(node) {
  return node ? node.innerHTML.trim() : "";
}

function safelyParseHTML(html) {
  const template = document.createElement("template");
  try {
    template.innerHTML = html && html.trim() ? html.trim() : "";
  } catch (error) {
    return { fragment: template.content, error };
  }
  return { fragment: template.content, error: null };
}

function renderHTMLIntoTarget(target, html) {
  const { fragment, error } = safelyParseHTML(html);
  target.innerHTML = "";
  if (fragment.childNodes.length) {
    target.appendChild(fragment.cloneNode(true));
  }
  return error;
}

function isComparableDomNode(node) {
  if (!node) {
    return false;
  }
  if (node.nodeType === NODE_TYPE.COMMENT) {
    return false;
  }
  if (node.nodeType === NODE_TYPE.TEXT) {
    return Boolean((node.textContent || "").trim());
  }
  return node.nodeType === NODE_TYPE.ELEMENT;
}

function getComparableChildNodes(node) {
  return Array.from(node.childNodes || []).filter((child) => isComparableDomNode(child));
}

function pathToSegments(path) {
  return String(path)
    .split("-")
    .slice(1)
    .map((segment) => Number(segment))
    .filter((segment) => Number.isInteger(segment));
}

function getPathDepth(path) {
  return String(path).split("-").length;
}

function countNodes(vNode) {
  if (!vNode) {
    return 0;
  }
  return 1 + (vNode.children || []).reduce((total, child) => total + countNodes(child), 0);
}

function calculateMaxDepth(vNode) {
  if (!vNode) {
    return 0;
  }
  if (!vNode.children || !vNode.children.length) {
    return vNode.depth || 0;
  }
  return Math.max(...vNode.children.map((child) => calculateMaxDepth(child)));
}

function getNodeDescriptor(vNode) {
  if (!vNode) {
    return "null";
  }
  if (vNode.type === "text") {
    return `#text("${sanitizeText(vNode.text)}")`;
  }
  return `<${vNode.tag}>`;
}

function getReadableNodeSummary(vNode) {
  if (!vNode) {
    return "empty";
  }
  if (vNode.type === "text") {
    return `text:${sanitizeText(vNode.text) || "(blank)"}`;
  }
  return `${vNode.tag} | attrs:${Object.keys(vNode.attrs || {}).length} | children:${(vNode.children || []).length}`;
}

function getDomKey(node, index) {
  if (!node || node.nodeType !== NODE_TYPE.ELEMENT) {
    return `__index_${index}`;
  }
  return node.getAttribute("data-key") || node.getAttribute("key") || node.id || `__index_${index}`;
}


/* -------------------------------------------------------------------------- */
/* 4. virtual dom utils                                                        */
/* -------------------------------------------------------------------------- */

function createElementVNode(tag, attrs = {}, children = []) {
  return {
    type: "element",
    tag,
    attrs,
    children: children.map((child) => (typeof child === "string" ? createTextVNode(child) : child)),
    text: "",
    key: null,
    path: "",
    depth: 0
  };
}

function createTextVNode(text) {
  return {
    type: "text",
    tag: null,
    attrs: {},
    children: [],
    text,
    key: null,
    path: "",
    depth: 0
  };
}

/*
  이 함수의 역할:
  실제 DOM 노드를 Virtual DOM 객체 트리로 변환한다.
  입력:
  DOM Node, 현재 path 문자열, depth 숫자
  출력:
  Virtual DOM 객체 또는 null
  왜 필요한지:
  브라우저가 관리하는 실제 DOM을 diff 가능한 메모리 상 객체 트리로 바꿔야 React-style 비교를 직접 구현할 수 있다.
*/
function domNodeToVNode(node, path, depth) {
  if (!node) {
    return null;
  }
  if (node.nodeType === NODE_TYPE.COMMENT) {
    return null;
  }
  if (node.nodeType === NODE_TYPE.TEXT) {
    const rawText = node.textContent || "";
    if (!rawText.trim()) {
      return null;
    }
    return {
      type: "text",
      tag: null,
      attrs: {},
      children: [],
      text: rawText,
      key: null,
      path,
      depth
    };
  }
  if (node.nodeType !== NODE_TYPE.ELEMENT) {
    return null;
  }
  const attrs = {};
  Array.from(node.attributes || []).forEach((attribute) => {
    attrs[attribute.name] = attribute.value === "" ? true : attribute.value;
  });
  const children = [];
  let childIndex = 0;
  Array.from(node.childNodes || []).forEach((child) => {
    const childVNode = domNodeToVNode(child, `${path}-${childIndex}`, depth + 1);
    if (childVNode) {
      children.push(childVNode);
      childIndex += 1;
    }
  });
  return {
    type: "element",
    tag: node.tagName.toLowerCase(),
    attrs,
    children,
    text: "",
    key: buildKey(attrs, `${node.tagName.toLowerCase()}-${path}`),
    path,
    depth
  };
}

/*
  이 함수의 역할:
  DOM 컨테이너의 자식들을 읽어서 루트 래퍼 Virtual DOM으로 변환한다.
  입력:
  DOM Element 컨테이너
  출력:
  루트 Virtual DOM 객체
  왜 필요한지:
  비교 대상이 여러 루트 노드를 가질 수 있으므로 하나의 트리 루트로 감싸야 diff와 history를 단순하게 유지할 수 있다.
*/
function domToVNode(container) {
  const root = createRootContainer();
  let childIndex = 0;
  Array.from(container.childNodes || []).forEach((child) => {
    const childVNode = domNodeToVNode(child, `0-${childIndex}`, 1);
    if (childVNode) {
      root.children.push(childVNode);
      childIndex += 1;
    }
  });
  return root;
}

function normalizeVNodePaths(vNode, path = "0", depth = 0) {
  if (!vNode) {
    return null;
  }
  vNode.path = path;
  vNode.depth = depth;
  if (vNode.type === "element") {
    vNode.key = buildKey(vNode.attrs, `${vNode.tag}-${path}`);
  }
  (vNode.children || []).forEach((child, index) => {
    normalizeVNodePaths(child, `${path}-${index}`, depth + 1);
  });
  return vNode;
}

/*
  이 함수의 역할:
  Virtual DOM 객체 하나를 실제 DOM 노드로 생성한다.
  입력:
  Virtual DOM 객체
  출력:
  DOM Node
  왜 필요한지:
  CREATE, REPLACE, REORDER 단계에서 메모리상의 Virtual DOM을 다시 실제 DOM 노드로 만들어야 patch를 적용할 수 있다.
*/
function createDOMFromVNode(vNode) {
  if (!vNode) {
    return document.createTextNode("");
  }
  if (vNode.type === "text") {
    return document.createTextNode(vNode.text || "");
  }
  const element = document.createElement(vNode.tag);
  Object.entries(vNode.attrs || {}).forEach(([name, value]) => {
    if (value === true) {
      element.setAttribute(name, "");
    } else if (value !== false && value != null) {
      element.setAttribute(name, String(value));
    }
  });
  (vNode.children || []).forEach((child) => element.appendChild(createDOMFromVNode(child)));
  return element;
}

function renderVNodeToRoot(root, vNode) {
  root.innerHTML = "";
  (vNode.children || []).forEach((child) => root.appendChild(createDOMFromVNode(child)));
}

function findVNodeByPath(vNode, path) {
  if (!vNode) {
    return null;
  }
  if (vNode.path === path) {
    return vNode;
  }
  for (const child of vNode.children || []) {
    const found = findVNodeByPath(child, path);
    if (found) {
      return found;
    }
  }
  return null;
}

/* -------------------------------------------------------------------------- */
/* 5. traversal utils                                                          */
/* -------------------------------------------------------------------------- */

/*
  이 함수의 역할:
  Virtual DOM 트리를 깊이 우선 탐색으로 순회한다.
  입력:
  루트 Virtual DOM
  출력:
  방문 순서 배열
  왜 필요한지:
  Virtual DOM이 일반 트리라는 점과 depth 기반 방문 순서를 UI로 설명하기 위해 필요하다.
*/
function traverseDFS(root) {
  const order = [];
  function visit(node) {
    if (!node) {
      return;
    }
    order.push({ path: node.path, label: getNodeDescriptor(node), depth: node.depth });
    (node.children || []).forEach((child) => visit(child));
  }
  visit(root);
  return order;
}

/*
  이 함수의 역할:
  Virtual DOM 트리를 너비 우선 탐색으로 순회한다.
  입력:
  루트 Virtual DOM
  출력:
  방문 순서 배열
  왜 필요한지:
  레벨 순회를 통해 같은 depth에 있는 노드가 어떻게 배치되는지 보여주기 위해 필요하다.
*/
function traverseBFS(root) {
  if (!root) {
    return [];
  }
  const order = [];
  const queue = [root];
  while (queue.length) {
    const current = queue.shift();
    order.push({ path: current.path, label: getNodeDescriptor(current), depth: current.depth });
    (current.children || []).forEach((child) => queue.push(child));
  }
  return order;
}

/* -------------------------------------------------------------------------- */
/* 6. diff engine                                                              */
/* -------------------------------------------------------------------------- */

function diffAttrs(oldAttrs = {}, newAttrs = {}, path, patches) {
  Object.keys(newAttrs).forEach((name) => {
    if (oldAttrs[name] !== newAttrs[name]) {
      patches.push({ type: PATCH_TYPES.ATTR_SET, path, name, value: newAttrs[name] });
    }
  });
  Object.keys(oldAttrs).forEach((name) => {
    if (!(name in newAttrs)) {
      patches.push({ type: PATCH_TYPES.ATTR_REMOVE, path, name });
    }
  });
}

function createChildKeyMap(children) {
  const map = new Map();
  children.forEach((child, index) => {
    map.set(child.key || `__index_${index}`, index);
  });
  return map;
}

/*
  이 함수의 역할:
  두 자식 배열을 비교해 생성, 삭제, 재정렬, 하위 diff를 계산한다.
  입력:
  이전 자식 배열, 새 자식 배열, 부모 path, patch 배열
  출력:
  patch 배열에 자식 관련 patch를 추가
  왜 필요한지:
  React-style reconciliation의 핵심은 형제 리스트 비교이므로 별도 단계로 분리해야 patch를 명확하게 설명할 수 있다.
*/
function diffChildren(oldChildren, newChildren, parentPath, patches) {
  const oldKeyMap = createChildKeyMap(oldChildren);
  const newKeyMap = createChildKeyMap(newChildren);
  const nextOrder = [];

  newChildren.forEach((newChild, index) => {
    const lookupKey = newChild.key || `__index_${index}`;
    nextOrder.push(lookupKey);

    if (!oldKeyMap.has(lookupKey)) {
      patches.push({
        type: PATCH_TYPES.CREATE,
        path: `${parentPath}-${index}`,
        parentPath,
        index,
        node: newChild
      });
      return;
    }

    const oldIndex = oldKeyMap.get(lookupKey);
    diff(oldChildren[oldIndex], newChild, `${parentPath}-${index}`, patches);
  });

  oldChildren.forEach((oldChild, index) => {
    const lookupKey = oldChild.key || `__index_${index}`;
    if (!newKeyMap.has(lookupKey)) {
      patches.push({
        type: PATCH_TYPES.REMOVE,
        path: oldChild.path || `${parentPath}-${index}`,
        parentPath,
        index,
        node: oldChild
      });
    }
  });

  const previousOrder = oldChildren.map((child, index) => child.key || `__index_${index}`);
  if (previousOrder.length === nextOrder.length && previousOrder.join("|") !== nextOrder.join("|")) {
    patches.push({
      type: PATCH_TYPES.REORDER_CHILDREN,
      path: parentPath,
      parentPath,
      order: nextOrder
    });
  }
}

/*
  이 함수의 역할:
  이전 Virtual DOM과 새로운 Virtual DOM을 비교해 patch 목록을 만든다.
  입력:
  이전 Virtual DOM, 새 Virtual DOM, 현재 path, patch 배열
  출력:
  patch 배열
  왜 필요한지:
  실제 DOM에 들어가기 전에 메모리 상에서 변경점을 계산해야 최소 변경 방식이 가능하다.
*/
function diff(oldNode, newNode, path = "0", patches = []) {
  if (!oldNode && newNode) {
    patches.push({
      type: PATCH_TYPES.CREATE,
      path,
      parentPath: path.split("-").slice(0, -1).join("-") || "0",
      index: Number(path.split("-").pop() || 0),
      node: newNode
    });
    return patches;
  }

  if (oldNode && !newNode) {
    patches.push({
      type: PATCH_TYPES.REMOVE,
      path,
      parentPath: path.split("-").slice(0, -1).join("-") || "0",
      index: Number(path.split("-").pop() || 0),
      node: oldNode
    });
    return patches;
  }

  if (!oldNode || !newNode) {
    return patches;
  }

  if (oldNode.type !== newNode.type || oldNode.tag !== newNode.tag) {
    patches.push({ type: PATCH_TYPES.REPLACE, path, oldNode, newNode });
    return patches;
  }

  if (oldNode.type === "text" && newNode.type === "text") {
    if (oldNode.text !== newNode.text) {
      patches.push({ type: PATCH_TYPES.TEXT, path, oldText: oldNode.text, newText: newNode.text });
    }
    return patches;
  }

  diffAttrs(oldNode.attrs, newNode.attrs, path, patches);
  diffChildren(oldNode.children || [], newNode.children || [], path, patches);
  return patches;
}

/* -------------------------------------------------------------------------- */
/* 7. patch engine                                                             */
/* -------------------------------------------------------------------------- */

function getDomNodeByPath(root, path) {
  if (path === "0") {
    return root;
  }
  let current = root;
  const segments = pathToSegments(path);
  for (const segment of segments) {
    const comparableChildren = getComparableChildNodes(current);
    if (!current || !comparableChildren[segment]) {
      return null;
    }
    current = comparableChildren[segment];
  }
  return current;
}

function applyCreatePatch(root, patch) {
  const parent = getDomNodeByPath(root, patch.parentPath);
  if (!parent) {
    return;
  }
  const comparableChildren = getComparableChildNodes(parent);
  const referenceNode = comparableChildren[patch.index] || null;
  parent.insertBefore(createDOMFromVNode(patch.node), referenceNode);
}

function applyRemovePatch(root, patch) {
  const target = getDomNodeByPath(root, patch.path);
  if (target && target.parentNode) {
    target.parentNode.removeChild(target);
  }
}

function applyReplacePatch(root, patch) {
  const target = getDomNodeByPath(root, patch.path);
  if (target && target.parentNode) {
    target.parentNode.replaceChild(createDOMFromVNode(patch.newNode), target);
  }
}

function applyTextPatch(root, patch) {
  const target = getDomNodeByPath(root, patch.path);
  if (target) {
    target.textContent = patch.newText;
  }
}

function applyAttrSetPatch(root, patch) {
  const target = getDomNodeByPath(root, patch.path);
  if (!target || target.nodeType !== NODE_TYPE.ELEMENT) {
    return;
  }
  if (patch.value === true) {
    target.setAttribute(patch.name, "");
  } else {
    target.setAttribute(patch.name, String(patch.value));
  }
}

function applyAttrRemovePatch(root, patch) {
  const target = getDomNodeByPath(root, patch.path);
  if (target && target.nodeType === NODE_TYPE.ELEMENT) {
    target.removeAttribute(patch.name);
  }
}

function applyReorderPatch(root, patch, newVNodeRoot) {
  const parent = getDomNodeByPath(root, patch.path);
  const parentVNode = findVNodeByPath(newVNodeRoot, patch.path);
  if (!parent || !parentVNode) {
    return;
  }

  const existingChildren = getComparableChildNodes(parent);
  const existingByKey = new Map();
  existingChildren.forEach((child, index) => {
    existingByKey.set(getDomKey(child, index), child);
  });

  const fragment = document.createDocumentFragment();
  (parentVNode.children || []).forEach((childVNode, index) => {
    const lookupKey = childVNode.key || `__index_${index}`;
    const existingNode = existingByKey.get(lookupKey);
    fragment.appendChild(existingNode || createDOMFromVNode(childVNode));
  });

  parent.replaceChildren(fragment);
}

/*
  이 함수의 역할:
  patch 배열을 실제 DOM에 순서 있게 적용한다.
  입력:
  실제 DOM 루트, patch 배열, 새 Virtual DOM 루트
  출력:
  없음. 실제 DOM이 직접 갱신된다.
  왜 필요한지:
  diff 결과를 실제 화면 변화로 연결하는 단계이며, Virtual DOM의 핵심 가치는 바로 여기서 드러난다.
*/
function applyPatches(root, patches, newVNodeRoot) {
  const removePatches = patches
    .filter((patch) => patch.type === PATCH_TYPES.REMOVE)
    .sort((a, b) => getPathDepth(b.path) - getPathDepth(a.path));
  const createPatches = patches
    .filter((patch) => patch.type === PATCH_TYPES.CREATE)
    .sort((a, b) => getPathDepth(a.path) - getPathDepth(b.path));
  const updatePatches = patches.filter(
    (patch) => ![PATCH_TYPES.CREATE, PATCH_TYPES.REMOVE, PATCH_TYPES.REORDER_CHILDREN].includes(patch.type)
  );
  const reorderPatches = patches.filter((patch) => patch.type === PATCH_TYPES.REORDER_CHILDREN);

  removePatches.forEach((patch) => applyRemovePatch(root, patch));
  updatePatches.forEach((patch) => {
    switch (patch.type) {
      case PATCH_TYPES.REPLACE:
        applyReplacePatch(root, patch);
        break;
      case PATCH_TYPES.TEXT:
        applyTextPatch(root, patch);
        break;
      case PATCH_TYPES.ATTR_SET:
        applyAttrSetPatch(root, patch);
        break;
      case PATCH_TYPES.ATTR_REMOVE:
        applyAttrRemovePatch(root, patch);
        break;
      default:
        break;
    }
  });
  createPatches.forEach((patch) => applyCreatePatch(root, patch));
  reorderPatches.forEach((patch) => applyReorderPatch(root, patch, newVNodeRoot));

  }

/* -------------------------------------------------------------------------- */

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
