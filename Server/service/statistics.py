import math
from typing import List, Dict
from Server.service.user import find_user_by_username_service
from Server.models.user import User
from Statistics.create_chart import create_clock_pie_chart


def get_statistics_service(user):
    print(user.statistics)
    return create_clock_pie_chart(user.statistics)


async def update_statistics_service(user, unfocused_array):
    try:
        user = await find_user_by_username_service(user)
        for i in range(len(unfocused_array)):
            user.statistics[i] = user.statistics[i] + unfocused_array[i]
        user.save()

        return True, None  # Success indicator and no error message
    except Exception as e:
        return False, str(e)
