# Property Dependencies Guide

Deep dive into n8n property dependencies and displayOptions mechanism.

---

## displayOptions Structure

### Basic Format

```javascript
{
  "name": "fieldName",
  "type": "string",
  "displayOptions": {
    "show": {
      "otherField": ["value1", "value2"]
    }
  }
}
```

**Translation**: Show `fieldName` when `otherField` equals "value1" OR "value2"

### Show vs Hide

**show** (Most Common): Show field when condition matches
**hide** (Less Common): Hide field when condition matches

### Multiple Conditions (AND Logic)

All conditions in `show` must match simultaneously.

### Multiple Values (OR Logic)

Any value in the array matches.

---

## Common Dependency Patterns

### Pattern 1: Boolean Toggle
`sendBody: true → body field appears`

### Pattern 2: Resource/Operation Cascade
Different operations show different fields (e.g., Slack post needs channel, update needs messageId)

### Pattern 3: Type-Specific Configuration
Different types need different fields (e.g., IF node string vs number conditions)

### Pattern 4: Method-Specific Fields
HTTP methods have different options (GET no body, POST/PUT body visible)

---

## Troubleshooting

| Problem | Likely Cause | Solution |
|---------|-------------|----------|
| Field required but not visible | Dependency not met | Check displayOptions with search_properties |
| Field disappears after change | Operation changed requirements | Re-check get_node after operation change |
| Field doesn't save | Hidden by dependencies | Respect dependencies from the start |

---

**Related Files**:
- **[SKILL.md](SKILL.md)** - Main configuration guide
- **[OPERATION_PATTERNS.md](OPERATION_PATTERNS.md)** - Common patterns by node type