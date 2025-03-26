"""
Custom exceptions for handling errors during webpage fetching.
"""


class NoPageFetched(Exception):
    """
    Custom exception raised when a page is not fetched successfully. This can be used to handle specific cases where a webpage retrieval fails.
    """

    def __init__(self, message: str):
        super().__init__(message)
