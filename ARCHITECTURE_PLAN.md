# BDPDB Modernization Architecture Plan

## Executive Summary

This document outlines the planned architecture for rebuilding the Brain Damage Patient Data Browser (BDPDB) using modern frameworks and best practices while maintaining integration with the Python and Nipy ecosystems.

## Current State Analysis

### Existing Technology Stack
- **Backend Framework**: Flask + Flask-AppBuilder
- **Database**: SQLite (with support for MySQL/PostgreSQL)
- **Image Processing**: nibabel, numpy, pandas (HDF5 storage)
- **Frontend**: Jinja2 templates, Bootstrap, Papaya viewer (JavaScript)
- **Authentication**: Flask-AppBuilder's built-in auth (DB, LDAP, OpenID)

### Core Functionality (from existing codebase)

1. **Patient Data Management**
   - Patient demographics (ID, DOB, sex)
   - Brain damage metadata (damaged areas, laterality, etiology, data source)
   - Lesion mask storage (MNI space)
   - Notes and annotations

2. **Scan Management**
   - Multiple scan modalities per patient
   - Scan metadata (date, modality, filename)
   - Linkage to patient records

3. **Neuroimaging Visualization**
   - Interactive brain image viewing (Papaya viewer)
   - Lesion mask overlay visualization
   - Overlap heatmap generation across patients
   - Support for MNI and native space viewing

4. **Search and Query**
   - MNI coordinate-based search
   - ROI-based overlap analysis
   - Patient filtering by demographics and damage characteristics

5. **Data Security**
   - User authentication and authorization
   - Role-based access control (Admin, Public)
   - Protected patient data access

## Proposed Modern Architecture

### Design Principles

1. **Separation of Concerns**: Clear separation between backend API, data processing, and frontend
2. **Scalability**: Support for growing datasets and concurrent users
3. **Maintainability**: Modern, well-documented frameworks with active communities
4. **Security-First**: Enhanced security measures for sensitive patient data
5. **Extensibility**: Plugin architecture for custom analyses and integrations
6. **Cloud-Ready**: Containerized deployment with cloud storage options

### Technology Stack

#### Backend (Python Ecosystem)

**Core Framework**: FastAPI
- Modern async Python web framework
- Automatic OpenAPI/Swagger documentation
- Strong type hints with Pydantic
- Better performance than Flask
- Native async support for concurrent operations

**Database Layer**:
- **ORM**: SQLAlchemy 2.0 with async support
- **Database**: PostgreSQL (primary), with SQLite for development
- **Migrations**: Alembic
- **File Storage**: 
  - S3-compatible object storage for NIfTI files (MinIO for on-prem, AWS S3 for cloud)
  - PostgreSQL for metadata and search indices

**Authentication & Authorization**:
- **Framework**: FastAPI-Users or custom JWT implementation
- **Standards**: OAuth2 with JWT tokens
- **Features**:
  - Multi-factor authentication (MFA)
  - SSO support (SAML, OAuth)
  - Fine-grained RBAC (Role-Based Access Control)
  - Audit logging for HIPAA compliance

**Image Processing (Nipy Ecosystem)**:
- **nibabel**: NIfTI file I/O
- **nilearn**: Image manipulation and analysis
- **numpy**: Array operations
- **scipy**: Scientific computing
- **nipype**: Workflow management for complex analyses
- **SimpleITK** or **ANTs** (via nipype): Advanced registration

**Data Processing**:
- **pandas**: Tabular data manipulation
- **xarray**: N-dimensional labeled arrays (alternative to HDF5)
- **zarr**: Chunked, compressed array storage (cloud-friendly alternative to HDF5)
- **dask**: Parallel computing for large datasets

**API Documentation**:
- **OpenAPI**: Automatic via FastAPI
- **ReDoc/Swagger UI**: Interactive API documentation

#### Frontend

**Framework**: React with TypeScript
- Component-based architecture
- Strong typing for better maintainability
- Large ecosystem and community

**State Management**: 
- **TanStack Query** (React Query): Server state management
- **Zustand** or **Jotai**: Client state management (lightweight)

**UI Framework**:
- **Material-UI (MUI)** or **Ant Design**: Component library
- **Tailwind CSS**: Utility-first styling
- Responsive design for tablets and desktops

**Neuroimaging Visualization**:
- **Niivue**: Modern WebGL-based NIfTI viewer (successor to Papaya)
  - Better performance
  - Active development
  - More features (annotations, drawing tools)
  - TypeScript support
- **AMI (A Medical Imaging)**: Alternative WebGL viewer
- **VTK.js**: For advanced 3D visualizations

**Data Visualization**:
- **Plotly.js** or **D3.js**: Interactive charts for statistics
- **React-Plotly**: React bindings

