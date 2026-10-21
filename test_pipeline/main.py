# main.py
# Entry point. Run with:  python main.py
# Exits with code 0 on success and 1 on failure, so Airflow knows if it worked.

import datetime
import sys

import utils

logger = utils.setup_logging()


def main():
    logger.info("Pipeline started")
    try:
        utils.check_config()

        price = utils.fetch_price()
        logger.info("price is received: %s", price)

        run_time = datetime.datetime.now(datetime.timezone.utc).isoformat(timespec="seconds")
        utils.insert_row(run_time, price)
        logger.info("price is written to supabase")

        logger.info("Pipeline is finished")
        return 0
    except Exception:
        logger.exception("Pipeline FAILED")
        return 1


if __name__ == "__main__":
    sys.exit(main())
