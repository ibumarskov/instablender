# -*- coding: utf-8 -*-

import os
from prettytable import PrettyTable
from lib.instablender import InstaBlenderMedia

my_app_id = os.environ.get('MY_APP_ID')
my_app_secret = os.environ.get('MY_APP_SECRET')
my_access_token = os.environ.get('MY_ACCESS_TOKEN')

ig_post = InstaBlenderMedia(my_access_token, my_app_id, my_app_secret,
                            media_id=17869431460292915)
pass_list, deny_list = ig_post.filter_by_rule()
table = PrettyTable(["Num", "User", "Comment"])
for i in range(len(pass_list)):
    table.add_row([i, pass_list[i]['username'], pass_list[i]['text']])
print "=== Pass list ==="
print table.get_string()

table = PrettyTable(["Num", "User", "Comment"])
for i in range(len(deny_list)):
    table.add_row([i, deny_list[i]['username'], deny_list[i]['text'][:50]])
print "=== Deny list ==="
print table.get_string()
