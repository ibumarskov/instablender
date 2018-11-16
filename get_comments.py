# -*- coding: utf-8 -*-

import os
import json

from facebook_business.api import FacebookAdsApi
from facebook_business.adobjects.page import Page
from facebook_business.adobjects.shadowigmedia import ShadowIGMedia


my_app_id = os.environ.get('MY_APP_ID')
my_app_secret = os.environ.get('MY_APP_SECRET')
my_access_token = os.environ.get('MY_ACCESS_TOKEN')

FacebookAdsApi.init(my_app_id, my_app_secret, my_access_token)


def get_instagram_business_id():
    fields = [
        'instagram_business_account',
    ]
    params = {
    }
    accounts = Page('me/accounts').api_get(
        fields=fields,
        params=params,
    )
    for acc in  accounts["data"]:
        if "instagram_business_account" in acc:
            return acc["instagram_business_account"]["id"]

def get_media_id_by_text(acc_id, text):
    fields = [
        'caption',
    ]
    params = {
    }
    media = Page(acc_id + '/media').api_get(
        fields=fields,
        params=params,
    )
    for m in media["data"]:
        print m["id"]
        if text in m["caption"]:
            return m["id"]


def get_comments(media_id, next=None, clist=[]):
    fields = [
        "text", "username"
    ]
    params = {
        "limit": 50,
        "after": next,
    }
    comments = Page(str(media_id) + '/comments').api_get(
        fields=fields,
        params=params,
    )

    if "paging" in comments:
        return clist + get_comments(media_id, next=comments["paging"]["cursors"]["after"], clist=comments["data"])
    else:
        return clist + comments["data"]


acc_id = get_instagram_business_id()
media_id = get_media_id_by_text(acc_id, "some_text")  # 17869431460292915
ig_comments = get_comments(media_id)
for i in ig_comments:
    print i
print len(ig_comments)