**Build Tools**:
- **Vite**: Fast build tool and dev server
- **ESLint/Prettier**: Code quality and formatting

#### Infrastructure

**Containerization**:
- **Docker**: Application containers
- **Docker Compose**: Local development orchestration
- **Kubernetes**: Production orchestration (optional)

**API Gateway/Reverse Proxy**:
- **Nginx** or **Traefik**: Load balancing, SSL termination

**Monitoring & Logging**:
- **Prometheus + Grafana**: Metrics and dashboards
- **ELK Stack** or **Loki**: Centralized logging
- **Sentry**: Error tracking

**CI/CD**:
- **GitHub Actions**: Automated testing and deployment
- **Pre-commit hooks**: Code quality checks

### Architecture Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                         Frontend                             │
│  ┌─────────────┐  ┌──────────────┐  ┌──────────────────┐  │
│  │   React     │  │  Niivue      │  │  Data Viz        │  │
│  │   (TypeScript)  │  (WebGL)    │  │  (Plotly)        │  │
│  └─────────────┘  └──────────────┘  └──────────────────┘  │
└─────────────────────────────────────────────────────────────┘
                            │
                     HTTPS/REST API
                            │
┌─────────────────────────────────────────────────────────────┐
│                     API Gateway (Nginx)                      │
└─────────────────────────────────────────────────────────────┘
                            │
┌─────────────────────────────────────────────────────────────┐
│                    Backend (FastAPI)                         │
│  ┌──────────────┐  ┌──────────────┐  ┌─────────────────┐  │
│  │   API        │  │   Auth       │  │   Background    │  │
│  │   Endpoints  │  │   Service    │  │   Tasks         │  │
│  └──────────────┘  └──────────────┘  └─────────────────┘  │
│                                                              │
│  ┌──────────────┐  ┌──────────────┐  ┌─────────────────┐  │
│  │   Image      │  │   Search     │  │   Analysis      │  │
│  │   Processing │  │   Service    │  │   Pipelines     │  │
│  └──────────────┘  └──────────────┘  └─────────────────┘  │
└─────────────────────────────────────────────────────────────┘
            │                     │                    │
    ┌───────┴─────────┐  ┌────────┴────────┐  ┌──────┴──────┐
    │   PostgreSQL    │  │  Object Storage │  │   Redis     │
    │   (Metadata)    │  │  (NIfTI files)  │  │   (Cache)   │
    └─────────────────┘  └─────────────────┘  └─────────────┘
