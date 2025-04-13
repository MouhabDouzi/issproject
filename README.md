# TravelPlanner

TravelPlanner is a modern web application that helps users create personalized travel plans using AI-powered recommendations. Built with Vue.js, Vuetify, and Flask, it offers a beautiful and intuitive interface for planning your next adventure.

## Features

- 🎨 Modern UI with Vuetify components
- 🧠 AI-powered travel recommendations
- 📱 Responsive design for all devices
- 🔒 Secure user authentication
- 📊 Smart itinerary planning
- 💾 Save and manage travel plans
- ⭐ Favorite and share plans

## Tech Stack

### Frontend
- Vue.js 3
- Vuetify 3
- Vuex 4
- Vue Router 4
- Axios
- Chart.js

### Backend
- Python 3.8+
- Flask
- SQLAlchemy
- JWT Authentication
- OpenAI API

## Getting Started

### Prerequisites
- Node.js 14+
- Python 3.8+
- pip
- npm or yarn

### Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/travelplanner.git
cd travelplanner
```

2. Install frontend dependencies:
```bash
npm install
```

3. Create and activate a Python virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

4. Install backend dependencies:
```bash
pip install -r requirements.txt
```

5. Set up environment variables:
```bash
cp .env.example .env
# Edit .env with your configuration
```

6. Initialize the database:
```bash
flask db upgrade
```

### Running the Application

1. Start the backend server:
```bash
flask run
```

2. Start the frontend development server:
```bash
npm run serve
```

3. Open your browser and navigate to `http://localhost:8080`

## Project Structure

```
travelplanner/
├── frontend/
│   ├── src/
│   │   ├── assets/
│   │   ├── components/
│   │   ├── views/
│   │   ├── router/
│   │   ├── store/
│   │   ├── App.vue
│   │   └── main.js
│   ├── public/
│   └── package.json
├── backend/
│   ├── app/
│   │   ├── models/
│   │   ├── routes/
│   │   ├── services/
│   │   └── utils/
│   ├── migrations/
│   ├── config.py
│   └── requirements.txt
└── README.md
```

## API Documentation

### Authentication
- POST `/api/auth/signup` - Register a new user
- POST `/api/auth/login` - User login
- POST `/api/auth/logout` - User logout

### Travel Plans
- GET `/api/plans` - Get user's travel plans
- POST `/api/plans/create` - Create a new travel plan
- GET `/api/plans/:id` - Get plan details
- PUT `/api/plans/:id` - Update a plan
- DELETE `/api/plans/:id` - Delete a plan

### Favorites
- GET `/api/favorites` - Get user's favorite plans
- POST `/api/favorites/:planId` - Add plan to favorites
- DELETE `/api/favorites/:planId` - Remove plan from favorites

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- OpenAI for providing the AI capabilities
- Vuetify team for the amazing UI components
- Vue.js team for the fantastic framework
- All contributors and users of TravelPlanner 