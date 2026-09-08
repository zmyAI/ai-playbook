# Operation Patterns Guide

Common node configuration patterns organized by node type.

---

## HTTP & API Nodes

### HTTP Request (nodes-base.httpRequest)

**GET Request**:
```javascript
{
  "method": "GET",
  "url": "https://api.example.com/users",
  "authentication": "none"
}
```

**POST with JSON**:
```javascript
{
  "method": "POST",
  "url": "https://api.example.com/users",
  "authentication": "none",
  "sendBody": true,
  "body": {
    "contentType": "json",
    "content": { "name": "John", "email": "john@example.com" }
  }
}
```

> ⚠️ Remember `sendBody: true` for POST/PUT/PATCH!

### Webhook (nodes-base.webhook)

```javascript
{
  "path": "my-webhook",
  "httpMethod": "POST",
  "responseMode": "onReceived"
}
```

> ⚠️ Webhook data is under `$json.body`, not `$json`!

---

## Communication Nodes

### Slack (nodes-base.slack)

**Post message**:
```javascript
{
  "resource": "message",
  "operation": "post",
  "channel": "#general",
  "text": "Hello!"
}
```

> ⚠️ Channel format: `#name` (not just `name`)

---

## Transform Nodes

### Set (nodes-base.set)

```javascript
{
  "assignments": {
    "assignments": [
      { "name": "field1", "value": "={{$json.source}}", "type": "string" }
    ]
  }
}
```

### Code (nodes-base.code)

**Per-item mode** (default): Code runs once per item
**All-items mode**: Code runs once with all items

---

## Conditional Nodes

### IF (nodes-base.if)

```javascript
{
  "conditions": {
    "string": [
      {
        "value1": "={{$json.status}}",
        "operation": "equals",
        "value2": "active"
      }
    ]
  },
  "combineOperation": "all"
}
```

> ⚠️ Unary operations (isEmpty, isNotEmpty) don't need value2!

---

## Summary

| Category | Key Gotcha |
|---|---|
| HTTP/API | Remember sendBody: true for POST |
| Webhooks | Data under $json.body |
| Slack | Channel format (#name) |
| IF/Switch | Unary vs binary operators |
| Schedule | Set timezone explicitly |
