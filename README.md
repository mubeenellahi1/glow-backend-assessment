# Workflow API

This project implements a RESTful API for managing business workflows. It allows businesses to progress through various stages of a workflow, from creation to completion.

## Project Setup

1. Clone the repository:
   ```
   git clone https://github.com/your-username/workflow-api.git
   cd workflow-api
   ```

2. Create a virtual environment and activate it:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

4. Apply the database migrations:
   ```
   python manage.py migrate
   ```

5. Run the development server:
   ```
   python manage.py runserver
   ```

6. Access the API at `http://localhost:8000/api/` and the Swagger documentation at `http://localhost:8000/swagger/`

## Best Practices Used

1. **DRY (Don't Repeat Yourself) Principle**: 
   - Utilized Django's ORM and DRF's serializers to avoid code duplication.
   - Implemented reusable validation logic in the serializer.

2. **Model Validations**: 
   - Added field-level validators (e.g., for FEIN and phone numbers).
   - Implemented model-level validation in the `clean()` method.

3. **Serializer Validations**: 
   - Added custom validation logic in the serializer's `validate()` method to ensure data integrity and business rules.

4. **API Documentation**: 
   - Integrated Swagger/OpenAPI using `drf-yasg` for clear and interactive API documentation.

5. **Separation of Concerns**: 
   - Kept business logic in the model (`progress_workflow` method).
   - Handled data validation in the serializer.
   - Used viewsets for handling HTTP methods and requests.

6. **Error Handling**: 
   - Implemented custom error messages for various validation scenarios.

7. **Next Step Information**: 
   - Added a `get_next_step_info()` method to provide clear guidance on the next required action.

## API Swagger Documentation

- Swagger UI is available at `/swagger/`
- ReDoc UI is available at `/redoc/`

These provide interactive documentation for all API endpoints, allowing easy exploration and testing of the API.

## Assumptions

1. **Workflow Stages**: 
   - The workflow follows a specific order: New -> Market Approved/Declined -> Sales Approved -> Won/Lost.
   - Only businesses in the 'restaurants' or 'stores' industries can progress beyond the 'Market Approved' stage.

2. **Data Requirements**:
   - FEIN (Federal Employer Identification Number) is required and must be a 9-digit number.
   - Business name is required and must be at least 2 characters long.
   - Industry is optional when creating a business but required to progress from the 'New' stage.
   - Contact information (name and phone) is required to progress from 'Market Approved' to 'Sales Approved'.

3. **API Usage**:
   - The API is assumed to be used by authenticated clients (authentication system not implemented in this version).
   - Partial updates are allowed, meaning not all fields need to be provided in every request.

4. **Database**:
   - The project uses SQLite as the database for simplicity. In a production environment, a more robust database system would be recommended.

