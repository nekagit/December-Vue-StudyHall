# Database Documentation

Complete database schema and model documentation for the StudyHall Platform.

## Database Overview

The StudyHall Platform uses SQLAlchemy ORM with SQLite for MVP. The database can be easily migrated to PostgreSQL for production.

**Current Database**: SQLite (`backend/studyhall.db`)  
**ORM**: SQLAlchemy  
**Migration Tool**: Manual schema updates (Alembic recommended for production)

## Schema Diagram

```
┌─────────────┐
│   Student   │
├─────────────┤
│ id (PK)     │
│ email (UK)  │
│ name        │
│ password_   │
│   hash      │
│ is_active   │
│ created_at  │
└──────┬──────┘
       │
       │ 1
       │
       │ M
       │
┌──────▼──────┐      ┌─────────────┐
│  Bookmark   │      │  Material   │
├─────────────┤      ├─────────────┤
│ id (PK)     │      │ id (PK)     │
│ student_id  │──────┤ title       │
│   (FK)      │  M   │ content     │
│ material_id │      │ notion_     │
│   (FK)      │      │   page_id   │
│ created_at  │      │   (UK)      │
└─────────────┘      │ notion_url  │
       │             │ category    │
       │             │ order_index │
       │             │ created_at  │
       │             │ updated_at  │
       │             └──────┬──────┘
       │                    │
       │                    │ 1
       │                    │
       │                    │ M
       │                    │
┌──────▼────────────────────▼──────┐
│           Progress               │
├──────────────────────────────────┤
│ id (PK)                          │
│ student_id (FK)                  │
│ material_id (FK)                 │
│ status                           │
│ progress_percentage              │
│ last_accessed_at                 │
│ completed_at                     │
│ created_at                       │
│ updated_at                       │
└──────────────────────────────────┘
```

## Tables

### students

Stores student account information.

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | Integer | Primary Key, Auto-increment | Unique student identifier |
| email | String | Unique, Not Null, Indexed | Student email address (login) |
| name | String | Not Null | Student's full name |
| password_hash | String | Not Null | Hashed password (SHA-256 in MVP) |
| is_active | Boolean | Default: True | Account active status |
| created_at | DateTime | Auto-generated | Account creation timestamp |

**Indexes:**
- Primary key on `id`
- Unique index on `email`
- Index on `email` for fast lookups

**Constraints:**
- Email must be unique
- Email cannot be null
- Password hash cannot be null

**Relationships:**
- One-to-Many with `bookmarks`
- One-to-Many with `progress`

---

### materials

Stores course materials/content.

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | Integer | Primary Key, Auto-increment | Unique material identifier |
| title | String | Not Null, Indexed | Material title |
| content | Text | Nullable | Material content (Markdown/HTML) |
| notion_page_id | String | Unique, Indexed, Nullable | Notion page ID if synced |
| notion_url | String | Nullable | Original Notion URL |
| category | String | Nullable | Material category (e.g., "Python") |
| order_index | Integer | Default: 0 | Ordering index for display |
| created_at | DateTime | Auto-generated | Creation timestamp |
| updated_at | DateTime | Auto-updated | Last update timestamp |

**Indexes:**
- Primary key on `id`
- Index on `title` for search
- Unique index on `notion_page_id`

**Constraints:**
- Title cannot be null
- Notion page ID must be unique (if provided)

**Relationships:**
- One-to-Many with `bookmarks`
- One-to-Many with `progress`

---

### bookmarks

Tracks which materials students have bookmarked.

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | Integer | Primary Key, Auto-increment | Unique bookmark identifier |
| student_id | Integer | Foreign Key, Not Null | Reference to student |
| material_id | Integer | Foreign Key, Not Null | Reference to material |
| created_at | DateTime | Auto-generated | Bookmark creation timestamp |

**Indexes:**
- Primary key on `id`
- Foreign key indexes on `student_id` and `material_id`

**Constraints:**
- Student ID must reference existing student
- Material ID must reference existing material
- Application-level uniqueness: (student_id, material_id) pair should be unique

**Relationships:**
- Many-to-One with `students`
- Many-to-One with `materials`

---

### progress

Tracks student progress through materials.

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | Integer | Primary Key, Auto-increment | Unique progress identifier |
| student_id | Integer | Foreign Key, Not Null | Reference to student |
| material_id | Integer | Foreign Key, Not Null | Reference to material |
| status | String | Not Null | Progress status (enum) |
| progress_percentage | Float | Default: 0.0 | Progress percentage (0-100) |
| last_accessed_at | DateTime | Nullable | Last access timestamp |
| completed_at | DateTime | Nullable | Completion timestamp |
| created_at | DateTime | Auto-generated | Record creation timestamp |
| updated_at | DateTime | Auto-updated | Last update timestamp |

**Status Values:**
- `not_started`: Material not yet accessed
- `in_progress`: Material currently being studied
- `completed`: Material completed

**Indexes:**
- Primary key on `id`
- Foreign key indexes on `student_id` and `material_id`

**Constraints:**
- Student ID must reference existing student
- Material ID must reference existing material
- Status must be one of: `not_started`, `in_progress`, `completed`
- Progress percentage should be between 0 and 100 (enforced in application)

**Relationships:**
- Many-to-One with `students`
- Many-to-One with `materials`

## Models

### Student Model

**File**: `backend/models/student.py`

```python
class Student(Base):
    __tablename__ = "students"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    name = Column(String, nullable=False)
    password_hash = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
```

**Usage:**
```python
from backend.models import Student

# Create student
student = Student(
    email="student@example.com",
    name="John Doe",
    password_hash=hash_password("password")
)
db.add(student)
db.commit()
```

---

### Material Model

**File**: `backend/models/material.py`

