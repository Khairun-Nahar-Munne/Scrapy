import unittest
from unittest.mock import MagicMock
from scrapy.http import Response, Request
from scrapy.spiders import Spider
from scrapingcourse_scraper.middlewares import ScrapingcourseScraperSpiderMiddleware, ScrapingcourseScraperDownloaderMiddleware

class TestScrapingcourseScraperSpiderMiddleware(unittest.TestCase):

    def setUp(self):
        self.middleware = ScrapingcourseScraperSpiderMiddleware()
        self.spider = MagicMock(spec=Spider)
        self.response = MagicMock(spec=Response)
        self.result = [MagicMock(), MagicMock()]

    def test_process_spider_input(self):
        # Test process_spider_input
        result = self.middleware.process_spider_input(self.response, self.spider)
        self.assertIsNone(result)  # Should return None or raise an exception

    def test_process_spider_output(self):
        # Test process_spider_output
        result = list(self.middleware.process_spider_output(self.response, self.result, self.spider))
        self.assertEqual(len(result), 2)  # Should yield 2 items
        self.assertEqual(result, self.result)

    def test_process_spider_exception(self):
        # Test process_spider_exception
        result = self.middleware.process_spider_exception(self.response, Exception("Test Exception"), self.spider)
        self.assertIsNone(result)  # Should return None or an iterable of requests/items

    def test_process_start_requests(self):
        # Test process_start_requests
        start_requests = [MagicMock(spec=Request)]
        result = list(self.middleware.process_start_requests(start_requests, self.spider))
        self.assertEqual(len(result), 1)  # Should yield 1 request
        self.assertEqual(result[0], start_requests[0])

  

class TestScrapingcourseScraperDownloaderMiddleware(unittest.TestCase):

    def setUp(self):
        self.middleware = ScrapingcourseScraperDownloaderMiddleware()
        self.request = MagicMock(spec=Request)
        self.response = MagicMock(spec=Response)
        self.spider = MagicMock(spec=Spider)

    def test_process_request(self):
        # Test process_request
        result = self.middleware.process_request(self.request, self.spider)
        self.assertIsNone(result)  # Should return None, or handle request accordingly

    def test_process_response(self):
        # Test process_response
        result = self.middleware.process_response(self.request, self.response, self.spider)
        self.assertEqual(result, self.response)  # Should return the response

    def test_process_exception(self):
        # Test process_exception
        result = self.middleware.process_exception(self.request, Exception("Test Exception"), self.spider)
        self.assertIsNone(result)  # Should return None or a response/request



if __name__ == '__main__':
    unittest.main()
