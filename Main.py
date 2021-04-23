# We'll compare these two types of posts to determine the following:
#
#     Do Ask HN or Show HN receive more comments on average?
#     Do posts created at a certain time receive more comments on average?
#
# Tasks for further improvement:

#    Determine if show or ask posts receive more points on average.
#    Determine if posts created at a certain time are more likely to receive more points.
#    Compare your results to the average number of comments and points other posts receive.

import datetime as dt
from csv import reader

opener = open('Hacker_News.csv', encoding='utf8')
read = reader(opener)
hn = list(read)
headers = hn[:1]
hn = hn[1:]
print(hn[:5])

ask_posts = []
show_posts = []
other_posts = []

count_a_pnts = 0
count_s_pnts = 0

for row in hn:
    title = row[1]
    title = title.lower()
    if title.startswith('ask hn'):
        ask_posts.append(row)
    elif title.startswith('show hn'):
        show_posts.append(row)
    else:
        other_posts.append(row)

print('ask posts: ', len(ask_posts), '\n')
print(ask_posts[:4])
print('\n')
print('show posts: ', len(show_posts), '\n')
print(show_posts[:4])
print('other posts: ', len(other_posts))

total_ask_comments = 0
total_show_comments = 0

for s_post in show_posts:
    s_num_comments = int(s_post[-3])
    total_show_comments += s_num_comments

for a_post in ask_posts:
    a_num_comments = int(a_post[-3])
    total_ask_comments += a_num_comments

avg_ask_comments = (total_ask_comments / len(ask_posts))
print('Average Ask Comments per Post: ', avg_ask_comments)
print('\n')
avg_show_comments = (total_show_comments / len(show_posts))
print('Average Show Comments per Post: ', avg_show_comments)

# Determine if show or ask posts receive more points on average.

for a_pnts in ask_posts:
    pnts = int(a_pnts[3])
    count_a_pnts += pnts

for s_pnts in show_posts:
    pnts2 = int(s_pnts[3])
    count_s_pnts += pnts2

ask_post_avrg_points = count_a_pnts / len(ask_posts)
show_post_avrg_points = count_s_pnts / len(show_posts)

print('Overall points for ask: ', count_a_pnts)
print(ask_post_avrg_points)
print('Overall points for show: ', count_s_pnts)
print(show_post_avrg_points)


result_list = []
counts_by_hour = {}
comments_by_hour = {}

points_list = []
points_by_hour = {}

for post in ask_posts:
    created_at = post[-1]
    num_comments = int(post[-3])
    result_list.append([created_at, num_comments])

for row2 in show_posts:
    pnts = int(row2[3])
    created = row2[-1]
    points_list.append([created, pnts])

for row in result_list:
    date_str = row[0]
    comment = row[1]
    date_dt = dt.datetime.strptime(date_str, "%m/%d/%Y %H:%M")
    hour = date_dt.strftime("%H")
    if hour not in counts_by_hour:
        counts_by_hour[hour] = 1
        comments_by_hour[hour] = comment
    elif hour in counts_by_hour:
        counts_by_hour[hour] += 1
        comments_by_hour[hour] += comment

for i in points_list:
    d_str = row[0]
    d_obj = dt.datetime.strptime(d_str, "%m/%d/%Y %H:%M")
    h_points = d_obj.strftime("%H")
    pnts2 = row[1]
    if h_points not in points_by_hour:
        points_by_hour[h_points] = pnts
    elif h_points in points_by_hour:
        points_by_hour[h_points] += pnts
print(points_list[:5])
print('\n')
print(points_by_hour)
print(counts_by_hour)
print(comments_by_hour)

avg_by_hour = []

for post in counts_by_hour:
    avg_by_hour.append([post,(comments_by_hour[post] / counts_by_hour[post])])
print(avg_by_hour, '\n')

swap_avg_by_hour = []

for row in avg_by_hour:
    swap_avg_by_hour.append([row[1], row[0]])

sorted_swap = sorted(swap_avg_by_hour, reverse=True)

print("Top 5 Hours for Ask Posts Comments")

for i in sorted_swap[:5]:
    dt_obj = dt.datetime.strptime(i[1], "%H")
    dt_str = dt.datetime.strftime(dt_obj, "%H:%M")
    print("{}: {} average comments per post".format(dt_str, i[0]))
#print(sorted_swap)