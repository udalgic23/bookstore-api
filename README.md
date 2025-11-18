# bookstore-api
A simple API for managing a bookstore, built with FastAPI.
## Installation
1. Download the ZIP file and extract it.
2. Open the project in your IDE.
3. Create a virtual environment using the command:
  ```
  python -m venv myvenv
  ```
4. Activate the virtual environment:
   - On **Windows**:
   ```
   .\myvenv\Scripts\Activate.ps1
   ```
   - On **macOS/Linux**:
     ```
     source myvenv/bin/activate
     ```
5. Install required packages from requirements.txt using:
     ```
     pip install -r requirements.txt
     ```
6. Run the app using Uvicorn:
     ```
     uvicorn app:app --reload
     ```
7. Open Swagger UI in your web browser to test the APIs:
    ```
    https://127.0.0.1:8000/docs
    ```


- Developed a high-performance RESTful API using FastAPI to manage bookstore inventory, enabling efficient handling of CRUD operations and asynchronous request processing.
- Architected a robust data layer by integrating SQLAlchemy ORM with SQLite, designing relational database models and implementing automated data seeding scripts for rapid development and testing.
- Ensured data integrity and type safety by utilizing Pydantic schemas for strict request validation and response serialization, while leveraging auto-generated Swagger UI for interactive API documentation.
    
