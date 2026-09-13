Sync the knowledge base used by all contract review skills.

Run via Bash:
```bash
python3 knowledge/sync.py
```

Pass `--force` if the user explicitly asked to re-download everything:
```bash
python3 knowledge/sync.py --force
```

The script fetches:
- All finalized EIPs from the ethereum/EIPs GitHub repo → `knowledge/eips/`
- SWC registry entries (SWC-100 through SWC-136) → `knowledge/swc/`
- Solidity security docs (security-considerations, common-patterns, units-and-global-variables, known-bugs) → `knowledge/solidity/`

Already-cached files are skipped unless `--force` is passed. Report the output from the script verbatim.
