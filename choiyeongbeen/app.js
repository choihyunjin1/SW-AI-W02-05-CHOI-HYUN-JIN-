const PRESETS = {
  base: `<section class="lab-screen" data-mode="preview">
  <header class="lab-screen__header">
    <div>
      <p class="kicker">Live Drop</p>
      <h3>AURA Runner 01</h3>
    </div>
    <span class="state-chip">PREVIEW</span>
  </header>

  <p class="lab-screen__body">
    멤버 전용 프리뷰가 열려 있습니다. 아직 실제 결제는 잠겨 있고,
    사용자는 재고 상태와 번들 구성만 확인할 수 있습니다.
  </p>

  <div class="feature-grid">
    <article class="section-card">
      <span>입장 상태</span>
      <h4>멤버 대기 중</h4>
      <p>일반 사용자에게는 아직 공개되지 않았습니다.</p>
    </article>
    <article class="section-card">
      <span>배송</span>
      <h4>당일 발송</h4>
      <p>오후 6시 이전 결제 건은 오늘 출고됩니다.</p>
    </article>
  </div>

  <ul class="kpi-list">
    <li data-key="stock">
      <span>재고 상태</span>
      <strong>82 pairs</strong>
    </li>
    <li data-key="queue">
      <span>대기열</span>
      <strong>Preview only</strong>
    </li>
    <li data-key="bundle">
      <span>추천 번들</span>
      <strong>Starter Pack</strong>
    </li>
  </ul>

  <div class="action-row">
    <button class="ghost-btn" type="button">알림 받기</button>
    <button class="solid-btn" type="button" disabled>멤버 입장</button>
  </div>
</section>`,
  textAttr: `<section class="lab-screen" data-mode="live">
  <header class="lab-screen__header">
    <div>
      <p class="kicker">Live Drop</p>
      <h3>AURA Runner 01</h3>
    </div>
    <span class="state-chip is-live">LIVE</span>
  </header>

  <p class="lab-screen__body">
    멤버 입장이 열렸습니다. 이제 실제 주문이 가능하며,
    우선 구매 대상은 멤버십 사용자입니다.
  </p>

  <div class="feature-grid">
    <article class="section-card">
      <span>입장 상태</span>
      <h4>입장 가능</h4>
      <p>멤버십 인증 후 바로 주문 단계로 이동할 수 있습니다.</p>
    </article>
    <article class="section-card">
      <span>배송</span>
      <h4>당일 발송</h4>
      <p>현재 결제량이 많아 일부 지역은 1일 지연될 수 있습니다.</p>
    </article>
  </div>

  <ul class="kpi-list">
    <li data-key="stock">
      <span>재고 상태</span>
      <strong>61 pairs</strong>
    </li>
    <li data-key="queue">
      <span>대기열</span>
      <strong>Members first</strong>
    </li>
    <li data-key="bundle">
      <span>추천 번들</span>
      <strong>Core Pair</strong>
    </li>
  </ul>

  <div class="action-row">
    <button class="ghost-btn" type="button">사이즈 가이드</button>
    <button class="solid-btn" type="button">지금 구매</button>
  </div>
</section>`,
  addNode: `<section class="lab-screen" data-mode="preview">
  <header class="lab-screen__header">
    <div>
      <p class="kicker">Live Drop</p>
      <h3>AURA Runner 01</h3>
    </div>
    <span class="state-chip">PREVIEW</span>
  </header>

  <p class="lab-screen__body">
    멤버 전용 프리뷰가 열려 있습니다. 아직 실제 결제는 잠겨 있고,
    사용자는 재고 상태와 번들 구성만 확인할 수 있습니다.
  </p>

  <div class="feature-grid">
    <article class="section-card">
      <span>입장 상태</span>
      <h4>멤버 대기 중</h4>
      <p>일반 사용자에게는 아직 공개되지 않았습니다.</p>
    </article>
    <article class="section-card">
      <span>배송</span>
      <h4>당일 발송</h4>
      <p>오후 6시 이전 결제 건은 오늘 출고됩니다.</p>
    </article>
  </div>

  <aside class="notice-card">
    <div>
      <strong>새 노드 추가</strong>
      <p>한정 수량 20족이 추가 공개되어 별도 공지 카드가 생겼습니다.</p>
    </div>
    <span class="state-chip is-live">NEW</span>
  </aside>

  <ul class="kpi-list">
    <li data-key="stock">
      <span>재고 상태</span>
      <strong>102 pairs</strong>
    </li>
    <li data-key="queue">
      <span>대기열</span>
      <strong>Preview only</strong>
    </li>
    <li data-key="bundle">
      <span>추천 번들</span>
      <strong>Starter Pack</strong>
    </li>
    <li data-key="gift">
      <span>추가 혜택</span>
      <strong>한정 양말 증정</strong>
    </li>
  </ul>

  <div class="action-row">
    <button class="ghost-btn" type="button">알림 받기</button>
    <button class="solid-btn" type="button" disabled>멤버 입장</button>
  </div>
</section>`,
  removeNode: `<section class="lab-screen" data-mode="preview">
  <header class="lab-screen__header">
    <div>
      <p class="kicker">Live Drop</p>
      <h3>AURA Runner 01</h3>
    </div>
    <span class="state-chip is-danger">SOLD OUT</span>
  </header>

  <p class="lab-screen__body">
    준비된 수량이 모두 소진되어 번들 정보와 입장 버튼이 제거되었습니다.
  </p>

  <div class="empty-state">
    현재 재고가 모두 소진되었습니다. 재입고 알림만 신청할 수 있습니다.
  </div>

  <div class="action-row">
    <button class="ghost-btn" type="button">재입고 알림 받기</button>
  </div>
</section>`,
  replaceTag: `<section class="lab-screen" data-mode="checkout">
  <header class="lab-screen__header">
    <div>
      <p class="kicker">Checkout</p>
      <h3>AURA Runner 01</h3>
    </div>
    <span class="state-chip is-live">ORDER</span>
  </header>

  <div class="lab-screen__body">
    주문 단계에서는 설명 문단 대신 요약 블록이 렌더링됩니다.
  </div>

  <div class="feature-grid">
    <article class="section-card">
      <span>결제 수단</span>
      <h4>카드 / 간편결제</h4>
      <p>즉시 결제 가능한 수단만 노출됩니다.</p>
    </article>
    <article class="section-card">
      <span>배송지</span>
      <h4>기본 주소지</h4>
      <p>최근 사용한 주소지가 자동으로 적용됩니다.</p>
    </article>
  </div>

  <ol class="kpi-list">
    <li>
      <span>상품 금액</span>
      <strong>189,000원</strong>
    </li>
    <li>
      <span>배송비</span>
      <strong>무료</strong>
    </li>
    <li>
      <span>총 결제 금액</span>
      <strong>189,000원</strong>
    </li>
  </ol>

  <div class="action-row">
    <button class="solid-btn" type="button">결제하기</button>
  </div>
</section>`,
  mixed: `<section class="lab-screen" data-mode="checkout">
  <header class="lab-screen__header">
    <div>
      <p class="kicker">Checkout</p>
      <h3>AURA Runner 01 Final Step</h3>
    </div>
    <span class="state-chip is-live">PAY NOW</span>
  </header>

  <div class="lab-screen__body">
    주문 단계에서는 설명 문단 대신 요약 블록이 렌더링됩니다.
  </div>

  <aside class="notice-card">
    <div>
      <strong>배송지 확인 필요</strong>
      <p>주문 완료 전 주소지와 사이즈를 마지막으로 점검하세요.</p>
    </div>
    <span class="state-chip">CHECK</span>
  </aside>

  <div class="feature-grid">
    <article class="section-card">
      <span>결제 수단</span>
      <h4>카드 / 간편결제</h4>
      <p>즉시 결제 가능한 수단만 노출됩니다.</p>
    </article>
    <article class="section-card">
      <span>배송지</span>
      <h4>기본 주소지</h4>
      <p>최근 사용한 주소지가 자동으로 적용됩니다.</p>
    </article>
  </div>

  <ol class="kpi-list">
    <li>
      <span>상품 금액</span>
      <strong>189,000원</strong>
    </li>
    <li>
      <span>쿠폰 할인</span>
      <strong>-10,000원</strong>
    </li>
    <li>
      <span>총 결제 금액</span>
      <strong>179,000원</strong>
    </li>
  </ol>

  <div class="action-row">
    <button class="ghost-btn" type="button">이전 단계</button>
    <button class="solid-btn" type="button">결제 완료</button>
  </div>
</section>`
};

