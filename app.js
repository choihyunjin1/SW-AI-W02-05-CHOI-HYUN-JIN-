/*
  Virtual DOM + Diff Algorithm Verification App
  Vanilla JavaScript implementation focused on explainability.
*/

/* -------------------------------------------------------------------------- */
/* 1. constants                                                                */
/* -------------------------------------------------------------------------- */

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

const UI_TEXT = {
  idle: "드롭 커머스 데모를 바로 실행할 수 있는 상태입니다. 멤버 입장, 번들 예약, 주문 전환 같은 사용자 흐름을 눌러보세요.",
  patchReady: "테스트 영역의 최신 DOM을 기준으로 diff를 계산할 준비가 되었습니다.",
  noChange: "이전 Virtual DOM과 동일하여 patch가 생성되지 않았습니다.",
  invalidHtml: "잘못된 HTML 입력이 감지되었습니다. 브라우저 파서 결과를 기준으로 렌더링합니다.",
  emptyTest: "테스트 영역이 비어 있어 빈 컨테이너 상태로 처리했습니다.",
  playbackIdle: "patch가 생성되면 적용 순서를 단계별로 재생할 수 있습니다.",
  playbackReady: "타임라인을 클릭하면 해당 patch를 집중적으로 설명합니다.",
  playbackDone: "마지막 patch까지 재생했습니다.",
  tourIdle: "서비스 이벤트 시나리오를 고르거나 데모 투어를 시작하세요.",
  tourDone: "서비스 데모 투어를 모두 재생했습니다. 원하는 이벤트 시나리오를 다시 실행해도 됩니다."
};

const SELECTORS = {
  serviceStateEyebrow: "#serviceStateEyebrow",
  serviceStateTitle: "#serviceStateTitle",
  serviceStateBody: "#serviceStateBody",
  serviceModeValue: "#serviceModeValue",
  serviceReasonTitle: "#serviceReasonTitle",
  serviceReasonPatch: "#serviceReasonPatch",
  serviceReasonBody: "#serviceReasonBody",
  serviceImpactAreas: "#serviceImpactAreas",
  serviceImpactSummary: "#serviceImpactSummary",
  serviceReasonBenefit: "#serviceReasonBenefit",
  serviceReasonCompare: "#serviceReasonCompare",
  serviceHomeButton: "#serviceHomeButton",
  openWorkbenchButton: "#openWorkbenchButton",
  closeWorkbenchButton: "#closeWorkbenchButton",
  workbenchShell: "#workbenchShell",
  workbenchBackdrop: "#workbenchBackdrop",
  realDomRoot: "#realDomRoot",
  realDomOverlay: "#realDomOverlay",
  testDomRoot: "#testDomRoot",
  testDomOverlay: "#testDomOverlay",
  sourceEditor: "#sourceEditor",
  patchButton: "#patchButton",
  backButton: "#backButton",
  forwardButton: "#forwardButton",
  resetButton: "#resetButton",
  syncSourceButton: "#syncSourceButton",
  currentStateLabel: "#currentStateLabel",
  currentStateDescription: "#currentStateDescription",
  diffLogPanel: "#diffLogPanel",
  historyPanel: "#historyPanel",
  treePanel: "#treePanel",
  dfsPanel: "#dfsPanel",
  bfsPanel: "#bfsPanel",
  explanationPanel: "#explanationPanel",
  patchSummary: "#patchSummary",
  historyMeta: "#historyMeta",
  patchCountMeta: "#patchCountMeta",
  treeMeta: "#treeMeta",
  depthMeta: "#depthMeta",
  observerMeta: "#observerMeta",
  editorMessage: "#editorMessage",
  treeNodeTemplate: "#treeNodeTemplate",
  scenarioPanel: "#scenarioPanel",
  patchTimelinePanel: "#patchTimelinePanel",
  playbackToggleButton: "#playbackToggleButton",
  playbackNextButton: "#playbackNextButton",
  playbackResetButton: "#playbackResetButton",
  playbackStatus: "#playbackStatus",
  performancePanel: "#performancePanel",
  inspectorPanel: "#inspectorPanel",
  demoBriefingPanel: "#demoBriefingPanel",
  demoSignalPanel: "#demoSignalPanel",
  pipelinePanel: "#pipelinePanel",
  demoTourStatus: "#demoTourStatus",
  demoTourButton: "#demoTourButton",
  demoFocusButton: "#demoFocusButton"
};

/* -------------------------------------------------------------------------- */
/* 2. state                                                                    */
/* -------------------------------------------------------------------------- */

const state = {
  realVNode: null,
  testVNode: null,
  patches: [],
  history: [],
  currentHistoryIndex: -1,
  mutationCount: 0,
  observer: null,
  selectedPath: "0",
  selectedPatchIndex: null,
  playbackIndex: null,
  playbackPlaying: false,
  playbackTimer: null,
  demoTourPlaying: false,
  demoTourTimer: null,
  demoTourIndex: null,
  demoTourCompleted: false,
  comparisonStats: null,
  activeScenarioId: null,
  ui: {}
};

/* -------------------------------------------------------------------------- */
/* 3. sample template                                                          */
/* -------------------------------------------------------------------------- */

const SAMPLE_TEMPLATE = `
<div id="app" class="sample-box drop-shell storefront-shell" data-screen="flashdrop" data-version="1">
  <section id="hero" class="panel commerce-hero" data-role="hero">
    <div class="status-strip">
      <span class="event-chip" data-state="preview">멤버 프리뷰</span>
      <span class="event-chip event-chip--soft" data-window="18:00">드롭 18:00</span>
    </div>
    <h1>FlashDrop Live</h1>
    <p>
      <strong>AURA Runner 01</strong> 오픈까지
      <span class="highlight" data-tone="blue">12분</span>
      남았고 <em>멤버 입장</em>이 순차적으로 열립니다.
    </p>
    <div class="hero-metrics">
      <div class="hero-metric">
        <span>입장 상태</span>
        <strong>입장 전</strong>
      </div>
      <div class="hero-metric">
        <span>재고 상태</span>
        <strong>안정적</strong>
      </div>
      <div class="hero-metric">
        <span>주목 번들</span>
        <strong>스타터 우선 노출</strong>
      </div>
    </div>
    <button type="button" class="ghost" data-service-scenario="text-attr">멤버 입장하기</button>
  </section>
  <section id="dashboard" class="panel service-grid service-grid--storefront" data-role="dashboard">
    <article class="commerce-card overview-card" data-topic="overview">
      <h2>드롭 현황</h2>
      <div class="overview-grid">
        <div class="overview-stat">
          <span>진행 상태</span>
          <strong>프리뷰</strong>
        </div>
        <div class="overview-stat">
          <span>입장 대상</span>
          <strong>멤버</strong>
        </div>
        <div class="overview-stat">
          <span>출고</span>
          <strong>당일 발송</strong>
        </div>
      </div>
      <p class="note">입장 전에는 번들 구성을 둘러보고 대기만 할 수 있습니다.</p>
    </article>
    <article class="commerce-card bundle-card" data-topic="bundles">
      <div class="section-head">
        <h2>번들 구성</h2>
        <span>선택 가능한 번들 3종</span>
      </div>
      <ul class="offer-list" data-list="bundles">
        <li class="offer-item" data-key="starter">
          <span>스타터 번들</span>
          <strong>₩129,000</strong>
        </li>
        <li class="offer-item" data-key="core">
          <span>코어 페어</span>
          <strong>₩189,000</strong>
        </li>
        <li class="offer-item" data-key="collector">
          <span>컬렉터 팩</span>
          <strong>₩249,000</strong>
          <button type="button" class="solid offer-item__action" data-service-scenario="create-remove">드롭 백에 담기</button>
        </li>
      </ul>
    </article>
    <aside class="commerce-card summary-card" data-topic="summary">
      <h2>내 드롭 백</h2>
      <p class="note empty-copy" data-state="empty" data-key="empty-state">관심 번들을 담으면 요약이 바로 나타납니다.</p>
      <div class="summary-list">
        <div class="summary-row">
          <span>입장 상태</span>
          <strong>멤버 프리뷰</strong>
        </div>
        <div class="summary-row">
          <span>선택 상태</span>
          <strong>선택 대기</strong>
        </div>
        <div class="summary-row">
          <span>주문 단계</span>
          <strong>잠금</strong>
        </div>
      </div>
      <button type="button" class="solid" data-service-scenario="replace-tag">주문서 열기</button>
    </aside>
    <article class="commerce-card recommendation-card" data-topic="recommendations">
      <div class="section-head">
        <h2>멤버 추천</h2>
        <button type="button" class="ghost section-head__action" data-service-scenario="reorder-keyed">인기순 보기</button>
      </div>
      <ul class="recommendation-list" data-list="recommendations">
        <li class="recommendation-item" data-key="starter">
          <span>스타터 번들</span>
          <strong>입문 선호</strong>
        </li>
        <li class="recommendation-item" data-key="core">
          <span>코어 페어</span>
          <strong>빠른 소진 예상</strong>
        </li>
        <li class="recommendation-item" data-key="collector">
          <span>컬렉터 팩</span>
          <strong>희소성 최고</strong>
        </li>
      </ul>
    </article>
  </section>
</div>
`.trim();

