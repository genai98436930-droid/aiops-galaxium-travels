
🚀 Quick Start
pip install -r requirements.txt
python backend/server.py

Server:

http://localhost:8001

🔌 API Usage
1. Get flights
curl -X POST http://localhost:8001/api/agent \
-H "Content-Type: application/json" \
-d '{"input":"show flights"}'
2. Find user
curl -X POST http://localhost:8001/api/agent \
-H "Content-Type: application/json" \
-d '{"input":"find user Alice","name":"Alice","email":"alice@example.com"}'
3. Book flight
curl -X POST http://localhost:8001/api/agent \
-H "Content-Type: application/json" \
-d '{
  "input": "book flight for Alice",
  "user_id": 1,
  "flight_id": 3,
  "seat_class": "economy"
}'
4. View bookings
curl -X POST http://localhost:8001/api/agent \
-H "Content-Type: application/json" \
-d '{"input":"show bookings for Alice","user_id":1}'
5. Cancel booking
curl -X POST http://localhost:8001/api/agent \
-H "Content-Type: application/json" \
-d '{"input":"cancel booking 21","booking_id":21}'

