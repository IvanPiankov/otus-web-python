from web_parser import (is_string_an_url, get_request)


class TestStringToUrl:

    def test_string_is_url(self):
        self.string = "https://aka.ms/pscore6"
        result = is_string_an_url(self.string)
        assert result

    def test_string_not_url(self):
        self.string = "aka.ms"
        result = is_string_an_url(self.string)
        assert not result


class TestGetRequest:

    def test_get_request_status_code_200(self, requests_mock):
        requests_mock.get('http://test.com', text='data', status_code=200)
        expected_code, expected_text = get_request('http://test.com')
        assert expected_text == 'data'
        assert expected_code == 200

    def test_get_request_status_code_400(self, requests_mock):
        requests_mock.get('http://test.com', text='data', status_code=400)
        expected_code, expected_text = get_request('http://test.com')
        assert expected_text == 'data'
        assert expected_code == 400




