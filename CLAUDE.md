# CLAUDE.md

This file provides guidance for AI assistants working with the RATT repository.

## Repository Overview

**RATT** is a new project owned by `bfeeny`. The repository is currently in its initial setup phase.

## Project Structure

```
RATT/
├── CLAUDE.md          # AI assistant guidance (this file)
└── (project files TBD)
```

As the project grows, update this section to reflect the directory layout.

## Development Workflow

### Git Conventions

- **Default branch:** `main`
- Write clear, descriptive commit messages in imperative mood (e.g., "Add feature X", not "Added feature X")
- Keep commits focused — one logical change per commit
- Push feature branches and open pull requests for review

### Branch Naming

- Feature branches: `feature/<short-description>`
- Bug fixes: `fix/<short-description>`
- Documentation: `docs/<short-description>`

### Code Style

- Follow the conventions of whichever language(s) are adopted for this project
- Prefer readability over cleverness
- Keep functions small and focused

### Testing

- Add tests for new functionality
- Run the full test suite before pushing changes
- Do not merge code with failing tests

## Commands

_No build/test commands configured yet. Update this section as tooling is added._

<!-- Example entries to fill in later:
```
npm install        # Install dependencies
npm test           # Run tests
npm run build      # Build the project
npm run lint       # Lint code
```
-->

## Key Conventions for AI Assistants

1. **Read before editing** — Always read a file before modifying it
2. **Minimal changes** — Only change what is necessary to accomplish the task
3. **No over-engineering** — Keep solutions simple; avoid premature abstractions
4. **Security first** — Do not introduce vulnerabilities (injection, XSS, etc.)
5. **No secrets in code** — Never commit credentials, API keys, or tokens
6. **Preserve existing patterns** — Match the style and conventions already present in the codebase
7. **Test your changes** — Run available tests after making modifications
