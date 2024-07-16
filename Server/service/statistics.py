from typing import List, Dict

from Server.models.user import User


def get_statistics(user: User) -> List[Dict[str, float]]:
    # Return the hour slots as a list of dictionaries
    return [{"percentage": slot.percentage} for slot in user.hour_slots]


def update_statistics_service(user, start, end, unfocused):
    try:
        # Update the user's statistics
        user.statistics[start:end] = unfocused  # Example update logic
        user.save()

        return True, None  # Success indicator and error message
    except Exception as e:
        return False, str(e)