```python
class Material(Base):
    __tablename__ = "materials"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False, index=True)
    content = Column(Text)
    notion_page_id = Column(String, unique=True, index=True)
    notion_url = Column(String)
    category = Column(String)
    order_index = Column(Integer, default=0)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
```

**Usage:**
```python
from backend.models import Material

# Create material
material = Material(
    title="Introduction to Python",
    content="Python is a programming language...",
    category="Python"
)
db.add(material)
db.commit()
```

---

### Bookmark Model

**File**: `backend/models/bookmark.py`

```python
class Bookmark(Base):
    __tablename__ = "bookmarks"
    
    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("students.id"), nullable=False)
    material_id = Column(Integer, ForeignKey("materials.id"), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    student = relationship("Student", backref="bookmarks")
    material = relationship("Material", backref="bookmarks")
```

**Usage:**
```python
from backend.models import Bookmark

# Create bookmark
bookmark = Bookmark(
    student_id=1,
    material_id=5
)
db.add(bookmark)
db.commit()
```

---

### Progress Model

**File**: `backend/models/progress.py`

```python
class Progress(Base):
    __tablename__ = "progress"
    
    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("students.id"), nullable=False)
    material_id = Column(Integer, ForeignKey("materials.id"), nullable=False)
    status = Column(String, nullable=False, default="not_started")
    progress_percentage = Column(Float, default=0.0)
    last_accessed_at = Column(DateTime(timezone=True))
    completed_at = Column(DateTime(timezone=True))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    student = relationship("Student", backref="progress_records")
    material = relationship("Material", backref="progress_records")
```

**Usage:**
```python
from backend.models import Progress

# Create progress
progress = Progress(
    student_id=1,
    material_id=5,
    status="in_progress",
    progress_percentage=45.0
)
db.add(progress)
db.commit()
```

## Common Queries

### Get Student with Bookmarks

```python
student = db.query(Student).filter(Student.id == student_id).first()
bookmarks = db.query(Bookmark).filter(Bookmark.student_id == student_id).all()
```

### Get Materials with Progress

```python
materials = db.query(Material).all()
for material in materials:
    progress = db.query(Progress).filter(
        Progress.student_id == student_id,
        Progress.material_id == material.id
    ).first()
```

### Search Materials

```python
search_term = "python"
materials = db.query(Material).filter(
    Material.title.ilike(f"%{search_term}%")
).all()
```

### Get Student Statistics

```python
from sqlalchemy import func

total_materials = db.query(func.count(Material.id)).scalar()
completed = db.query(func.count(Progress.id)).filter(
    Progress.student_id == student_id,
    Progress.status == "completed"
).scalar()
```

## Database Initialization

### Initial Setup

Run `backend/init_db.py` to:
1. Create all tables
2. Create default student account
3. Set up initial schema

### Manual Initialization

```python
from backend.database import Base, engine
from backend.models import Student, Material, Bookmark, Progress

# Create all tables
Base.metadata.create_all(bind=engine)

# Create default student
db = SessionLocal()
student = Student(
    email="student@studyhall.com",
    name="Default Student",
    password_hash=hash_password("password123")
)
db.add(student)
db.commit()
```

## Migrations

### Current Approach (MVP)

Tables are auto-created on application startup via:
```python
Base.metadata.create_all(bind=engine)
```

### Production Approach (Recommended)

Use Alembic for migrations:

1. **Install Alembic**:
```bash
pip install alembic
```

2. **Initialize**:
```bash
alembic init alembic
```

3. **Create Migration**:
```bash
alembic revision --autogenerate -m "Add new column"
```

4. **Apply Migration**:
```bash
alembic upgrade head
```

## Database Maintenance

### Backup

**SQLite:**
```bash
cp backend/studyhall.db backups/studyhall-$(date +%Y%m%d).db
```

**PostgreSQL:**
```bash
pg_dump studyhall > backups/studyhall-$(date +%Y%m%d).sql
```

### Restore

**SQLite:**
```bash
cp backups/studyhall-20240101.db backend/studyhall.db
```

**PostgreSQL:**
```bash
psql studyhall < backups/studyhall-20240101.sql
```

### Reset Database

```bash
# Delete database file
rm backend/studyhall.db

# Reinitialize
python backend/init_db.py
```

## Performance Considerations

### Indexes

Current indexes:
- `students.email` - Fast login lookups
- `materials.title` - Fast search
- `materials.notion_page_id` - Fast Notion sync lookups
- Foreign keys automatically indexed

### Query Optimization

- Use `filter()` before `join()` when possible
- Use `select_related()` for eager loading (if using SQLAlchemy relationships)
- Limit results with `.limit()` for pagination
- Use database functions for aggregations

### Future Optimizations

- Add composite indexes for common query patterns
- Implement pagination for large result sets
- Add full-text search index for material content
- Consider materialized views for dashboard stats

## Migration to PostgreSQL

### Update Connection String

In `backend/database.py`:
```python
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://user:password@localhost/studyhall"
)
engine = create_engine(DATABASE_URL)
```

### Update Column Types

Some SQLite-specific types may need adjustment:
- `DateTime(timezone=True)` works in both
- `Text` works in both
- `Boolean` works in both

### Test Migration

1. Export SQLite data
2. Import to PostgreSQL
3. Verify all relationships
4. Test application functionality

## Security Considerations

### Password Storage

- **Current**: SHA-256 hash (MVP)
- **Production**: Use bcrypt with salt rounds

### SQL Injection

- Protected by SQLAlchemy ORM
- Always use parameterized queries
- Never use string formatting for queries

### Data Validation

- Validate all inputs before database operations
- Use SQLAlchemy validators where appropriate
- Enforce constraints at application level
