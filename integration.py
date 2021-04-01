import sevenSeg
import database
import asyncio
from time import sleep
from random import randint
async def main():
    seg=sevenSeg.sevenseg()
    seg.clear()
    db=database.Database("Schrank")
    count = await db.getCurrentCount()
    seg.updateDisplay(count)
    for i in range(10):
        sleep(1)
        if randint(0,1) == 0:
            await db.IncDatabase()
            count+=1
        else:
            await db.DecDatabase()
            count-=1
        seg.updateDisplay(count)



if __name__=="__main__":
    loop=asyncio.new_event_loop()
    loop.run_until_complete(main())