import logging
from rich.logging import RichHandler
from tele.search import search_group

# 配置日志记录
logging.basicConfig(
    level="NOTSET",
    format="%(message)s",
    datefmt="[%X]",
    handlers=[RichHandler()]
)
logger = logging.getLogger("rich")


def main():
    search_group('geopolitics')


if __name__ == "__main__":
    main()
