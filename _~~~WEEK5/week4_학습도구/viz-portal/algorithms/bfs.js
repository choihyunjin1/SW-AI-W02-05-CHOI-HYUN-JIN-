class BFSVisualizer extends BaseVisualizer {
    constructor() {
        super();
        this.nodes = { 1: [150, 150], 2: [300, 50], 3: [450, 150], 4: [150, 300], 5: [300, 300], 6: [450, 300] };
        this.edges = [[1, 2], [1, 4], [2, 3], [2, 5], [3, 6], [4, 5]];
        this.adj = { 1: [2, 4], 2: [1, 3, 5], 3: [2, 6], 4: [1, 5], 5: [2, 4], 6: [3] };
    }

    onReset() {
        this.clearSvg();
        this.drawGraph();
        this.setCode(`def bfs_traversal(graph, start):\n    visited = {start}\n    queue = [start]\n    while queue:\n        curr = queue.pop(0)\n        for neighbor in graph[curr]:\n            if neighbor not in visited:\n                visited.add(neighbor)\n                queue.append(neighbor)`);
        this.updateStatus("BFS 탐색 준비 완료");
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
        const visited = new Set([start]);
        const queue = [start];
        yield [4, { queue: [...queue], visited: [...visited] }];
        while (queue.length > 0) {
            const curr = queue.shift();
            yield [6, { curr, queue: [...queue], visited: [...visited] }];
            for (const neighbor of this.adj[curr]) {
                if (!visited.has(neighbor)) {
                    visited.add(neighbor);
                    queue.push(neighbor);
                    yield [10, { curr, neighbor, queue: [...queue], visited: [...visited] }];
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
            this.highlightNode(neighbor, '#f1c40f');
        }
    }
}
