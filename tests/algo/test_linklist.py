from devman.algo.linklist import LinkList, ListNode


def test_listnode():
    nums = [1, 2, 3]
    head = ListNode()
    linklist = LinkList(head)
    linklist.add_linklist(nums)
    linklist.traverse_linklist()
