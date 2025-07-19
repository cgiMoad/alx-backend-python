#!/usr/bin/env python3
"""
Unit tests for GithubOrgClient.
"""
import unittest
from unittest.mock import patch
from parameterized import parameterized
from client import GithubOrgClient


class TestGithubOrgClient(unittest.TestCase):
    """Unit tests for GithubOrgClient"""

    @parameterized.expand([
        ("google",),
        ("abc",),
    ])
    @patch('client.get_json')
    def test_org(self, org_name, mock_get_json):
        """
        Test that GithubOrgClient.org calls get_json once with the expected URL
        and returns the correct result.
        """
        # Mock get_json to return a dummy response
        expected_payload = {"org": org_name}
        mock_get_json.return_value = expected_payload

        # Instantiate the client and call org
        client = GithubOrgClient(org_name)
        result = client.org

        # Check that get_json was called with the correct URL
        mock_get_json.assert_called_once_with(
            f"https://api.github.com/orgs/{org_name}"
        )
        # Verify that the result matches the mocked return value
        self.assertEqual(result, expected_payload)


if __name__ == '__main__':
    unittest.main()
