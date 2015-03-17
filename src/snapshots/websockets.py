from ws4redis.publisher import RedisPublisher
from ws4redis.redis_store import RedisMessage

redis_publisher = RedisPublisher(facility='foobar', broadcast=True)
message = RedisMessage('Hello World')
# and somewhere else
redis_publisher.publish_message(message)