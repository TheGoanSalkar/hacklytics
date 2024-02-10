import unittest

from llm.prompt import get_issues_and_fixes

class TestPrompt(unittest.TestCase):
    def test_prompt(self):
        get_issues_and_fixes('Damage from within the home due to a tornado')

if __name__ == '__main__':
    unittest.main()