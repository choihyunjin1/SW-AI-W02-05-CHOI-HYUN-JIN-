const fs = require('fs');
let code = fs.readFileSync('benchmark/app.js', 'utf8');

const helpers = `
function setManualStatus(label, description) {
  state.ui.currentStateLabel.textContent = label;
  state.ui.currentStateDescription.textContent = description;
}
`;

if (!code.includes('function setManualStatus(')) {
  code = code.replace('function startExecutionCycle(', helpers + '\nfunction startExecutionCycle(');
  fs.writeFileSync('benchmark/app.js', code);
  console.log('Fixed benchmark/app.js: setManualStatus restored.');
} else {
  console.log('benchmark/app.js already has setManualStatus.');
}
