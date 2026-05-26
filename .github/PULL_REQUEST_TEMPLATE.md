## Description

<!-- Brief description of changes -->

## Type of Change

- [ ] 📰 Content (news, publication, project, team member)
- [ ] ✨ Feature (new page, functionality)
- [ ] 🐛 Bug fix
- [ ] 🎨 Style/design change
- [ ] ⚙️ Configuration/CI change
- [ ] 📝 Documentation

## Checklist

- [ ] I tested locally with `docker compose up`
- [ ] I ran `npx prettier . --write` to format my changes
- [ ] Images are optimized (compressed, reasonable size)
- [ ] BibTeX entries are valid (if applicable)
- [ ] Links are not broken

### Content agent submissions

- [ ] Intake JSON validates: `python3 bin/content/intake.py content-intake/...json`
- [ ] Preflight passes: `python3 bin/content/validate.py --skip-build`
- [ ] Expected live URLs documented in PR body
- [ ] After merge: `python3 bin/content/verify_live.py --intake ...`

## Screenshots

<!-- If applicable, add before/after screenshots -->