const SCENARIOS = [
  {
    id: "text-attr",
    title: "硫ㅻ쾭 ?낆옣",
    description: "?꾨━酉??곹깭?먯꽌 硫ㅻ쾭 ?낆옣???대━硫?媛숈? 援ъ“ ?덉쓽 ?띿뒪?몄? ?띿꽦留?諛붾뚮뒗 ?쒕굹由ъ삤?낅땲??",
    demoHeadline: "?묎렐 沅뚰븳???대━硫??щ윭 而댄룷?뚰듃媛 媛숈? 援ъ“瑜??좎???梨??곹깭? 移댄뵾留??숈떆??諛붾앸땲??",
    businessValue: "Hero, overview, bag summary, CTA泥섎읆 ?щ윭 ?곸뿭???숈떆??媛숈? ?곹깭瑜?諛섏쁺?섎뒗 ?붾㈃? 吏곸젒 DOM 議곗옉蹂대떎 ?곹깭 湲곕컲 ?뚮뜑留곸씠 ?좊━?⑸땲??",
    expectedTypes: [PATCH_TYPES.TEXT, PATCH_TYPES.ATTR_SET, PATCH_TYPES.ATTR_REMOVE],
    html: `
<div id="app" class="sample-box drop-shell storefront-shell live-shell" data-screen="flashdrop" data-version="2">
  <section id="hero" class="panel commerce-hero" data-role="hero" data-state="live">
    <div class="status-strip">
      <span class="event-chip event-chip--live" data-state="live">?낆옣 ?ㅽ뵂</span>
      <span class="event-chip event-chip--soft" data-window="live">吏湲?吏꾪뻾 以?/span>
    </div>
    <h1>FlashDrop 硫ㅻ쾭 ?낆옣</h1>
    <p>
      <strong>AURA Runner 01</strong>??      <span class="highlight" data-tone="green">硫ㅻ쾭?먭쾶 ?ㅽ뵂</span>
      ?섏뿀怨?<em>?곗꽑 二쇰Ц</em>??媛?ν빀?덈떎.
    </p>
    <div class="hero-metrics">
      <div class="hero-metric">
        <span>?낆옣 ?곹깭</span>
        <strong>硫ㅻ쾭 ?낆옣 媛??/strong>
      </div>
      <div class="hero-metric">
        <span>?ш퀬 ?곹깭</span>
        <strong>Moving fast</strong>
      </div>
      <div class="hero-metric">
        <span>二쇰ぉ 踰덈뱾</span>
        <strong>肄붿뼱 ?섏뼱 湲됱긽??/strong>
      </div>
    </div>
    <button type="button" class="ghost" data-action="drop" data-live="true">吏湲??낆옣?섍린</button>
  </section>
  <section id="dashboard" class="panel service-grid service-grid--storefront" data-role="dashboard">
    <article class="commerce-card overview-card" data-topic="overview">
      <h2>?쒕∼ ?꾪솴</h2>
      <div class="overview-grid">
        <div class="overview-stat">
          <span>吏꾪뻾 ?곹깭</span>
          <strong>?ㅽ뵂</strong>
        </div>
        <div class="overview-stat">
          <span>?낆옣 ???/span>
          <strong>硫ㅻ쾭 ?곗꽑</strong>
        </div>
        <div class="overview-stat">
          <span>異쒓퀬</span>
          <strong>?곗꽑 異쒓퀬</strong>
        </div>
      </div>
      <p class="note">?댁젣 踰덈뱾???섎굹 ?닿퀬 諛붾줈 二쇰Ц ?④퀎濡??대룞?????덉뒿?덈떎.</p>
    </article>
    <article class="commerce-card bundle-card" data-topic="bundles">
      <div class="section-head">
        <h2>踰덈뱾 援ъ꽦</h2>
        <span>3媛?踰덈뱾 援ъ꽦</span>
      </div>
      <ul class="offer-list" data-list="bundles">
        <li class="offer-item" data-key="starter">
          <span>?ㅽ???踰덈뱾</span>
          <strong>??29,000</strong>
        </li>
        <li class="offer-item" data-key="core">
          <span>肄붿뼱 ?섏뼱</span>
          <strong>??89,000</strong>
        </li>
        <li class="offer-item" data-key="collector">
          <span>而щ젆????/span>
          <strong>??49,000</strong>
          <button type="button" class="solid offer-item__action" data-service-scenario="create-remove">Bag???닿린</button>
        </li>
      </ul>
    </article>
    <aside class="commerce-card summary-card" data-topic="summary">
      <h2>???쒕∼ 諛?/h2>
      <p class="note empty-copy" data-state="empty" data-key="empty-state">愿??踰덈뱾???댁쑝硫??붿빟??諛붾줈 ?섑??⑸땲??</p>
      <div class="summary-list">
        <div class="summary-row">
          <span>?낆옣 ?곹깭</span>
          <strong>硫ㅻ쾭 ?낆옣 媛??/strong>
        </div>
        <div class="summary-row">
          <span>踰덈뱾 ?곹깭</span>
          <strong>Choose now</strong>
        </div>
        <div class="summary-row">
          <span>二쇰Ц ?④퀎</span>
          <strong>?대┝</strong>
        </div>
      </div>
      <button type="button" class="solid" disabled>踰덈뱾 ?좏깮 ???쒖꽦??/button>
    </aside>
    <article class="commerce-card recommendation-card" data-topic="recommendations">
      <div class="section-head">
        <h2>硫ㅻ쾭 異붿쿇</h2>
        <button type="button" class="ghost section-head__action" data-service-scenario="reorder-keyed">?멸린??蹂닿린</button>
      </div>
      <ul class="recommendation-list" data-list="recommendations">
        <li class="recommendation-item" data-key="starter">
          <span>Starter Bundle</span>
          <strong>?낅Ц ?좏샇</strong>
        </li>
        <li class="recommendation-item" data-key="core">
          <span>Core Pair</span>
          <strong>鍮좊Ⅸ ?뚯쭊 ?덉긽</strong>
        </li>
        <li class="recommendation-item" data-key="collector">
          <span>Collector Pack</span>
          <strong>?ъ냼??理쒓퀬</strong>
        </li>
      </ul>
    </article>
  </section>
</div>
    `.trim()
  },
  {
    id: "create-remove",
    title: "Collector Pack ?닿린",
    description: "鍮?媛諛??곹깭瑜??쒓굅?섍퀬 ?덉빟 諛곗?瑜??앹꽦?섎뒗 ?쒕굹由ъ삤?낅땲??",
    demoHeadline: "媛숈? ?곹깭?쇰룄 ?대뼡 ?곸뿭? ?щ씪吏怨? ?대뼡 ?곸뿭? ?덈줈 ?앷퉩?덈떎. ?대븣 CREATE? REMOVE媛 媛??吏곸젒?곸쑝濡??쒕윭?⑸땲??",
    businessValue: "鍮??곹깭 ?쒓굅? ?좏깮 ?곹깭 ?앹꽦???숈떆???쇱뼱?섎뒗 bag summary???곹깭 湲곕컲 UI?먯꽌 ?먯＜ ?섏삤???⑦꽩?낅땲??",
    expectedTypes: [PATCH_TYPES.CREATE, PATCH_TYPES.REMOVE],
    html: `
<div id="app" class="sample-box drop-shell storefront-shell" data-screen="flashdrop" data-version="1">
  <section id="hero" class="panel commerce-hero" data-role="hero">
    <div class="status-strip">
      <span class="event-chip" data-state="preview">MEMBER PREVIEW</span>
      <span class="event-chip event-chip--soft" data-window="18:00">DROP 18:00</span>
    </div>
    <h1>FlashDrop Live</h1>
    <p>
      <strong>AURA Runner 01</strong> ?ㅽ뵂源뚯?
      <span class="highlight" data-tone="blue">12 minutes</span>
      and <em>member access</em> opens in waves.
    </p>
    <div class="hero-metrics">
      <div class="hero-metric">
        <span>?낆옣 ?곹깭</span>
        <strong>Preview only</strong>
      </div>
      <div class="hero-metric">
        <span>?ш퀬 ?곹깭</span>
        <strong>Stable</strong>
      </div>
      <div class="hero-metric">
        <span>Spotlight</span>
        <strong>Starter first</strong>
      </div>
    </div>
    <button type="button" class="ghost" data-action="drop" disabled>硫ㅻ쾭 ?낆옣 ?湲?/button>
  </section>
  <section id="dashboard" class="panel service-grid service-grid--storefront" data-role="dashboard">
    <article class="commerce-card overview-card" data-topic="overview">
      <h2>Drop Overview</h2>
      <div class="overview-grid">
        <div class="overview-stat">
          <span>Launch mode</span>
          <strong>Preview</strong>
        </div>
        <div class="overview-stat">
          <span>Eligible access</span>
          <strong>Members</strong>
        </div>
        <div class="overview-stat">
          <span>Dispatch</span>
          <strong>Same day</strong>
        </div>
      </div>
      <p class="note">Members can bookmark one bundle before access opens.</p>
    </article>
    <article class="commerce-card bundle-card" data-topic="bundles">
      <div class="section-head">
        <h2>Bundle Lineup</h2>
        <span>3媛?踰덈뱾 援ъ꽦</span>
      </div>
      <ul class="offer-list" data-list="bundles">
        <li class="offer-item" data-key="starter">
          <span>Starter Bundle</span>
          <strong>??29,000</strong>
        </li>
        <li class="offer-item" data-key="core">
          <span>Core Pair</span>
          <strong>??89,000</strong>
        </li>
        <li class="offer-item" data-key="collector">
          <span>Collector Pack</span>
          <strong>??49,000</strong>
        </li>
      </ul>
    </article>
    <aside class="commerce-card summary-card" data-topic="summary">
      <h2>My Drop Bag</h2>
      <div class="reservation-pill" data-badge="reserved" data-key="reserved-state">Collector Pack reserved for 5 min</div>
      <div class="summary-list">
        <div class="summary-row">
          <span>?낆옣 ?곹깭</span>
          <strong>Member preview</strong>
        </div>
        <div class="summary-row">
          <span>踰덈뱾 ?곹깭</span>
          <strong>Waiting choice</strong>
        </div>
        <div class="summary-row">
          <span>Checkout</span>
          <strong>Locked</strong>
        </div>
      </div>
      <button type="button" class="solid" data-service-scenario="replace-tag">二쇰Ц???닿린</button>
    </aside>
    <article class="commerce-card recommendation-card" data-topic="recommendations">
      <div class="section-head">
        <h2>Recommended for Members</h2>
        <button type="button" class="ghost section-head__action" data-service-scenario="reorder-keyed">?멸린??蹂닿린</button>
      </div>
      <ul class="recommendation-list" data-list="recommendations">
        <li class="recommendation-item" data-key="starter">
          <span>Starter Bundle</span>
          <strong>?낅Ц ?좏샇</strong>
        </li>
        <li class="recommendation-item" data-key="core">
          <span>Core Pair</span>
          <strong>鍮좊Ⅸ ?뚯쭊 ?덉긽</strong>
        </li>
        <li class="recommendation-item" data-key="collector">
          <span>Collector Pack</span>
          <strong>?ъ냼??理쒓퀬</strong>
        </li>
      </ul>
    </article>
  </section>
</div>
    `.trim()
  },
  {
    id: "replace-tag",
    title: "二쇰Ц???닿린",
    description: "媛諛??붿빟 移대뱶媛 二쇰Ц ?④퀎 ?뱀뀡?쇰줈 援먯껜?섎뒗 ?쒕굹由ъ삤?낅땲??",
    demoHeadline: "援ъ“媛 ?щ씪吏???쒓컙?먮뒗 ?몃? ?섏젙???꾨땲??subtree 援먯껜媛 ???먯뿰?ㅻ읇?듬땲??",
    businessValue: "?먯깋??移대뱶?먯꽌 寃곗젣??移대뱶濡??꾪솚?섎뒗 ?쒓컙? ?ㅼ젣 ?쒕퉬?ㅼ뿉?쒕룄 議곌굔遺 ?뚮뜑留곸씠 紐낇솗??援ш컙?낅땲??",
    expectedTypes: [PATCH_TYPES.REPLACE],
    html: `
<div id="app" class="sample-box drop-shell storefront-shell" data-screen="flashdrop" data-version="1">
  <section id="hero" class="panel commerce-hero" data-role="hero">
    <div class="status-strip">
      <span class="event-chip" data-state="preview">MEMBER PREVIEW</span>
      <span class="event-chip event-chip--soft" data-window="18:00">DROP 18:00</span>
    </div>
    <h1>FlashDrop Live</h1>
    <p>
      <strong>AURA Runner 01</strong> ?ㅽ뵂源뚯?
      <span class="highlight" data-tone="blue">12 minutes</span>
      and <em>member access</em> opens in waves.
    </p>
    <div class="hero-metrics">
      <div class="hero-metric">
        <span>?낆옣 ?곹깭</span>
        <strong>Preview only</strong>
      </div>
      <div class="hero-metric">
        <span>?ш퀬 ?곹깭</span>
        <strong>Stable</strong>
      </div>
      <div class="hero-metric">
        <span>Spotlight</span>
        <strong>Starter first</strong>
      </div>
    </div>
    <button type="button" class="ghost" data-action="drop" disabled>硫ㅻ쾭 ?낆옣 ?湲?/button>
  </section>
  <section id="dashboard" class="panel service-grid service-grid--storefront" data-role="dashboard">
    <article class="commerce-card overview-card" data-topic="overview">
      <h2>Drop Overview</h2>
      <div class="overview-grid">
        <div class="overview-stat">
          <span>Launch mode</span>
          <strong>Preview</strong>
        </div>
        <div class="overview-stat">
          <span>Eligible access</span>
          <strong>Members</strong>
        </div>
        <div class="overview-stat">
          <span>Dispatch</span>
          <strong>Same day</strong>
        </div>
      </div>
      <p class="note">Members can bookmark one bundle before access opens.</p>
    </article>
    <article class="commerce-card bundle-card" data-topic="bundles">
      <div class="section-head">
        <h2>Bundle Lineup</h2>
        <span>3媛?踰덈뱾 援ъ꽦</span>
      </div>
      <ul class="offer-list" data-list="bundles">
        <li class="offer-item" data-key="starter">
          <span>Starter Bundle</span>
          <strong>??29,000</strong>
        </li>
        <li class="offer-item" data-key="core">
          <span>Core Pair</span>
          <strong>??89,000</strong>
        </li>
        <li class="offer-item" data-key="collector">
          <span>Collector Pack</span>
          <strong>??49,000</strong>
        </li>
      </ul>
    </article>
    <section class="commerce-card order-stage" data-topic="summary">
      <div class="section-head">
        <h2>Order Stage</h2>
        <span>Step 2 of 3</span>
      </div>
      <div class="order-metrics">
        <div class="order-metric">
          <span>Selected bundle</span>
          <strong>Core Pair</strong>
        </div>
        <div class="order-metric">
          <span>Dispatch lane</span>
          <strong>Priority</strong>
        </div>
        <div class="order-metric">
          <span>Total</span>
          <strong>??89,000</strong>
        </div>
      </div>
      <p class="note">Address and payment blocks are now ready because the screen switched from reservation mode to checkout mode.</p>
      <button type="button" class="solid" data-action="purchase">寃곗젣 吏꾪뻾</button>
    </section>
    <article class="commerce-card recommendation-card" data-topic="recommendations">
      <div class="section-head">
        <h2>Recommended for Members</h2>
        <button type="button" class="ghost section-head__action" data-service-scenario="reorder-keyed">?멸린??蹂닿린</button>
      </div>
      <ul class="recommendation-list" data-list="recommendations">
        <li class="recommendation-item" data-key="starter">
          <span>Starter Bundle</span>
          <strong>?낅Ц ?좏샇</strong>
        </li>
        <li class="recommendation-item" data-key="core">
          <span>Core Pair</span>
          <strong>鍮좊Ⅸ ?뚯쭊 ?덉긽</strong>
        </li>
        <li class="recommendation-item" data-key="collector">
          <span>Collector Pack</span>
          <strong>?ъ냼??理쒓퀬</strong>
        </li>
      </ul>
    </article>
  </section>
</div>
    `.trim()
  },
  {
    id: "reorder-keyed",
    title: "異붿쿇??蹂닿린",
    description: "異붿쿇 由ъ뒪?몄쓽 ?곗꽑?쒖쐞留?諛붾뚮뒗 ?쒕굹由ъ삤?낅땲??",
    demoHeadline: "媛숈? ?꾩씠?쒖씠?쇰룄 ?몄텧 ?쒖꽌留??ㅼ떆 怨꾩궛?댁빞 ???뚮뒗 key 湲곕컲 reorder媛 以묒슂?⑸땲??",
    businessValue: "異붿쿇 ?곸뿭, ??궧 ?곸뿭, ?뺣젹 ?좉? 媛숈? UI???몃뱶 ?뺤껜?깆쓣 ?좎???梨??쒖꽌留??먯＜ 諛붾앸땲??",
    expectedTypes: [PATCH_TYPES.REORDER_CHILDREN],
    html: `
<div id="app" class="sample-box drop-shell storefront-shell" data-screen="flashdrop" data-version="1">
  <section id="hero" class="panel commerce-hero" data-role="hero">
    <div class="status-strip">
      <span class="event-chip" data-state="preview">MEMBER PREVIEW</span>
      <span class="event-chip event-chip--soft" data-window="18:00">DROP 18:00</span>
    </div>
    <h1>FlashDrop Live</h1>
    <p>
      <strong>AURA Runner 01</strong> ?ㅽ뵂源뚯?
      <span class="highlight" data-tone="blue">12 minutes</span>
      and <em>member access</em> opens in waves.
    </p>
    <div class="hero-metrics">
      <div class="hero-metric">
        <span>?낆옣 ?곹깭</span>
        <strong>Preview only</strong>
      </div>
      <div class="hero-metric">
        <span>?ш퀬 ?곹깭</span>
        <strong>Stable</strong>
      </div>
      <div class="hero-metric">
        <span>Spotlight</span>
        <strong>Starter first</strong>
      </div>
    </div>
    <button type="button" class="ghost" data-action="drop" disabled>硫ㅻ쾭 ?낆옣 ?湲?/button>
  </section>
  <section id="dashboard" class="panel service-grid service-grid--storefront" data-role="dashboard">
    <article class="commerce-card overview-card" data-topic="overview">
      <h2>Drop Overview</h2>
      <div class="overview-grid">
        <div class="overview-stat">
          <span>Launch mode</span>
          <strong>Preview</strong>
        </div>
        <div class="overview-stat">
          <span>Eligible access</span>
          <strong>Members</strong>
        </div>
        <div class="overview-stat">
          <span>Dispatch</span>
          <strong>Same day</strong>
        </div>
      </div>
      <p class="note">Members can bookmark one bundle before access opens.</p>
    </article>
    <article class="commerce-card bundle-card" data-topic="bundles">
      <div class="section-head">
        <h2>Bundle Lineup</h2>
        <span>3媛?踰덈뱾 援ъ꽦</span>
      </div>
      <ul class="offer-list" data-list="bundles">
        <li class="offer-item" data-key="starter">
          <span>Starter Bundle</span>
          <strong>??29,000</strong>
        </li>
        <li class="offer-item" data-key="core">
          <span>Core Pair</span>
          <strong>??89,000</strong>
        </li>
        <li class="offer-item" data-key="collector">
          <span>Collector Pack</span>
          <strong>??49,000</strong>
        </li>
      </ul>
    </article>
    <aside class="commerce-card summary-card" data-topic="summary">
      <h2>My Drop Bag</h2>
      <p class="note empty-copy" data-state="empty" data-key="empty-state">愿??踰덈뱾???댁쑝硫??붿빟??諛붾줈 ?섑??⑸땲??</p>
      <div class="summary-list">
        <div class="summary-row">
          <span>?낆옣 ?곹깭</span>
          <strong>Member preview</strong>
        </div>
        <div class="summary-row">
          <span>踰덈뱾 ?곹깭</span>
          <strong>Waiting choice</strong>
        </div>
        <div class="summary-row">
          <span>Checkout</span>
          <strong>Locked</strong>
        </div>
      </div>
      <button type="button" class="solid" data-service-scenario="replace-tag">二쇰Ц???닿린</button>
    </aside>
    <article class="commerce-card recommendation-card" data-topic="recommendations">
      <div class="section-head">
        <h2>Recommended for Members</h2>
        <button type="button" class="ghost section-head__action" data-service-scenario="reorder-keyed">?멸린??蹂닿린</button>
      </div>
      <ul class="recommendation-list" data-list="recommendations">
        <li class="recommendation-item" data-key="collector">
          <span>Collector Pack</span>
          <strong>?ъ냼??理쒓퀬</strong>
        </li>
        <li class="recommendation-item" data-key="core">
          <span>Core Pair</span>
          <strong>鍮좊Ⅸ ?뚯쭊 ?덉긽</strong>
        </li>
        <li class="recommendation-item" data-key="starter">
          <span>Starter Bundle</span>
          <strong>?낅Ц ?좏샇</strong>
        </li>
      </ul>
    </article>
  </section>
</div>
    `.trim()
  }
];

const textAttrScenario = SCENARIOS.find((scenario) => scenario.id === "text-attr");
if (textAttrScenario) {
  textAttrScenario.title = "멤버 입장";
  textAttrScenario.description = "프리뷰 상태에서 멤버 입장이 열리며 같은 구조 안의 텍스트와 속성만 바뀌는 시나리오입니다.";
  textAttrScenario.demoHeadline = "접근 권한이 열리면 여러 컴포넌트가 같은 구조를 유지한 채 상태와 카피만 동시에 바뀝니다.";
  textAttrScenario.businessValue = "Hero, overview, 드롭 백 요약처럼 여러 영역이 동시에 같은 상태를 반영해야 할 때 상태 기반 렌더링이 유리합니다.";
  textAttrScenario.html = `
<div id="app" class="sample-box drop-shell storefront-shell live-shell" data-screen="flashdrop" data-version="2">
  <section id="hero" class="panel commerce-hero" data-role="hero" data-state="live">
    <div class="status-strip">
      <span class="event-chip event-chip--live" data-state="live">입장 오픈</span>
      <span class="event-chip event-chip--soft" data-window="live">지금 진행 중</span>
    </div>
    <h1>FlashDrop 멤버 입장</h1>
    <p>
      <strong>AURA Runner 01</strong>이
      <span class="highlight" data-tone="green">멤버에게 오픈</span>
      되었고 <em>우선 주문</em>이 가능합니다.
    </p>
    <div class="hero-metrics">
      <div class="hero-metric">
        <span>입장 상태</span>
        <strong>멤버 입장 가능</strong>
      </div>
      <div class="hero-metric">
        <span>재고 상태</span>
        <strong>빠르게 소진 중</strong>
      </div>
      <div class="hero-metric">
        <span>주목 번들</span>
        <strong>코어 페어 급상승</strong>
      </div>
    </div>
    <button type="button" class="ghost" data-action="drop" data-live="true">지금 입장하기</button>
  </section>
  <section id="dashboard" class="panel service-grid service-grid--storefront" data-role="dashboard">
    <article class="commerce-card overview-card" data-topic="overview">
      <h2>드롭 현황</h2>
      <div class="overview-grid">
        <div class="overview-stat">
          <span>진행 상태</span>
          <strong>오픈</strong>
        </div>
        <div class="overview-stat">
          <span>입장 대상</span>
          <strong>멤버 우선</strong>
        </div>
        <div class="overview-stat">
          <span>출고</span>
          <strong>우선 출고</strong>
        </div>
      </div>
      <p class="note">이제 번들을 하나 담고 바로 주문 단계로 이동할 수 있습니다.</p>
    </article>
    <article class="commerce-card bundle-card" data-topic="bundles">
      <div class="section-head">
        <h2>번들 구성</h2>
        <span>선택 가능한 번들 3종</span>
      </div>
      <ul class="offer-list" data-list="bundles">
        <li class="offer-item" data-key="starter">
          <span>스타터 번들</span>
          <strong>₩129,000</strong>
        </li>
        <li class="offer-item" data-key="core">
          <span>코어 페어</span>
          <strong>₩189,000</strong>
        </li>
        <li class="offer-item" data-key="collector">
          <span>컬렉터 팩</span>
          <strong>₩249,000</strong>
          <button type="button" class="solid offer-item__action" data-service-scenario="create-remove">드롭 백에 담기</button>
        </li>
      </ul>
    </article>
    <aside class="commerce-card summary-card" data-topic="summary">
      <h2>내 드롭 백</h2>
      <p class="note empty-copy" data-state="empty" data-key="empty-state">관심 번들을 담으면 요약이 바로 나타납니다.</p>
      <div class="summary-list">
        <div class="summary-row">
          <span>입장 상태</span>
          <strong>멤버 입장 가능</strong>
        </div>
        <div class="summary-row">
          <span>선택 상태</span>
          <strong>지금 선택 가능</strong>
        </div>
        <div class="summary-row">
          <span>주문 단계</span>
          <strong>열림</strong>
        </div>
      </div>
      <button type="button" class="solid" disabled>번들 선택 후 활성화</button>
    </aside>
    <article class="commerce-card recommendation-card" data-topic="recommendations">
      <div class="section-head">
        <h2>멤버 추천</h2>
        <button type="button" class="ghost section-head__action" data-service-scenario="reorder-keyed">인기순 보기</button>
      </div>
      <ul class="recommendation-list" data-list="recommendations">
        <li class="recommendation-item" data-key="starter">
          <span>스타터 번들</span>
          <strong>입문 선호</strong>
        </li>
        <li class="recommendation-item" data-key="core">
          <span>코어 페어</span>
          <strong>빠른 소진 예상</strong>
        </li>
        <li class="recommendation-item" data-key="collector">
          <span>컬렉터 팩</span>
          <strong>희소성 최고</strong>
        </li>
      </ul>
    </article>
  </section>
</div>
  `.trim();
}

const createRemoveScenario = SCENARIOS.find((scenario) => scenario.id === "create-remove");
if (createRemoveScenario) {
  createRemoveScenario.title = "컬렉터 팩 담기";
  createRemoveScenario.description = "빈 가방 상태를 제거하고 예약 배지를 생성하는 시나리오입니다.";
  createRemoveScenario.demoHeadline = "같은 영역 안에서 비어 있던 상태가 사라지고 예약 상태가 새로 생깁니다.";
  createRemoveScenario.businessValue = "장바구니, 예약, 북마크 같은 상태 전환은 빈 상태 제거와 선택 상태 생성이 동시에 일어나는 전형적인 패턴입니다.";
  createRemoveScenario.html = `
<div id="app" class="sample-box drop-shell storefront-shell" data-screen="flashdrop" data-version="1">
  <section id="hero" class="panel commerce-hero" data-role="hero">
    <div class="status-strip">
      <span class="event-chip" data-state="preview">멤버 프리뷰</span>
      <span class="event-chip event-chip--soft" data-window="18:00">드롭 18:00</span>
    </div>
    <h1>FlashDrop Live</h1>
    <p>
      <strong>AURA Runner 01</strong> 오픈까지
      <span class="highlight" data-tone="blue">12분</span>
      남았고 <em>멤버 입장</em>이 순차적으로 열립니다.
    </p>
    <div class="hero-metrics">
      <div class="hero-metric">
        <span>입장 상태</span>
        <strong>입장 전</strong>
      </div>
      <div class="hero-metric">
        <span>재고 상태</span>
        <strong>안정적</strong>
      </div>
      <div class="hero-metric">
        <span>주목 번들</span>
        <strong>스타터 우선 노출</strong>
      </div>
    </div>
    <button type="button" class="ghost" data-action="drop" disabled>멤버 입장 대기</button>
  </section>
  <section id="dashboard" class="panel service-grid service-grid--storefront" data-role="dashboard">
    <article class="commerce-card overview-card" data-topic="overview">
      <h2>드롭 현황</h2>
      <div class="overview-grid">
        <div class="overview-stat">
          <span>진행 상태</span>
          <strong>프리뷰</strong>
        </div>
        <div class="overview-stat">
          <span>입장 대상</span>
          <strong>멤버</strong>
        </div>
        <div class="overview-stat">
          <span>출고</span>
          <strong>당일 발송</strong>
        </div>
      </div>
      <p class="note">입장 전에는 번들 구성을 둘러보고 대기만 할 수 있습니다.</p>
    </article>
    <article class="commerce-card bundle-card" data-topic="bundles">
      <div class="section-head">
        <h2>번들 구성</h2>
        <span>선택 가능한 번들 3종</span>
      </div>
      <ul class="offer-list" data-list="bundles">
        <li class="offer-item" data-key="starter">
          <span>스타터 번들</span>
          <strong>₩129,000</strong>
        </li>
        <li class="offer-item" data-key="core">
          <span>코어 페어</span>
          <strong>₩189,000</strong>
        </li>
        <li class="offer-item" data-key="collector">
          <span>컬렉터 팩</span>
          <strong>₩249,000</strong>
        </li>
      </ul>
    </article>
    <aside class="commerce-card summary-card" data-topic="summary">
      <h2>내 드롭 백</h2>
      <div class="reservation-pill" data-badge="reserved" data-key="reserved-state">컬렉터 팩이 5분 동안 예약되었습니다</div>
      <div class="summary-list">
        <div class="summary-row">
          <span>입장 상태</span>
          <strong>멤버 프리뷰</strong>
        </div>
        <div class="summary-row">
          <span>선택 상태</span>
          <strong>선택 대기</strong>
        </div>
        <div class="summary-row">
          <span>주문 단계</span>
          <strong>잠금</strong>
        </div>
      </div>
      <button type="button" class="solid" data-service-scenario="replace-tag">주문서 열기</button>
    </aside>
    <article class="commerce-card recommendation-card" data-topic="recommendations">
      <div class="section-head">
        <h2>멤버 추천</h2>
        <button type="button" class="ghost section-head__action" data-service-scenario="reorder-keyed">인기순 보기</button>
      </div>
      <ul class="recommendation-list" data-list="recommendations">
        <li class="recommendation-item" data-key="starter">
          <span>스타터 번들</span>
          <strong>입문 선호</strong>
        </li>
        <li class="recommendation-item" data-key="core">
          <span>코어 페어</span>
          <strong>빠른 소진 예상</strong>
        </li>
        <li class="recommendation-item" data-key="collector">
          <span>컬렉터 팩</span>
          <strong>희소성 최고</strong>
        </li>
      </ul>
    </article>
  </section>
</div>
  `.trim();
}

