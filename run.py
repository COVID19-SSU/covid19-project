from conf import constants
from src import crawl
import sys

# 타입, 날짜
# python3 run
# python3 run -d 20200909
# python3 run -d 
## python3 run -csv ~

if __name__ == "__main__":

    if len(sys.argv) == 1:
        crawl.crawl_city()
        crawl.crawl_gen_age()
        crawl.crawl_status()

    else:
        if len(sys.argv) == 2 and sys.argv[1] == '-d':
            start = end = constants.TODAY

        elif len(sys.argv) == 3 and sys.argv[1] == '-d':
            start = end = sys.argv[2]
        elif len(sys.argv) == 4 and sys.argv[1] == '-d':
            start = sys.argv[2]
            end = sys.argv[3]

        crawl.crawl_city_date(start, end)
        crawl.crawl_gen_age_date(start, end)
        crawl.crawl_status_date(start, end)
