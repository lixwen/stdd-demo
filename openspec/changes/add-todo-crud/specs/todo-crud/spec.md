## ADDED Requirements

### Requirement: Create a todo
The system SHALL allow creating a new todo item via POST /todos with a title field. The created todo SHALL have a unique auto-incremented integer id, the given title, and completed defaulting to false. The response SHALL return the created todo with status 201.

#### Scenario: Create todo with title only
- **WHEN** POST /todos with body `{"title": "Buy milk"}`
- **THEN** response status is 201 and body contains `{"id": 1, "title": "Buy milk", "completed": false}`

#### Scenario: Create todo with title and completed
- **WHEN** POST /todos with body `{"title": "Buy milk", "completed": true}`
- **THEN** response status is 201 and body contains `{"id": 1, "title": "Buy milk", "completed": true}`

#### Scenario: Create todo with missing title
- **WHEN** POST /todos with body `{}`
- **THEN** response status is 422 (validation error)

### Requirement: List all todos
The system SHALL return all existing todos via GET /todos as a JSON array. When no todos exist, the response SHALL be an empty array.

#### Scenario: List todos when empty
- **WHEN** GET /todos with no existing todos
- **THEN** response status is 200 and body is `[]`

#### Scenario: List todos with existing items
- **WHEN** two todos have been created and GET /todos is called
- **THEN** response status is 200 and body is an array of 2 todo objects

### Requirement: Get a single todo
The system SHALL return a single todo by id via GET /todos/{id}. If the todo does not exist, the system SHALL return 404.

#### Scenario: Get existing todo
- **WHEN** a todo with id 1 exists and GET /todos/1 is called
- **THEN** response status is 200 and body contains the todo with id 1

#### Scenario: Get non-existing todo
- **WHEN** no todo with id 999 exists and GET /todos/999 is called
- **THEN** response status is 404

### Requirement: Update a todo
The system SHALL allow updating a todo via PUT /todos/{id}. Both title and completed fields SHALL be optional in the update body. Only provided fields SHALL be updated. If the todo does not exist, the system SHALL return 404.

#### Scenario: Update todo title
- **WHEN** a todo with id 1 exists and PUT /todos/1 with body `{"title": "Buy eggs"}`
- **THEN** response status is 200 and the todo title is updated to "Buy eggs"

#### Scenario: Update todo completed status
- **WHEN** a todo with id 1 exists and PUT /todos/1 with body `{"completed": true}`
- **THEN** response status is 200 and the todo completed is updated to true

#### Scenario: Update non-existing todo
- **WHEN** no todo with id 999 exists and PUT /todos/999 is called
- **THEN** response status is 404

### Requirement: Delete a todo
The system SHALL allow deleting a todo via DELETE /todos/{id}. A successful deletion SHALL return 204 with no body. If the todo does not exist, the system SHALL return 404.

#### Scenario: Delete existing todo
- **WHEN** a todo with id 1 exists and DELETE /todos/1 is called
- **THEN** response status is 204 and the todo is no longer in the list

#### Scenario: Delete non-existing todo
- **WHEN** no todo with id 999 exists and DELETE /todos/999 is called
- **THEN** response status is 404
