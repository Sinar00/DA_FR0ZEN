import unittest
from reconNmap import recon
from reconNmap import map_url


class MyTestCase(unittest.TestCase):
    # Testing user agent for point 5.
    # by using http://httpbin.org/headers, we can see our user-agent.
    # This test case verifies the user-agent shown is 'Mobile'.
    def test_UserAgent(self):
        response = recon('http://httpbin.org/headers')
        self.assertTrue('"User-Agent": "Mobile"' in response)

    # Testing if image link is jpg for point 7.
    # This test case verifies that the image link extracted are jpg files.
    def test_isJPG(self):
        response = map_url('https://www.w3schools.com/w3css/w3css_images.asp')
        if response is not None:
            self.assertTrue("jpg" in next(response) or "jpeg" in next(response))


if __name__ == '__main__':
    unittest.main()
