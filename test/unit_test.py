import os
import csv
import json
import unittest
from ..send_email import auto_generate_folder, get_template, output_error, Customer
from mock import patch, mock_open, MagicMock
from ..send_email import datetime_, default_dir


class TestSendMail(unittest.TestCase):
    @patch('pi.send_email.sys.argv', [])
    @patch('pi.send_email.os')
    def test_auto_create_folder_not_params(self, mock_os):
        auto_generate_folder()
        mock_os.makedirs.assert_called_with(mock_os.path.join(default_dir, f'{datetime_.date()}/{datetime_.time()}'))

    @patch('pi.send_email.sys.argv', True)
    @patch('pi.send_email.os')
    def test_auto_create_folder_has_params_not_exists(self, mock_os):
        mock_os.path.exists.return_value = ['mock_folder/email_template.json', 'mock_folder_1/customers.csv',
                                            'mock_folder_2/output.json',
                                            'mock_folder_3/errors.csv']
        auto_generate_folder()
        for path_ in mock_os.path.exists.value:
            mock_os.makedirs.assert_called_with(path_)

    @patch('pi.send_email.sys.argv', True)
    @patch('pi.send_email.os')
    def test_auto_create_folder_has_params_exists(self, mock_os):
        mock_os.path.exists.return_value = True
        auto_generate_folder()
        self.assertEqual(mock_os.makedirs.call_count, 0)

    @patch('pi.send_email.sys.argv', [])
    @patch('pi.send_email.os')
    def test_auto_create_folder_exception(self, mock_os):
        mock_os.makedirs.side_effect = Exception
        with self.assertRaises(Exception) as context:
            auto_generate_folder()
            self.assertTrue("can't create file" in context.exception)

    @patch("builtins.open", new_callable=mock_open,
           read_data=json.dumps({
               "from": "The Marketing Team<marketing@example.com",
               "subject": "A new product is being launched soon...",
               "mimeType": "text/plain",
               "body": "Hi {{TITLE}} {{FIRST_NAME}} {{LAST_NAME}}"
           }))
    def test_get_template(self, mock_open):
        expected_output = {
            "from": "The Marketing Team<marketing@example.com",
            "subject": "A new product is being launched soon...",
            "mimeType": "text/plain",
            "body": "Hi {{TITLE}} {{FIRST_NAME}} {{LAST_NAME}}"
        }
        actual_output = get_template()
        self.assertEqual(expected_output, actual_output)

    @patch("builtins.open", new_callable=mock_open, create=True)
    @patch('pi.send_email.csv')
    def test_output_error(self, mock_open, mock_csv):
        ope = output_error()
        ope.__next__()
        customer = Customer(*('Mr', 'Michelle', 'ba', 'nan'))
        ope.send(customer)
        ope.close()


if __name__ == '__main__':
    unittest.main()
