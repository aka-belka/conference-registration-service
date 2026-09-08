from datetime import date 

room_name = "Аудитория 301" 
capacity = 30 
booking_date = date(2026, 9, 15) 
is_available = True 

def get_booking_status(is_available): 
    if is_available: 
        return "Помещение доступно для бронирования" 
    return "Помещение уже занято" 

print(f"Помещение: {room_name}") 
print(f"Вместимость: {capacity} человек") 
print(f"Дата: {booking_date}") 
print(get_booking_status(is_available))