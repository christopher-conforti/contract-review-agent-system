Sync the global knowledge base used by all contract review skills.

Run via Bash:
```bash
python3 ~/.claude/knowledge/sync.py
```

Pass `--force` if the user explicitly asked to re-download everything:
```bash
python3 ~/.claude/knowledge/sync.py --force
```

The script fetches into `~/.claude/knowledge/`:
- All finalized EIPs from the ethereum/EIPs GitHub repo → `eips/`
- SWC registry entries (SWC-100 through SWC-136) → `swc/`
- Solidity security docs (security-considerations, common-patterns, units-and-global-variables, known-bugs) → `solidity/`

Already-cached files are skipped unless `--force` is passed. Report the output from the script verbatim.
