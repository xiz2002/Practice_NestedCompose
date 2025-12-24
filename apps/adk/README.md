# Agent확인
```bash
curl "http://localhost:8000/api/v1/agent"
```

# Session생성
```bash
curl -X POST "http://localhost:8000/api/v1/sessions" \
  -H "Content-Type: application/json" \
  -d '{"user_id":"user123"}'

```
# Chat
```bash
curl -X POST "http://localhost:8000/api/v1/chat" \
  -H "Content-Type: application/json" \
  -d '{"user_id":"user123","session_id":"<session_id>","message":"안녕! 오늘 뭐하면 좋을까?"}'

  
curl -X POST "http://localhost:8000/api/v1/chat" \
  -H "Content-Type: application/json" \
  -d '{"user_id":"user123","session_id":"sess_abc123","message":"지금 서울의 날씨는?"}'

```

# Session Reconnect
```bash
curl "http://localhost:8000/api/v1/sessions/user123/<session_id>"
```