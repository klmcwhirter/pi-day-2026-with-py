# pi-day-2026-with-py
Experiment with visualization of 1,000,000,000 (1 billion) digits of π

## Overview

Last year in [pi-day-2025-with-py](https://github.com/klmcwhirter/pi-day-2025-with-py) I attempted to pay homage to a recent discovery of a series that outputs π. Not surprising (because of the computational complexity), even though it converges to 10 digits of precision in as little as 30 terms, evaluating even 5000 terms (to produce 711 digits) took hours. This was far less than the 1M digits I was targeting.

This year I would like to focus on a bump up to 1,000,000,000 (1 billion) digits of π.

The use case is to find palindromes of π digits.
* the palindrome '314413' exists 3 times in the first million digits of pi.
* the palindrome '3141413' exists 0 times in the first million digits of pi.
* How many digits are needed for '3141413' to appear? _initial manual testing suggests just over 2.5M digits are needed. And that '314151413' appears soon after 88K digits. What other interesting palindrome insights can be found with a reasonably meager compute investment?_

The standard for success will be:
* performant mechanism to use a reference source for digits of pi (_See [billion digits of pi](https://stuff.mit.edu/afs/sipb/contrib/pi/)_) and index as many palimdromes that can be found
* experiment should complete as quickly as practical; preferably in less than 5 mins
  * bonus if individual palindrome searches complete in less than 15 secs
* a UI to visualize the results of palindrome position searches with counts - histogram
  * bonus UI to "paginate" all 1 giga-digits of π
* satisfy the use case requirements
* bonus if the software deploys via OCI tech and runs on a Raspberry Pi 4B with 8GB RAM

## Reference
* [billion digits of pi](https://stuff.mit.edu/afs/sipb/contrib/pi/)
