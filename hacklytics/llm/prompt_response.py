class PromptResponse():
    def __init__(self, overall_health_status, immediate_issues, immediate_issue_fixes, longterm_issues, longterm_issue_fixes, top_three_recommendations):
        self.overall_health = overall_health_status
        self.immediate_issues = immediate_issues
        self.immediate_issue_fixes = immediate_issue_fixes
        self.longterm_issues = longterm_issues
        self.longterm_issue_fixes = longterm_issue_fixes
        self.top_three_recommendations = top_three_recommendations
