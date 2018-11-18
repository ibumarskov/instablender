from operator import itemgetter
from facebook_business.api import FacebookAdsApi
from facebook_business.adobjects.page import Page


class InstaBlender(object):
    def __init__(self, token, app_id, app_secret):
        self.my_access_token = token
        self.my_app_id = app_id
        self.my_app_secret = app_secret
        self.api = FacebookAdsApi.init(self.my_app_id, self.my_app_secret,
                                       self.my_access_token)
        self.business_acc_id = self._get_instagram_business_id()

    @staticmethod
    def _get_instagram_business_id():
        fields = ["instagram_business_account"]
        params = {
        }
        accounts = Page('me/accounts').api_get(
            fields=fields,
            params=params,
        )
        for acc in accounts["data"]:
            if "instagram_business_account" in acc:
                return acc["instagram_business_account"]["id"]


class InstaBlenderMedia(InstaBlender):

    def __init__(self, token, app_id, app_secret, media_id=None):
        super(InstaBlenderMedia, self).__init__(token, app_id, app_secret)
        self.media_id = media_id

    def get_media_id_by_text(self, text):
        fields = ["caption"]
        params = {
        }
        media = Page(self.business_acc_id + '/media').api_get(
            fields=fields,
            params=params,
        )
        for m in media["data"]:
            if text in m["caption"]:
                self.media_id = m["id"]

    def get_comments(self, next_page=None, clist=[]):
        fields = ["text", "username"]
        params = {
            "limit": 50,
            "after": next_page,
        }
        comments = Page(str(self.media_id) + '/comments').api_get(
            fields=fields,
            params=params,
        )

        if "paging" in comments:
            return clist + self.get_comments(
                next_page=comments["paging"]["cursors"]["after"],
                clist=comments["data"])
        else:
            return clist + comments["data"]

    def _check_mentioned_users(self, comment, count=1, unique=True):
        users = self._get_mentioned_users(comment, unique=unique)
        if len(users) >= count:
            return True
        else:
            return False

    @staticmethod
    def _get_mentioned_users(comment, unique=True):
        users = []
        for word in comment['text'].split():
            if word.startswith('@'):
                if word in users and unique:
                    continue
                else:
                    users.append(word)
        return users

    def _check_unique_mentioned_users(self, comments):
        sortedlist = sorted(comments, key=itemgetter('username'))
        current_user = None
        deny_list =[]
        for i in range(len(sortedlist)):
            if current_user != sortedlist[i]['username']:
                current_user = sortedlist[i]['username']
                userlist = []
            u = self._get_mentioned_users(sortedlist[i])
            if len(userlist+u) == len(set(userlist+u)):
                userlist.extend(u)
            else:
                deny_list.append(sortedlist[i])
        return sortedlist, deny_list

    def filter_by_rule(self):
        comments = self.get_comments()
        pass_list = []
        deny_list = []
        for c in comments:
            if not self._check_mentioned_users(c, count=2):
                deny_list.append(c)
            else:
                pass_list.append(c)
        pass_list, d = self._check_unique_mentioned_users(pass_list)
        deny_list.extend(d)
        return pass_list, deny_list
