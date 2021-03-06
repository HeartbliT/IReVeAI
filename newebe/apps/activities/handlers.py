import logging

from newebe.lib import date_util
from newebe.apps.core.handlers import NewebeAuthHandler
from newebe.apps.activities.models import ActivityManager, Activity


logger = logging.getLogger("newebe.activities")


class ActivityHandler(NewebeAuthHandler):
    '''
    This handler handles requests that retrieve lists of activities.
    GET : Retrieves last LIMIT activities published before a given date.
    '''

    def get(self, startKey=None):
        '''
        Return activities by pack of LIMIT at JSON format. If a start key
        is given in URL (it means a date like 2010-10-05-12-30-48),
        activities until this date are returned. Else latest activities are
        returned.

        Arguments:
            *startKey* The date until where activities should be returned.
        '''
        if startKey:
            dateString = date_util.get_db_utc_date_from_url_date(startKey)
            docs = ActivityManager.get_all(startKey=dateString, tag="all")
        else:
            docs = ActivityManager.get_all()

        for doc in docs:
            try:
                subdoc = Activity.get_db().get(doc.docId)
                doc.subdoc = subdoc
            except:
                pass

        self.return_documents(docs)



class MyActivityHandler(NewebeAuthHandler):
    '''
    This handler handles requests that retrieve lists of activities of
    newebe owner.
    GET : Retrieve last LIMIT activities published before a given date.
    '''

    def get(self, startKey=None):
        '''
        Return activities by pack of LIMIT at JSON format. If a start key
        is given in URL (it means a date like 2010-10-05-12-30-48),
        activities until this date are returned. Else latest activities are
        returned. Only activities of newebe owner are returned.

        Arguments:
            *startKey* The date until where activities should be returned.
        '''
        self.return_documents_since(ActivityManager.get_mine, startKey)


# Template handlers

class ActivityContentHandler(NewebeAuthHandler):
    def get(self):
        self.render("templates/activities_content.html")


class ActivityPageHandler(NewebeAuthHandler):
    def get(self):
        self.render("templates/activities.html",
                    isTheme=self.is_file_theme_exists())
