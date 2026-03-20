class TopoSortVisualizer extends BaseVisualizer {
    constructor() {
        super();
        this.nodes = { 1: [100, 150], 2: [250, 100], 3: [400, 150], 4: [100, 300], 5: [250, 250], 6: [400, 300] };
        this.edges = [[1, 4], [1, 2], [2, 5], [2, 3], [4, 5], [3, 6]];
        this.adj = { 1: [4, 2], 2: [5, 3], 3: [6], 4: [5], 5: [], 6: [] };
        this.origInDegree = { 1: 0, 2: 1, 3: 1, 4: 1, 5: 2, 6: 1 };
    }

    onReset() {
        this.clearSvg();
        this.drawGraph(this.origInDegree);
        this.setCode(`def topological_sort(graph, in_degree):\n    queue = [n for n in graph if in_degree[n] == 0]\n    result = []\n    while queue:\n        curr = queue.pop(0)\n        result.append(curr)\n        for neighbor in graph[curr]:\n            in_degree[neighbor] -= 1\n            if in_degree[neighbor] == 0:\n                queue.append(neighbor)`);
        this.updateStatus("위상 정렬 준비 완료");
    }

    drawGraph(inDegree) {
        this.edges.forEach(([u, v]) => {
            this.createEdge(`e-${u}-${v}`, this.nodes[u][0], this.nodes[u][1], this.nodes[v][0], this.nodes[v][1], true);
        });
        Object.entries(this.nodes).forEach(([id, [x, y]]) => {
            const g = this.createNode(id, x, y, id);
            
            // In-degree label
            const deg = inDegree[id];
            const color = deg > 0 ? '#f85149' : '#3fb950';
            const rect = document.createElementNS('http://www.w3.org/2000/svg', 'rect');
            rect.setAttribute('x', x + 15);
            rect.setAttribute('y', y - 35);
            rect.setAttribute('width', 20);
            rect.setAttribute('height', 15);
            rect.setAttribute('fill', color);
            rect.setAttribute('id', `deg-rect-${id}`);
            
            const text = document.createElementNS('http://www.w3.org/2000/svg', 'text');
            text.setAttribute('x', x + 25);
            text.setAttribute('y', y - 24);
            text.setAttribute('text-anchor', 'middle');
            text.setAttribute('font-size', '10px');
            text.setAttribute('fill', 'white');
            text.setAttribute('id', `deg-text-${id}`);
            text.textContent = deg;
            
            g.appendChild(rect);
            g.appendChild(text);
        });
    }

    *getGenerator() {
        const inDegree = { ...this.origInDegree };
        const queue = Object.keys(this.nodes).filter(n => inDegree[n] === 0).map(Number);
        const result = [];
        yield [3, { queue: [...queue], result: [...result], inDegree: { ...inDegree } }];
        
        while (queue.length > 0) {
            const curr = queue.shift();
            result.push(curr);
            yield [8, { curr, queue: [...queue], result: [...result], inDegree: { ...inDegree } }];
            
            for (const neighbor of this.adj[curr]) {
                inDegree[neighbor] -= 1;
                yield [11, { curr, neighbor, inDegree: { ...inDegree } }];
                if (inDegree[neighbor] === 0) {
                    queue.push(neighbor);
                    yield [14, { curr, neighbor, queue: [...queue], inDegree: { ...inDegree } }];
                }
            }
        }
    }

    onStep(ln, sd) {
        const { curr, result, queue, inDegree, neighbor } = sd;
        if (inDegree) {
            Object.entries(inDegree).forEach(([id, deg]) => {
                const rect = document.getElementById(`deg-rect-${id}`);
                const text = document.getElementById(`deg-text-${id}`);
                if (rect) rect.setAttribute('fill', deg > 0 ? '#f85149' : '#3fb950');
                if (text) text.textContent = deg;
            });
        }
        if (result) {
            result.forEach(v => this.highlightNode(v, '#3fb950'));
        }
        if (queue) {
            queue.forEach(v => this.highlightNode(v, '#d29922'));
        }
        if (curr) {
            this.highlightNode(curr, '#f85149');
        }
    }
}
