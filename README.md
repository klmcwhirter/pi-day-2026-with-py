# pi-day-2026-with-py
Experiment with series that produce digits of π using python utilizing as many CPU cores as available

## Overview

Last year in [pi-day-2025-with-py](https://github.com/klmcwhirter/pi-day-2025-with-py) I attempted to pay homage to a recent discovery of a series that outputs π. Not surprising (because of the computational complexity), even though it converges to 10 digits of accuracy in as little as 30 terms, evaluating even 5000 terms (to produce 711 digits) took hours. This was far less than the 1M digits I was targeting.

This year I would like to focus on using some algorithm that allows for maximum parallelization so as to make use of features in Python 3.14 (a.k.a. π-thon).

These features are:
* concurrent.futures.InterpreterPoolExecutor (threading, single process) - new in 3.14
* concurrent.futures.ProcessPoolExecutor (multi-process) - introduced in 3.2

The standard for success will be:
* generate 1M digits repeatably (consistently)
* ability to saturate as many CPU cores as made available to the experiment
* experiment should complete in less than 1 hour; preferably in less than 30 mins
* a UI to visualize the results of different runs including accuracy as a percentage of correct digits vs a baseline

My continuing goal is to discover patterns that can be used with Python to evaluate series (with similar computational complexity characteristics) at runtime with acceptable perceived performance.

## Expected Challenges

Although Python 3.14 has tools to enable utilizing multiple CPU cores, aggregating the results from the workers always involves serialization / deserialization at multiple levels. This was a lesson learned from last years project.

The Executor sub-classes utilize the [`pickle`](https://docs.python.org/3.14/library/pickle.html) protocol for intra-process (or inter-process respectively) serialization.

And the mpmath library (used last year) relies on an internal binary representation that requires serialization / deserialization via (at least) the `mp.mathify` and `mp.nstr` functions designed for that purpose.

These operations can be slow especially if the right balance is not struck.

A couple of naive thoughts to overcome this (or at least to attempt to manage the risks) are:

* use sqlite db to store intermediate results to be aggregated later - this also involves serialization / deserialization in the data access layer
* use shared object cache (e.g., keydb, memcachedb, in-memory sqlite db) - same issue - but isolates the site that needs to address the anticipated competing producers / consumers problem
* rely on commonly used python modules that have extensions written in a lower level language (e.g., numpy, mpmath, etc.) to free up more time for the serialization / deserialization to improve perceived performance
* utilize blob storage (in a db or set of files, etc.) to minimize the need for extraneous deserialization / object activation
  * note that most linux distros have an in-memory, ephemeral filesystem available at `/run/user/1000/` that can be utilized to store intermediate results without the need for deserialization

But none of these seem to be obviously part of a best approach.

Hence, my continuing desire for further experimentation.

## Reference
* [concurrent.futures.ProcessPoolExecutor](https://docs.python.org/3.14/library/concurrent.futures.html#processpoolexecutor)
* [concurrent.futures.InterpreterPoolExecutor](https://docs.python.org/3.14/library/concurrent.futures.html#interpreterpoolexecutor)
