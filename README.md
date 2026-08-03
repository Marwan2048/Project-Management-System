
-------------------

# SprintHub

SprintHub is a web-based project management system built with **Django** that helps teams organize projects, manage tasks, and collaborate efficiently. It follows a structured workflow where projects are divided into stages, tasks are assigned to team members, and progress is tracked throughout the project's lifecycle.

The application implements **role-based authorization**, ensuring that every user can only perform actions permitted by their role.

---

## Features

### Project Management
- Create, edit, and delete projects.
- Define project title, description, start date, and deadline.
- Track project progress automatically based on completed tasks.
- Dashboard displaying active and completed projects.

### Stage Management
- Create, update, and delete project stages.
- Organize project workflow into multiple phases.

### Task Management
- Create tasks inside project stages.
- Assign tasks to project members.
- Edit and delete tasks.
- Mark assigned tasks as completed.
- Filter tasks by:
  - Completion status
  - Priority
  - Assigned member

### Team Management
- Invite users to projects using their email address.
- Accept or decline project invitations.
- Remove members from a project.
- Members can leave projects voluntarily.

### Authorization & Security
The application includes backend authorization to protect every sensitive action.

Examples include:
- Only authenticated users can access the system.
- Only project members can view project details.
- Only team leaders can:
  - Edit projects
  - Delete projects
  - Manage stages
  - Create tasks
  - Assign tasks
  - Invite members
  - Remove project members
- Only task owners can mark their tasks as completed.
- Users cannot access projects they are not members of, even by manually entering URLs.

---





# Roles

## Team Leader

A Team Leader can:

- Create projects
- Edit projects
- Delete projects
- Create stages
- Edit stages
- Delete stages
- Create tasks
- Assign tasks
- Invite members
- Remove members

---

## Member

A Member can:

- View joined projects
- View project tasks
- Complete tasks assigned to them
- Accept or decline invitations
- Leave a project

---

# Project Workflow

1. Register or log in.
2. Create a new project.
3. Add project stages.
4. Invite team members.
5. Members accept invitations.
6. Create tasks inside stages.
7. Assign tasks to project members.
8. Members complete assigned tasks.
9. Track project progress from the dashboard.

---

# Installation

## Clone the repository

```bash
git clone <repository-url>
cd SprintHub
```

---

## Create a virtual environment

### Windows

```powershell
python -m venv myenv
.\myenv\Scripts\Activate.ps1
```

### Linux / macOS

```bash
python3 -m venv myenv
source myenv/bin/activate
```

---

## Install dependencies

```bash
pip install -r requirements.txt
```

---

## Apply migrations

```bash
python manage.py migrate
```

---

## Create a superuser (Optional)

```bash
python manage.py createsuperuser
```

---

## Run the development server

```bash
python manage.py runserver
```

Open your browser and visit:

```
http://127.0.0.1:8000/
```

---

# Security

SprintHub uses Django's built-in authentication system together with custom role-based authorization.

Permissions are enforced on the **backend**, preventing unauthorized users from accessing protected resources even if they manually modify URLs.

Examples include:

- Project membership verification
- Team leader authorization
- Task ownership validation
- Invitation ownership validation
- Login protection using `LoginRequiredMixin`
- `PermissionDenied` responses for unauthorized actions

---
