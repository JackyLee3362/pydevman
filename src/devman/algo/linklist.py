from __future__ import annotations

from typing import List, Optional


class ListNode:
    def __init__(
        self, val: Optional[int] = None, next_: Optional[ListNode] = None
    ) -> None:
        self.val = val
        self.next_ = next_


class LinkList:
    def __init__(self, head: ListNode) -> None:
        """
        create linklist with head
        """
        self.head = head

    def traverse_linklist(self, call=print) -> None:
        """
        traverse link list
        """
        node = self.head
        while node:
            call(node.val)
            node = node.next_

    def add_linklist(self, nums: List[int]) -> None:
        """
        build linklist with list
        """
        node = self.head
        for i in range(len(nums)):
            next_node = ListNode(nums[i], None)
            node.next_ = next_node
            node = next_node
