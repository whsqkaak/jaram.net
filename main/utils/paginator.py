from django.core.paginator import Paginator, EmptyPage
from django.db.models import QuerySet


def easy_paginator(data, page, each_data_count=12, display_button_range=3, save_to=None):
    super_paginator = Paginator(data, each_data_count)
    page = int(page)
    range_size = display_button_range * 2 + 1

    prefix_size = 2
    postfix_size = 2

    try:
        page_data = super_paginator.page(page)
    except EmptyPage:
        page_data = super_paginator.page(super_paginator.num_pages)

    last_page = super_paginator.num_pages
    visible_first_page = page - display_button_range
    visible_last_page = page + display_button_range

    if visible_first_page < 1 or last_page <= range_size:
        visible_first_page = 1
    elif last_page > range_size + postfix_size and visible_first_page > last_page - range_size - postfix_size:
        visible_first_page = last_page - range_size - postfix_size

    if visible_last_page > last_page or last_page <= range_size:
        visible_last_page = last_page
    elif last_page > range_size + prefix_size > visible_last_page:
        visible_last_page = range_size + prefix_size

    display_button_list = map(lambda x: x + 1, range(visible_first_page - 1, visible_last_page))

    if isinstance(data, QuerySet):
        count = data.count()
    else:
        count = len(data)

    if save_to is not None:
        save_to['page'] = page_data
        save_to['count'] = count
        save_to['last_page'] = last_page
        save_to['display_button_list'] = display_button_list

    return page_data, last_page, display_button_list, count