```

### Data Model

#### Enhanced Entity-Relationship Design

**Core Entities**:

1. **User** (enhanced)
   - id, email, hashed_password
   - roles (admin, researcher, viewer)
   - mfa_enabled, mfa_secret
   - last_login, is_active
   - institution, department

2. **Patient** (enhanced from current)
   - id, patient_label (anonymized)
   - dob (year only or full date based on requirements)
   - sex, handedness
   - institution_id (for multi-site support)
   - created_at, updated_at, created_by

3. **BrainDamage** (new, extracted from Patient)
   - id, patient_id
   - damaged_areas (many-to-many with BrainArea)
   - laterality, etiology
   - insult_date
   - notes

4. **Scan** (enhanced)
   - id, patient_id
   - modality, scan_date
   - object_key (S3/MinIO path)
   - metadata (JSONB for BIDS sidecar data)
   - quality_rating
   - processing_status

5. **LesionMask** (new, extracted from Patient)
   - id, patient_id
   - space (native, MNI152, etc.)
   - object_key (S3/MinIO path)
   - volume_mm3, center_of_mass
   - overlap_map_id (for caching)

6. **SpatialIndex** (new for coordinate search)
   - Spatial data structure for efficient coordinate queries
   - Could use PostGIS extension or custom implementation

7. **Analysis** (new)
   - id, name, description
   - type (overlap, connectivity, etc.)
   - parameters (JSONB)
   - status, result_path
   - created_by, created_at

8. **AuditLog** (new)
   - id, user_id, action
   - resource_type, resource_id
   - timestamp, ip_address

### API Design

RESTful API with the following main endpoints:

#### Authentication
```
POST   /api/v1/auth/register
POST   /api/v1/auth/login
POST   /api/v1/auth/logout
POST   /api/v1/auth/refresh
GET    /api/v1/auth/me
```

#### Patients
```
GET    /api/v1/patients              # List with filtering
GET    /api/v1/patients/{id}         # Detail view
POST   /api/v1/patients              # Create
PUT    /api/v1/patients/{id}         # Update
DELETE /api/v1/patients/{id}         # Delete
GET    /api/v1/patients/{id}/scans   # Patient scans
GET    /api/v1/patients/{id}/masks   # Patient masks
```

#### Search
```
POST   /api/v1/search/coordinates    # MNI coordinate search
POST   /api/v1/search/roi            # ROI overlap search
POST   /api/v1/search/demographics   # Search by patient attributes
```

#### Scans
```
GET    /api/v1/scans
GET    /api/v1/scans/{id}
POST   /api/v1/scans
GET    /api/v1/scans/{id}/download   # Secure file download
```

#### Analysis
```
GET    /api/v1/analysis              # List analyses
POST   /api/v1/analysis/overlap      # Generate overlap map
POST   /api/v1/analysis/connectivity # Connectivity analysis
GET    /api/v1/analysis/{id}         # Analysis status/results
```

#### Visualization
```
GET    /api/v1/viewer/image/{id}     # Get image for viewer
GET    /api/v1/viewer/overlay-map    # Generate overlay heatmap
```

### Security Enhancements

1. **Authentication**
   - JWT tokens with short expiration (15 min) and refresh tokens
   - MFA support (TOTP-based)
   - SSO integration (SAML 2.0, OAuth 2.0)

2. **Authorization**
   - Granular RBAC with custom permissions
   - Row-level security in PostgreSQL
   - API rate limiting

3. **Data Protection**
   - Encryption at rest (database, object storage)
   - Encryption in transit (TLS 1.3)
   - PHI/PII redaction in logs
   - Automatic data anonymization tools

4. **Audit & Compliance**
   - Comprehensive audit logging
   - HIPAA compliance features
   - GDPR compliance tools (right to access, right to deletion)
   - Regular security scanning (OWASP)

5. **Network Security**
   - VPN/VPC deployment options
   - IP whitelisting
   - DDoS protection

### Key Features Implementation

#### 1. Patient Data Management
- RESTful CRUD API for patients
- Bulk import from CSV/BIDS format
- Data validation and integrity checks
- Versioning for data changes

#### 2. Neuroimaging Visualization
- **Frontend**: Niivue component for interactive viewing
- **Backend**: Efficient image serving with range requests
- **Features**:
  - Multi-planar views (axial, sagittal, coronal)
  - Lesion mask overlay with adjustable opacity
  - Crosshair synchronization
  - Annotations and measurements
  - Export views as images

#### 3. Coordinate Search
**Implementation**:
```python
# Backend pseudo-code
def coordinate_search(x, y, z, radius=0):
    # Convert MNI coords to voxel indices
    voxel_coords = mni_to_voxel([x, y, z])
    
    # Query spatial index (could use PostGIS)
    # or query pre-computed mask database
    patients = query_masks_at_coordinate(voxel_coords, radius)
    
    return patients
```
- Use zarr or similar for efficient partial array access
- Spatial indexing for fast queries
- Option for radius-based search

#### 4. ROI Overlap Analysis
- Upload custom ROI (NIfTI format)
- Calculate overlap percentage with each patient mask
- Generate report and visualization
- Background job processing for large ROIs

#### 5. Overlap Heatmap
- Pre-computed or on-demand generation
- Efficient caching strategy
- Interactive visualization with patient filtering

#### 6. Multi-site Support (New Feature)
- Institution/site management
- Data segregation by institution
- Cross-site queries (with permissions)

### Migration Strategy

#### Phase 1: Foundation (Weeks 1-4)
- [ ] Set up development environment
- [ ] Initialize FastAPI project structure
- [ ] Set up PostgreSQL database
- [ ] Implement basic authentication
- [ ] Create data models and migrations
- [ ] Set up object storage (MinIO for dev)

#### Phase 2: Core Backend (Weeks 5-8)
- [ ] Implement patient CRUD API
- [ ] Implement scan management API
- [ ] Set up image processing service
- [ ] Implement coordinate search
- [ ] Create data migration scripts from old DB

#### Phase 3: Frontend Foundation (Weeks 9-12)
- [ ] Set up React + TypeScript project
- [ ] Implement authentication UI
- [ ] Create patient list and detail views
- [ ] Integrate Niivue for image viewing
- [ ] Implement search interface

#### Phase 4: Advanced Features (Weeks 13-16)
- [ ] ROI overlap analysis
- [ ] Overlap heatmap generation
- [ ] Analysis pipelines
- [ ] Admin dashboard
- [ ] Reporting features

#### Phase 5: Testing & Hardening (Weeks 17-20)
- [ ] Comprehensive testing (unit, integration, e2e)
- [ ] Security audit and penetration testing
- [ ] Performance optimization
- [ ] Load testing
- [ ] Documentation completion

#### Phase 6: Deployment & Migration (Weeks 21-24)
- [ ] Production deployment setup
- [ ] Data migration from legacy system
- [ ] User training
- [ ] Gradual rollout
- [ ] Legacy system parallel operation
- [ ] Final cutover

### Data Migration Plan

1. **Export from Legacy System**
   - Export SQLite database to SQL dumps
   - Copy all NIfTI files with directory structure
   - Export user accounts and permissions

2. **Transform Data**
   - Map old schema to new schema
   - Update file paths to object storage keys
   - Anonymize any additional PII if needed
   - Validate data integrity

3. **Import to New System**
   - Load metadata into PostgreSQL
   - Upload images to object storage
   - Recreate user accounts
   - Verify all relationships

4. **Validation**
   - Compare record counts
   - Spot-check patient records
   - Verify image accessibility
   - Test search functionality

### Development Environment Setup

```bash
# Backend
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Database
docker-compose up -d postgres minio redis

