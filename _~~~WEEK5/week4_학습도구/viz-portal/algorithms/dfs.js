class DFSVisualizer extends BaseVisualizer {
    constructor() {
        super();
        this.nodes = { 1: [150, 150], 2: [300, 50], 3: [450, 150], 4: [150, 300], 5: [300, 300], 6: [450, 300] };
        this.edges = [[1, 2], [1, 3], [2, 4], [2, 5], [3, 6], [4, 5]];
        this.adj = { 1: [2, 3], 2: [1, 4, 5], 3: [1, 6], 4: [2, 5], 5: [2, 4], 6: [3] };
    }

    onReset() {
        this.clearSvg();
        this.drawGraph();
        this.setCode(`def dfs_traversal(graph, start):\n    visited = set()\n    stack = [start]\n    while stack:\n        curr = stack.pop()\n        if curr not in visited:\n            visited.add(curr)\n            for neighbor in reversed(graph[curr]):\n                if neighbor not in visited:\n                    stack.append(neighbor)`);
        this.updateStatus("DFS 탐색 준비 완료");
    }

    drawGraph() {
        this.edges.forEach(([u, v]) => {
            this.createEdge(`e-${u}-${v}`, this.nodes[u][0], this.nodes[u][1], this.nodes[v][0], this.nodes[v][1]);
        });
        Object.entries(this.nodes).forEach(([id, [x, y]]) => {
            this.createNode(id, x, y, id);
        });
    }

    *getGenerator() {
        const start = 1;
        const visited = new Set();
        const stack = [start];
        yield [4, { stack: [...stack], visited: [...visited] }];
        while (stack.length > 0) {
            const curr = stack.pop();
            yield [6, { curr, stack: [...stack], visited: [...visited] }];
            if (!visited.has(curr)) {
                visited.add(curr);
                yield [8, { curr, stack: [...stack], visited: [...visited] }];
                for (const neighbor of [...this.adj[curr]].reverse()) {
                    if (!visited.has(neighbor)) {
                        stack.push(neighbor);
                        yield [12, { curr, neighbor, stack: [...stack] }];
                    }
                }
            }
        }
    }

    onStep(ln, sd) {
        const { curr, visited, neighbor } = sd;
        if (visited) {
            visited.forEach(v => this.highlightNode(v, '#2ecc71'));
        }
        if (curr) {
            this.highlightNode(curr, '#f85149');
        }
        if (neighbor) {
            this.highlightNode(neighbor, '#9b59b6');
        }
    }
}
