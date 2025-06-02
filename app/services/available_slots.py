from typing import List, Tuple
from datetime import datetime, timedelta, time as Time, date
from dto.request_schema import RequestGet

async def get_available_slots(dt: date, schedule_start: Time, schedule_end: Time, requests: List['RequestGet'], minutes_delta: int) -> list[Time]:
    busy_intervals: List[Tuple[datetime, datetime]] = await generate_busy_intervals(requests)
    slots = []
    cursor = datetime.combine(date.today(), schedule_start)
    schedule_end_dt = datetime.combine(date.today(), schedule_end)
    if len(busy_intervals) > 0:
        cursor = datetime.combine(dt, schedule_start)
        schedule_end_dt = datetime.combine(dt, schedule_end)

    while cursor + timedelta(minutes=minutes_delta) <= schedule_end_dt:
        overlap = any(b <= cursor <= e for b, e in busy_intervals)
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