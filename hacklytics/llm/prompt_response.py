class PromptResponse():
    def __init__(self, immediate_issues, immediate_issue_fixes, longterm_issues, longterm_issue_fixes):
        self.immediate_issues = immediate_issues
        self.immediate_issue_fixes = immediate_issue_fixes
        self.longterm_issues = longterm_issues
        self.longterm_issue_fixes = longterm_issue_fixes
