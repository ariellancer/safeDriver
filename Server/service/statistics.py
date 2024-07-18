from typing import List, Dict

from Server.models.user import User
from Statistics.create_chart import create_clock_pie_chart


def get_statistics_service(user: User) -> List[Dict[str, float]]:
    # Return the hour slots as a list of dictionaries
    return create_clock_pie_chart(user.statistics, 'a')


def update_statistics_service(user, start_hour, end_hour, unfocused):
    try:
        # Define the number of hours per cell
        hours_per_cell = 2

        # Calculate the total hours of driving
        total_hours = end_hour - start_hour

        # Check if the driving duration is more than 2 hours
        if total_hours > 2:
            # Calculate the number of full 2-hour intervals
            num_intervals = total_hours // 2

            # Distribute unfocused evenly across the intervals
            unfocused_per_interval = unfocused // num_intervals
            remainder = unfocused % num_intervals
        else:
            num_intervals = 1  # Only one interval if driving duration <= 2 hours
            unfocused_per_interval = unfocused
            remainder = 0

        # Convert start and end hours to cell indices
        start_index = start_hour // hours_per_cell
        end_index = end_hour // hours_per_cell

        # Ensure the indices are within the valid range
        start_index = max(0, min(start_index, len(user.statistics) - 1))
        end_index = max(0, min(end_index, len(user.statistics) - 1))

        # Update the Statistics for each cell in the range
        for index in range(start_index, end_index + 1):
            # Distribute unfocused evenly across the intervals
            if index < start_index + num_intervals:
                user.statistics[index] += unfocused_per_interval
                # Add one more unit to the last interval if there's a remainder
                if remainder > 0 and index == start_index + num_intervals - 1:
                    user.statistics[index] += 1
                    remainder -= 1
            else:
                break

        # Save the updated user document
        user.save()

        return True, None  # Success indicator and no error message
    except Exception as e:
        return False, str(e)
