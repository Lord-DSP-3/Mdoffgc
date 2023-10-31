import redis
# dihabor940@wisnick.com pp_00000_DSP
Redis_client1 = redis.Redis(
  host='redis-18712.c299.asia-northeast1-1.gce.cloud.redislabs.com',
  port=18712,
  password='hBZT6va5IkajpOOUK7XlPDG26WS6EoqW')


pubsub = Redis_client1.pubsub()
pubsub.subscribe('InvertMDtask')


async def handle_redis_messages(app):
    for message in pubsub.listen():
        if message['type'] == 'message':
            key = message['data'].decode('utf-8')
            await app.send_message(
                5912572748,
                f"Got Key: {key}"
            )
