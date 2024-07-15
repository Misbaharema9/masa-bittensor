# The MIT License (MIT)
# Copyright © 2023 Yuma Rao
# TODO(developer): Set your name
# Copyright © 2023 <your name>

# Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated
# documentation files (the “Software”), to deal in the Software without restriction, including without limitation
# the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software,
# and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all copies or substantial portions of
# the Software.

# THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO
# THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL
# THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
# OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
# DEALINGS IN THE SOFTWARE.

import torch
import bittensor as bt
from typing import List
from masa.types.twitter import TwitterTweetObject


def reward(query: str, response: List[TwitterTweetObject]) -> float:
    # Return a reward of 0.0 if the response is None
    if response is None or len(response) == 0:
        return 0.0
    bt.logging.info(f"Calculating reward for tweets: {len(response)}")

    score = 1.0
    required_keys = TwitterTweetObject.__annotations__.keys()  # Get all required keys from TwitterFollowersObject
    missing_keys = sum(1 for key in required_keys for tweet in response if key not in tweet)
    score -= 0.1 * missing_keys

    return max(score, 0)


def get_rewards(
    self,
    query: str,
    responses: TwitterTweetObject,
) -> torch.FloatTensor:
    bt.logging.info("Getting rewards...")
    return torch.FloatTensor([reward(query, response) for response in responses]).to(
        self.device
    )
