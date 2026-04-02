class BaseVisualizer {
    constructor() {
        this.svg = document.getElementById('viz-svg');
        this.codeArea = document.getElementById('code-content');
        this.stateArea = document.getElementById('state-display');
        this.statusBar = document.getElementById('status-bar');
        this.btnPlay = document.getElementById('btn-play');
        this.btnStep = document.getElementById('btn-step');
        this.btnReset = document.getElementById('btn-reset');
        this.speedScale = document.getElementById('speed-scale');

        this.delay = 800;
        this.isPlaying = false;
        this.generator = null;
        this.timer = null;

        this.setupEventListeners();
    }

    setupEventListeners() {
        this.btnPlay.onclick = () => this.play();
        this.btnStep.onclick = () => this.step();
        this.btnReset.onclick = () => this.reset();
        this.speedScale.oninput = (e) => this.delay = 2100 - e.target.value;
    }

    init() {
        this.reset();
    }

    stop() {
        this.pause();
        this.clearSvg();
    }

    play() {
        if (this.isPlaying) {
            this.pause();
        } else {
            this.isPlaying = true;
            this.btnPlay.textContent = '⏸ Pause';
            this.runAnimation();
        }
    }

    pause() {
        this.isPlaying = false;
        this.btnPlay.textContent = '▶ Play';
        if (this.timer) clearTimeout(this.timer);
    }

    step() {
        this.pause();
        this._doStep();
    }

    reset() {
        this.pause();
        this.generator = null;
        this.clearSvg();
        this.updateStatus("초기화되었습니다.");
        this.onReset();
    }

    _doStep() {
        if (!this.generator) this.generator = this.getGenerator();
        const { value, done } = this.generator.next();
        
        if (done) {
            this.pause();
            this.updateStatus("알고리즘 종료");
            return false;
        }

        const [lineNum, state] = value;
        this.highlightLine(lineNum);
        if (state) this.updateState(state);
        this.onStep(lineNum, state);
        return true;
    }

    runAnimation() {
        if (this.isPlaying) {
            if (this._doStep()) {
                this.timer = setTimeout(() => this.runAnimation(), this.delay);
            } else {
                this.isPlaying = false;
                this.btnPlay.textContent = '▶ Play';
            }
        }
    }

    // --- Display Helpers ---

    clearSvg() {
        while (this.svg.firstChild) this.svg.removeChild(this.svg.firstChild);
        // Add arrow marker
        const defs = document.createElementNS('http://www.w3.org/2000/svg', 'defs');
        const marker = document.createElementNS('http://www.w3.org/2000/svg', 'marker');
        marker.setAttribute('id', 'arrowhead');
        marker.setAttribute('markerWidth', '10');
        marker.setAttribute('markerHeight', '7');
        marker.setAttribute('refX', '20'); 
        marker.setAttribute('refY', '3.5');
        marker.setAttribute('orient', 'auto');
        
        const polygon = document.createElementNS('http://www.w3.org/2000/svg', 'polygon');
        polygon.setAttribute('points', '0 0, 10 3.5, 0 7');
        polygon.setAttribute('fill', '#bdc3c7');
        
        marker.appendChild(polygon);
        defs.appendChild(marker);
        this.svg.appendChild(defs);
    }

    updateStatus(text) {
        this.statusBar.textContent = text;
    }

    setCode(code) {
        this.codeArea.innerHTML = code.split('\n').map((line, i) => 
            `<span class="code-line" data-line="${i+1}">${line || '&nbsp;'}</span>`
        ).join('');
    }

    highlightLine(lineNum) {
        document.querySelectorAll('.code-line').forEach(el => el.classList.remove('active'));
        const line = document.querySelector(`.code-line[data-line="${lineNum}"]`);
        if (line) {
            line.classList.add('active');
            line.scrollIntoView({ behavior: 'smooth', block: 'center' });
        }
    }

    updateState(stateDict) {
        this.stateArea.innerHTML = Object.entries(stateDict)
            .map(([k, v]) => `
                <div class="state-item">
                    <span class="state-key">${k}:</span>
                    <span class="state-val">${Array.isArray(v) ? '[' + v.join(', ') + ']' : v}</span>
                </div>
            `).join('');
    }

    // --- SVG Helpers ---

    createNode(id, x, y, label, color = '#ecf0f1') {
        const g = document.createElementNS('http://www.w3.org/2000/svg', 'g');
        g.setAttribute('id', `node-group-${id}`);

        const circle = document.createElementNS('http://www.w3.org/2000/svg', 'circle');
        circle.setAttribute('cx', x);
        circle.setAttribute('cy', y);
        circle.setAttribute('r', 22);
        circle.setAttribute('fill', color);
        circle.setAttribute('stroke', '#2c3e50');
        circle.setAttribute('stroke-width', '2');
        circle.setAttribute('id', `node-circle-${id}`);
        circle.style.transition = 'all 0.3s';

        const text = document.createElementNS('http://www.w3.org/2000/svg', 'text');
        text.setAttribute('x', x);
        text.setAttribute('y', y + 5);
        text.setAttribute('text-anchor', 'middle');
        text.setAttribute('font-size', '12px');
        text.setAttribute('font-weight', 'bold');
        text.textContent = label;

        g.appendChild(circle);
        g.appendChild(text);
        this.svg.appendChild(g);
        return g;
    }

    createEdge(id1, id2, x1, y1, x2, y2, directed = false) {
        const line = document.createElementNS('http://www.w3.org/2000/svg', 'line');
        line.setAttribute('x1', x1);
        line.setAttribute('y1', y1);
        line.setAttribute('x2', x2);
        line.setAttribute('y2', y2);
        line.setAttribute('stroke', '#bdc3c7');
        line.setAttribute('stroke-width', '2');
        if (directed) {
            line.setAttribute('marker-end', 'url(#arrowhead)');
        }
        this.svg.insertBefore(line, this.svg.firstChild);
        return line;
    }

    highlightNode(id, color) {
        const el = document.getElementById(`node-circle-${id}`);
        if (el) el.setAttribute('fill', color);
    }

    // --- Abstract Methods ---
    getGenerator() { throw new Error('Not implemented'); }
    onStep(ln, sd) { }
    onReset() { }
}
