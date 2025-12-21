from pydevman.string.rule import Rule, RuleEngine


def test_include_rule():
    foo_rule = Rule(name="foo", strategy="include", patterns=["foo"], priority=1)
    assert foo_rule.match("foobar")
    assert foo_rule.match("bar foo")
    assert not foo_rule.match("bar")


def test_always_rule():
    foo_rule = Rule(name="foo", strategy="always", patterns=["foo"], priority=1)
    assert foo_rule.match("foobar")
    assert foo_rule.match("bar foo")
    assert foo_rule.match("bar")


def test_rules_engine():
    foo_rule = Rule(name="", strategy="include", patterns=["foo"], priority=10)
    baz_rule = Rule(name="", strategy="include", patterns=["baz"], priority=10)
    bar_rule = Rule(name="", strategy="prefix", patterns=["fo"], priority=100)
    default_rule = Rule(name="", strategy="always", patterns=["any"], priority=0)
    engine = RuleEngine()

    engine.register(foo_rule)
    engine.register(baz_rule)
    engine.register(bar_rule)
    engine.register(default_rule)

    assert engine.match("foo") == [bar_rule]
    assert engine.match("baz foo") == [foo_rule, baz_rule]
    assert engine.match("bar") == [default_rule]


def test_rules_engine_v2():
    foo_rule = Rule(name="", strategy="include", patterns=["foo"], priority=0)
    baz_rule = Rule(name="", strategy="include", patterns=["baz"], priority=0)
    bar_rule = Rule(name="", strategy="prefix", patterns=["fo"], priority=0)
    default_rule = Rule(name="", strategy="always", patterns=["any"], priority=0)

    engine = RuleEngine()

    engine.register(foo_rule)
    engine.register(baz_rule)
    engine.register(bar_rule)
    engine.register(default_rule)

    assert engine.match("foobar") == [foo_rule, bar_rule, default_rule]
