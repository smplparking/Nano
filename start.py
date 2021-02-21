import asyncio
import direction


def main():
    loop = asyncio.get_event_loop()
    loop.run_until_complete(direction.mainloop())
    loop.close()


if __name__ == '__main__':
    main()
