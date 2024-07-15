import logging
from rich.logging import RichHandler
from tele.search import search_group
from chain.evm import search_evm_data
from chain.evm_driver import evm_data_driver
from chain.evm_driver import baidu_driver

logging.basicConfig(
    level="NOTSET",
    format="%(message)s",
    datefmt="[%X]",
    handlers=[RichHandler()]
)
logger = logging.getLogger("rich")


def main():
    search_group('geopolitics')
    # search_evm_data('0xf6372ef94026f71e5e48f0ff2ff5ceb06fdff303')
    # evm_data_driver()
    # baidu_driver()


if __name__ == "__main__":
    main()
