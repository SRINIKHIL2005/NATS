# [START pubsub_code]
import asyncio
from nats.aio.client import Client as NATS

async def message_handler(msg):
    subject = msg.subject
    data = msg.data.decode()
    print(f"\n💌 Received message on '{subject}':\n")
    print(data)

async def run_subscriber(nats_server):
    nc = NATS()
    await nc.connect(servers=[nats_server])
    await nc.subscribe("code.update", cb=message_handler)
    print(f"✅ Subscriber connected to {nats_server} and listening on 'code.update'... (Ctrl+C to stop)")

    try:
        while True:
            await asyncio.sleep(1)
    except KeyboardInterrupt:
        print("\n👋 Subscriber shutting down...")
    await nc.close()

if __name__ == '__main__':
    import sys
    nats_server = sys.argv[1] if len(sys.argv) > 1 else "nats://127.0.0.1:4222"
    asyncio.run(run_subscriber(nats_server))
# [END pubsub_code]