class BSTVisualizer extends BaseVisualizer {
    constructor() {
        super();
        this.nodesData = {
            1: { val: 50, left: 2, right: 3, x: 400, y: 80 },
            2: { val: 30, left: 4, right: 5, x: 250, y: 180 },
            3: { val: 70, left: 6, right: 7, x: 550, y: 180 },
            4: { val: 20, left: 8, right: 9, x: 150, y: 280 },
            5: { val: 40, left: 10, right: 11, x: 350, y: 280 },
            6: { val: 60, left: 12, right: null, x: 450, y: 280 },
            7: { val: 80, left: null, right: null, x: 650, y: 280 },
            8: { val: 10, left: null, right: null, x: 100, y: 380 },
            9: { val: 25, left: null, right: null, x: 200, y: 380 },
            10: { val: 35, left: null, right: null, x: 300, y: 380 },
            11: { val: 45, left: null, right: null, x: 400, y: 380 },
            12: { val: 55, left: null, right: null, x: 500, y: 380 }
        };
        this.target = 45;
    }

    onReset() {
        this.clearSvg();
        this.drawTree();
        this.setCode(`def bst_search(node, target):\n    curr = node\n    while curr:\n        if curr.val == target:\n            return curr\n        if target < curr.val:\n            curr = curr.left\n        else:\n            curr = curr.right\n    return None`);
        this.updateStatus(`타겟 ${this.target}을(를) 검색할 준비 완료`);
    }

    drawTree() {
        Object.values(this.nodesData).forEach(v => {
            if (v.left) {
                const left = this.nodesData[v.left];
                this.createEdge(`e-${v.val}-${left.val}`, v.x, v.y, left.x, left.y);
            }
            if (v.right) {
                const right = this.nodesData[v.right];
                this.createEdge(`e-${v.val}-${right.val}`, v.x, v.y, right.x, right.y);
            }
        });
        Object.values(this.nodesData).forEach(v => {
            this.createNode(v.val, v.x, v.y, v.val);
        });

        // Target display
        const text = document.createElementNS('http://www.w3.org/2000/svg', 'text');
        text.setAttribute('x', 50);
        text.setAttribute('y', 50);
        text.setAttribute('font-size', '16px');
        text.setAttribute('font-weight', 'bold');
        text.setAttribute('fill', '#f85149');
        text.textContent = `찾을 값: ${this.target}`;
        this.svg.appendChild(text);
    }

    *getGenerator() {
        let curr = this.nodesData[1];
        yield [2, { curr: curr.val, action: 'init' }];
        while (curr) {
            yield [3, { curr: curr.val, action: 'check_while' }];
            yield [4, { curr: curr.val, action: 'check_target' }];
            if (curr.val === this.target) {
                yield [5, { curr: curr.val, action: 'found' }];
                return;
            }
            yield [6, { curr: curr.val, action: 'check_left' }];
            if (this.target < curr.val) {
                curr = this.nodesData[curr.left];
                yield [7, { curr: curr ? curr.val : 'None', action: 'go_left' }];
            } else {
                yield [8, { curr: curr.val, action: 'go_right' }];
                curr = this.nodesData[curr.right];
                yield [9, { curr: curr ? curr.val : 'None', action: 'moved_right' }];
            }
        }
        yield [10, { curr: 'None', action: 'not_found' }];
    }

    onStep(ln, sd) {
        const { curr, action } = sd;
        if (typeof curr === 'number') {
            const color = action === 'found' ? '#2ecc71' : '#f85149';
            this.highlightNode(curr, color);
        }
    }
}
