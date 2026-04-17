# GitHub Repository Setup Guide

**Purpose**: Initialize GitHub repository for team submission  
**Team Size**: 4 Students  
**Framework**: CrewAI (Multi-Agent System)

---

## Step 1: Create GitHub Repository

**Option A: One team member creates (recommended)**

1. Go to https://github.com/new
2. Fill in:
   - **Repository name**: `devops-helper-mas` (or your choice)
   - **Description**: "Multi-Agent System for DevOps Pipeline Monitoring - SE4010 CTSE Assignment 2"
   - **Visibility**: Public or Private (check with instructor)
   - **Add README**: No (we already have one)
   - **Add .gitignore**: Python
   - **License**: MIT or Academic

3. Click "Create repository"

**Option B: Existing repository**
- If repository exists, skip to Step 3

---

## Step 2: Add Collaborators

1. Go to repository Settings → Collaborators
2. Email invite all 4 team members
3. Each member accepts invitation

---

## Step 3: Clone Locally

```bash
# One team member:
git clone https://github.com/YOUR_USERNAME/devops-helper-mas.git
cd devops-helper-mas

# Other team members:
git clone https://github.com/YOUR_USERNAME/devops-helper-mas.git
cd devops-helper-mas
```

---

## Step 4: Copy Files to Repository

```bash
# Copy all files from current project
# Make sure you're in the cloned directory

cp d:\Devops Agent\* .
cp -r d:\Devops Agent\src ./
cp -r d:\Devops Agent\tests ./
cp -r d:\Devops Agent\pipeline ./
cp -r d:\Devops Agent\logs ./
```

---

## Step 5: Remove Sensitive Files

Before committing:

```bash
# Remove environment file
rm .env

# Keep .env.example for templates
# .env.example should be in repo, .env should NOT

# Verify .gitignore includes:
# .env
# .env.local
# __pycache__/
# *.pyc
# venv/
# logs/
```

---

## Step 6: Initial Commit

```bash
git add .
git commit -m "Initial commit: Complete multi-agent system for CTSE assignment 2"
git push origin main
```

---

## Step 7: Set Up Branching Strategy

Each student works on separate branch:

```bash
# Student 1: Pipeline Monitor
git checkout -b feature/pipeline-monitor-agent
# Make changes, commit, push

# Student 2: Error Analyzer
git checkout -b feature/error-analyzer-agent

# Student 3: Solution Generator
git checkout -b feature/solution-generator-agent

# Student 4: Notification Agent
git checkout -b feature/notification-agent
```

---

## Step 8: Create Pull Requests

Each student creates PR for review:

```bash
# After committing your changes:
git push origin feature/YOUR_FEATURE

# Then create PR on GitHub:
# 1. Go to repository
# 2. Click "New Pull Request"
# 3. Select your feature branch
# 4. Add description
# 5. Request review from teammates
# 6. Merge after approval
```

---

## Step 9: Link Assignment Information

Add to repository description and README:

```markdown
## Assignment Information
- **Course**: SE4010 - CTSE (Collaborative Tagged Software Engineering)
- **Assignment**: Assignment 2 - Machine Learning Multi-Agent System
- **University**: Sri Lanka Institute of Information Technology
- **Team Size**: 4 Students
- **Framework**: CrewAI (Multi-Agent Orchestration)
- **LLM Engine**: Ollama (Local, No Cloud APIs)

## Team Members
- Student 1: [Name] - Pipeline Monitor Agent
- Student 2: [Name] - Error Analyzer Agent  
- Student 3: [Name] - Solution Generator Agent
- Student 4: [Name] - Notification Agent
```

---

## Step 10: Document Individual Contributions

Update `TECHNICAL_REPORT_TEMPLATE.md` Section 8 with:

```
### Student 1: [Full Name]
**GitHub Username**: @username
**Agent Developed**: Pipeline Monitor Agent
**Tool Implemented**: execute_pipeline_stage()
**Test Cases**: PipelineMonitorAgentTests (6 tests)
**Commits**:
- abc123 - Implement Pipeline Monitor Agent
- def456 - Add execute_pipeline_stage() tool
- ghi789 - Add test cases

### Student 2: [Full Name]
...
```

---

## Step 11: Weekly Syncs

Create Issues for tracking:

```bash
# GitHub Issues for coordination

Issue 1: "Agent Design Review"
Issue 2: "Tool Implementation Status"
Issue 3: "Test Coverage"
Issue 4: "Technical Report"
Issue 5: "Demo Video"
```

---

## Step 12: Final Submission

**Before submitting to instructor**:

1. ✅ All code committed
2. ✅ All branches merged to main
3. ✅ All tests passing
4. ✅ README complete
5. ✅ Technical report complete
6. ✅ Commit history has all 4 students
7. ✅ .env NOT committed (only .env.example)
8. ✅ No merge conflicts
9. ✅ Documentation complete
10. ✅ Repository public (or access given to instructor)

---

## Repository Structure (After Setup)

