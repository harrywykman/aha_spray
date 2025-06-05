# AHA Spray Records App

A web application developed using FastAPI and Jinja2 templates for managing and recording spray activities in vineyards. This application allows users to:

- Add, edit, and delete vineyard records.
- Manage spray units and associate them with vineyards.
- Record spray activities, including details like date, operator, weather conditions, and spray program.
- View and manage spray records associated with specific spray programs.

## Features

- **Vineyard Management**: Add and edit vineyard details.
- **Spray Unit Management**: Manage spray units and associate them with vineyards.
- **Spray Record Management**: Record and manage spray activities with detailed information.
- **Spray Program Association**: Link spray records to specific spray programs.
- **User Interface**: Clean and responsive web interface using Bootstrap.

## Installation

1. Clone the repository:

   git clone https://github.com/harrywykman/aha_spray.git
   cd aha_spray

2. Create a virtual environment:

    python3 -m venv venv
    source venv/bin/activate

3. Install dependencies:

    pip install -r requirements.txt

4. Run the application:

    uvicorn main:app --reload

The application will be accessible at http://127.0.0.1:8000.
`uvicorn main:app --reload`