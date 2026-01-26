# DMG Security Specification

Version: 1.0  
Status: Draft  
Last Updated: 2026-01-26

---

## 1. Overview

This document defines the security model for Decision Moment Graph (DMG) implementations. It covers threat modeling, authentication, integrity verification, and privacy considerations.

---

## 2. Threat Model

### 2.1 Assets

| Asset | Description | Sensitivity |
|-------|-------------|-------------|
| Decision content | MEMO, options, rationale | Medium-High |
| Audit trail | MOMENT events | High |
| Identity data | Actor identities in events | High |
| Evidence sources | TRACE URIs and citations | Medium |
| Outcome data | OUTCOME checks and verdicts | Medium |

### 2.2 Threat Actors

| Actor | Capability | Motivation |
|-------|------------|------------|
| **Insider** | Full system access | Cover up poor decisions |
| **External Attacker** | Network access | Data theft, manipulation |
| **Competitor** | Public access | Competitive intelligence |
| **Auditor** | Read access | Verify integrity |

### 2.3 Attack Vectors

#### T1: Event Tampering
- **Threat**: Modify historical events to change decision narrative
- **Impact**: Critical — undermines auditability
- **Mitigation**: Hash chain integrity (see §4)

#### T2: Event Insertion
- **Threat**: Insert fabricated events into MOMENT
- **Impact**: High — false attribution
- **Mitigation**: Append-only log, signature verification (see §5)

#### T3: Event Deletion
- **Threat**: Remove unfavorable events from history
- **Impact**: High — loss of accountability
- **Mitigation**: Append-only log, external witnesses

#### T4: Identity Spoofing
- **Threat**: Claim actions were taken by different actor
- **Impact**: High — accountability failure
- **Mitigation**: Event signing (see §5)

#### T5: Replay Attack
- **Threat**: Replay signed events in different context
- **Impact**: Medium — confusion, denial of service
- **Mitigation**: Unique nonces, timestamp validation

#### T6: Information Disclosure
- **Threat**: Unauthorized access to sensitive decisions
- **Impact**: Medium-High — confidentiality breach
- **Mitigation**: Access control (see §6)

---

## 3. Security Principles

1. **Immutability**: MOMENT events are append-only
2. **Verifiability**: Hash chain enables integrity verification
3. **Attribution**: Events must identify actors
4. **Auditability**: Complete trail from creation to outcome
5. **Transparency**: MERIT compliance is machine-verifiable

---

## 4. Hash Chain Integrity

### 4.1 Hash Algorithm

**REQUIRED**: SHA-256 (as defined in FIPS 180-4)

### 4.2 Canonicalization

Before hashing, the event payload MUST be canonicalized:

1. Remove the `hash` field from the event object
2. Serialize to JSON with keys sorted alphabetically
3. Use UTF-8 encoding
4. No whitespace between tokens

```python
import json
import hashlib

def compute_event_hash(event: dict, prev_hash: str) -> str:
    """Compute hash for a MOMENT event."""
    # Create hashable payload
    payload = {k: v for k, v in event.items() if k != "hash"}
    payload["prev_hash"] = prev_hash
    
    # Canonicalize
    canonical = json.dumps(payload, sort_keys=True, separators=(",", ":"))
    
    # Hash
    return hashlib.sha256(canonical.encode("utf-8")).hexdigest()
```

### 4.3 Chain Verification

```python
def verify_hash_chain(events: list) -> bool:
    """Verify MOMENT event hash chain integrity."""
    prev_hash = ""
    
    for event in events:
        expected = compute_event_hash(event, prev_hash)
        if event.get("hash") != expected:
            return False
        prev_hash = event["hash"]
    
    return True
```

---

## 5. Event Signing (Optional)

> [!NOTE]
> Event signing is OPTIONAL in DMG v0.1 but RECOMMENDED for high-RAMP decisions.

### 5.1 Signature Format

Use JSON Web Signature (JWS) compact serialization:

```json
{
  "event_id": "e1",
  "seq": 1,
  "ts": "2026-01-26T10:00:00Z",
  "type": "MEMO_CREATED",
  "actor": "alice@example.com",
  "payload": {},
  "prev_hash": "",
  "hash": "abc123...",
  "signature": "eyJhbGciOiJFUzI1NiJ9.eyJoYXNoIjoiYWJjMTIzLi4uIn0.dGVzdA"
}
```

### 5.2 Signature Algorithm

**RECOMMENDED**: ES256 (ECDSA with P-256 and SHA-256)

**ALTERNATIVE**: RS256 (RSASSA-PKCS1-v1_5 with SHA-256)

### 5.3 Key Management

| RAMP Level | Key Management Requirement |
|------------|---------------------------|
| 1-2 | No signing required |
| 3 | Signed by named owner |
| 4-5 | Multi-signature or HSM |

---

## 6. Access Control Model

### 6.1 Roles

| Role | Permissions |
|------|-------------|
| **Creator** | Create MEMO, set RAMP, define options |
| **Contributor** | Add DISSENT, attach TRACE |
| **Approver** | Approve/reject, change COMMIT state |
| **Owner** | Update DOORS, record OUTCOME |
| **Auditor** | Read all, verify integrity |
| **Public** | Read publicly-flagged decisions |

### 6.2 RAMP-Based Access

| RAMP Level | Default Access |
|------------|---------------|
| 1 | Team-visible |
| 2 | Department-visible |
| 3 | Leadership-visible |
| 4-5 | Restricted / Board-only |

### 6.3 Access Control Fields

```json
{
  "memo": {
    "memo_id": "...",
    "access": {
      "visibility": "restricted",
      "allowed_roles": ["leadership", "board"],
      "allowed_users": ["ceo@example.com", "cfo@example.com"]
    }
  }
}
```

---

## 7. Privacy Considerations

### 7.1 PII in Decisions

DMG documents may contain Personally Identifiable Information (PII) in:
- `actor` fields in MOMENT events
- `author` fields in DISSENT objects
- `own.name` in DOORS

### 7.2 GDPR Compliance

| Requirement | DMG Implementation |
|-------------|-------------------|
| Right to access | Export decision history |
| Right to erasure | Pseudonymization (not deletion) |
| Data minimization | Avoid unnecessary PII |
| Purpose limitation | Document purpose in MEMO context |

### 7.3 Pseudonymization Strategy

For decisions requiring PII protection:

```json
{
  "actor": "user:a1b2c3d4",
  "actor_pseudonym_map": "external://pseudonym-service/lookup"
}
```

> [!CAUTION]
> Never delete MOMENT events to satisfy erasure requests. Pseudonymize actor identities instead.

---

## 8. Implementation Checklist

### 8.1 Minimum Security (All Implementations)

- [ ] Validate hash chain on read
- [ ] Enforce append-only MOMENT
- [ ] Validate event timestamps are monotonic
- [ ] Sanitize user input in all fields

### 8.2 Recommended Security (RAMP ≥ 3)

- [ ] Sign events with actor key
- [ ] Implement access control
- [ ] Encrypt at rest
- [ ] Log access attempts

### 8.3 High Security (RAMP 4-5)

- [ ] Multi-signature approval
- [ ] Hardware security module (HSM) for keys
- [ ] External witness/notarization
- [ ] Air-gapped approval workflow

---

## 9. Security Reporting

Report security vulnerabilities to: security@dmg-standard.org

We follow coordinated disclosure with a 90-day timeline.

---

*End of Security Specification v1.0*