const replaceScenario = SCENARIOS.find((scenario) => scenario.id === "replace-tag");
if (replaceScenario) {
  replaceScenario.title = "주문서 열기";
  replaceScenario.description = "가방 요약 카드가 주문 단계 섹션으로 교체되는 시나리오입니다.";
  replaceScenario.demoHeadline = "구조가 달라지는 순간에는 세부 수정이 아니라 subtree 교체가 더 자연스럽습니다.";
  replaceScenario.businessValue = "탐색용 카드에서 결제용 카드로 전환되는 순간은 실제 서비스에서도 조건부 렌더링이 가장 뚜렷한 구간입니다.";
  replaceScenario.html = `
<div id="app" class="sample-box drop-shell storefront-shell" data-screen="flashdrop" data-version="1">
  <section id="hero" class="panel commerce-hero" data-role="hero">
    <div class="status-strip">
      <span class="event-chip" data-state="preview">멤버 프리뷰</span>
      <span class="event-chip event-chip--soft" data-window="18:00">드롭 18:00</span>
    </div>
    <h1>FlashDrop Live</h1>
    <p>
      <strong>AURA Runner 01</strong> 오픈까지
      <span class="highlight" data-tone="blue">12분</span>
      남았고 <em>멤버 입장</em>이 순차적으로 열립니다.
    </p>
    <div class="hero-metrics">
      <div class="hero-metric">
        <span>입장 상태</span>
        <strong>입장 전</strong>
      </div>
      <div class="hero-metric">
        <span>재고 상태</span>
        <strong>안정적</strong>
      </div>
      <div class="hero-metric">
        <span>주목 번들</span>
        <strong>스타터 우선 노출</strong>
      </div>
    </div>
    <button type="button" class="ghost" data-action="drop" disabled>멤버 입장 대기</button>
  </section>
  <section id="dashboard" class="panel service-grid service-grid--storefront" data-role="dashboard">
    <article class="commerce-card overview-card" data-topic="overview">
      <h2>드롭 현황</h2>
      <div class="overview-grid">
        <div class="overview-stat">
          <span>진행 상태</span>
          <strong>프리뷰</strong>
        </div>
        <div class="overview-stat">
          <span>입장 대상</span>
          <strong>멤버</strong>
        </div>
        <div class="overview-stat">
          <span>출고</span>
          <strong>당일 발송</strong>
        </div>
      </div>
      <p class="note">입장 전에는 번들 구성을 둘러보고 대기만 할 수 있습니다.</p>
    </article>
    <article class="commerce-card bundle-card" data-topic="bundles">
      <div class="section-head">
        <h2>번들 구성</h2>
        <span>선택 가능한 번들 3종</span>
      </div>
      <ul class="offer-list" data-list="bundles">
        <li class="offer-item" data-key="starter">
          <span>스타터 번들</span>
          <strong>₩129,000</strong>
        </li>
        <li class="offer-item" data-key="core">
          <span>코어 페어</span>
          <strong>₩189,000</strong>
        </li>
        <li class="offer-item" data-key="collector">
          <span>컬렉터 팩</span>
          <strong>₩249,000</strong>
        </li>
      </ul>
    </article>
    <section class="commerce-card order-stage" data-topic="summary">
      <div class="section-head">
        <h2>주문 단계</h2>
        <span>3단계 중 2단계</span>
      </div>
      <div class="order-metrics">
        <div class="order-metric">
          <span>선택 번들</span>
          <strong>코어 페어</strong>
        </div>
        <div class="order-metric">
          <span>출고 방식</span>
          <strong>우선 출고</strong>
        </div>
        <div class="order-metric">
          <span>결제 예정 금액</span>
          <strong>₩189,000</strong>
        </div>
      </div>
      <p class="note">예약 확인 카드가 결제 단계 카드로 전환되면서 주소와 결제 수단 입력이 열렸습니다.</p>
      <button type="button" class="solid" data-action="purchase">결제 진행</button>
    </section>
    <article class="commerce-card recommendation-card" data-topic="recommendations">
      <div class="section-head">
        <h2>멤버 추천</h2>
        <button type="button" class="ghost section-head__action" data-service-scenario="reorder-keyed">인기순 보기</button>
      </div>
      <ul class="recommendation-list" data-list="recommendations">
        <li class="recommendation-item" data-key="starter">
          <span>스타터 번들</span>
          <strong>입문 선호</strong>
        </li>
        <li class="recommendation-item" data-key="core">
          <span>코어 페어</span>
          <strong>빠른 소진 예상</strong>
        </li>
        <li class="recommendation-item" data-key="collector">
          <span>컬렉터 팩</span>
          <strong>희소성 최고</strong>
        </li>
      </ul>
    </article>
  </section>
</div>
  `.trim();
}

const reorderScenario = SCENARIOS.find((scenario) => scenario.id === "reorder-keyed");
if (reorderScenario) {
  reorderScenario.title = "인기순 보기";
  reorderScenario.description = "추천 리스트의 우선순위만 바뀌는 시나리오입니다.";
  reorderScenario.demoHeadline = "같은 아이템이라도 노출 순서만 다시 계산해야 할 때는 key 기반 reorder가 중요합니다.";
  reorderScenario.businessValue = "추천 영역, 랭킹 영역, 정렬 토글 같은 UI는 노드 정체성을 유지한 채 순서만 자주 바뀝니다.";
  reorderScenario.html = `
<div id="app" class="sample-box drop-shell storefront-shell" data-screen="flashdrop" data-version="1">
  <section id="hero" class="panel commerce-hero" data-role="hero">
    <div class="status-strip">
      <span class="event-chip" data-state="preview">멤버 프리뷰</span>
      <span class="event-chip event-chip--soft" data-window="18:00">드롭 18:00</span>
    </div>
    <h1>FlashDrop Live</h1>
    <p>
      <strong>AURA Runner 01</strong> 오픈까지
      <span class="highlight" data-tone="blue">12분</span>
      남았고 <em>멤버 입장</em>이 순차적으로 열립니다.
    </p>
    <div class="hero-metrics">
      <div class="hero-metric">
        <span>입장 상태</span>
        <strong>입장 전</strong>
      </div>
      <div class="hero-metric">
        <span>재고 상태</span>
        <strong>안정적</strong>
      </div>
      <div class="hero-metric">
        <span>주목 번들</span>
        <strong>스타터 우선 노출</strong>
      </div>
    </div>
    <button type="button" class="ghost" data-action="drop" disabled>멤버 입장 대기</button>
  </section>
  <section id="dashboard" class="panel service-grid service-grid--storefront" data-role="dashboard">
    <article class="commerce-card overview-card" data-topic="overview">
      <h2>드롭 현황</h2>
      <div class="overview-grid">
        <div class="overview-stat">
          <span>진행 상태</span>
          <strong>프리뷰</strong>
        </div>
        <div class="overview-stat">
          <span>입장 대상</span>
          <strong>멤버</strong>
        </div>
        <div class="overview-stat">
          <span>출고</span>
          <strong>당일 발송</strong>
        </div>
      </div>
      <p class="note">입장 전에는 번들 구성을 둘러보고 대기만 할 수 있습니다.</p>
    </article>
    <article class="commerce-card bundle-card" data-topic="bundles">
      <div class="section-head">
        <h2>번들 구성</h2>
        <span>선택 가능한 번들 3종</span>
      </div>
      <ul class="offer-list" data-list="bundles">
        <li class="offer-item" data-key="starter">
          <span>스타터 번들</span>
          <strong>₩129,000</strong>
        </li>
        <li class="offer-item" data-key="core">
          <span>코어 페어</span>
          <strong>₩189,000</strong>
        </li>
        <li class="offer-item" data-key="collector">
          <span>컬렉터 팩</span>
          <strong>₩249,000</strong>
        </li>
      </ul>
    </article>
    <aside class="commerce-card summary-card" data-topic="summary">
      <h2>내 드롭 백</h2>
      <p class="note empty-copy" data-state="empty" data-key="empty-state">관심 번들을 담으면 요약이 바로 나타납니다.</p>
      <div class="summary-list">
        <div class="summary-row">
          <span>입장 상태</span>
          <strong>멤버 프리뷰</strong>
        </div>
        <div class="summary-row">
          <span>선택 상태</span>
          <strong>선택 대기</strong>
        </div>
        <div class="summary-row">
          <span>주문 단계</span>
          <strong>잠금</strong>
        </div>
      </div>
      <button type="button" class="solid" data-service-scenario="replace-tag">주문서 열기</button>
    </aside>
    <article class="commerce-card recommendation-card" data-topic="recommendations">
      <div class="section-head">
        <h2>멤버 추천</h2>
        <button type="button" class="ghost section-head__action" data-service-scenario="reorder-keyed">인기순 보기</button>
      </div>
      <ul class="recommendation-list" data-list="recommendations">
        <li class="recommendation-item" data-key="collector">
          <span>컬렉터 팩</span>
          <strong>희소성 최고</strong>
        </li>
        <li class="recommendation-item" data-key="core">
          <span>코어 페어</span>
          <strong>빠른 소진 예상</strong>
        </li>
        <li class="recommendation-item" data-key="starter">
          <span>스타터 번들</span>
          <strong>입문 선호</strong>
        </li>
      </ul>
    </article>
  </section>
</div>
  `.trim();
}

SCENARIOS.push({
  id: "purchase-complete",
  title: "결제 완료",
  description: "실제 결제창 대신 시연용 완료 화면으로 전환되는 단계입니다.",
  demoHeadline: "주문 단계 다음에는 외부 결제창 대신 서비스 내부 완료 화면으로 이어지도록 구성했습니다.",
  businessValue: "발표에서는 결제 API 연동보다 결제 이후 상태가 서비스 화면에 어떻게 반영되는지가 더 중요하므로, 완료 상태를 한 번 더 diff하는 흐름이 적합합니다.",
  expectedTypes: [PATCH_TYPES.TEXT, PATCH_TYPES.ATTR_SET, PATCH_TYPES.CREATE, PATCH_TYPES.REMOVE],
  hiddenFromPanel: true,
  hiddenFromTour: true,
  html: `
<div id="app" class="sample-box drop-shell storefront-shell live-shell" data-screen="flashdrop" data-version="3">
  <section id="hero" class="panel commerce-hero" data-role="hero" data-state="complete">
    <div class="status-strip">
      <span class="event-chip event-chip--live" data-state="complete">결제 완료</span>
      <span class="event-chip event-chip--soft" data-window="shipment">오늘 출고 예정</span>
    </div>
    <h1>FlashDrop 주문이 완료되었습니다</h1>
    <p>
      <strong>AURA Runner 01 코어 페어</strong> 결제가 완료되었고
      <span class="highlight" data-tone="green">주문 번호 FD-240318</span>
      로 배송 준비가 시작되었습니다.
    </p>
    <div class="hero-metrics">
      <div class="hero-metric">
        <span>주문 상태</span>
        <strong>결제 완료</strong>
      </div>
      <div class="hero-metric">
        <span>출고 상태</span>
        <strong>오늘 출고 예정</strong>
      </div>
      <div class="hero-metric">
        <span>다음 단계</span>
        <strong>배송 추적 대기</strong>
      </div>
    </div>
    <button type="button" class="ghost" data-action="restart-demo">처음 화면으로 돌아가기</button>
  </section>
  <section id="dashboard" class="panel service-grid service-grid--storefront" data-role="dashboard">
    <article class="commerce-card overview-card" data-topic="overview">
      <h2>주문 요약</h2>
      <div class="overview-grid">
        <div class="overview-stat">
          <span>주문 번호</span>
          <strong>FD-240318</strong>
        </div>
        <div class="overview-stat">
          <span>결제 수단</span>
          <strong>시연용 간편결제</strong>
        </div>
        <div class="overview-stat">
          <span>출고</span>
          <strong>오늘 발송</strong>
        </div>
      </div>
      <p class="note">실제 PG 호출 대신 주문 완료 상태를 바로 보여줘 서비스 흐름이 끊기지 않도록 했습니다.</p>
    </article>
    <article class="commerce-card bundle-card" data-topic="bundles">
      <div class="section-head">
        <h2>구매 완료 상품</h2>
        <span>결제된 번들 1종</span>
      </div>
      <ul class="offer-list" data-list="bundles">
        <li class="offer-item" data-key="core">
          <span>코어 페어</span>
          <strong>₩189,000</strong>
        </li>
        <li class="offer-item" data-key="benefit">
          <span>멤버 한정 배송</span>
          <strong>무료</strong>
        </li>
      </ul>
    </article>
    <section class="commerce-card order-stage" data-topic="summary" data-order-state="complete">
      <div class="section-head">
        <h2>결제 완료</h2>
        <span>3단계 중 3단계</span>
      </div>
      <div class="order-metrics">
        <div class="order-metric">
          <span>결제 금액</span>
          <strong>₩189,000</strong>
        </div>
        <div class="order-metric">
          <span>배송 예정</span>
          <strong>오늘 출고</strong>
        </div>
        <div class="order-metric">
          <span>다음 안내</span>
          <strong>알림톡 발송</strong>
        </div>
      </div>
      <p class="note">시연용이라 외부 결제창을 열지 않고, 주문 성공 이후 고객이 보게 되는 상태를 바로 렌더링합니다.</p>
      <button type="button" class="solid" data-action="restart-demo">다시 둘러보기</button>
    </section>
    <article class="commerce-card recommendation-card" data-topic="recommendations">
      <div class="section-head">
        <h2>다음 추천</h2>
        <button type="button" class="ghost section-head__action" data-service-scenario="reorder-keyed">인기순 보기</button>
      </div>
      <ul class="recommendation-list" data-list="recommendations">
        <li class="recommendation-item" data-key="collector">
          <span>컬렉터 팩</span>
          <strong>다음 드롭 추천</strong>
        </li>
        <li class="recommendation-item" data-key="starter">
          <span>스타터 번들</span>
          <strong>선물용 인기</strong>
        </li>
        <li class="recommendation-item" data-key="socks">
          <span>러닝 삭스 세트</span>
          <strong>함께 구매 많음</strong>
        </li>
      </ul>
    </article>
  </section>
</div>
  `.trim()
});

/* -------------------------------------------------------------------------- */
/* 4. helper utils                                                             */
/* -------------------------------------------------------------------------- */

function getElements() {
  return {
    serviceStateEyebrow: document.querySelector(SELECTORS.serviceStateEyebrow),
    serviceStateTitle: document.querySelector(SELECTORS.serviceStateTitle),
    serviceStateBody: document.querySelector(SELECTORS.serviceStateBody),
    serviceModeValue: document.querySelector(SELECTORS.serviceModeValue),
    serviceReasonTitle: document.querySelector(SELECTORS.serviceReasonTitle),
    serviceReasonPatch: document.querySelector(SELECTORS.serviceReasonPatch),
    serviceReasonBody: document.querySelector(SELECTORS.serviceReasonBody),
    serviceImpactAreas: document.querySelector(SELECTORS.serviceImpactAreas),
    serviceImpactSummary: document.querySelector(SELECTORS.serviceImpactSummary),
    serviceReasonBenefit: document.querySelector(SELECTORS.serviceReasonBenefit),
    serviceReasonCompare: document.querySelector(SELECTORS.serviceReasonCompare),
    serviceHomeButton: document.querySelector(SELECTORS.serviceHomeButton),
    openWorkbenchButton: document.querySelector(SELECTORS.openWorkbenchButton),
    closeWorkbenchButton: document.querySelector(SELECTORS.closeWorkbenchButton),
    workbenchShell: document.querySelector(SELECTORS.workbenchShell),
    workbenchBackdrop: document.querySelector(SELECTORS.workbenchBackdrop),
    realDomRoot: document.querySelector(SELECTORS.realDomRoot),
    realDomOverlay: document.querySelector(SELECTORS.realDomOverlay),
    testDomRoot: document.querySelector(SELECTORS.testDomRoot),
    testDomOverlay: document.querySelector(SELECTORS.testDomOverlay),
    sourceEditor: document.querySelector(SELECTORS.sourceEditor),
    patchButton: document.querySelector(SELECTORS.patchButton),
    backButton: document.querySelector(SELECTORS.backButton),
    forwardButton: document.querySelector(SELECTORS.forwardButton),
    resetButton: document.querySelector(SELECTORS.resetButton),
    syncSourceButton: document.querySelector(SELECTORS.syncSourceButton),
    currentStateLabel: document.querySelector(SELECTORS.currentStateLabel),
    currentStateDescription: document.querySelector(SELECTORS.currentStateDescription),
    diffLogPanel: document.querySelector(SELECTORS.diffLogPanel),
    historyPanel: document.querySelector(SELECTORS.historyPanel),
    treePanel: document.querySelector(SELECTORS.treePanel),
    dfsPanel: document.querySelector(SELECTORS.dfsPanel),
    bfsPanel: document.querySelector(SELECTORS.bfsPanel),
    explanationPanel: document.querySelector(SELECTORS.explanationPanel),
    patchSummary: document.querySelector(SELECTORS.patchSummary),
    historyMeta: document.querySelector(SELECTORS.historyMeta),
    patchCountMeta: document.querySelector(SELECTORS.patchCountMeta),
    treeMeta: document.querySelector(SELECTORS.treeMeta),
    depthMeta: document.querySelector(SELECTORS.depthMeta),
    observerMeta: document.querySelector(SELECTORS.observerMeta),
    editorMessage: document.querySelector(SELECTORS.editorMessage),
    treeNodeTemplate: document.querySelector(SELECTORS.treeNodeTemplate),
    scenarioPanel: document.querySelector(SELECTORS.scenarioPanel),
    patchTimelinePanel: document.querySelector(SELECTORS.patchTimelinePanel),
    playbackToggleButton: document.querySelector(SELECTORS.playbackToggleButton),
    playbackNextButton: document.querySelector(SELECTORS.playbackNextButton),
    playbackResetButton: document.querySelector(SELECTORS.playbackResetButton),
    playbackStatus: document.querySelector(SELECTORS.playbackStatus),
    performancePanel: document.querySelector(SELECTORS.performancePanel),
    inspectorPanel: document.querySelector(SELECTORS.inspectorPanel),
    demoBriefingPanel: document.querySelector(SELECTORS.demoBriefingPanel),
    demoSignalPanel: document.querySelector(SELECTORS.demoSignalPanel),
    pipelinePanel: document.querySelector(SELECTORS.pipelinePanel),
    demoTourStatus: document.querySelector(SELECTORS.demoTourStatus),
    demoTourButton: document.querySelector(SELECTORS.demoTourButton),
    demoFocusButton: document.querySelector(SELECTORS.demoFocusButton)
  };
}

