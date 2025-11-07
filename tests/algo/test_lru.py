from devman.algo.lru import BuildInLRU


def test_1():
    lru = BuildInLRU(3)
    assert list(lru.cache.keys()) == []
    lru.put("a", "A")
    assert list(lru.cache.keys()) == ["a"]
    assert lru.get("a") == "A"
    lru.put("b", "B")
    assert list(lru.cache.keys()) == ["a", "b"]
    lru.put("c", "C")
    assert list(lru.cache.keys()) == ["a", "b", "c"]
    lru.put("d", "D")
    assert list(lru.cache.keys()) == ["b", "c", "d"]


def test_2():
    lru = BuildInLRU(3)
    assert list(lru.cache.keys()) == []
    lru.put("a", "A")
    assert list(lru.cache.keys()) == ["a"]
    lru.put("b", "B")
    assert list(lru.cache.keys()) == ["a", "b"]
    lru.put("c", "C")
    assert list(lru.cache.keys()) == ["a", "b", "c"]
    lru.put("a", "A")
    assert list(lru.cache.keys()) == ["b", "c", "a"]
