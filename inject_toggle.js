const fs = require('fs');
let code = fs.readFileSync('benchmark/app.js', 'utf8');

const toggleScript = `
window.toggleRuntimeList = function() {
  state.ui.listExpanded = !state.ui.listExpanded;
  const wrapper = document.querySelector('.runtime-list-wrapper');
  const toggleBtn = document.querySelector('.runtime-list-toggle button');
  if (wrapper) {
    if (state.ui.listExpanded) {
      wrapper.classList.remove('is-collapsed');
      if (toggleBtn) toggleBtn.textContent = '접기 (가리기)';
    } else {
      wrapper.classList.add('is-collapsed');
      if (toggleBtn) toggleBtn.textContent = '모든 노드 보기 (펼치기)';
    }
  }
};
`;

if (!code.includes('window.toggleRuntimeList')) {
  code = code.replace('const elements = {', toggleScript + '\nconst elements = {');
  fs.writeFileSync('benchmark/app.js', code);
  console.log('toggleRuntimeList carefully injected.');
} else {
  console.log('toggleRuntimeList already exists.');
}
