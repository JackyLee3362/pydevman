import re
from abc import ABC, abstractmethod


class StringMatcher(ABC):
    @abstractmethod
    def match(self, pattern: str, string: str) -> bool: ...


class EqualStringMatcher(StringMatcher):
    def match(self, pattern, string):
        return pattern.lower() == string.lower()


class IncludeStringMatcher(StringMatcher):
    def match(self, pattern, string):
        return pattern.lower() in string.lower()


class PrefixStringMatcher(StringMatcher):
    def match(self, pattern, string):
        return string.lower().startswith(pattern.lower())


class SuffixStringMatcher(StringMatcher):
    def match(self, pattern, string):
        return string.lower().endswith(pattern.lower())


class RegexStringMatcher(StringMatcher):
    def match(self, pattern, string):
        return re.match(pattern, string) is not None
