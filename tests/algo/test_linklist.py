from pydevman.algo.linklist import LinkList, ListNode


def test_listnode():
    nums = [1, 2, 3]
    head = ListNode()
    linklist = LinkList(head)
    linklist.build_from_list(nums)
    linklist.traverse_linklist()
