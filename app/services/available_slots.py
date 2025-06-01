from typing import List, Tuple
from datetime import datetime, timedelta, time as Time, date
from dto.request_schema import RequestGet

async def get_available_slots(schedule_start: Time, schedule_end: Time, requests: List['RequestGet'], minutes_delta: int) -> list[Time]:
    busy_intervals: List[Tuple[datetime, datetime]] = await generate_busy_intervals(requests)
    slots = []
    cursor = datetime.combine(date.today(), schedule_start)
    schedule_end_dt = datetime.combine(date.today(), schedule_end)

    while cursor + timedelta(minutes=minutes_delta) <= schedule_end_dt:
        end = cursor + timedelta(minutes=minutes_delta)
        overlap = any(b <= cursor < e or b < end <= e for b, e in busy_intervals)
        if not overlap:
            slots.append(cursor.time())
        cursor = cursor + timedelta(minutes=minutes_delta)

    return slots

async def generate_busy_intervals(requests: List['RequestGet']) -> List[Tuple[datetime, datetime]]:
    output = []
    for req in requests:
        start = req.schedule_at
        end = start + timedelta(minutes=req.service.time_minutes)
        output.append((start, end))
    return output