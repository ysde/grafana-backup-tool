import os
import json
import tempfile
import shutil
import unittest
from unittest.mock import patch, MagicMock

from grafana_backup.save.save_dashboards import (
    get_individual_dashboard_setting_and_save,
    build_filename,
)


def _make_board(uid, title):
    return {'uid': uid, 'title': title, 'uri': 'db/{0}'.format(title.lower().replace(' ', '-'))}


def _mock_get_dashboard_ok(board_uri, *args, **kwargs):
    """Simulate a successful dashboard fetch."""
    return (200, {'dashboard': {'title': board_uri}, 'meta': {'slug': board_uri.replace('uid/', '')}})


def _mock_get_dashboard_mixed(board_uri, *args, **kwargs):
    """Return 500 for the second dashboard, 200 for the rest."""
    if 'uid-2' in board_uri:
        return (500, {})
    return (200, {'dashboard': {'title': board_uri}, 'meta': {'slug': board_uri.replace('uid/', '')}})


class TestGetIndividualDashboardSettingAndSave(unittest.TestCase):

    def setUp(self):
        self.test_dir = tempfile.mkdtemp()
        self.log_file = 'test_log.txt'
        self.common_args = dict(
            folder_path=self.test_dir,
            log_file=self.log_file,
            grafana_url='http://localhost:3000',
            http_get_headers={'Authorization': 'Bearer test'},
            verify_ssl=False,
            client_cert=None,
            debug=False,
            pretty_print=False,
            uid_support=True,
            slug_suffix=False,
        )

    def tearDown(self):
        shutil.rmtree(self.test_dir)

    @patch('grafana_backup.save.save_dashboards.get_dashboard', side_effect=_mock_get_dashboard_ok)
    def test_sequential_dashboard_save(self, mock_get):
        """With workers=1, dashboards are fetched and saved sequentially."""
        dashboards = [_make_board('uid-1', 'Dashboard One'), _make_board('uid-2', 'Dashboard Two')]

        get_individual_dashboard_setting_and_save(dashboards=dashboards, workers=1, **self.common_args)

        self.assertEqual(mock_get.call_count, 2)
        log_path = os.path.join(self.test_dir, self.log_file)
        self.assertTrue(os.path.exists(log_path))
        with open(log_path) as f:
            lines = f.readlines()
        self.assertEqual(len(lines), 2)
        self.assertIn('uid/uid-1', lines[0])
        self.assertIn('uid/uid-2', lines[1])

    @patch('grafana_backup.save.save_dashboards.get_dashboard', side_effect=_mock_get_dashboard_ok)
    def test_parallel_dashboard_save(self, mock_get):
        """With workers=3, all dashboards are fetched and saved."""
        dashboards = [_make_board('uid-{0}'.format(i), 'Dashboard {0}'.format(i)) for i in range(5)]

        get_individual_dashboard_setting_and_save(dashboards=dashboards, workers=3, **self.common_args)

        self.assertEqual(mock_get.call_count, 5)
        log_path = os.path.join(self.test_dir, self.log_file)
        with open(log_path) as f:
            lines = f.readlines()
        self.assertEqual(len(lines), 5)
        # All dashboard uids should be present (order may vary in parallel mode)
        log_content = ''.join(lines)
        for i in range(5):
            self.assertIn('uid/uid-{0}'.format(i), log_content)

    @patch('grafana_backup.save.save_dashboards.get_dashboard', side_effect=_mock_get_dashboard_mixed)
    def test_parallel_handles_failed_dashboard(self, mock_get):
        """Failed dashboards (non-200) are skipped, others still saved."""
        dashboards = [
            _make_board('uid-1', 'Dashboard One'),
            _make_board('uid-2', 'Dashboard Two'),  # This one will fail (500)
            _make_board('uid-3', 'Dashboard Three'),
        ]

        get_individual_dashboard_setting_and_save(dashboards=dashboards, workers=3, **self.common_args)

        self.assertEqual(mock_get.call_count, 3)
        log_path = os.path.join(self.test_dir, self.log_file)
        with open(log_path) as f:
            lines = f.readlines()
        # Only 2 should be saved (uid-2 returned 500)
        self.assertEqual(len(lines), 2)
        log_content = ''.join(lines)
        self.assertIn('uid/uid-1', log_content)
        self.assertNotIn('uid/uid-2', log_content)
        self.assertIn('uid/uid-3', log_content)

    def test_empty_dashboard_list(self):
        """Empty dashboard list should not crash or create files."""
        get_individual_dashboard_setting_and_save(dashboards=[], workers=3, **self.common_args)

        log_path = os.path.join(self.test_dir, self.log_file)
        self.assertFalse(os.path.exists(log_path))

    @patch('grafana_backup.save.save_dashboards.get_dashboard', side_effect=_mock_get_dashboard_ok)
    def test_sequential_fallback_with_zero_workers(self, mock_get):
        """workers=0 should use sequential fallback."""
        dashboards = [_make_board('uid-1', 'Dashboard One')]

        get_individual_dashboard_setting_and_save(dashboards=dashboards, workers=0, **self.common_args)

        self.assertEqual(mock_get.call_count, 1)
        log_path = os.path.join(self.test_dir, self.log_file)
        with open(log_path) as f:
            lines = f.readlines()
        self.assertEqual(len(lines), 1)


class TestBuildFilename(unittest.TestCase):

    def test_no_uid_support(self):
        self.assertEqual(build_filename('db/my-dash', {}, False, False), 'db/my-dash')

    def test_uid_no_slug_suffix(self):
        self.assertEqual(build_filename('uid/abc123', {}, True, False), 'uid/abc123')

    def test_uid_with_slug_suffix(self):
        content = {'meta': {'slug': 'my-dashboard'}}
        self.assertEqual(build_filename('uid/abc123', content, True, True), 'uid/abc123-my-dashboard')

    def test_uid_with_slug_suffix_no_slug_in_content(self):
        content = {'meta': {}}
        self.assertEqual(build_filename('uid/abc123', content, True, True), 'uid/abc123')


class TestSessionReuse(unittest.TestCase):

    @patch('grafana_backup.dashboardApi._session')
    def test_send_grafana_get_uses_session(self, mock_session):
        """send_grafana_get should use the module-level session for connection pooling."""
        from grafana_backup.dashboardApi import send_grafana_get

        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {'test': 'data'}
        mock_session.get.return_value = mock_response

        status, content = send_grafana_get(
            'http://localhost:3000/api/test', {}, False, None, False
        )

        mock_session.get.assert_called_once_with(
            'http://localhost:3000/api/test',
            headers={},
            verify=False,
            cert=None,
        )
        self.assertEqual(status, 200)
        self.assertEqual(content, {'test': 'data'})


if __name__ == '__main__':
    unittest.main()
