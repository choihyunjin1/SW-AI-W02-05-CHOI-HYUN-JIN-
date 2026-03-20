class Solution:
    def maxDepth(self, root: Optional[TreeNode]) -> int:
        # 1. 노드가 없으면 깊이 0
        if root is None:
            return 0

        # 2. 왼쪽 / 오른쪽 깊이 구하기
        left = self.maxDepth(root.left)
        right = self.maxDepth(root.right)

        # 3. 현재 노드 포함
        return 1 + max(left, right)