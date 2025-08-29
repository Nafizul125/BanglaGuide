import json
import time
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async
from django.utils.html import strip_tags
from django.utils.timezone import now
from .models import Post, Reply

GLOBAL_GROUP = "comments_global"
COOLDOWN_SECONDS = 2
_last_post_ts = {}

def display_name(user):
    if not user:
        return "Guest"
    return getattr(user, "name", None) or getattr(user, "username", None) or "User"

@sync_to_async
def create_post(user, text):
    return Post.objects.create(user=user, text=text)

@sync_to_async
def create_reply(user, post_id, text):
    return Reply.objects.create(user=user, post_id=post_id, text=text)

@sync_to_async
def recent_posts(limit=30):
    qs = (Post.objects
            .select_related("user")
            .prefetch_related("replies__user")
            .order_by("-timestamp")[:limit])
    data = []
    for p in reversed(list(qs)):
        data.append({
            "id": p.id,
            "user": display_name(p.user),
            "text": p.text,
            "ts": p.timestamp.isoformat(),
            "replies": [{
                "id": r.id,
                "user": display_name(r.user),
                "text": r.text,
                "ts": r.timestamp.isoformat()
            } for r in p.replies.all().order_by("timestamp")]
        })
    return data

class CommentsConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.channel_layer.group_add(GLOBAL_GROUP, self.channel_name)
        await self.accept()
        items = await recent_posts()
        await self.send(text_data=json.dumps({"type": "history", "items": items}))

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(GLOBAL_GROUP, self.channel_name)

    async def receive(self, text_data=None, bytes_data=None):
        # Require authentication for any write action
        user = self.scope.get("user")
        is_authed = bool(user and getattr(user, "is_authenticated", False))

        try:
            data = json.loads(text_data or "{}")
        except Exception:
            return

        action = (data.get("action") or "").lower()
        raw = (data.get("text") or "").strip()

        # Only "post" or "reply" require text; ignore others
        if action in {"post", "reply"}:
            if not is_authed:
                # Tell the client they must sign in
                await self.send(text_data=json.dumps({"type": "error", "code": "auth_required"}))
                return
            if not raw:
                return

            # throttle per connection
            t = time.time()
            last = _last_post_ts.get(self.channel_name, 0)
            if t - last < COOLDOWN_SECONDS:
                return
            _last_post_ts[self.channel_name] = t

            text = strip_tags(raw)[:500]

            if action == "post":
                post = await create_post(user, text)
                payload = {
                    "type": "new_post",
                    "id": post.id,
                    "user": display_name(user),
                    "text": text,
                    "ts": now().isoformat(),
                }
                await self.channel_layer.group_send(GLOBAL_GROUP, {"type": "broadcast", "payload": payload})

            elif action == "reply":
                post_id = data.get("post_id")
                if not post_id:
                    return
                reply = await create_reply(user, post_id, text)
                payload = {
                    "type": "new_reply",
                    "id": reply.id,
                    "post_id": int(post_id),
                    "user": display_name(user),
                    "text": text,
                    "ts": now().isoformat(),
                }
                await self.channel_layer.group_send(GLOBAL_GROUP, {"type": "broadcast", "payload": payload})

    async def broadcast(self, event):
        await self.send(text_data=json.dumps(event["payload"]))
