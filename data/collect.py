import asyncio
from twscrape import API, gather


async def main():
    api = API()
    tweets = await gather(api.search("elon musk", limit=20))
    for tweet in tweets:
            print(tweet.id, tweet.user.username, tweet.rawContent)

            

if __name__ == "__main__":
    asyncio.run(main())