```
devops-helper-mas/
├── .github/
│   └── workflows/
│       └── tests.yml          # Optional: CI/CD
├── src/
│   ├── agents.py
│   ├── tools.py
│   ├── state_management.py
│   ├── observability.py
│   ├── config.py
│   ├── pipeline.py
│   ├── analyzer.py
│   ├── ai_agent.py
│   ├── email_service.py
│   └── __init__.py
├── tests/
│   ├── test_agents.py
│   └── __init__.py
├── pipeline/
│   ├── stages.py
│   └── __init__.py
├── logs/
│   └── .gitkeep
├── .gitignore
├── .env.example
├── README.md
├── ARCHITECTURE.md
├── QUICKSTART.md
├── STUDENT_GUIDE.md
├── DEMO_SCRIPT.md
├── SUBMISSION_SUMMARY.md
├── TECHNICAL_REPORT_TEMPLATE.md
├── main_mas.py
├── main.py
├── requirements.txt
├── setup.bat
├── setup.sh
└── GITHUB_SETUP.md          # This file
```

---

## Git Commands Reference

```bash
# View branches
git branch -a

# Create new branch
git checkout -b feature/my-feature

# Switch branch
git checkout feature/my-feature

# View changes
git status
git diff

# Commit changes
git add .
git commit -m "Descriptive message"
git push origin feature/my-feature

# View history
git log --oneline
git log --author="Student Name"

# Merge branch
git checkout main
git merge feature/my-feature

# View graph
git log --graph --oneline --all

# Undo changes
git reset --soft HEAD~1    # Undo last commit, keep changes
git reset --hard HEAD~1    # Undo last commit, discard changes
```

---

## Commit Message Convention

Use consistent format:

```
[Agent] Brief description

More detailed explanation if needed.

Fixes issue: #123
Changes requested by: @teammate
```

Examples:
```
[Pipeline Monitor] Implement execute_pipeline_stage() tool
[Error Analyzer] Add error categorization logic
[Solution Generator] Implement fix step generation
[Notification] Add email sending functionality
[Tests] Add 6 test cases for pipeline monitor
[Docs] Update TECHNICAL_REPORT with architecture
```

---

## Code Review Checklist

Before merging PR:

- [ ] Code follows style guide
- [ ] Type hints on all functions
- [ ] Docstrings present and complete
- [ ] Test cases added/updated
- [ ] No hardcoded credentials/secrets
- [ ] .env file NOT committed
- [ ] Comments explain complex logic
- [ ] No merge conflicts
- [ ] All tests passing
- [ ] Teammate approval received

---

## Troubleshooting

### Merge Conflicts
```bash
# If conflicts when merging:
git merge --abort        # Cancel merge
# Fix conflicts manually, then:
git add .
git commit -m "Resolve merge conflicts"
```

### Accidentally Committed .env
```bash
# Remove from Git history:
git rm --cached .env
git commit --amend -m "Remove .env from tracking"
```

### Large Files
```bash
# Use Git LFS for large files:
git lfs install
git lfs track "*.bin"
git add .gitattributes
```

---

## Instructor Access

**To give instructor access**:

1. Go to Settings → Collaborators
2. Click "Add people"
3. Enter instructor's GitHub username
4. Select "Admin" or "Maintainer" role
5. Send invitation

**Alternatively**: Make repository public (if allowed)

---

## Additional Resources

- Git Documentation: https://git-scm.com/doc
- GitHub Help: https://docs.github.com
- CrewAI: https://docs.crewai.io
- Ollama: https://ollama.ai

---

## Timeline Suggestion

| Week | Milestone |
|------|-----------|
| Week 1 | Repository setup, environment configuration |
| Week 2 | Agent implementations (each student) |
| Week 3 | Tool implementations (each student) |
| Week 4 | Testing & integration (all students) |
| Week 5 | Documentation & demo video (all students) |
| Week 6 | Final review & submission (all students) |

---

## Final Checklist Before Submission

```
BEFORE SUBMITTING TO INSTRUCTOR:

Code Quality:
- [ ] All 4 agents complete
- [ ] All tools implemented
- [ ] 34 tests all passing
- [ ] No syntax errors
- [ ] Type hints complete
- [ ] Docstrings complete

Version Control:
- [ ] All changes committed
- [ ] All branches merged
- [ ] No merge conflicts
- [ ] .env NOT in repository
- [ ] .env.example IN repository
- [ ] All student names in git history

Documentation:
- [ ] README.md complete
- [ ] ARCHITECTURE.md complete
- [ ] STUDENT_GUIDE.md complete
- [ ] TECHNICAL_REPORT_TEMPLATE.md filled out
- [ ] DEMO_SCRIPT.md used for video

Testing:
- [ ] All 34 tests passing
- [ ] Configuration validated
- [ ] System runs without errors
- [ ] Email configuration verified

Submission:
- [ ] Repository link ready
- [ ] Demo video (4-5 min) uploaded
- [ ] Technical report (4-8 pages) ready
- [ ] All files in repository

INSTRUCTOR ACCESS:
- [ ] Instructor has repository access
- [ ] Can view all commits
- [ ] Can run tests
- [ ] Can review code
```

---

**Setup Complete!** 🎉

You're ready to start development. Remember:
- Communicate with teammates via GitHub Issues
- Review each other's code via Pull Requests
- Document everything as you go
- Test frequently
- Commit regularly

Good luck with your assignment!
