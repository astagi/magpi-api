import app
import mock
import json
from nose.tools import assert_equal
from app.models.issue import Issue
from app.models.news import News

class TestMagpiApi():

    def setUp(self):
        self.app = app.app.test_client()

    def test_issue_conversion_from_original(self):
        old_issue = {
            "id":848,
            "title":"20",
            "date":"February 3, 2014",
            "url":"http:\/\/www.themagpi.com\/issue\/issue-20\/",
            "issuu":"issue20final",
            "pdf":"http:\/\/www.themagpi.com\/issue\/issue-20\/pdf",
            "cover":"http:\/\/www.themagpi.com\/assets\/20.jpg",
            "editorial":"Welcome"
        }
        expected = {
            "id": 20, 
            "id_issuu":"issue20final",
            "pdf_url": "http:\/\/www.themagpi.com\/issue\/issue-20\/pdf",
            "image_url": "http:\/\/www.themagpi.com\/assets\/20.jpg",
            "date": "February 3, 2014", 
            "content": "Welcome",
        }
        issue = Issue()
        issue.fill_from_old(old_issue)
        assert_equal(issue.maximize(), expected)

    def test_news_conversion_from_original(self):
        old_news = {
            "title": "Title",
            "published" : "Tue, 04 Feb 2014 12:29:32 PST",
            "summary" : "My summary",
        }
        expected = {
            "title": "Title",
            "date" : "2014-02-04 12:29:32",
            "content" : "My summary",
        }
        news = News()
        news.fill_from_old(old_news)
        assert_equal(news.maximize(), expected)

    def test_minimize_issue(self):
        expected = {
            "id": 19, 
            "pdf_url": "https://issuee",
            "image_url": "https://issuee.jpg",
            "date": "Feb 2013", 
        }
        issue = Issue()
        issue.id = 19
        issue.date = "Feb 2013"
        issue.pdf_url = "https://issuee"
        issue.image_url = "https://issuee.jpg"
        assert_equal(issue.minimize(), expected)

    def test_maximize_issue(self):
        expected = {
            "id": 19,
            "id_issuu":"issuu19final",
            "pdf_url": "https://issuee",
            "image_url": "https://issuee.jpg",
            "date": "Feb 2013", 
            "content": "Bla Bla Bla content"
        }
        issue = Issue()
        issue.id = 19
        issue.id_issuu = "issuu19final"
        issue.date = "Feb 2013"
        issue.pdf_url = "https://issuee"
        issue.image_url = "https://issuee.jpg" 
        issue.content = "Bla Bla Bla content"
        assert_equal(issue.maximize(), expected)

    @mock.patch('app.views.get_issues_list_from_db')
    def test_get_list_issues(self, mock_get_issues_list_from_db):
        expected = {'issues':[{
            "id": 18, 
            "pdf_url": "https://issuee", 
            "date": "Jan 2013", 
        },{
            "id": 19, 
            "pdf_url": "https://issuee", 
            "date": "Feb 2013", 
        }]}
        mock_get_issues_list_from_db.return_value = expected
        rv = self.app.get('/issues')
        mock_get_issues_list_from_db.assert_called_once()
        assert_equal(json.loads(rv.data), expected)

    @mock.patch('app.views.get_issue_from_db')
    def test_get_issue(self, mock_get_issue_from_db):
        expected = {
            "id": 19, 
            "pdf_url": "https://issuee", 
            "date": "Feb 2013", 
        }
        mock_get_issue_from_db.return_value = expected
        rv = self.app.get('/issues/19')
        mock_get_issue_from_db.assert_called_once_with(19)
        assert_equal(json.loads(rv.data), expected)

    @mock.patch('app.views.get_news_list_from_db')
    def test_get_list_news(self, mock_get_news_list_from_db):
        expected = {'news':[{
            "date": "25 Feb 2011", 
            "title": "MagPi 20 released", 
            "content": "Bla bla bla", 
        },{
            "date": "28 Feb 2011", 
            "title": "MagPi 21 released", 
            "content": "Bla bla bla", 
        }]}
        mock_get_news_list_from_db.return_value = expected
        rv = self.app.get('/news')
        mock_get_news_list_from_db.assert_called_once()
        assert_equal(json.loads(rv.data), expected)
