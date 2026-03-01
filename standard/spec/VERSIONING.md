# DMG Versioning Strategy

Version: 1.0  
Status: Draft  
Last Updated: 2026-01-26

---

## 1. Version Format

DMG uses Semantic Versioning (SemVer):

```
MAJOR.MINOR
```

- **MAJOR**: Breaking changes to core schema or semantics
- **MINOR**: Backward-compatible additions

Current version: **0.1** (pre-release)

---

## 2. Version Field

Every DMG document MUST include a version field:

```json
{
  "dmg_version": "0.1",
  ...
}
```

---

## 3. Compatibility Rules

### 3.1 Backward Compatibility

| Change Type | Compatibility | Example |
|-------------|---------------|---------|
| New optional field | ✅ Backward compatible | Adding `memo.tags` |
| New object type | ✅ Backward compatible | Adding `objects.impacts[]` |
| New event type | ✅ Backward compatible | Adding `IMPACT_ASSESSED` |
| Field type change | ❌ Breaking | `ramp.level` string→int |
| Remove required field | ❌ Breaking | Removing `memo.decision` |
| Rename field | ❌ Breaking | `memo_id` → `id` |

### 3.2 Forward Compatibility

Implementations SHOULD ignore unknown fields to enable forward compatibility.

```python
# Good: ignore unknown fields
def parse_memo(data: dict) -> Memo:
    return Memo(
        memo_id=data["memo_id"],
        title=data["title"],
        # unknown fields are ignored
    )
```

---

## 4. Version Roadmap

### v0.1 (Current)
- Core primitives: MEMO, MOMENT, OUTCOME, DOORS, DISSENT, TRACE, COMMIT
- RAMP levels 1-5
- MERIT validation framework
- Hash chain for event integrity

### v0.2 (Planned)
- Formal JSON Schema publication
- Signature field for events (optional)
- Cross-reference linking between decisions
- Batch/series support for related decisions

### v1.0 (Target Stable)
- Schema frozen for production use
- Full conformance test suite
- SDK packages (npm, PyPI)
- IANA media type registration

---

## 5. Migration Paths

### 5.1 v0.1 → v0.2

**Expected changes:**
- New optional `signature` field on events
- New optional `linked_decisions[]` on memo
- No breaking changes

**Migration:** None required (backward compatible)

### 5.2 v0.x → v1.0

**Potential breaking changes:**
- Field renames (if any) will be documented
- Schema tightening (optional fields becoming required)

**Migration:** Automated migration script will be provided:

```bash
dmg migrate --from 0.1 --to 1.0 <file.dmg.json>
```

---

## 6. Deprecation Policy

### 6.1 Deprecation Notices

Deprecated fields will be:
1. Documented in spec with `[DEPRECATED]` tag
2. Logged as warnings by validators
3. Removed only in MAJOR version bumps

### 6.2 Support Timeline

| Version | Status | Support |
|---------|--------|---------|
| 0.1 | Current | Full support |
| 0.2 | Planned | Will be supported |
| 1.0 | Target | LTS candidate |

---

## 7. Validation Behavior

### 7.1 Version Checking

```python
def validate_version(dmg: dict) -> bool:
    version = dmg.get("dmg_version", "")
    major, minor = version.split(".")
    
    # Accept same major version
    if int(major) == SUPPORTED_MAJOR:
        return True
    
    # Warn on newer minor version
    if int(minor) > SUPPORTED_MINOR:
        warn(f"Document version {version} is newer than validator")
    
    return True
```

### 7.2 Version Warnings

| Scenario | Behavior |
|----------|----------|
| Same version | ✅ Normal validation |
| Older document | ✅ Validate with compatibility |
| Newer minor | ⚠️ Warn, validate known fields |
| Newer major | ❌ Error, unsupported version |

---

## 8. Implementation Requirements

### 8.1 Minimum Version Support

Implementations MUST support:
- Current major version
- Previous major version (for migration)

### 8.2 Version Negotiation

When systems exchange DMG documents:

1. Check `dmg_version` first
2. If unsupported, reject with clear error
3. If newer minor, process with warnings

---

*End of Versioning Strategy v1.0*
