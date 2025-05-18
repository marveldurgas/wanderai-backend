# WanderAI Architecture Documentation

## Overview

WanderAI follows a **Domain-based Architecture with Layered Structure** pattern, which organizes code around business domains while providing clear separation of concerns through layered components within each domain.

## Architectural Principles

1. **Domain-driven design**: Code is organized around business domains (users, travels, ai, maps) rather than technical components.
2. **Separation of concerns**: Each domain has distinct layers for different responsibilities.
3. **Interface contracts**: Interfaces define clear contracts between components.
4. **Dependency injection**: Components receive their dependencies from the outside, enhancing testability.
5. **Domain isolation**: Domains are weakly coupled, with minimal interdependencies.

## Directory Structure

```
wanderai-backend/
├── core/                      # Core shared functionality
│   ├── exceptions/            # Custom exception classes
│   ├── models/                # Base model classes
│   └── utils/                 # Shared utilities
├── users/                     # Users domain
│   ├── models/                # User-related data models
│   ├── repositories/          # Data access for users
│   ├── services/              # User business logic
│   ├── serializers/           # API data transformation
│   ├── interfaces.py          # User domain interfaces
│   ├── config.py              # Domain-specific configuration
│   └── views.py               # API endpoints
├── travels/                   # Travels domain
│   ├── models/                # Travel-related data models
│   ├── repositories/          # Data access for travels
│   ├── services/              # Travel business logic
│   ├── serializers/           # API data transformation
│   ├── interfaces.py          # Travel domain interfaces
│   ├── config.py              # Domain-specific configuration
│   └── views.py               # API endpoints
├── ai/                        # AI domain
│   ├── models/                # AI-related data models
│   ├── repositories/          # Data access for AI
│   ├── services/              # AI business logic
│   ├── serializers/           # API data transformation
│   ├── interfaces.py          # AI domain interfaces
│   ├── config.py              # Domain-specific configuration
│   └── views.py               # API endpoints
├── maps/                      # Maps domain
│   ├── interfaces.py          # Maps domain interfaces
│   ├── config.py              # Domain-specific configuration
│   └── views.py               # API endpoints
├── integrations/              # External service integrations
│   ├── supabase/              # Supabase integration
│   ├── openrouter/            # OpenRouter AI integration
│   ├── maps/                  # Maps API integration
│   └── interfaces.py          # Integration interfaces
└── wanderai/                  # Project configuration
    ├── settings.py            # Django settings
    ├── urls.py                # URL routing
    └── wsgi.py                # WSGI configuration
```

## Layers within Domains

Each domain follows a layered structure:

1. **Models Layer** (`models/`): Defines the data structure using Django models.
2. **Repository Layer** (`repositories/`): Handles data access operations, abstracting the database.
3. **Service Layer** (`services/`): Implements business logic, orchestrating repositories and other services.
4. **Serializer Layer** (`serializers/`): Transforms data between API and internal representations.
5. **Interface Layer** (`interfaces.py`): Defines contracts between components using Protocol classes.
6. **Configuration Layer** (`config.py`): Contains domain-specific configuration separate from global settings.
7. **View Layer** (`views.py`): Exposes API endpoints, uses services to process requests.

## Key Design Patterns

### Repository Pattern

The Repository pattern abstracts data access operations. Each domain has repositories that handle CRUD operations for the domain's entities.

Example:
```python
class UserRepository(BaseRepository):
    model_class = User
    
    def get_user_by_email(self, email):
        return self.model_class.objects.filter(email=email).first()
```

### Service Layer Pattern

The Service Layer pattern encapsulates business logic and orchestrates repositories and other services. Services implement domain-specific operations and use repositories for data access.

Example:
```python
class UserService(BaseService):
    def __init__(self):
        self.user_repository = UserRepository()
    
    def create_user(self, user_data):
        # Validate data
        # Create user in database
        # Additional business logic
        return user
```

### Dependency Injection

Components receive their dependencies from the outside, enhancing testability and decoupling.

Example:
```python
class TravelAIService(BaseService):
    def __init__(self, ai_client=None, maps_client=None, recommendation_repository=None):
        self.ai_client = ai_client or self._get_default_ai_client()
        self.maps_client = maps_client or self._get_default_maps_client()
        self.recommendation_repository = recommendation_repository or self._get_default_recommendation_repository()
```

### Interface Contracts

Interfaces define contracts between components using Python's Protocol classes.

Example:
```python
class AIModelProvider(Protocol):
    def get_available_models(self) -> List[Dict[str, Any]]:
        ...
    
    def generate_travel_suggestion(self, travel_data: Dict[str, Any]) -> Dict[str, Any]:
        ...
```

## Request Flow

1. Client request arrives at a view endpoint.
2. View calls appropriate service method.
3. Service implements business logic, calling repositories and other services as needed.
4. Repository performs data access operations.
5. Service processes repository results.
6. View serializes service response and returns to client.

## Benefits of this Architecture

1. **Maintainability**: Clear separation of concerns makes code easier to understand and maintain.
2. **Testability**: Dependency injection and interface contracts facilitate unit testing.
3. **Scalability**: Domain isolation allows different teams to work on different domains.
4. **Flexibility**: Implementation details can change within layers without affecting other layers.
5. **Clarity**: Organization follows business domains rather than technical concerns. 