const PATCH_TYPES = {
  CREATE: "CREATE",
  REMOVE: "REMOVE",
  REPLACE: "REPLACE",
  TEXT: "TEXT",
  PROPS: "PROPS"
};

function describeVNode(vnode) {
  if (!vnode) {
    return "empty";
  }

  if (vnode.type === TEXT_TYPE) {
    return "text";
  }

  return `<${vnode.tag}>`;
}

function countNodes(vnode) {
  if (!vnode) {
    return 0;
  }

  if (vnode.type === TEXT_TYPE) {
    return 1;
  }

  if (vnode.type === ROOT_TYPE) {
    return vnode.children.reduce((total, child) => total + countNodes(child), 0);
  }

  return 1 + vnode.children.reduce((total, child) => total + countNodes(child), 0);
}

function calculateMaxDepth(vnode, depth = 0) {
  if (!vnode) {
    return depth;
  }

  if (!vnode.children || vnode.children.length === 0) {
    return depth;
  }

  return Math.max(...vnode.children.map((child) => calculateMaxDepth(child, depth + 1)));
}

function summarizeMutation(mutation) {
  if (mutation.type === "childList") {
    return {
      summary: `childList @ ${describeTarget(mutation.target)}`,
      detail: `added ${mutation.addedNodes.length} / removed ${mutation.removedNodes.length}`
    };
  }

  if (mutation.type === "attributes") {
    return {
      summary: `attributes @ ${describeTarget(mutation.target)}`,
      detail: `${mutation.attributeName} changed`
    };
  }

  return {
    summary: `characterData @ ${describeTarget(mutation.target.parentNode)}`,
    detail: truncate(mutation.target.textContent || "")
  };
}

function describeTarget(node) {
  if (!node) {
    return "unknown";
  }

  if (node.nodeType === Node.TEXT_NODE) {
    return "#text";
  }

  const id = node.id ? `#${node.id}` : "";
  const className = typeof node.className === "string" && node.className.trim()
    ? `.${node.className.trim().split(/\s+/).join(".")}`
    : "";

  return `${node.nodeName.toLowerCase()}${id}${className}`;
}

function truncate(text) {
  return text.length > 40 ? `${text.slice(0, 40)}...` : text;
}

function cloneVNode(vnode) {
  return JSON.parse(JSON.stringify(vnode));
}

function cloneVNode(vNode) {
  return vNode == null ? vNode : JSON.parse(JSON.stringify(vNode));
}
function sourceToVNode(source) {
  const container = document.createElement("div");
  container.innerHTML = source;
  container.querySelectorAll("script").forEach((node) => node.remove());
  return domToVNode(container); 
}
