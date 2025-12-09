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
    foo_rule = Rule(name="foo", strategy="include", patterns=["foo"], priority=10)
    baz_rule = Rule(name="foo", strategy="include", patterns=["baz"], priority=10)
    bar_rule = Rule(name="foo", strategy="prefix", patterns=["fo"], priority=100)
    default_rule = Rule(name="foo", strategy="always", patterns=["any"], priority=0)
    engine = RuleEngine()

    engine.register(foo_rule)
    engine.register(baz_rule)
    engine.register(bar_rule)
    engine.register(default_rule)

    engine.match("foo") == [bar_rule]
    engine.match("baz foo") == [foo_rule, baz_rule]
    engine.match("bar") == [default_rule]
