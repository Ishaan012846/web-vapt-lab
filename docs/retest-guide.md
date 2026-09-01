# Vulnerability Retest Procedure

## Purpose
Retesting ensures that remediation patches deployed by developers effectively eliminate identified security risks without introducing regressions.

## Retest Workflow

```
+------------------+     +-------------------+     +--------------------+
| 1. Review Patch  | --> | 2. Execute Test   | --> | 3. Update Finding  |
| (CodeDiff Audit) |     | (Automated/Manual)|     | (retest_status)    |
+------------------+     +-------------------+     +--------------------+
```

### Steps:
1. **Pull Patch Code**: Check out updated codebase inside local lab environment.
2. **Re-run Automated Scans**:
   ```bash
   make scan
   ```
3. **Execute Manual Regression Verification**: Follow steps in `docs/manual-testing-guide.md` for target finding IDs.
4. **Update Findings Model**: Update `retest_status` field in `findings/findings.example.json` or normalized dataset:
   - `passed`: Vulnerability is fully resolved.
   - `failed`: Remediation was incomplete or bypassed.
5. **Re-generate Dashboard & Report**:
   ```bash
   make report
   ```
