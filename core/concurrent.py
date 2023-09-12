import concurrent.futures

from utils.constants import Const
from utils.debug import Debug  # noqa


def pool_executor(func, dataset, *args, **kwargs):
    if isinstance(dataset, list):
        count = len(dataset)
    else:
        count = dataset.count()

    with concurrent.futures.ThreadPoolExecutor(
        max_workers=Const.MAX_WORKERS
    ) as executor:
        futures = {
            executor.submit(
                func,
                data,
                *args
            ): data for data in dataset
        }
        for i, future in enumerate(concurrent.futures.as_completed(futures)):
            if future.result():
                Debug.trace(
                    'job finished (%d/%d) with %s.' % (
                        i + 1,
                        count,
                        future.result()
                    )
                )