function createRootContainer() {
  return {
    type: "element",
    tag: "div",
    attrs: {
      "data-virtual-root": "true"
    },
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

function getExplicitKey(attrs = {}) {
  return attrs["data-key"] || attrs.key || attrs.id || null;
}

function getVNodeLookupKey(vNode, index) {
  if (!vNode || vNode.type !== "element") {
    return `__index_${index}`;
  }

  return getExplicitKey(vNode.attrs || {}) || `__index_${index}`;
}

function serializeHTML(node) {
  return node ? node.innerHTML.trim() : "";
}

function sanitizeText(text) {
  return typeof text === "string" ? text.replace(/\s+/g, " ").trim() : "";
}

function escapeHTML(value) {
  return String(value)
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;");
}

function cloneValue(value) {
  return value ? JSON.parse(JSON.stringify(value)) : value;
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

  const attrCount = Object.keys(vNode.attrs || {}).length;
  return `${vNode.tag} | attrs:${attrCount} | children:${(vNode.children || []).length}`;
}

function countNodes(vNode) {
  if (!vNode) {
    return 0;
  }

  return 1 + (vNode.children || []).reduce((total, child) => total + countNodes(child), 0);
}

function countRenderableNodes(vNode) {
  return Math.max(0, countNodes(vNode) - 1);
}

function calculateMaxDepth(vNode) {
  if (!vNode) {
    return 0;
  }

  if (!vNode.children || vNode.children.length === 0) {
    return vNode.depth || 0;
  }

  return Math.max(...vNode.children.map((child) => calculateMaxDepth(child)));
}

function setStatus(label, description) {
  state.ui.currentStateLabel.textContent = label;
  state.ui.currentStateDescription.textContent = description;
}

function safelyParseHTML(html) {
  const template = document.createElement("template");

  try {
    template.innerHTML = html && html.trim() ? html.trim() : "";
  } catch (error) {
    return {
      fragment: template.content,
      error
    };
  }

  return {
    fragment: template.content,
    error: null
  };
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

function getPathDepth(path) {
  return String(path).split("-").length;
}

function pathToSegments(path) {
  return String(path)
    .split("-")
    .slice(1)
    .map((segment) => Number(segment))
    .filter((segment) => Number.isInteger(segment));
}

function formatPatchDetail(patch) {
  switch (patch.type) {
    case PATCH_TYPES.CREATE:
      return `새 노드 ${getNodeDescriptor(patch.node)} 생성`;
    case PATCH_TYPES.REMOVE:
      return `기존 노드 ${getNodeDescriptor(patch.node)} 제거`;
    case PATCH_TYPES.REPLACE:
      return `${getNodeDescriptor(patch.oldNode)} -> ${getNodeDescriptor(patch.newNode)} 교체`;
    case PATCH_TYPES.TEXT:
      return `"${sanitizeText(patch.oldText)}" -> "${sanitizeText(patch.newText)}"`;
    case PATCH_TYPES.ATTR_SET:
      return `속성 ${patch.name} = "${patch.value}" 설정`;
    case PATCH_TYPES.ATTR_REMOVE:
      return `속성 ${patch.name} 제거`;
    case PATCH_TYPES.REORDER_CHILDREN:
      return `형제 노드 순서 변경 [${patch.order.join(", ")}]`;
    default:
      return "변경 내용 없음";
  }
}

function createPatchCountMap() {
  return {
    [PATCH_TYPES.CREATE]: 0,
    [PATCH_TYPES.REMOVE]: 0,
    [PATCH_TYPES.REPLACE]: 0,
    [PATCH_TYPES.TEXT]: 0,
    [PATCH_TYPES.ATTR_SET]: 0,
    [PATCH_TYPES.ATTR_REMOVE]: 0,
    [PATCH_TYPES.REORDER_CHILDREN]: 0
  };
}

function countPatchTypes(patches) {
  return patches.reduce((counts, patch) => {
    counts[patch.type] = (counts[patch.type] || 0) + 1;
    return counts;
  }, createPatchCountMap());
}

function createBaselineComparisonStats(vNode) {
  const nodes = countRenderableNodes(vNode);

  return {
    beforeNodes: nodes,
    afterNodes: nodes,
    fullRenderOps: nodes,
    patchOps: 0,
    savedOps: 0,
    efficiencyRate: 0,
    patchCounts: createPatchCountMap(),
    mode: "baseline"
  };
}

function createComparisonStats(previousVNode, nextVNode, patches) {
  const beforeNodes = countRenderableNodes(previousVNode);
  const afterNodes = countRenderableNodes(nextVNode);
  const fullRenderOps = Math.max(afterNodes, beforeNodes);
  const patchOps = patches.length;
  const savedOps = Math.max(0, fullRenderOps - patchOps);
  const efficiencyRate = fullRenderOps ? Math.round((savedOps / fullRenderOps) * 100) : 0;

  return {
    beforeNodes,
    afterNodes,
    fullRenderOps,
    patchOps,
    savedOps,
    efficiencyRate,
    patchCounts: countPatchTypes(patches),
    mode: patchOps === 0 ? "noop" : "patch"
  };
}

function getPatchPriorityScore(patchType) {
  const priority = {
    [PATCH_TYPES.REPLACE]: 70,
    [PATCH_TYPES.REORDER_CHILDREN]: 60,
    [PATCH_TYPES.CREATE]: 50,
    [PATCH_TYPES.REMOVE]: 40,
    [PATCH_TYPES.TEXT]: 30,
    [PATCH_TYPES.ATTR_SET]: 20,
    [PATCH_TYPES.ATTR_REMOVE]: 10
  };

  return priority[patchType] || 0;
}

function getPrimaryPatchIndex(patches = state.patches) {
  if (!patches.length) {
    return null;
  }

  return patches.reduce((bestIndex, patch, index) => {
    const currentScore = getPatchPriorityScore(patch.type);
    const bestScore = getPatchPriorityScore(patches[bestIndex].type);

    if (currentScore > bestScore) {
      return index;
    }

    return bestIndex;
  }, 0);
}

function getDefaultSelectionPath(vNode) {
  return vNode?.children?.[0]?.path || "0";
}

function getNearestExistingPath(vNode, candidatePaths = []) {
  const queue = Array.isArray(candidatePaths) ? [...candidatePaths] : [candidatePaths];

  while (queue.length) {
    let currentPath = queue.shift();
    if (!currentPath) {
      continue;
    }

    while (currentPath) {
      if (findVNodeByPath(vNode, currentPath)) {
        return currentPath;
      }

      if (currentPath === "0") {
        break;
      }

      currentPath = currentPath.split("-").slice(0, -1).join("-") || "0";
    }
  }

  return getDefaultSelectionPath(vNode);
}

function getPatchPrimaryPath(patch, vNodeRoot) {
  if (!patch) {
    return getDefaultSelectionPath(vNodeRoot);
  }

  if (patch.type === PATCH_TYPES.REMOVE) {
    return getNearestExistingPath(vNodeRoot, [patch.parentPath, patch.path]);
  }

  return getNearestExistingPath(vNodeRoot, [patch.path, patch.parentPath]);
}

function clearPlaybackTimer() {
  if (state.playbackTimer) {
    window.clearInterval(state.playbackTimer);
    state.playbackTimer = null;
  }
}

function clearDemoTourTimer() {
  if (state.demoTourTimer) {
    window.clearTimeout(state.demoTourTimer);
    state.demoTourTimer = null;
  }
}

function createEmptyState(message) {
  return `<div class="empty-state">${escapeHTML(message)}</div>`;
}

function findScenarioById(scenarioId) {
  return SCENARIOS.find((scenario) => scenario.id === scenarioId) || null;
}

function getPatchMetaLabel(patchType) {
  const labels = {
    [PATCH_TYPES.CREATE]: "생성",
    [PATCH_TYPES.REMOVE]: "삭제",
    [PATCH_TYPES.REPLACE]: "교체",
    [PATCH_TYPES.TEXT]: "텍스트",
    [PATCH_TYPES.ATTR_SET]: "속성 설정",
    [PATCH_TYPES.ATTR_REMOVE]: "속성 제거",
    [PATCH_TYPES.REORDER_CHILDREN]: "순서 변경"
  };

  return labels[patchType] || patchType;
}

function getPatchFocusDescriptors() {
  const descriptors = [];
  const selectionPath = getNearestExistingPath(state.realVNode, [state.selectedPath]);
  const focusPatchIndex = state.selectedPatchIndex != null ? state.selectedPatchIndex : getPrimaryPatchIndex(state.patches);
  const focusPatch = focusPatchIndex != null ? state.patches[focusPatchIndex] : null;

  if (selectionPath) {
    descriptors.push({
      path: selectionPath,
      label: `선택 노드 · ${selectionPath}`,
      tone: "selection"
    });
  }

  if (focusPatch) {
    const patch = focusPatch;
    const patchPath = getPatchPrimaryPath(patch, state.realVNode);
    descriptors.push({
      path: patchPath,
      label: `${patch.type} · ${patchPath}`,
      tone: "patch"
    });
  }

  return descriptors;
}

function getActualPatchTypes(patches = state.patches) {
  return patches.reduce((types, patch) => {
    if (!types.includes(patch.type)) {
      types.push(patch.type);
    }

    return types;
  }, []);
}

function getScenarioValidation(scenario, patches = state.patches) {
  if (!scenario) {
    return null;
  }

  const actual = getActualPatchTypes(patches);
  const expected = [...scenario.expectedTypes];
  const missing = expected.filter((type) => !actual.includes(type));
  const unexpected = actual.filter((type) => !expected.includes(type));
  const matched = missing.length === 0 && unexpected.length === 0 && actual.length === expected.length;

  return {
    expected,
    actual,
    missing,
    unexpected,
    matched
  };
}

function getDemoContext() {
  const scenario = findScenarioById(state.activeScenarioId);
  const stats = state.comparisonStats || createBaselineComparisonStats(state.realVNode);
  const fallbackPatchIndex = getPrimaryPatchIndex(state.patches);
  const focusPatchIndex = state.selectedPatchIndex != null ? state.selectedPatchIndex : fallbackPatchIndex;
  const focusPatch = focusPatchIndex != null ? state.patches[focusPatchIndex] : null;
  const focusPath = focusPatch ? getPatchPrimaryPath(focusPatch, state.realVNode) : getDefaultSelectionPath(state.realVNode);
  const focusVNode = findVNodeByPath(state.realVNode, focusPath);
  const validation = getScenarioValidation(scenario, state.patches);
  const actualPatchTypes = getActualPatchTypes(state.patches);

  return {
    scenario,
    stats,
    focusPatchIndex,
    focusPatch,
    focusPath,
    focusVNode,
    validation,
    actualPatchTypes
  };
}

/* -------------------------------------------------------------------------- */
/* 5. virtual dom utils                                                        */
/* -------------------------------------------------------------------------- */

/*
  ???⑥닔????븷:
  ?ㅼ젣 DOM ?몃뱶瑜?Virtual DOM 媛앹껜 ?몃━濡?蹂?섑븳??
  ?낅젰:
  DOM Node, ?꾩옱 path 臾몄옄?? depth ?レ옄
  異쒕젰:
  Virtual DOM 媛앹껜 ?먮뒗 null
  ???꾩슂?쒖?:
  釉뚮씪?곗?媛 媛吏??ㅼ젣 DOM??鍮꾧탳 媛?ν븳 硫붾え由????몃━ 援ъ“濡?諛붽퓭??diff ?뚭퀬由ъ쬁???곸슜?????덈떎.
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
  ???⑥닔????븷:
  DOM 而⑦뀒?대꼫???먯떇?ㅼ쓣 ?쎌뼱??猷⑦듃 ?섑띁 Virtual DOM?쇰줈 蹂?섑븳??
  ?낅젰:
  DOM Element 而⑦뀒?대꼫
  異쒕젰:
  猷⑦듃 Virtual DOM 媛앹껜
  ???꾩슂?쒖?:
  ?ㅼ젣 ?곸뿭怨??뚯뒪???곸뿭 紐⑤몢 ?щ윭 猷⑦듃 ?몃뱶瑜?媛吏????덉쑝誘濡?鍮꾧탳瑜??⑥씪 ?몃━ 愿?먯쑝濡??⑥닚?뷀븳??
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

/*
  ???⑥닔????븷:
  Virtual DOM 媛앹껜 ?섎굹瑜??ㅼ젣 DOM ?몃뱶濡??앹꽦?쒕떎.
  ?낅젰:
  Virtual DOM 媛앹껜
  異쒕젰:
  DOM Node
  ???꾩슂?쒖?:
  CREATE, REPLACE, REORDER_CHILDREN 媛숈? patch瑜??곸슜????Virtual DOM???ㅼ떆 ?ㅼ젣 DOM?쇰줈 留뚮뱾?댁빞 ?쒕떎.
*/
function createDOMFromVNode(vNode) {
  if (!vNode) {
    return document.createTextNode("");
  }

  if (vNode.type === "text") {
    const textNode = document.createTextNode(vNode.text || "");
    textNode.__vdomMeta = {
      type: vNode.type,
      tag: vNode.tag,
      key: vNode.key,
      path: vNode.path
    };
    return textNode;
  }

  const element = document.createElement(vNode.tag);
  const attrs = vNode.attrs || {};

  Object.entries(attrs).forEach(([name, value]) => {
    if (value === true) {
      element.setAttribute(name, "");
    } else if (value !== false && value != null) {
      element.setAttribute(name, String(value));
    }
  });

  element.__vdomMeta = {
    type: vNode.type,
    tag: vNode.tag,
    key: vNode.key,
    path: vNode.path
  };

  (vNode.children || []).forEach((child) => {
    element.appendChild(createDOMFromVNode(child));
  });

  return element;
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
/* 6. traversal utils                                                          */
/* -------------------------------------------------------------------------- */

/*
  ???⑥닔????븷:
  Virtual DOM ?몃━瑜?源딆씠 ?곗꽑 ?먯깋?쇰줈 ?쒗쉶?쒕떎.
  ?낅젰:
  猷⑦듃 Virtual DOM
  異쒕젰:
  諛⑸Ц ?쒖꽌 諛곗뿴
  ???꾩슂?쒖?:
  ?몃━ 援ъ“媛 ?ㅼ젣濡?depth 湲곕컲?쇰줈 ?먯깋?쒕떎???먯쓣 ?쒓컖?곸쑝濡??ㅻ챸?섍퀬, DFS 媛쒕뀗???숈뒿 ?ㅼ썙?쒖? ?곌껐?섍린 ?꾪빐 ?꾩슂?섎떎.
*/
function traverseDFS(root) {
  const order = [];

  function visit(node) {
    if (!node) {
      return;
    }

    order.push({
      path: node.path,
      label: getNodeDescriptor(node),
      depth: node.depth
    });

    (node.children || []).forEach((child) => visit(child));
  }

  visit(root);
  return order;
}

/*
  ???⑥닔????븷:
  Virtual DOM ?몃━瑜??덈퉬 ?곗꽑 ?먯깋?쇰줈 ?쒗쉶?쒕떎.
  ?낅젰:
  猷⑦듃 Virtual DOM
  異쒕젰:
  諛⑸Ц ?쒖꽌 諛곗뿴
  ???꾩슂?쒖?:
  ??湲곕컲 BFS媛 ?덈꺼 ?쒗쉶?쇰뒗 ?먯쓣 蹂댁뿬二쇨퀬, UI?먯꽌 depth蹂?援ъ“瑜??댄빐?섍린 ?쎄쾶 留뚮뱾湲??꾪빐 ?꾩슂?섎떎.
*/
function traverseBFS(root) {
  if (!root) {
    return [];
  }

  const order = [];
  const queue = [root];

  while (queue.length) {
    const current = queue.shift();
    order.push({
      path: current.path,
      label: getNodeDescriptor(current),
      depth: current.depth
    });

    (current.children || []).forEach((child) => queue.push(child));
  }

  return order;
}

/* -------------------------------------------------------------------------- */
/* 7. diff engine                                                              */
/* -------------------------------------------------------------------------- */

function diffAttrs(oldAttrs = {}, newAttrs = {}, path, patches) {
  Object.keys(newAttrs).forEach((name) => {
    if (oldAttrs[name] !== newAttrs[name]) {
      patches.push({
        type: PATCH_TYPES.ATTR_SET,
        path,
        name,
        value: newAttrs[name]
      });
    }
  });

  Object.keys(oldAttrs).forEach((name) => {
    if (!(name in newAttrs)) {
      patches.push({
        type: PATCH_TYPES.ATTR_REMOVE,
        path,
        name
      });
    }
  });
}

function createChildKeyMap(children) {
  const map = new Map();

  children.forEach((child, index) => {
    const key = getVNodeLookupKey(child, index);
    map.set(key, index);
  });

  return map;
}

/*
  ???⑥닔????븷:
  ???먯떇 諛곗뿴??鍮꾧탳???앹꽦/??젣/?쒖꽌 蹂寃??섏쐞 diff瑜?怨꾩궛?쒕떎.
  ?낅젰:
  ?댁쟾 ?먯떇 諛곗뿴, ???먯떇 諛곗뿴, 遺紐?path, patch 諛곗뿴
  異쒕젰:
  patch 諛곗뿴???먯떇 愿??patch瑜?異붽?
  ???꾩슂?쒖?:
  Virtual DOM diff?먯꽌 媛??留롮? 蹂?붽? ?먯떇 由ъ뒪?몄뿉???쇱뼱?섎?濡?蹂꾨룄 ?④퀎濡?遺꾨━?댁빞 ?ㅻ챸怨??좎?蹂댁닔媛 ?ъ썙吏꾨떎.
*/
function diffChildren(oldChildren, newChildren, parentPath, patches) {
  const oldKeyMap = createChildKeyMap(oldChildren);
  const newKeyMap = createChildKeyMap(newChildren);
  const order = [];

  newChildren.forEach((newChild, index) => {
    const lookupKey = getVNodeLookupKey(newChild, index);
    order.push(lookupKey);

    if (!oldKeyMap.has(lookupKey)) {
      patches.push({
        type: PATCH_TYPES.CREATE,
        path: `${parentPath}-${index}`,
        index,
        parentPath,
        node: newChild
      });
      return;
    }

    const oldIndex = oldKeyMap.get(lookupKey);
    diff(oldChildren[oldIndex], newChild, `${parentPath}-${index}`, patches);
  });

  oldChildren.forEach((oldChild, index) => {
    const lookupKey = getVNodeLookupKey(oldChild, index);
    if (!newKeyMap.has(lookupKey)) {
      patches.push({
        type: PATCH_TYPES.REMOVE,
        path: oldChild.path || `${parentPath}-${index}`,
        index,
        parentPath,
        node: oldChild
      });
    }
  });

  const oldOrder = oldChildren.map((child, index) => getVNodeLookupKey(child, index));
  const hasSameKeySet =
    oldOrder.length === order.length &&
    oldOrder.every((lookupKey) => newKeyMap.has(lookupKey)) &&
    order.every((lookupKey) => oldKeyMap.has(lookupKey));

  if (hasSameKeySet && oldOrder.join("|") !== order.join("|")) {
    patches.push({
      type: PATCH_TYPES.REORDER_CHILDREN,
      path: parentPath,
      parentPath,
      order
    });
  }
}

/*
  ???⑥닔????븷:
  ?댁쟾 Virtual DOM怨??덈줈??Virtual DOM??鍮꾧탳??patch 紐⑸줉??留뚮뱺??
  ?낅젰:
  ?댁쟾 Virtual DOM, ??Virtual DOM, ?꾩옱 path, patch 諛곗뿴
  異쒕젰:
  patch 諛곗뿴
  ???꾩슂?쒖?:
  蹂寃쎌젏??硫붾え由??곸뿉??癒쇱? 怨꾩궛?댁빞 ?ㅼ젣 DOM?먮뒗 ?꾩슂??理쒖냼 ?묒뾽留??곸슜?????덈떎.
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
    patches.push({
      type: PATCH_TYPES.REPLACE,
      path,
      oldNode,
      newNode
    });
    return patches;
  }

  if (oldNode.type === "text" && newNode.type === "text") {
    if (sanitizeText(oldNode.text) !== sanitizeText(newNode.text)) {
      patches.push({
        type: PATCH_TYPES.TEXT,
        path,
        oldText: oldNode.text,
        newText: newNode.text
      });
    }

    return patches;
  }

  diffAttrs(oldNode.attrs, newNode.attrs, path, patches);
  diffChildren(oldNode.children || [], newNode.children || [], path, patches);
  return patches;
}

/* -------------------------------------------------------------------------- */
/* 8. patch engine                                                             */
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

  const newDom = createDOMFromVNode(patch.node);
  const comparableChildren = getComparableChildNodes(parent);
  const referenceNode = comparableChildren[patch.index] || null;
  parent.insertBefore(newDom, referenceNode);
}

function applyRemovePatch(root, patch) {
  const node = getDomNodeByPath(root, patch.path);
  if (node && node.parentNode) {
    node.parentNode.removeChild(node);
  }
}

function applyReplacePatch(root, patch) {
  const node = getDomNodeByPath(root, patch.path);
  if (node && node.parentNode) {
    node.parentNode.replaceChild(createDOMFromVNode(patch.newNode), node);
  }
}

function applyTextPatch(root, patch) {
  const node = getDomNodeByPath(root, patch.path);
  if (node) {
    node.textContent = patch.newText;
  }
}

function applyAttrSetPatch(root, patch) {
  const node = getDomNodeByPath(root, patch.path);
  if (!node || node.nodeType !== NODE_TYPE.ELEMENT) {
    return;
  }

  if (patch.value === true) {
    node.setAttribute(patch.name, "");
  } else {
    node.setAttribute(patch.name, String(patch.value));
  }
}

function applyAttrRemovePatch(root, patch) {
  const node = getDomNodeByPath(root, patch.path);
  if (node && node.nodeType === NODE_TYPE.ELEMENT) {
    node.removeAttribute(patch.name);
  }
}

function applyReorderPatch(root, patch, oldVNodeRoot, newVNodeRoot) {
  const parent = getDomNodeByPath(root, patch.path);
  const oldParentVNode = findVNodeByPath(oldVNodeRoot, patch.path);
  const parentVNode = findVNodeByPath(newVNodeRoot, patch.path);

  if (!parent || !parentVNode || !oldParentVNode) {
    return;
  }

  const currentChildren = getComparableChildNodes(parent);
  const keyedNodeMap = new Map();

  currentChildren.forEach((childNode, index) => {
    const childVNode = oldParentVNode.children[index];
    const lookupKey = getVNodeLookupKey(childVNode, index);
    keyedNodeMap.set(lookupKey, childNode);
  });

  patch.order.forEach((lookupKey) => {
    const existingNode = keyedNodeMap.get(lookupKey);
    if (existingNode) {
      parent.appendChild(existingNode);
    }
  });
}

/*
  ???⑥닔????븷:
  patch 諛곗뿴???ㅼ젣 DOM???쒖꽌 ?덇쾶 ?곸슜?쒕떎.
  ?낅젰:
  ?ㅼ젣 DOM 猷⑦듃, patch 諛곗뿴, ??Virtual DOM 猷⑦듃
  異쒕젰:
  ?놁쓬. ?ㅼ젣 DOM??吏곸젒 媛깆떊?쒕떎.
  ???꾩슂?쒖?:
  diff 寃곌낵瑜??ㅼ젣 UI 蹂?붾줈 ?곌껐?섎뒗 ?④퀎?대ŉ, ?꾩껜 ?щ젋?붾쭅 ???理쒖냼 蹂寃??곸슜 ?꾨왂???듭떖?대떎.
*/
function applyPatches(root, patches, oldVNodeRoot, newVNodeRoot) {
  const comparePathOrder = (pathA, pathB) => {
    const segmentsA = pathToSegments(pathA);
    const segmentsB = pathToSegments(pathB);
    const maxLength = Math.max(segmentsA.length, segmentsB.length);

    for (let index = 0; index < maxLength; index += 1) {
      const segmentA = segmentsA[index] ?? -1;
      const segmentB = segmentsB[index] ?? -1;

      if (segmentA !== segmentB) {
        return segmentA - segmentB;
      }
    }

    return segmentsA.length - segmentsB.length;
  };

  const removalPatches = patches
    .filter((patch) => patch.type === PATCH_TYPES.REMOVE)
    .sort((a, b) => {
      const depthGap = getPathDepth(b.path) - getPathDepth(a.path);
      if (depthGap !== 0) {
        return depthGap;
      }

      return comparePathOrder(b.path, a.path);
    });

  const creationPatches = patches
    .filter((patch) => patch.type === PATCH_TYPES.CREATE)
    .sort((a, b) => {
      const depthGap = getPathDepth(a.path) - getPathDepth(b.path);
      if (depthGap !== 0) {
        return depthGap;
      }

      return comparePathOrder(a.path, b.path);
    });

  const updatePatches = patches.filter(
    (patch) => ![PATCH_TYPES.REMOVE, PATCH_TYPES.CREATE, PATCH_TYPES.REORDER_CHILDREN].includes(patch.type)
  );

  const reorderPatches = patches.filter((patch) => patch.type === PATCH_TYPES.REORDER_CHILDREN);

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

  removalPatches.forEach((patch) => applyRemovePatch(root, patch));
  creationPatches.forEach((patch) => applyCreatePatch(root, patch));
  reorderPatches.forEach((patch) => applyReorderPatch(root, patch, oldVNodeRoot, newVNodeRoot));
}

/* -------------------------------------------------------------------------- */
/* 9. history manager                                                          */
/* -------------------------------------------------------------------------- */

function serializeVNodeChildrenToHTML(vNode) {
  const wrapper = document.createElement("div");
  (vNode.children || []).forEach((child) => {
    wrapper.appendChild(createDOMFromVNode(child));
  });
  return wrapper.innerHTML;
}

function createHistorySnapshot(label, description, vNode, patches, comparisonStats, activeScenarioId) {
  return {
    id: Date.now() + Math.random(),
    label,
    description,
    vNode: cloneValue(vNode),
    html: serializeVNodeChildrenToHTML(vNode),
    patches: cloneValue(patches),
    comparisonStats: cloneValue(comparisonStats),
    activeScenarioId: activeScenarioId || null,
    timestamp: new Date().toLocaleTimeString("ko-KR", {
      hour: "2-digit",
      minute: "2-digit",
      second: "2-digit"
    })
  };
}

/*
  ???⑥닔????븷:
  ?꾩옱 Virtual DOM ?곹깭瑜?history 諛곗뿴??push?섍퀬 currentIndex瑜?媛깆떊?쒕떎.
  ?낅젰:
  ?곹깭 ?쇰꺼, ?곹깭 ?ㅻ챸, Virtual DOM, patch 諛곗뿴
  異쒕젰:
  ?놁쓬. state.history? state.currentHistoryIndex媛 媛깆떊?쒕떎.
  ???꾩슂?쒖?:
  patch ?댄썑 ?댁쟾 ?곹깭濡??뚯븘媛嫄곕굹 ?욎쑝濡??대룞?섎젮硫??곹깭 ?ㅽ깮???꾨땲??諛곗뿴 + ?꾩옱 ?몃뜳??援ъ“媛 媛???⑥닚?섍퀬 ?ㅻ챸?섍린 ?쎈떎.
*/
function pushHistory(label, description, vNode, patches) {
  if (state.currentHistoryIndex < state.history.length - 1) {
    state.history = state.history.slice(0, state.currentHistoryIndex + 1);
  }

  state.history.push(
    createHistorySnapshot(label, description, vNode, patches, state.comparisonStats, state.activeScenarioId)
  );
  state.currentHistoryIndex = state.history.length - 1;
}

function restoreSelectionDefaults() {
  if (state.patches.length) {
    const primaryPatchIndex = getPrimaryPatchIndex(state.patches);
    state.selectedPatchIndex = primaryPatchIndex;
    state.playbackIndex = null;
    state.selectedPath = getPatchPrimaryPath(state.patches[primaryPatchIndex], state.realVNode);
    return;
  }

  state.selectedPatchIndex = null;
  state.playbackIndex = null;
  state.selectedPath = getDefaultSelectionPath(state.realVNode);
}

function restoreSnapshot(snapshot) {
  if (!snapshot) {
    return;
  }

  clearPlaybackTimer();
  clearDemoTourTimer();
  state.playbackPlaying = false;
  state.demoTourPlaying = false;
  state.demoTourIndex = null;
  state.demoTourCompleted = false;
  state.realVNode = cloneValue(snapshot.vNode);
  state.testVNode = cloneValue(snapshot.vNode);
  state.patches = cloneValue(snapshot.patches || []);
  state.comparisonStats = cloneValue(snapshot.comparisonStats || createBaselineComparisonStats(snapshot.vNode));
  state.activeScenarioId = snapshot.activeScenarioId || null;

  renderVNodeToRoot(state.ui.realDomRoot, state.realVNode);
  renderVNodeToRoot(state.ui.testDomRoot, state.testVNode);
  syncSourceEditorFromTest();
  restoreSelectionDefaults();

  renderAllPanels();
  setStatus(snapshot.label, snapshot.description);
}

/*
  ???⑥닔????븷:
  history ?몃뜳?ㅻ? ?섎굹 ?ㅻ줈 ?대룞?쒗궎怨??대떦 ?곹깭瑜?蹂듭썝?쒕떎.
  ?낅젰:
  ?놁쓬
  異쒕젰:
  ?놁쓬
  ???꾩슂?쒖?:
  patch 湲곕컲 ?곹깭 蹂?붽? ?꾩쟻?????댁쟾 ?몃━ 援ъ“? ?쒗쉶 寃곌낵源뚯? ?④퍡 ?섎룎由щ뒗 湲곕뒫???꾩슂?섎떎.
*/
function goBack() {
  if (state.currentHistoryIndex <= 0) {
    return;
  }

  state.currentHistoryIndex -= 1;
  restoreSnapshot(state.history[state.currentHistoryIndex]);
}

/*
  ???⑥닔????븷:
  history ?몃뜳?ㅻ? ?섎굹 ?욎쑝濡??대룞?쒗궎怨??대떦 ?곹깭瑜?蹂듭썝?쒕떎.
  ?낅젰:
  ?놁쓬
  異쒕젰:
  ?놁쓬
  ???꾩슂?쒖?:
  諛곗뿴 湲곕컲 history ?먯깋?먯꽌 redo ?깃꺽???곹깭 ?대룞??吏?먰븯湲??꾪빐 ?꾩슂?섎떎.
*/
function goForward() {
  if (state.currentHistoryIndex >= state.history.length - 1) {
    return;
  }

  state.currentHistoryIndex += 1;
  restoreSnapshot(state.history[state.currentHistoryIndex]);
}

/* -------------------------------------------------------------------------- */
/* 10. UI renderer                                                             */
/* -------------------------------------------------------------------------- */

function renderVNodeToRoot(root, vNode) {
  root.innerHTML = "";
  (vNode.children || []).forEach((child) => {
    root.appendChild(createDOMFromVNode(child));
  });
}

function syncSourceEditorFromTest() {
  state.ui.sourceEditor.value = serializeHTML(state.ui.testDomRoot);
}

function syncTestFromSourceEditor() {
  const rawHtml = state.ui.sourceEditor.value.trim();
  const html = rawHtml || "";
  const error = renderHTMLIntoTarget(state.ui.testDomRoot, html);

  if (error) {
    state.ui.editorMessage.textContent = `${UI_TEXT.invalidHtml} (${error.message})`;
    return;
  }

  if (!rawHtml) {
    state.ui.editorMessage.textContent = UI_TEXT.emptyTest;
    return;
  }

  state.ui.editorMessage.textContent = UI_TEXT.patchReady;
}

function renderDemoBriefingPanel() {
  const panel = state.ui.demoBriefingPanel;
  const { scenario, stats, focusPatch, focusPath, focusVNode, validation, actualPatchTypes } = getDemoContext();

  if (!focusPatch) {
    panel.innerHTML = `
      <div class="demo-copy">
        <h3 class="demo-copy__headline">서비스 화면은 준비됐고, 이제 실제 사용자 이벤트를 눌러 Virtual DOM 엔진이 어떻게 반응하는지 보여줄 수 있습니다.</h3>
        <p class="demo-copy__body">
          지금 보이는 화면은 FlashDrop Live의 기본 상태입니다. 멤버 입장, 번들 담기, 주문서 열기, 추천순 보기 같은 이벤트를 실행하면
          서비스 화면 변화와 내부 patch 결과가 함께 갱신됩니다.
        </p>
        <p class="demo-copy__aside">
          시연에서는 먼저 서비스가 어떻게 바뀌는지 보여주고, 그 다음에 그 변화가 Virtual DOM diff와 patch로 어떻게 계산됐는지 연결해 설명하면 됩니다.
        </p>
      </div>
      <div class="demo-kpi-grid">
        <article class="demo-kpi">
          <span class="demo-kpi__label">현재 모드</span>
          <strong>기본 상태</strong>
          <span class="demo-kpi__caption">아직 patch가 적용되지 않은 기준 화면</span>
        </article>
        <article class="demo-kpi">
          <span class="demo-kpi__label">렌더 노드 수</span>
          <strong>${stats.beforeNodes}</strong>
          <span class="demo-kpi__caption">현재 비교 대상이 되는 실제 노드 수</span>
        </article>
        <article class="demo-kpi">
          <span class="demo-kpi__label">권장 액션</span>
          <strong>서비스 이벤트 실행</strong>
          <span class="demo-kpi__caption">멤버 입장이나 번들 담기부터 시작</span>
        </article>
      </div>
      <div class="demo-chip-row">
        <span class="demo-tag">서비스 기본 상태 준비 완료</span>
        <span class="demo-tag">실제 화면과 테스트 화면 동기화 완료</span>
      </div>
      <div class="demo-proof">
        <span class="demo-proof__label">이 화면은 이렇게 설명하면 됩니다</span>
        <ol class="demo-proof__list">
          <li>먼저 사용자가 보는 서비스 변화부터 설명합니다.</li>
          <li>그 다음 어떤 상태 변경이 일어났는지 한 문장으로 요약합니다.</li>
          <li>마지막으로 어떤 patch가 그 변화를 만들었는지 연결합니다.</li>
        </ol>
      </div>
    `;
    return;
  }

  const headline = scenario?.demoHeadline || `${focusPatch.type} patch가 실제 DOM에 반영되었습니다.`;
  const body = scenario
    ? `${scenario.description} 현재 핵심 변화는 ${focusPatch.type} patch이고, ${formatPatchDetail(focusPatch)}`
    : `${formatPatchDetail(focusPatch)}.`;
  const aside =
    scenario?.businessValue ||
    `전체 재렌더링 대신 ${stats.patchOps}개 patch만 적용해서 ${stats.savedOps}개의 DOM 작업을 줄였습니다.`;
  const validationCopy = validation?.matched
    ? `시나리오가 의도한 patch 조합만 발생했습니다. actual: ${actualPatchTypes.join(", ")}`
    : validation
      ? `기대 patch와 다른 결과가 있습니다. missing: ${validation.missing.join(", ") || "-"}, unexpected: ${validation.unexpected.join(", ") || "-"}`
      : `수동 patch 실행이므로 현재 핵심 patch는 ${focusPatch.type}입니다.`;

  panel.innerHTML = `
    <div class="demo-copy">
      <h3 class="demo-copy__headline">${escapeHTML(headline)}</h3>
      <p class="demo-copy__body">${escapeHTML(body)}</p>
      <p class="demo-copy__aside">${escapeHTML(aside)}</p>
    </div>
    <div class="demo-kpi-grid">
      <article class="demo-kpi">
        <span class="demo-kpi__label">핵심 patch</span>
        <strong>${escapeHTML(focusPatch.type)}</strong>
        <span class="demo-kpi__caption">지금 브리핑이 설명하는 변화</span>
      </article>
      <article class="demo-kpi">
        <span class="demo-kpi__label">Patch 수</span>
        <strong>${stats.patchOps}</strong>
        <span class="demo-kpi__caption">실제로 수행한 DOM 작업 수</span>
      </article>
      <article class="demo-kpi">
        <span class="demo-kpi__label">대상 노드</span>
        <strong>${escapeHTML(focusVNode ? getNodeDescriptor(focusVNode) : focusPatch.path)}</strong>
        <span class="demo-kpi__caption">${escapeHTML(focusPath)}</span>
      </article>
    </div>
    <div class="demo-chip-row">
      <span class="demo-tag">${escapeHTML(scenario?.title || "수동 patch")}</span>
      <span class="demo-tag">DOM 작업 ${stats.efficiencyRate}% 절감</span>
      <span class="demo-tag">Path ${escapeHTML(focusPath)}</span>
    </div>
    <div class="demo-proof">
      <span class="demo-proof__label">시연 멘트 포인트</span>
      <ol class="demo-proof__list">
        <li>이 이벤트로 새 Virtual DOM을 만들고 이전 트리와 비교했습니다.</li>
        <li>${escapeHTML(validationCopy)}</li>
        <li>${escapeHTML(`${focusPath}의 ${focusVNode ? getNodeDescriptor(focusVNode) : focusPatch.path}가 이번 서비스 이벤트에서 실제로 바뀐 핵심 UI입니다.`)}</li>
      </ol>
    </div>
  `;
}

function renderDemoSignalPanel() {
  const panel = state.ui.demoSignalPanel;
  const { scenario, stats, focusPatch, focusPath, focusVNode, validation, actualPatchTypes } = getDemoContext();

  if (!focusPatch) {
    panel.innerHTML = `
      <article class="signal-card signal-card--primary">
        <span class="signal-card__label">현재 모드</span>
        <strong>기본 상태 준비 완료</strong>
        <p>실제 DOM과 테스트 DOM이 같은 초기 상태입니다.</p>
      </article>
      <article class="signal-card signal-card--good">
        <span class="signal-card__label">다음 액션</span>
        <strong>서비스 이벤트 실행</strong>
        <p>멤버 입장, 번들 담기, 주문서 열기, 인기순 보기 중 하나를 눌러 시연을 시작하세요.</p>
      </article>
      <article class="signal-card signal-card--warn">
        <span class="signal-card__label">집중 포인트</span>
        <strong>서비스 변화와 patch 연결</strong>
        <p>사용자에게 보이는 변화가 어떤 patch로 계산됐는지 바로 연결해서 설명합니다.</p>
      </article>
      <article class="signal-card signal-card--accent">
        <span class="signal-card__label">의미</span>
        <strong>렌더 노드 ${stats.beforeNodes}개</strong>
        <p>기준 화면의 노드 수를 알고 있어 patch 절감 효과를 바로 비교할 수 있습니다.</p>
      </article>
    `;
    return;
  }

  const validationTitle = validation?.matched ? "예상 patch 검증" : "검증 상태";
  const validationBody = validation?.matched
    ? `${scenario?.title || "시나리오"}가 의도한 patch 타입만 발생했습니다.`
    : validation
      ? `missing: ${validation.missing.join(", ") || "-"} / unexpected: ${validation.unexpected.join(", ") || "-"}`
      : "수동 patch 실행입니다.";

  panel.innerHTML = `
    <article class="signal-card signal-card--primary">
      <span class="signal-card__label">활성 시나리오</span>
      <strong>${escapeHTML(scenario?.title || "수동 patch")}</strong>
      <p>${escapeHTML(scenario?.description || "직접 수정한 DOM을 기준으로 diff를 계산했습니다.")}</p>
    </article>
    <article class="signal-card signal-card--good">
      <span class="signal-card__label">${escapeHTML(validationTitle)}</span>
      <strong>${escapeHTML(validation?.matched ? "검증 완료" : `${actualPatchTypes.length}개 patch 타입`)}</strong>
      <p>${escapeHTML(validationBody)}</p>
    </article>
    <article class="signal-card signal-card--warn">
      <span class="signal-card__label">핵심 patch</span>
      <strong>${escapeHTML(focusPatch.type)}</strong>
      <p>${escapeHTML(`${focusPath} · ${focusVNode ? getNodeDescriptor(focusVNode) : focusPatch.path}`)}</p>
    </article>
    <article class="signal-card signal-card--accent">
      <span class="signal-card__label">DOM 절감 효과</span>
      <strong>${escapeHTML(`${stats.savedOps}개 작업 절감`)}</strong>
      <p>${escapeHTML(`전체 렌더 ${stats.fullRenderOps} vs patch ${stats.patchOps} · ${stats.efficiencyRate}% 절감`)}</p>
    </article>
  `;
}

function renderPipelinePanel() {
  const panel = state.ui.pipelinePanel;
  const { focusPatch, focusPath, stats } = getDemoContext();
  const activeStage = focusPatch ? "patch" : "diff";
  const steps = [
    {
      key: "real",
      title: "실제 DOM 스냅샷",
      meta: `기준 노드 ${stats.beforeNodes}개`,
      complete: true
    },
    {
      key: "candidate",
      title: "후보 Virtual DOM",
      meta: "테스트 영역 DOM을 새 Virtual DOM 트리로 변환합니다.",
      complete: true
    },
    {
      key: "diff",
      title: "Diff",
      meta: focusPatch ? `${stats.patchOps}개의 patch를 생성했습니다.` : "patch를 만들 준비가 된 상태입니다.",
      complete: Boolean(focusPatch)
    },
    {
      key: "patch",
      title: "Patch",
      meta: focusPatch ? `${focusPatch.type} @ ${focusPath}` : "핵심 patch가 아직 없습니다.",
      complete: Boolean(focusPatch)
    },
    {
      key: "history",
      title: "History",
      meta: `${state.currentHistoryIndex + 1} / ${state.history.length} 스냅샷`,
      complete: state.history.length > 0
    }
  ];

  panel.innerHTML = `
    <div class="pipeline-strip">
      ${steps
        .map((step, index) => {
          const classNames = [
            "pipeline-step",
            step.complete ? "is-complete" : "",
            activeStage === step.key ? "is-active" : ""
          ]
            .filter(Boolean)
            .join(" ");

          return `
            <article class="${classNames}">
              <span class="pipeline-step__index">0${index + 1}</span>
              <strong class="pipeline-step__title">${escapeHTML(step.title)}</strong>
              <span class="pipeline-step__meta">${escapeHTML(step.meta)}</span>
            </article>
          `;
        })
        .join("")}
    </div>
    <div class="pipeline-footer">
      <strong>현재 흐름:</strong>
      ${escapeHTML(
        focusPatch
          ? `다음 상태를 만들고 diff를 수행했습니다. 현재 ${focusPatch.type} patch가 실제 서비스 화면을 어떻게 바꾸는지 설명하는 단계입니다.`
          : "기준 서비스 화면만 준비된 상태입니다. 다음 이벤트를 실행하면 candidate VDOM 생성부터 diff, patch, history 저장까지 전체 흐름을 볼 수 있습니다."
      )}
    </div>
  `;
}

function getServicePresentationContent() {
  const scenario = findScenarioById(state.activeScenarioId);

  if (!scenario) {
    return {
      eyebrow: "오늘의 한정 드롭",
      title: "멤버 전용 프리뷰가 진행 중입니다",
      body: "AURA Runner 01 한정 드롭을 준비 중입니다. 한 상태가 hero, overview, 드롭 백, 추천 영역까지 함께 바뀌는 구조로 설계된 화면입니다.",
      mode: "멤버 프리뷰"
    };
  }

  switch (scenario.id) {
    case "text-attr":
      return {
        eyebrow: "입장 오픈",
        title: "멤버 입장이 열리면서 여러 영역이 동시에 갱신되었습니다",
        body: "같은 화면 구조를 유지한 채 hero 문구, 입장 상태, 드롭 백 요약, CTA가 함께 바뀝니다. 이 구간은 TEXT와 ATTR patch를 설명하기 좋습니다.",
        mode: "멤버 입장 가능"
      };
    case "create-remove":
      return {
        eyebrow: "번들 담기 완료",
        title: "빈 상태가 사라지고 예약 배지가 새로 생겼습니다",
        body: "컬렉터 팩을 담는 순간 empty 상태가 제거되고 예약 배지가 생성됩니다. 같은 카드 안에서 REMOVE와 CREATE가 동시에 일어나는 대표적인 사례입니다.",
        mode: "예약 완료"
      };
    case "replace-tag":
      return {
        eyebrow: "주문 단계 진입",
        title: "요약 카드가 주문 단계 화면으로 교체되었습니다",
        body: "예약 확인 영역이 결제 전용 단계 화면으로 바뀌면서 subtree 전체가 다른 구조로 전환됩니다. 이 구간은 REPLACE로 설명하기 가장 자연스럽습니다.",
        mode: "주문 진행"
      };
    case "reorder-keyed":
      return {
        eyebrow: "추천 순서 재정렬",
        title: "추천 리스트가 다시 인기순으로 정렬되었습니다",
        body: "아이템 자체는 유지한 채 노출 순서만 다시 계산하는 흐름입니다. 추천, 랭킹, 카탈로그 정렬 UI에서 자주 필요한 패턴입니다.",
        mode: "인기순"
      };
    case "purchase-complete":
      return {
        eyebrow: "결제 완료",
        title: "외부 결제창 없이 주문 완료 상태까지 시연이 이어집니다",
        body: "실제 PG 연동 대신 결제 완료 이후 고객이 보게 되는 서비스 상태를 바로 렌더링했습니다. 발표에서는 주문 단계에서 완료 단계로 넘어가는 마지막 patch까지 이어서 보여줄 수 있습니다.",
        mode: "주문 완료"
      };
    default:
      return {
        eyebrow: "오늘의 한정 드롭",
        title: "멤버 전용 프리뷰가 진행 중입니다",
        body: "AURA Runner 01 한정 드롭을 준비 중입니다. 사용자는 이 화면에서 입장 오픈, 번들 담기, 주문 전환, 인기순 정렬 같은 상태 변화를 직접 경험합니다.",
        mode: "멤버 프리뷰"
      };
  }
}

function getVisiblePatchLabel() {
  if (!state.patches.length) {
    return "기본 상태";
  }

  return getActualPatchTypes(state.patches).join(" · ");
}

function getServiceAdoptionContent() {
  switch (state.activeScenarioId) {
    case "text-attr":
      return {
        title: "왜 여기서 React-style 방식이 유리한가",
        patchLabel: getVisiblePatchLabel(),
        body: "멤버 입장 이벤트 하나가 hero 카피, 진행 상태, 버튼 문구, 드롭 백 요약처럼 서로 떨어진 여러 위치를 함께 바꿉니다. 이럴 때 상태를 기준으로 새 UI 트리를 만들고 텍스트와 속성만 patch하는 편이 훨씬 일관적입니다.",
        areas: "Hero · 드롭 현황 · 드롭 백 요약",
        impactSummary: "한 번의 상태 변경이 여러 카드의 문구와 배지를 동시에 갱신합니다.",
        benefit: "흩어진 텍스트/속성을 한 번에 계산",
        compare: "직접 DOM 조작이면 각 카드의 textContent, class, 버튼 상태를 각각 찾아 수정해야 합니다."
      };
    case "create-remove":
      return {
        title: "왜 이 단계에서 우리가 만든 방식이 드러나는가",
        patchLabel: getVisiblePatchLabel(),
        body: "드롭 백은 빈 상태 문구를 제거하고 예약 배지를 새로 넣어야 합니다. 같은 카드 안에서 기존 child를 지우고 새 child를 추가하는 흐름이라 children reconciliation이 직접 보입니다.",
        areas: "드롭 백 카드",
        impactSummary: "비어 있던 UI가 예약 완료 UI로 바뀌면서 REMOVE와 CREATE가 같이 일어납니다.",
        benefit: "child 생성/삭제를 구조 기준으로 처리",
        compare: "직접 DOM 조작이면 empty 노드를 지우고 배지 노드를 삽입하는 순서를 수동으로 맞춰야 합니다."
      };
    case "replace-tag":
      return {
        title: "왜 주문 전환에서 React-style 방식이 맞는가",
        patchLabel: getVisiblePatchLabel(),
        body: "요약 카드가 주문 단계 섹션으로 통째로 바뀌는 순간에는 부분 수정보다 subtree 교체가 더 자연스럽습니다. 구조가 바뀌는 화면은 React-style 조건부 렌더링이 강점을 가지는 구간입니다.",
        areas: "주문 요약 카드 전체",
        impactSummary: "예약 확인 UI가 결제 단계 UI로 성격 자체를 바꿉니다.",
        benefit: "구조가 달라지는 화면을 subtree 단위로 교체",
        compare: "직접 DOM 조작이면 카드 내부 노드를 하나씩 지우고 새 입력/요약 구조를 다시 조립해야 합니다."
      };
    case "purchase-complete":
      return {
        title: "왜 시연용 결제 완료 단계도 같은 방식으로 이어지는가",
        patchLabel: getVisiblePatchLabel(),
        body: "실제 PG를 붙이지 않아도 주문 완료 이후 고객이 보게 되는 상태는 여전히 UI 상태 전환입니다. 그래서 마지막 단계도 새 Virtual DOM을 만들고 완료 화면으로 patch하는 쪽이 시연 목적에 더 맞습니다.",
        areas: "Hero · 주문 요약 · 완료 단계 · 다음 추천",
        impactSummary: "결제 완료 한 번으로 완료 배지, 배송 상태, 추천 상품까지 함께 바뀝니다.",
        benefit: "외부 결제 의존 없이도 완료 상태를 일관되게 시연",
        compare: "단순 모달로 끝내면 서비스가 어디까지 바뀌는지 안 보이지만, 지금은 완료 이후 화면 상태까지 한 번에 설명할 수 있습니다."
      };
    case "reorder-keyed":
      return {
        title: "왜 추천 정렬에는 key 기반 diff가 중요했는가",
        patchLabel: getVisiblePatchLabel(),
        body: "추천 리스트는 상품 자체는 그대로 두고 노출 순서만 자주 바뀝니다. 이때 key 기반으로 같은 아이템의 정체성을 유지한 채 순서만 다시 계산하는 방식이 적합합니다.",
        areas: "추천 리스트",
        impactSummary: "같은 상품을 다시 만들지 않고, 형제 순서만 재배치합니다.",
        benefit: "리스트 항목 정체성을 유지한 reorder",
        compare: "index 기준만 쓰면 이동과 재생성을 구분하기 어렵고, 정렬이 잦을수록 설명력도 떨어집니다."
      };
    default:
      return {
        title: "왜 이 화면에 React-style 방식이 맞나",
        patchLabel: "기본 상태",
        body: "이 화면은 hero, 드롭 현황, 드롭 백, 추천 영역이 같은 상태를 공유합니다. 그래서 영역마다 DOM을 수동으로 고치기보다 상태 기준으로 새 UI 트리를 만들고 필요한 부분만 patch하는 방식이 더 자연스럽습니다.",
        areas: "Hero · 드롭 현황 · 드롭 백 · 추천 영역",
        impactSummary: "멤버 입장 여부, 번들 선택, 주문 단계 같은 상태가 여러 카드에 동시에 퍼집니다.",
        benefit: "상태 한 번으로 전체 UI를 다시 계산",
        compare: "직접 DOM 조작이라면 각 카드의 텍스트, 버튼 상태, 배지, 리스트 순서를 따로 찾아 바꿔야 합니다."
      };
  }
}

function renderServicePresentation() {
  const content = getServicePresentationContent();
  const adoption = getServiceAdoptionContent();

  state.ui.serviceStateEyebrow.textContent = content.eyebrow;
  state.ui.serviceStateTitle.textContent = content.title;
  state.ui.serviceStateBody.textContent = content.body;
  state.ui.serviceModeValue.textContent = content.mode;
  state.ui.serviceReasonTitle.textContent = adoption.title;
  state.ui.serviceReasonPatch.textContent = adoption.patchLabel;
  state.ui.serviceReasonBody.textContent = adoption.body;
  state.ui.serviceImpactAreas.textContent = adoption.areas;
  state.ui.serviceImpactSummary.textContent = adoption.impactSummary;
  state.ui.serviceReasonBenefit.textContent = adoption.benefit;
  state.ui.serviceReasonCompare.textContent = adoption.compare;
}

function renderScenarioPanel() {
  const panel = state.ui.scenarioPanel;
  panel.innerHTML = "";

  SCENARIOS.filter((scenario) => !scenario.hiddenFromPanel).forEach((scenario) => {
    const isActive = state.activeScenarioId === scenario.id;
    const validation = isActive ? getScenarioValidation(scenario, state.patches) : null;
    const statusCopy = !isActive
      ? "시나리오 실행 전"
      : validation?.matched
        ? `검증 완료 · actual: ${validation.actual.join(", ")}`
        : `누락: ${validation?.missing.join(", ") || "-"} / 추가: ${validation?.unexpected.join(", ") || "-"}`;
    const article = document.createElement("article");
    article.className = `scenario-card ${isActive ? "is-active" : ""}`;
    article.innerHTML = `
      <h3 class="scenario-card__title">${escapeHTML(scenario.title)}</h3>
      <p class="scenario-card__description">${escapeHTML(scenario.description)}</p>
      <div class="scenario-card__badges">
        ${scenario.expectedTypes
          .map((type) => `<span class="patch-badge" data-type="${type}">${type}</span>`)
          .join("")}
      </div>
      <p class="scenario-card__status">${escapeHTML(statusCopy)}</p>
      <div class="scenario-card__footer">
        <span class="chip ${isActive && validation?.matched ? "chip--green" : "chip--slate"}">${escapeHTML(
          isActive && validation?.matched ? "예상과 일치" : getPatchMetaLabel(scenario.expectedTypes[0])
        )}</span>
        <button class="button button--small" type="button" data-scenario-id="${scenario.id}">실행</button>
      </div>
    `;
    panel.appendChild(article);
  });
}

function renderPatchLog() {
  const panel = state.ui.diffLogPanel;
  panel.innerHTML = "";

  if (!state.patches.length) {
    panel.innerHTML = createEmptyState(UI_TEXT.noChange);
    return;
  }

  state.patches.forEach((patch, index) => {
    const item = document.createElement("button");
    item.type = "button";
    item.className = `log-item ${state.selectedPatchIndex === index ? "is-active" : ""}`;
    item.dataset.patchIndex = String(index);
    item.innerHTML = `
      <div class="log-item__head">
        <span class="patch-badge" data-type="${patch.type}">${patch.type}</span>
        <strong>#${index + 1}</strong>
      </div>
      <div class="log-item__path">path: ${escapeHTML(patch.path)}</div>
      <p class="log-item__detail">${escapeHTML(formatPatchDetail(patch))}</p>
    `;
    panel.appendChild(item);
  });
}

function renderPatchTimelinePanel() {
  const panel = state.ui.patchTimelinePanel;
  panel.innerHTML = "";

  if (!state.patches.length) {
    panel.innerHTML = createEmptyState("시나리오를 실행하거나 Patch 버튼을 눌러 타임라인을 생성하세요.");
    return;
  }

  state.patches.forEach((patch, index) => {
    const item = document.createElement("button");
    item.type = "button";
    item.className = `timeline-item ${state.selectedPatchIndex === index ? "is-active" : ""}`;
    item.dataset.patchIndex = String(index);
    item.innerHTML = `
      <div class="timeline-item__top">
        <span class="patch-badge" data-type="${patch.type}">${patch.type}</span>
        <strong>단계 ${index + 1}</strong>
      </div>
      <div class="timeline-item__detail">${escapeHTML(formatPatchDetail(patch))}</div>
    `;
    panel.appendChild(item);
  });
}

function renderHistoryPanel() {
  const panel = state.ui.historyPanel;
  panel.innerHTML = "";

  state.history.forEach((entry, index) => {
    const button = document.createElement("button");
    button.type = "button";
    button.className = `history-card ${index === state.currentHistoryIndex ? "is-active" : ""}`;
    button.dataset.historyIndex = String(index);
    button.innerHTML = `
      <div class="history-card__top">
        <span class="history-card__title">${escapeHTML(entry.label)}</span>
        <span class="chip chip--slate">${index}</span>
      </div>
      <div class="history-card__meta">${escapeHTML(entry.timestamp)}</div>
      <p class="history-card__stats">${escapeHTML(entry.description)}</p>
    `;
    panel.appendChild(button);
  });
}

function renderTreeNode(vNode) {
  const fragment = state.ui.treeNodeTemplate.content.cloneNode(true);
  const wrapper = fragment.querySelector(".tree-node");
  const tagEl = fragment.querySelector(".tree-node__tag");
  const pathEl = fragment.querySelector(".tree-node__path");
  const metaEl = fragment.querySelector(".tree-node__meta");

  wrapper.dataset.path = vNode.path;
  wrapper.style.marginLeft = `${vNode.depth * 14}px`;
  wrapper.classList.toggle("is-active", state.selectedPath === vNode.path);
  tagEl.textContent = getNodeDescriptor(vNode);
  pathEl.textContent = vNode.path;
  metaEl.textContent = getReadableNodeSummary(vNode);
  return fragment;
}

function renderTreePanel() {
  const panel = state.ui.treePanel;
  panel.innerHTML = "";

  const dfsOrder = traverseDFS(state.realVNode);
  dfsOrder.forEach((item) => {
    const node = findVNodeByPath(state.realVNode, item.path);
    if (node) {
      panel.appendChild(renderTreeNode(node));
    }
  });
}

function renderTraversalSequence(panel, sequence) {
  panel.innerHTML = "";
  const list = document.createElement("ol");
  list.className = "sequence-list";

  sequence.forEach((item, index) => {
    const listItem = document.createElement("li");
    listItem.className = item.path === state.selectedPath ? "is-active" : "";
    listItem.textContent = `${index + 1}. ${item.label} @ ${item.path} (depth ${item.depth})`;
    list.appendChild(listItem);
  });

  panel.appendChild(list);
}

function renderPerformancePanel() {
  const panel = state.ui.performancePanel;
  const stats = state.comparisonStats || createBaselineComparisonStats(state.realVNode);
  const patchCounts = Object.entries(stats.patchCounts || createPatchCountMap())
    .filter(([, count]) => count > 0)
    .map(([type, count]) => `<span class="patch-badge" data-type="${type}">${type} × ${count}</span>`)
    .join("");

  panel.innerHTML = `
    <div class="performance-grid">
      <article class="performance-card">
        <h3>변경 전 노드 수</h3>
        <strong>${stats.beforeNodes}</strong>
        <div class="performance-card__body">patch 전 Virtual DOM 노드 수</div>
      </article>
      <article class="performance-card">
        <h3>변경 후 노드 수</h3>
        <strong>${stats.afterNodes}</strong>
        <div class="performance-card__body">patch 후 Virtual DOM 노드 수</div>
      </article>
      <article class="performance-card">
        <h3>전체 렌더 비용</h3>
        <strong>${stats.fullRenderOps}</strong>
        <div class="performance-card__body">가정상 전체 재렌더링에 필요한 작업 수</div>
      </article>
      <article class="performance-card">
        <h3>Patch 비용</h3>
        <strong>${stats.patchOps}</strong>
        <div class="performance-card__body">실제로 수행한 patch 작업 수</div>
      </article>
    </div>
    <article class="performance-card">
      <div class="performance-card__head">
        <h3>예상 절감 효과</h3>
        <span class="chip chip--teal">${stats.efficiencyRate}% 절감</span>
      </div>
      <div class="performance-card__body">
        ${stats.mode === "baseline"
          ? "초기 상태입니다. 아직 비교 대상 patch가 없어 절감 효과는 0으로 표시됩니다."
          : `전체 재렌더링 대비 ${stats.savedOps}개의 DOM 작업을 줄였습니다.`}
      </div>
      <div class="performance-bar">
        <div class="performance-bar__fill" style="width: ${stats.efficiencyRate}%"></div>
      </div>
    </article>
    <article class="performance-card">
      <h3>Patch 구성</h3>
      <div class="attribute-list">
        ${patchCounts || '<span class="chip chip--slate">patch 없음</span>'}
      </div>
    </article>
  `;
}

function renderInspectorAttributes(attrs) {
  const entries = Object.entries(attrs || {});
  if (!entries.length) {
    return '<div class="empty-state">선택한 노드에는 속성이 없습니다.</div>';
  }

  return `
    <div class="attribute-list">
      ${entries
        .map(([name, value]) => `<span class="attribute-pill">${escapeHTML(name)}=${escapeHTML(String(value))}</span>`)
        .join("")}
    </div>
  `;
}

function renderInspectorPanel() {
  const panel = state.ui.inspectorPanel;
  const selectedVNode = findVNodeByPath(state.realVNode, state.selectedPath) || findVNodeByPath(state.testVNode, state.selectedPath);
  const selectedPatch = state.selectedPatchIndex != null ? state.patches[state.selectedPatchIndex] : null;

  const nodeCard = selectedVNode
    ? `
      <article class="inspector-card">
        <h3>Selected Node</h3>
        <div class="inspector-list">
          <div class="inspector-row"><span class="inspector-key">path</span><span class="inspector-value">${escapeHTML(selectedVNode.path)}</span></div>
          <div class="inspector-row"><span class="inspector-key">descriptor</span><span class="inspector-value">${escapeHTML(getNodeDescriptor(selectedVNode))}</span></div>
          <div class="inspector-row"><span class="inspector-key">depth</span><span class="inspector-value">${selectedVNode.depth}</span></div>
          <div class="inspector-row"><span class="inspector-key">key</span><span class="inspector-value">${escapeHTML(String(selectedVNode.key || "null"))}</span></div>
          <div class="inspector-row"><span class="inspector-key">summary</span><span class="inspector-value">${escapeHTML(getReadableNodeSummary(selectedVNode))}</span></div>
        </div>
      </article>
      <article class="inspector-card">
        <h3>Attributes</h3>
        ${renderInspectorAttributes(selectedVNode.attrs)}
      </article>
    `
    : createEmptyState("트리, 실제 영역, 테스트 영역 중 하나를 클릭해 노드를 선택하세요.");

  const patchCard = selectedPatch
    ? `
      <article class="inspector-card">
        <h3>Selected Patch</h3>
        <div class="inspector-list">
          <div class="inspector-row"><span class="inspector-key">type</span><span class="inspector-value">${escapeHTML(selectedPatch.type)}</span></div>
          <div class="inspector-row"><span class="inspector-key">path</span><span class="inspector-value">${escapeHTML(selectedPatch.path)}</span></div>
          <div class="inspector-row"><span class="inspector-key">detail</span><span class="inspector-value">${escapeHTML(formatPatchDetail(selectedPatch))}</span></div>
          <div class="inspector-row"><span class="inspector-key">old</span><span class="inspector-value">${escapeHTML(getNodeDescriptor(selectedPatch.oldNode || selectedPatch.node || null))}</span></div>
          <div class="inspector-row"><span class="inspector-key">new</span><span class="inspector-value">${escapeHTML(getNodeDescriptor(selectedPatch.newNode || selectedPatch.node || null))}</span></div>
        </div>
      </article>
    `
    : createEmptyState("Patch 로그나 타임라인을 클릭하면 해당 변경을 자세히 확인할 수 있습니다.");

  panel.innerHTML = `${nodeCard}${patchCard}`;
}

function resolveDomHighlightTarget(surface, path) {
  let node = getDomNodeByPath(surface, path);
  if (!node && path !== "0") {
    const fallbackPath = path.split("-").slice(0, -1).join("-") || "0";
    node = getDomNodeByPath(surface, fallbackPath);
  }

  if (!node) {
    return null;
  }

  if (node.nodeType === NODE_TYPE.TEXT) {
    return node.parentElement;
  }

  return node;
}

function renderSurfaceOverlay(surface, overlay, descriptors) {
  overlay.innerHTML = "";
  const surfaceRect = surface.getBoundingClientRect();

  descriptors.forEach((descriptor) => {
    const target = resolveDomHighlightTarget(surface, descriptor.path);
    if (!target) {
      return;
    }

    const targetRect = target.getBoundingClientRect();
    if (targetRect.width <= 0 || targetRect.height <= 0) {
      return;
    }

    const highlight = document.createElement("div");
    highlight.className = `dom-highlight dom-highlight--${descriptor.tone}`;
    highlight.style.left = `${targetRect.left - surfaceRect.left}px`;
    highlight.style.top = `${targetRect.top - surfaceRect.top}px`;
    highlight.style.width = `${targetRect.width}px`;
    highlight.style.height = `${targetRect.height}px`;
    highlight.innerHTML = `<span class="dom-highlight__label">${escapeHTML(descriptor.label)}</span>`;
    overlay.appendChild(highlight);
  });
}

function renderDomHighlights() {
  const descriptors = getPatchFocusDescriptors();
  renderSurfaceOverlay(state.ui.realDomRoot, state.ui.realDomOverlay, descriptors);
  renderSurfaceOverlay(state.ui.testDomRoot, state.ui.testDomOverlay, descriptors);
}

function createExplanationHTML() {
  return `
    <section class="explanation-block">
      <h3>프로젝트 개요</h3>
      <ul>
        <li>이 앱은 React-style Virtual DOM, diff, patch 흐름을 직접 구현한 뒤 실제 서비스 화면에 적용한 학습용 데모입니다.</li>
        <li>서비스 변화만 보여주는 것이 아니라, 어떤 patch가 어떤 노드를 바꿨는지 타임라인과 인스펙터로 연결해 설명할 수 있습니다.</li>
        <li>포트폴리오 관점에서는 기능 구현보다 선택 이유와 trade-off를 설명할 수 있도록 구조를 분리한 점이 핵심입니다.</li>
      </ul>
    </section>
    <section class="explanation-block">
      <h3>아키텍처</h3>
      <ul>
        <li>상태 관리: 현재 Virtual DOM, patch 배열, history, 선택 path, playback 상태를 저장합니다.</li>
        <li>Virtual DOM 변환기: <span class="code-inline">domToVNode</span>가 실제 DOM을 객체 트리로 바꿉니다.</li>
        <li>렌더러: <span class="code-inline">createDOMFromVNode</span>와 <span class="code-inline">renderVNodeToRoot</span>가 트리를 실제 DOM으로 만듭니다.</li>
        <li>Diff 엔진: <span class="code-inline">diff</span>와 <span class="code-inline">diffChildren</span>가 최소 patch를 생성합니다.</li>
        <li>Patch 엔진: path 기반으로 DOM 노드를 찾아 필요한 변경만 반영합니다.</li>
        <li>Traversal 엔진: DFS/BFS로 트리 구조를 시각화합니다.</li>
        <li>UI 바인딩: 시나리오 버튼, 타임라인, 인스펙터, MutationObserver를 연결합니다.</li>
      </ul>
    </section>
    <section class="explanation-block">
      <h3>기술 선택 이유</h3>
      <ul>
        <li>Vanilla JS를 선택한 이유는 React 개념을 프레임워크 추상화 없이 직접 구현하고 설명하기 위해서입니다.</li>
        <li>Virtual DOM을 객체 트리로 표현한 이유는 tag, attrs, children, path를 한 구조 안에서 diff와 traversal까지 함께 설명할 수 있기 때문입니다.</li>
        <li>Path 기반 patch는 디버깅과 history 복원, 시연 설명에 가장 직관적입니다.</li>
        <li>자식 비교는 key를 우선하고 index를 fallback으로 둬서 reorder와 기본 비교를 모두 처리합니다.</li>
        <li>MutationObserver는 보조 검증 장치일 뿐이고, 핵심 변경 판단은 직접 구현한 Virtual DOM 비교가 담당합니다.</li>
      </ul>
    </section>
    <section class="explanation-block">
      <h3>자료구조 표</h3>
      <div class="table-wrap">
        <table class="table--data">
          <thead>
            <tr>
              <th>자료구조</th>
              <th>형태</th>
              <th>선택 이유</th>
            </tr>
          </thead>
          <tbody>
            <tr>
              <td>Virtual DOM 트리 객체</td>
              <td>{ type, tag, attrs, children, text, key, path, depth }</td>
              <td>트리, diff, traversal, inspector를 하나의 구조로 설명할 수 있습니다.</td>
            </tr>
            <tr>
              <td>patch 배열</td>
              <td>CREATE, REMOVE, REPLACE, TEXT, ATTR_SET, ATTR_REMOVE, REORDER_CHILDREN</td>
              <td>비교 결과를 실행 가능한 작업 목록으로 분리할 수 있습니다.</td>
            </tr>
            <tr>
              <td>history 배열 + currentIndex</td>
              <td>스냅샷 배열 + 현재 위치</td>
              <td>undo/redo와 timeline 복원을 가장 직관적으로 보여줍니다.</td>
            </tr>
            <tr>
              <td>BFS 큐</td>
              <td>배열 queue</td>
              <td>레벨 순회 설명과 시각화에 적합합니다.</td>
            </tr>
            <tr>
              <td>DFS 호출 스택</td>
              <td>재귀</td>
              <td>깊이 우선 탐색을 가장 간단하게 구현할 수 있습니다.</td>
            </tr>
            <tr>
              <td>속성 비교 객체</td>
              <td>attrs plain object</td>
              <td>속성 추가, 수정, 삭제를 key 단위로 설명할 수 있습니다.</td>
            </tr>
            <tr>
              <td>순서 비교 배열</td>
              <td>형제 key 배열</td>
              <td>REORDER_CHILDREN 판단을 단순하게 만듭니다.</td>
            </tr>
          </tbody>
        </table>
      </div>
    </section>
    <section class="explanation-block">
      <h3>알고리즘 흐름</h3>
      <ul>
        <li><span class="code-inline">domToVNode</span>: DOM childNodes를 순회하며 주석과 공백 노드를 정리하고 객체 트리로 만듭니다. 시간복잡도는 O(N)입니다.</li>
        <li><span class="code-inline">createDOMFromVNode</span>: Virtual DOM을 실제 DOM 노드로 재귀 생성합니다. 시간복잡도는 O(N)입니다.</li>
        <li><span class="code-inline">diff</span>: 타입, 태그, 텍스트, 속성, 자식을 비교해 patch를 생성합니다.</li>
        <li><span class="code-inline">diffChildren</span>: key 맵을 이용해 CREATE, REMOVE, REORDER를 계산합니다.</li>
        <li><span class="code-inline">applyPatches</span>: update → remove → create → reorder 순서로 실제 DOM에 반영합니다.</li>
        <li><span class="code-inline">traverseDFS</span>, <span class="code-inline">traverseBFS</span>: 트리 구조를 다른 순회 방식으로 보여줍니다.</li>
        <li><span class="code-inline">pushHistory</span>, <span class="code-inline">goBack</span>, <span class="code-inline">goForward</span>: 스냅샷 배열과 currentIndex를 조작합니다.</li>
      </ul>
    </section>
    <section class="explanation-block">
      <h3>학습 키워드 연결</h3>
      <ul>
        <li>트리: Virtual DOM은 루트, 부모/자식, 리프, depth를 갖는 일반 트리입니다.</li>
        <li>그래프: 각 노드는 vertex, 부모에서 자식으로 가는 연결은 directed edge 또는 arc로 설명할 수 있습니다.</li>
        <li>DFS/BFS: 같은 트리를 다른 순서로 방문해 구조 이해를 돕습니다.</li>
        <li>위상정렬: Virtual DOM 자체는 DAG가 아니지만, patch 적용 순서 설계와 연결해 설명할 수 있습니다.</li>
        <li>BST 비교: Virtual DOM은 정렬 규칙이 없는 일반 트리이므로 BST가 아닙니다.</li>
      </ul>
    </section>
    <section class="explanation-block">
      <h3>성능과 브라우저 API</h3>
      <ul>
        <li>실제 DOM 변경은 layout 계산, reflow, repaint 비용이 뒤따르기 때문에 비쌉니다.</li>
        <li>Virtual DOM은 메모리 상 트리 비교를 먼저 수행하고, 실제 DOM에는 필요한 patch만 적용합니다.</li>
        <li>이 앱은 document, window, querySelector, createElement, createTextNode, childNodes, attributes, nodeType, eventListener, MutationObserver를 사용합니다.</li>
        <li>문자열 비교보다 트리 비교가 어느 노드가 왜 바뀌었는지 설명하기 쉽습니다.</li>
      </ul>
    </section>
    <section class="explanation-block">
      <h3>Diff 핵심 5케이스</h3>
      <ul>
        <li>REPLACE: 노드 타입이나 태그가 바뀌면 기존 노드를 새 노드로 교체합니다.</li>
        <li>TEXT: 텍스트만 바뀌면 textContent만 갱신합니다.</li>
        <li>ATTR_SET / ATTR_REMOVE: 속성 추가, 수정, 삭제를 key 단위로 처리합니다.</li>
        <li>CREATE / REMOVE: 자식 노드 생성과 삭제를 부모 path 기준으로 반영합니다.</li>
        <li>REORDER_CHILDREN: 같은 key 집합 안에서 형제 순서만 바뀌면 reorder로 처리합니다.</li>
      </ul>
    </section>
    <section class="explanation-block">
      <h3>대안과 Trade-off</h3>
      <ul>
        <li>전체 재렌더링은 단순하지만 매번 많은 DOM 작업이 발생합니다. patch 방식은 복잡하지만 실제 변경 범위를 줄일 수 있습니다.</li>
        <li>문자열 비교는 위치와 의미를 설명하기 어렵고, 트리 비교는 path 기준으로 바뀐 지점을 추적할 수 있습니다.</li>
        <li>순수 index 비교는 reorder에 약하고, key 기반 비교는 노드 정체성을 더 안정적으로 유지합니다.</li>
        <li>시나리오, 타임라인, 인스펙터를 넣은 이유는 구현 사실만이 아니라 선택 이유까지 시연에서 설명하기 위해서입니다.</li>
      </ul>
    </section>
    <section class="explanation-block">
      <h3>엣지 케이스</h3>
      <ul>
        <li>공백 텍스트 노드는 Virtual DOM 변환과 path 탐색에서 모두 무시해 인덱스 불일치를 막습니다.</li>
        <li>주석 노드는 비교 대상에서 제외합니다.</li>
        <li>속성 순서는 객체 비교이므로 의미가 없습니다.</li>
        <li>boolean attribute는 빈 문자열을 true처럼 취급합니다.</li>
        <li>비어 있는 테스트 영역과 잘못된 HTML 입력도 안전하게 처리합니다.</li>
      </ul>
    </section>
  `;
}

function updateMetaInfo() {
  const historyLength = state.history.length;
  const current = state.currentHistoryIndex >= 0 ? state.currentHistoryIndex + 1 : 0;
  state.ui.historyMeta.textContent = `${current} / ${historyLength}`;
  state.ui.patchCountMeta.textContent = String(state.patches.length);
  state.ui.patchSummary.textContent = state.patches.length
    ? `${state.patches.length}개 patch 생성`
    : "patch 없음";

  const totalNodes = countNodes(state.realVNode);
  const maxDepth = calculateMaxDepth(state.realVNode);
  state.ui.treeMeta.textContent = `노드 수: ${totalNodes}`;
  state.ui.depthMeta.textContent = `깊이: ${maxDepth}`;
  state.ui.observerMeta.textContent = `변경 감지 ${state.mutationCount}`;
  state.ui.backButton.disabled = state.currentHistoryIndex <= 0;
  state.ui.forwardButton.disabled = state.currentHistoryIndex >= state.history.length - 1;
  state.ui.playbackToggleButton.disabled = state.patches.length === 0;
  state.ui.playbackNextButton.disabled = state.patches.length === 0;
  state.ui.playbackResetButton.disabled = state.patches.length === 0;
  state.ui.playbackToggleButton.textContent = state.playbackPlaying ? "일시정지" : "재생";
  state.ui.demoTourButton.textContent = state.demoTourPlaying ? "데모 투어 중지" : "데모 투어 시작";
  state.ui.demoFocusButton.disabled = state.patches.length === 0;

  if (!state.patches.length) {
    state.ui.playbackStatus.textContent = UI_TEXT.playbackIdle;
  } else if (state.playbackPlaying) {
    state.ui.playbackStatus.textContent = `Step ${state.selectedPatchIndex + 1} / ${state.patches.length} 재생 중`;
  } else if (state.selectedPatchIndex != null) {
    state.ui.playbackStatus.textContent = `Step ${state.selectedPatchIndex + 1} / ${state.patches.length} 선택됨`;
  } else {
    state.ui.playbackStatus.textContent = UI_TEXT.playbackReady;
  }

  if (state.demoTourPlaying) {
    state.ui.demoTourStatus.textContent = `데모 투어 진행 중 · ${state.demoTourIndex + 1} / ${SCENARIOS.length} 시나리오`;
  } else if (state.demoTourCompleted) {
    state.ui.demoTourStatus.textContent = UI_TEXT.tourDone;
  } else if (state.activeScenarioId) {
    const activeScenario = findScenarioById(state.activeScenarioId);
    state.ui.demoTourStatus.textContent = `${activeScenario?.title || "시나리오"}가 활성화되어 있습니다. 현재 patch를 바로 설명할 수 있는 상태입니다.`;
  } else {
    state.ui.demoTourStatus.textContent = UI_TEXT.tourIdle;
  }
}

function renderAllPanels() {
  renderServicePresentation();
  renderDemoBriefingPanel();
  renderDemoSignalPanel();
  renderPipelinePanel();
  renderScenarioPanel();
  renderPatchTimelinePanel();
  renderPatchLog();
  renderHistoryPanel();
  renderTreePanel();
  renderTraversalSequence(state.ui.dfsPanel, traverseDFS(state.realVNode));
  renderTraversalSequence(state.ui.bfsPanel, traverseBFS(state.realVNode));
  renderPerformancePanel();
  renderInspectorPanel();
  state.ui.explanationPanel.innerHTML = createExplanationHTML();
  updateMetaInfo();
  renderDomHighlights();
}

/* -------------------------------------------------------------------------- */
/* 11. event bindings                                                          */
/* -------------------------------------------------------------------------- */

function collectTestVNode() {
  return domToVNode(state.ui.testDomRoot);
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

function resetPlaybackState() {
  clearPlaybackTimer();
  state.playbackPlaying = false;
  state.playbackIndex = null;
  state.selectedPatchIndex = null;
}

function setPlaybackIndex(index) {
  if (!state.patches.length) {
    resetPlaybackState();
    state.selectedPath = getDefaultSelectionPath(state.realVNode);
    renderAllPanels();
    return;
  }

  const safeIndex = Math.max(0, Math.min(index, state.patches.length - 1));
  state.playbackIndex = safeIndex;
  state.selectedPatchIndex = safeIndex;
  state.selectedPath = getPatchPrimaryPath(state.patches[safeIndex], state.realVNode);
  renderAllPanels();
}

function pausePlayback() {
  clearPlaybackTimer();
  state.playbackPlaying = false;
  renderAllPanels();
}

function startPlayback() {
  if (!state.patches.length) {
    return;
  }

  clearPlaybackTimer();
  state.playbackPlaying = true;

  if (state.playbackIndex == null || state.playbackIndex >= state.patches.length - 1) {
    state.playbackIndex = -1;
  }

  state.playbackTimer = window.setInterval(() => {
    if (state.playbackIndex >= state.patches.length - 1) {
      pausePlayback();
      state.ui.playbackStatus.textContent = UI_TEXT.playbackDone;
      return;
    }

    setPlaybackIndex(state.playbackIndex + 1);
  }, 900);

  setPlaybackIndex(state.playbackIndex + 1);
}

function resetPlayback() {
  resetPlaybackState();
  state.selectedPath = getDefaultSelectionPath(state.realVNode);
  renderAllPanels();
}

function focusPrimaryPatch() {
  if (!state.patches.length) {
    return;
  }

  pausePlayback();
  const primaryPatchIndex = getPrimaryPatchIndex(state.patches);
  setPlaybackIndex(primaryPatchIndex);
}

function stopDemoTour(options = {}) {
  const { completed = false } = options;

  clearDemoTourTimer();
  state.demoTourPlaying = false;
  state.demoTourCompleted = completed;

  if (completed) {
    state.demoTourIndex = null;
    state.ui.demoTourStatus.textContent = UI_TEXT.tourDone;
  }
}

function queueDemoTourStep(index) {
  const tourScenarios = SCENARIOS.filter((scenario) => !scenario.hiddenFromTour);
  const scenario = tourScenarios[index];
  if (!scenario) {
    stopDemoTour({
      completed: true
    });
    renderAllPanels();
    return;
  }

  state.demoTourIndex = index;
  runScenario(scenario.id, {
    autoPlay: true,
    preserveTour: true
  });

  if (!state.demoTourPlaying) {
    return;
  }

  const delay = Math.min(7200, Math.max(2800, state.patches.length * 700 + 1800));
  clearDemoTourTimer();
  state.demoTourTimer = window.setTimeout(() => {
    const nextIndex = index + 1;
    if (nextIndex >= tourScenarios.length) {
      stopDemoTour({
        completed: true
      });
      renderAllPanels();
      return;
    }

    queueDemoTourStep(nextIndex);
  }, delay);
}

function startDemoTour() {
  stopDemoTour();
  state.demoTourCompleted = false;
  state.demoTourPlaying = true;
  queueDemoTourStep(0);
}

function executePatch(options = {}) {
  syncTestFromSourceEditor();

  const previousVNode = cloneValue(state.realVNode);
  const nextVNode = normalizeVNodePaths(collectTestVNode());
  const patches = diff(previousVNode, nextVNode, "0", []);

  state.patches = patches;
  state.comparisonStats = createComparisonStats(previousVNode, nextVNode, patches);

  if (patches.length) {
    applyPatches(state.ui.realDomRoot, patches, previousVNode, nextVNode);
    state.realVNode = normalizeVNodePaths(domToVNode(state.ui.realDomRoot));
    state.testVNode = cloneValue(nextVNode);
    renderVNodeToRoot(state.ui.testDomRoot, state.testVNode);
  } else {
    state.realVNode = cloneValue(nextVNode);
    state.testVNode = cloneValue(nextVNode);
    renderVNodeToRoot(state.ui.testDomRoot, state.testVNode);
  }

  state.activeScenarioId = options.scenarioId ?? state.activeScenarioId;
  restoreSelectionDefaults();
  clearPlaybackTimer();
  state.playbackPlaying = false;

  const label = options.label || `Patch #${state.history.length}`;
  const description =
    options.description ||
    (patches.length
      ? `${patches.length}개의 patch가 실제 DOM에 반영되었습니다.`
      : "변경이 없어 no-op 상태를 history에 기록했습니다.");

  pushHistory(label, description, state.realVNode, patches);
  setStatus(patches.length ? "Patch 적용 완료" : "No-op Patch", description);
  renderAllPanels();
}

function resetToSample(options = {}) {
  const { clearHistory = false, preserveScenario = false } = options;

  if (clearHistory) {
    state.history = [];
    state.currentHistoryIndex = -1;
  }

  resetPlaybackState();
  renderHTMLIntoTarget(state.ui.realDomRoot, SAMPLE_TEMPLATE);
  const initialVNode = normalizeVNodePaths(domToVNode(state.ui.realDomRoot));
  state.realVNode = cloneValue(initialVNode);
  state.testVNode = cloneValue(initialVNode);
  renderVNodeToRoot(state.ui.testDomRoot, state.testVNode);
  syncSourceEditorFromTest();
  state.patches = [];
  state.comparisonStats = createBaselineComparisonStats(state.realVNode);
  state.selectedPath = getDefaultSelectionPath(state.realVNode);

  if (!preserveScenario) {
    state.activeScenarioId = null;
  }

  pushHistory("초기 상태", "실제 DOM -> Virtual DOM -> 테스트 영역 렌더링이 완료된 첫 스냅샷", state.realVNode, []);
  setStatus("초기 상태", "실제 DOM -> Virtual DOM -> 테스트 영역 렌더링이 완료되었습니다.");
  renderAllPanels();
}

function runScenario(scenarioId, options = {}) {
  const scenario = findScenarioById(scenarioId);
  if (!scenario) {
    return;
  }

  if (!options.preserveTour) {
    stopDemoTour();
  }

  state.activeScenarioId = scenarioId;
  resetToSample({
    clearHistory: true,
    preserveScenario: true
  });

  state.ui.sourceEditor.value = scenario.html;
  syncTestFromSourceEditor();
  executePatch({
    label: `Scenario 쨌 ${scenario.title}`,
    description: scenario.description,
    scenarioId
  });

  if (options.autoPlay) {
    window.setTimeout(() => {
      startPlayback();
    }, 180);
  }
}

function runLiveTransition(scenarioId, options = {}) {
  const scenario = findScenarioById(scenarioId);
  if (!scenario) {
    return;
  }

  if (!options.preserveTour) {
    stopDemoTour();
  }

  state.activeScenarioId = scenarioId;
  state.ui.sourceEditor.value = scenario.html;
  syncTestFromSourceEditor();
  executePatch({
    label: options.label || `Service Flow · ${scenario.title}`,
    description: options.description || scenario.description,
    scenarioId
  });

  if (options.autoPlay) {
    window.setTimeout(() => {
      startPlayback();
    }, 180);
  }
}

function selectPath(path) {
  state.selectedPath = getNearestExistingPath(state.realVNode, [path]);
  renderAllPanels();
}

function setWorkbenchOpen(open) {
  if (!open && state.ui.workbenchShell?.contains(document.activeElement)) {
    document.activeElement.blur();
  }

  document.body.classList.toggle("is-workbench-open", open);

  if (state.ui.workbenchShell) {
    state.ui.workbenchShell.setAttribute("aria-hidden", open ? "false" : "true");
    state.ui.workbenchShell.toggleAttribute("inert", !open);
  }
}

function findSelectableMeta(target, stopNode) {
  let current = target;

  while (current && current !== stopNode) {
    if (current.__vdomMeta?.path) {
      return current.__vdomMeta;
    }

    current = current.parentNode;
  }

  return stopNode?.__vdomMeta || null;
}

function bindSurfaceSelection(surface) {
  surface.addEventListener("click", (event) => {
    if (event.target.closest("[data-service-scenario]")) {
      return;
    }

    const meta = findSelectableMeta(event.target, surface);
    if (!meta?.path) {
      return;
    }

    state.selectedPatchIndex = null;
    state.playbackIndex = null;
    selectPath(meta.path);
  });
}

function bindEvents() {
  if (state.ui.serviceHomeButton) {
    state.ui.serviceHomeButton.addEventListener("click", () => {
      stopDemoTour();
      resetToSample({
        clearHistory: true
      });
    });
  }

  if (state.ui.openWorkbenchButton) {
    state.ui.openWorkbenchButton.addEventListener("click", () => {
      setWorkbenchOpen(true);
    });
  }

  if (state.ui.closeWorkbenchButton) {
    state.ui.closeWorkbenchButton.addEventListener("click", () => {
      setWorkbenchOpen(false);
    });
  }

  if (state.ui.workbenchBackdrop) {
    state.ui.workbenchBackdrop.addEventListener("click", () => {
      setWorkbenchOpen(false);
    });
  }

  window.addEventListener("keydown", (event) => {
    if (event.key === "Escape") {
      setWorkbenchOpen(false);
    }
  });

  if (state.ui.realDomRoot) {
    state.ui.realDomRoot.addEventListener("click", (event) => {
      const scenarioButton = event.target.closest("[data-service-scenario]");
      if (scenarioButton) {
        event.preventDefault();
        stopDemoTour();
        runScenario(scenarioButton.dataset.serviceScenario);
        return;
      }

      const actionButton = event.target.closest("[data-action]");
      if (!actionButton) {
        return;
      }

      event.preventDefault();
      stopDemoTour();

      if (actionButton.dataset.action === "purchase") {
        runLiveTransition("purchase-complete", {
          label: "Service Flow · 결제 완료",
          description: "주문 단계에서 결제 완료 상태로 전환했습니다."
        });
        return;
      }

      if (actionButton.dataset.action === "restart-demo") {
        resetToSample({
          clearHistory: true
        });
      }
    });
  }

  state.ui.patchButton.addEventListener("click", () => {
    stopDemoTour();
    executePatch({
      label: `Patch #${state.history.length}`
    });
  });

  state.ui.backButton.addEventListener("click", () => {
    stopDemoTour();
    goBack();
  });
  state.ui.forwardButton.addEventListener("click", () => {
    stopDemoTour();
    goForward();
  });
  state.ui.resetButton.addEventListener("click", () => {
    stopDemoTour();
    resetToSample({
      clearHistory: true
    });
  });

  state.ui.syncSourceButton.addEventListener("click", () => {
    stopDemoTour();
    state.activeScenarioId = null;
    syncTestFromSourceEditor();
    setStatus("소스 동기화", "textarea의 HTML을 테스트 영역에 반영했습니다.");
    renderDomHighlights();
  });

  state.ui.demoTourButton.addEventListener("click", () => {
    if (state.demoTourPlaying) {
      stopDemoTour();
      renderAllPanels();
      return;
    }

    startDemoTour();
  });

  state.ui.demoFocusButton.addEventListener("click", () => {
    focusPrimaryPatch();
  });

  state.ui.playbackToggleButton.addEventListener("click", () => {
    if (state.playbackPlaying) {
      pausePlayback();
      return;
    }

    startPlayback();
  });

  state.ui.playbackNextButton.addEventListener("click", () => {
    pausePlayback();

    if (!state.patches.length) {
      return;
    }

    const nextIndex = state.selectedPatchIndex == null ? 0 : Math.min(state.selectedPatchIndex + 1, state.patches.length - 1);
    setPlaybackIndex(nextIndex);
  });

  state.ui.playbackResetButton.addEventListener("click", () => {
    pausePlayback();
    resetPlayback();
  });

  state.ui.sourceEditor.addEventListener("input", () => {
    stopDemoTour();
    state.activeScenarioId = null;
    state.ui.editorMessage.textContent = "HTML source가 변경되었습니다. 테스트 영역에 반영하거나 patch를 실행하세요.";
  });

  state.ui.testDomRoot.addEventListener("input", () => {
    stopDemoTour();
    state.activeScenarioId = null;
    syncSourceEditorFromTest();
    state.ui.editorMessage.textContent = "테스트 영역 DOM이 변경되었습니다. Patch를 실행하면 diff가 계산됩니다.";
  });

  state.ui.historyPanel.addEventListener("click", (event) => {
    const target = event.target.closest("[data-history-index]");
    if (!target) {
      return;
    }

    stopDemoTour();
    const index = Number(target.dataset.historyIndex);
    if (Number.isNaN(index)) {
      return;
    }

    state.currentHistoryIndex = index;
    restoreSnapshot(state.history[index]);
  });

  state.ui.scenarioPanel.addEventListener("click", (event) => {
    const button = event.target.closest("[data-scenario-id]");
    if (!button) {
      return;
    }

    stopDemoTour();
    runScenario(button.dataset.scenarioId);
  });

  state.ui.diffLogPanel.addEventListener("click", (event) => {
    const target = event.target.closest("[data-patch-index]");
    if (!target) {
      return;
    }

    pausePlayback();
    setPlaybackIndex(Number(target.dataset.patchIndex));
  });

  state.ui.patchTimelinePanel.addEventListener("click", (event) => {
    const target = event.target.closest("[data-patch-index]");
    if (!target) {
      return;
    }

    pausePlayback();
    setPlaybackIndex(Number(target.dataset.patchIndex));
  });

  state.ui.treePanel.addEventListener("click", (event) => {
    const target = event.target.closest("[data-path]");
    if (!target) {
      return;
    }

    pausePlayback();
    state.selectedPatchIndex = null;
    state.playbackIndex = null;
    selectPath(target.dataset.path);
  });

  bindSurfaceSelection(state.ui.realDomRoot);
  bindSurfaceSelection(state.ui.testDomRoot);

  state.ui.realDomRoot.addEventListener("scroll", renderDomHighlights);
  state.ui.testDomRoot.addEventListener("scroll", renderDomHighlights);
  window.addEventListener("resize", renderDomHighlights);
}

function setupMutationObserver() {
  state.observer = new MutationObserver((mutations) => {
    state.mutationCount += mutations.length;
    updateMetaInfo();
  });

  state.observer.observe(state.ui.realDomRoot, {
    childList: true,
    subtree: true,
    characterData: true,
    attributes: true
  });
}

/* -------------------------------------------------------------------------- */
/* 12. init                                                                    */
/* -------------------------------------------------------------------------- */

function init() {
  state.ui = getElements();
  bindEvents();
  setWorkbenchOpen(false);
  setupMutationObserver();
  resetToSample({
    clearHistory: true
  });
  state.ui.editorMessage.textContent = UI_TEXT.idle;
  window.__VDOM_APP__ = state;
}

window.addEventListener("DOMContentLoaded", init);