# Frontend
cd frontend
npm install
npm run dev
```

### Testing Strategy

1. **Backend Testing**
   - Unit tests (pytest)
   - Integration tests (TestClient)
   - API contract tests (Pydantic validation)
   - Database migration tests

2. **Frontend Testing**
   - Unit tests (Jest, React Testing Library)
   - Component tests (Storybook)
   - E2E tests (Playwright or Cypress)

3. **Security Testing**
   - OWASP ZAP scanning
   - Dependency vulnerability scanning (Snyk, Safety)
   - Penetration testing

4. **Performance Testing**
   - Load testing (Locust)
   - Image serving performance
   - Database query optimization

### Documentation Requirements

1. **User Documentation**
   - Getting started guide
   - User manual with screenshots
   - Video tutorials
   - FAQ

2. **API Documentation**
   - OpenAPI spec (auto-generated)
   - Integration examples
   - Authentication guide

3. **Developer Documentation**
   - Architecture overview
   - Setup instructions
   - Contribution guidelines
   - Code style guide

4. **Operations Documentation**
   - Deployment guide
   - Backup and recovery procedures
   - Monitoring and alerting setup
   - Troubleshooting guide

### Monitoring & Observability

1. **Application Metrics**
   - API response times
   - Error rates
   - Request volume
   - User activity

2. **Infrastructure Metrics**
   - CPU, memory, disk usage
   - Database performance
   - Object storage I/O
   - Network bandwidth

3. **Business Metrics**
   - Number of patients
   - Number of scans
   - Search queries
   - Active users

4. **Alerts**
   - System errors
   - Performance degradation
   - Security events
   - Resource exhaustion

### Cost Considerations

1. **Development**
   - Developer time (estimated 6 months)
   - Testing and QA
   - Security audit

2. **Infrastructure**
   - Cloud hosting (if applicable)
   - Object storage
   - Database
   - Monitoring services

3. **Maintenance**
   - Ongoing development
   - Security updates
   - Support

### Success Metrics

1. **Performance**
   - API response time < 200ms (p95)
   - Image load time < 2s
   - Search results < 1s

2. **Reliability**
   - 99.9% uptime
   - Zero data loss
   - Automated backups

3. **Security**
   - Zero security incidents
   - 100% audit trail coverage
   - Regular security updates

4. **Usability**
   - User satisfaction score > 4/5
   - Reduced time for common tasks
   - Positive feedback from researchers

### Risks and Mitigation

1. **Data Migration Risk**
   - **Risk**: Data loss or corruption during migration
   - **Mitigation**: Extensive testing, parallel running, rollback plan

2. **Performance Risk**
   - **Risk**: Slow image loading or search
   - **Mitigation**: Caching, CDN, optimization, load testing

3. **Security Risk**
   - **Risk**: Data breach or unauthorized access
   - **Mitigation**: Security audit, encryption, MFA, regular updates

4. **Adoption Risk**
   - **Risk**: Users prefer old system
   - **Mitigation**: User training, gradual rollout, feedback incorporation

5. **Scope Creep**
   - **Risk**: Project timeline extends
   - **Mitigation**: Strict scope management, MVP approach, phased delivery

### Open Questions

1. **Deployment Model**
   - On-premise, cloud, or hybrid?
   - Single-tenant or multi-tenant?

2. **Data Retention**
   - What is the data retention policy?
   - Archive strategy for old data?

3. **Compliance**
   - Specific institutional requirements?
   - IRB approval needs?

4. **Integration**
   - Need to integrate with existing systems (PACS, EMR)?
   - Export to other analysis tools?

5. **Scale**
   - Expected number of patients/scans?
   - Number of concurrent users?
   - Geographic distribution?

## Conclusion

This architecture provides a modern, scalable, and secure foundation for BDPDB while maintaining the core functionality that researchers depend on. The use of FastAPI, React, and the Nipy ecosystem ensures maintainability and extensibility while adhering to best practices in web development and neuroimaging research.

The phased implementation approach allows for iterative development with regular feedback, while the comprehensive security and compliance features ensure the system meets the stringent requirements for handling patient data.

Next steps:
1. Review and approval of this architecture plan
2. Finalize technology choices based on specific institutional requirements
3. Set up development environment
4. Begin Phase 1 implementation
