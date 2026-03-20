class BinaryTreeVisualizer extends BaseVisualizer {
    constructor() {
        super();
        this.nodes = [];
        this.root = null;
    }

    onReset() {
        this.clearSvg();
        this.nodes = [];
        this.buildTree();
        this.drawTree(this.root);
        this.setCode(`def preorder(node):\n    if not node:\n        return\n    visit(node)\n    preorder(node.left)\n    preorder(node.right)`);
        this.updateStatus("이진 트리 순회 준비 완료 (기본: Preorder)");
    }

    buildTree() {
        const createNode = (val, x, y) => ({ val, x, y, left: null, right: null });
        this.root = createNode(1, 400, 80);
        this.root.left = createNode(2, 250, 180);
        this.root.right = createNode(3, 550, 180);
        this.root.left.left = createNode(4, 170, 280);
        this.root.left.right = createNode(5, 330, 280);
        this.root.right.left = createNode(6, 470, 280);
        this.root.right.right = createNode(7, 630, 280);
    }

    drawTree(node) {
        if (!node) return;
        if (node.left) {
            this.createEdge(`e-${node.val}-${node.left.val}`, node.x, node.y, node.left.x, node.left.y);
            this.drawTree(node.left);
        }
        if (node.right) {
            this.createEdge(`e-${node.val}-${node.right.val}`, node.x, node.y, node.right.x, node.right.y);
            this.drawTree(node.right);
        }
        this.createNode(node.val, node.x, node.y, node.val);
    }

    *getGenerator() {
        yield* this.genPreorder(this.root);
    }

    *genPreorder(node) {
        yield [1, { node: node ? node.val : 'None', action: 'check' }];
        if (!node) {
            yield [2, { node: 'None', action: 'return' }];
            return;
        }
        yield [3, { node: node.val, action: 'visit' }];
        yield [4, { node: node.val, action: 'go_left' }];
        yield* this.genPreorder(node.left);
        yield [5, { node: node.val, action: 'go_right' }];
        yield* this.genPreorder(node.right);
    }

    onStep(ln, sd) {
        const { node, action } = sd;
        if (typeof node === 'number') {
            let color = '#ecf0f1';
            if (action === 'check') color = '#f1c40f';
            else if (action === 'visit') color = '#2ecc71';
            else if (action === 'go_left' || action === 'go_right') color = '#3498db';
            this.highlightNode(node, color);
        }
    }
}
