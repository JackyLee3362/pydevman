from devman.algo.tree import Tree


def test_tree():
    nums = [3, 1, 5, 0, 2, 4, 6]
    nums = [1, 2, 3, 4]
    tree = Tree(None)
    tree.add_tree(nums)
    print("preorder")
    tree.preorder(tree.root)
    print("inorder")
    tree.inorder(tree.root)
    print("postorder")
    tree.postorder(tree.root)
