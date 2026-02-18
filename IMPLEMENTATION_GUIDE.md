# BDPDB Implementation Guide

## Overview

This document provides detailed technical specifications and implementation guidance for developers working on the BDPDB modernization project. It complements the main Architecture Plan with specific code patterns, configurations, and best practices.

## Project Structure

```
bdpdb-v2/
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py                 # FastAPI application entry
│   │   ├── config.py               # Configuration management
│   │   ├── dependencies.py         # Dependency injection
│   │   │
│   │   ├── api/
│   │   │   ├── __init__.py
│   │   │   ├── v1/
│   │   │   │   ├── __init__.py
│   │   │   │   ├── auth.py         # Authentication endpoints
│   │   │   │   ├── patients.py     # Patient endpoints
│   │   │   │   ├── scans.py        # Scan endpoints
│   │   │   │   ├── search.py       # Search endpoints
│   │   │   │   └── analysis.py     # Analysis endpoints
│   │   │   └── dependencies.py
│   │   │
│   │   ├── core/
│   │   │   ├── __init__.py
│   │   │   ├── security.py         # Auth utilities
│   │   │   ├── config.py           # Settings
│   │   │   └── logging.py          # Logging setup
│   │   │
│   │   ├── models/
│   │   │   ├── __init__.py
│   │   │   ├── user.py
│   │   │   ├── patient.py
│   │   │   ├── scan.py
│   │   │   └── analysis.py
│   │   │
│   │   ├── schemas/
│   │   │   ├── __init__.py
│   │   │   ├── user.py             # Pydantic schemas
│   │   │   ├── patient.py
│   │   │   └── scan.py
│   │   │
│   │   ├── services/
│   │   │   ├── __init__.py
│   │   │   ├── auth.py
│   │   │   ├── patient.py
│   │   │   ├── imaging.py          # Image processing
│   │   │   ├── search.py           # Search logic
│   │   │   └── storage.py          # Object storage
│   │   │
│   │   ├── db/
│   │   │   ├── __init__.py
│   │   │   ├── session.py          # Database session
│   │   │   └── base.py             # Base model
│   │   │
│   │   └── tests/
│   │       ├── __init__.py
│   │       ├── conftest.py
│   │       ├── test_api/
│   │       ├── test_services/
│   │       └── test_models/
│   │
│   ├── alembic/                    # Database migrations
│   │   ├── versions/
│   │   └── env.py
│   │
│   ├── scripts/
│   │   ├── migrate_data.py         # Legacy data migration
│   │   └── generate_test_data.py
│   │
│   ├── requirements.txt
│   ├── requirements-dev.txt
│   ├── pyproject.toml
│   ├── pytest.ini
│   └── Dockerfile
│
├── frontend/
│   ├── public/
│   ├── src/
│   │   ├── components/
│   │   │   ├── common/
│   │   │   ├── auth/
│   │   │   ├── patients/
│   │   │   ├── viewer/            # Niivue components
│   │   │   └── search/
│   │   │
│   │   ├── pages/
│   │   │   ├── HomePage.tsx
│   │   │   ├── PatientsPage.tsx
│   │   │   ├── PatientDetailPage.tsx
│   │   │   ├── SearchPage.tsx
│   │   │   └── ViewerPage.tsx
│   │   │
│   │   ├── hooks/
│   │   │   ├── useAuth.ts
│   │   │   ├── usePatients.ts
│   │   │   └── useViewer.ts
│   │   │
│   │   ├── services/
│   │   │   ├── api.ts             # API client
│   │   │   └── auth.ts
│   │   │
│   │   ├── store/
│   │   │   └── authStore.ts       # State management
│   │   │
│   │   ├── types/
│   │   │   └── index.ts           # TypeScript types
│   │   │
│   │   ├── utils/
│   │   ├── App.tsx
│   │   └── main.tsx
│   │
│   ├── package.json
│   ├── tsconfig.json
│   ├── vite.config.ts
│   └── Dockerfile
│
├── docker-compose.yml
├── docker-compose.prod.yml
├── .github/
│   └── workflows/
│       ├── backend-tests.yml
│       ├── frontend-tests.yml
│       └── deploy.yml
│
└── docs/
    ├── api/
    ├── user-guide/
    └── deployment/
```

## Backend Implementation Details

### Configuration Management

Use Pydantic Settings for type-safe configuration:

```python
# app/core/config.py
from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    # App
    APP_NAME: str = "BDPDB"
    API_V1_STR: str = "/api/v1"
    
    # Security
    SECRET_KEY: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 15
    REFRESH_TOKEN_EXPIRE_DAYS: int = 30
    ALGORITHM: str = "HS256"
    
    # Database
    DATABASE_URL: str
    DATABASE_POOL_SIZE: int = 5
    
    # Object Storage
    S3_ENDPOINT: str
    S3_ACCESS_KEY: str
    S3_SECRET_KEY: str
    S3_BUCKET: str
    S3_REGION: str = "us-east-1"
    
    # Redis
    REDIS_URL: str = "redis://localhost:6379"
    
    # CORS
    BACKEND_CORS_ORIGINS: list[str] = ["http://localhost:3000"]
    
    # Logging
    LOG_LEVEL: str = "INFO"
    
    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings()
```

### Database Models

```python
# app/models/patient.py
from sqlalchemy import Column, Integer, String, Date, ForeignKey, Table
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import JSONB
from app.db.base import Base
from datetime import datetime

class Patient(Base):
    __tablename__ = "patients"
    
    id = Column(Integer, primary_key=True, index=True)
    patient_label = Column(String(25), unique=True, nullable=False, index=True)
    dob = Column(Date, nullable=True)
    sex_id = Column(Integer, ForeignKey("sex.id"), nullable=False)
    handedness = Column(String(10))
    institution_id = Column(Integer, ForeignKey("institutions.id"))
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    created_by_id = Column(Integer, ForeignKey("users.id"))
    
    # Relationships
    sex = relationship("Sex", back_populates="patients")
    brain_damage = relationship("BrainDamage", back_populates="patient", uselist=False)
    scans = relationship("Scan", back_populates="patient")
    lesion_masks = relationship("LesionMask", back_populates="patient")
    notes = relationship("PatientNote", back_populates="patient")
    created_by = relationship("User")
```

### Pydantic Schemas

```python
# app/schemas/patient.py
from pydantic import BaseModel, Field, ConfigDict
from datetime import date, datetime
from typing import Optional

class PatientBase(BaseModel):
    patient_label: str = Field(..., min_length=1, max_length=25)
    dob: Optional[date] = None
    sex_id: int
    handedness: Optional[str] = None

class PatientCreate(PatientBase):
    pass

class PatientUpdate(BaseModel):
    dob: Optional[date] = None
    sex_id: Optional[int] = None
    handedness: Optional[str] = None

class PatientInDB(PatientBase):
    id: int
    created_at: datetime
    updated_at: datetime
    
    model_config = ConfigDict(from_attributes=True)

class Patient(PatientInDB):
    scans_count: int = 0
    masks_count: int = 0
```

### API Endpoints

```python
# app/api/v1/patients.py
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from app.api import dependencies as deps
from app.schemas.patient import Patient, PatientCreate, PatientUpdate
from app.services import patient as patient_service

router = APIRouter()

@router.get("/", response_model=List[Patient])
async def list_patients(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    sex_id: Optional[int] = None,
    laterality_id: Optional[int] = None,
    db: AsyncSession = Depends(deps.get_db),
    current_user = Depends(deps.get_current_active_user)
):
    """List patients with optional filtering."""
    filters = {}
    if sex_id:
        filters['sex_id'] = sex_id
    if laterality_id:
        filters['laterality_id'] = laterality_id
    
    patients = await patient_service.get_patients(
        db, skip=skip, limit=limit, filters=filters
    )
    return patients

@router.get("/{patient_id}", response_model=Patient)
async def get_patient(
    patient_id: int,
    db: AsyncSession = Depends(deps.get_db),
    current_user = Depends(deps.get_current_active_user)
):
    """Get a specific patient by ID."""
    patient = await patient_service.get_patient(db, patient_id)
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")
    return patient

@router.post("/", response_model=Patient, status_code=201)
async def create_patient(
    patient_in: PatientCreate,
    db: AsyncSession = Depends(deps.get_db),
    current_user = Depends(deps.require_admin)
):
    """Create a new patient."""
    patient = await patient_service.create_patient(db, patient_in, current_user.id)
    return patient
```

### Service Layer

```python
# app/services/patient.py
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import Optional, Dict
from app.models.patient import Patient
from app.schemas.patient import PatientCreate, PatientUpdate

async def get_patients(
    db: AsyncSession,
    skip: int = 0,
    limit: int = 100,
    filters: Optional[Dict] = None
):
    """Get list of patients with optional filtering."""
    query = select(Patient)
    
    if filters:
        for key, value in filters.items():
            query = query.where(getattr(Patient, key) == value)
    
    query = query.offset(skip).limit(limit)
    result = await db.execute(query)
    return result.scalars().all()

async def get_patient(db: AsyncSession, patient_id: int):
    """Get a single patient by ID."""
    result = await db.execute(
        select(Patient).where(Patient.id == patient_id)
    )
    return result.scalar_one_or_none()

async def create_patient(
    db: AsyncSession,
    patient_in: PatientCreate,
    created_by_id: int
):
    """Create a new patient."""
    patient = Patient(**patient_in.model_dump(), created_by_id=created_by_id)
    db.add(patient)
    await db.commit()
    await db.refresh(patient)
    return patient
```

### Image Processing Service

```python
# app/services/imaging.py
import nibabel as nib
import numpy as np
from nilearn import image
from typing import Tuple, List
import asyncio
from functools import partial

class ImagingService:
    """Service for neuroimaging operations."""
    
    @staticmethod
    async def load_nifti_async(file_path: str) -> nib.Nifti1Image:
        """Load NIfTI file asynchronously."""
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, nib.load, file_path)
    
    @staticmethod
    def mni_to_voxel(coords: Tuple[float, float, float], affine: np.ndarray) -> Tuple[int, int, int]:
        """Convert MNI coordinates to voxel indices."""
        from nibabel import affines
        voxel_coords = affines.apply_affine(np.linalg.inv(affine), coords)
        return tuple(int(c) for c in voxel_coords)
    
    @staticmethod
    async def compute_overlap_map(mask_paths: List[str], output_path: str):
        """Compute overlap heatmap from multiple masks."""
        loop = asyncio.get_event_loop()
        
        def _compute():
            # Load all masks
            masks = [nib.load(path) for path in mask_paths]
            # Stack masks
            mask_stack = image.concat_imgs(masks)
            # Sum across patients
            overlap = image.math_img("np.sum(img, axis=-1)", img=mask_stack)
            # Save result
            overlap.to_filename(output_path)
            return output_path
        
        return await loop.run_in_executor(None, _compute)
    
    @staticmethod
    async def search_coordinate(
        coord: Tuple[float, float, float],
        mask_paths: List[str],
        affine: np.ndarray,
        shape: Tuple[int, int, int]
    ) -> List[int]:
        """Search which masks contain damage at the given coordinate."""
        voxel_coord = ImagingService.mni_to_voxel(coord, affine)
        
        loop = asyncio.get_event_loop()
        
        def _search():
            results = []
            for idx, mask_path in enumerate(mask_paths):
                mask_img = nib.load(mask_path)
                mask_data = mask_img.get_fdata()
                if mask_data[voxel_coord] > 0:
                    results.append(idx)
            return results
        
        return await loop.run_in_executor(None, _search)

imaging_service = ImagingService()
```

### Object Storage Service

```python
# app/services/storage.py
import boto3
from botocore.client import Config
from typing import BinaryIO
from app.core.config import settings

class StorageService:
    """Service for object storage operations."""
    
    def __init__(self):
        self.s3_client = boto3.client(
            's3',
            endpoint_url=settings.S3_ENDPOINT,
            aws_access_key_id=settings.S3_ACCESS_KEY,
            aws_secret_access_key=settings.S3_SECRET_KEY,
            config=Config(signature_version='s3v4'),
            region_name=settings.S3_REGION
        )
        self.bucket = settings.S3_BUCKET
    
    def upload_file(self, file: BinaryIO, object_key: str) -> str:
        """Upload a file to object storage."""
        self.s3_client.upload_fileobj(file, self.bucket, object_key)
        return object_key
    
    def download_file(self, object_key: str, file_path: str):
        """Download a file from object storage."""
        self.s3_client.download_file(self.bucket, object_key, file_path)
    
    def get_presigned_url(self, object_key: str, expiration: int = 3600) -> str:
        """Generate a presigned URL for temporary access."""
        return self.s3_client.generate_presigned_url(
            'get_object',
            Params={'Bucket': self.bucket, 'Key': object_key},
            ExpiresIn=expiration
        )
    
    def delete_file(self, object_key: str):
        """Delete a file from object storage."""
        self.s3_client.delete_object(Bucket=self.bucket, Key=object_key)

storage_service = StorageService()
```

## Frontend Implementation Details

### API Client

```typescript
// src/services/api.ts
import axios, { AxiosInstance } from 'axios';

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000';

class ApiClient {
  private client: AxiosInstance;

  constructor() {
    this.client = axios.create({
      baseURL: `${API_BASE_URL}/api/v1`,
      headers: {
        'Content-Type': 'application/json',
      },
    });

    // Request interceptor for adding auth token
    this.client.interceptors.request.use(
      (config) => {
        const token = localStorage.getItem('access_token');
        if (token) {
          config.headers.Authorization = `Bearer ${token}`;
        }
        return config;
      },
      (error) => Promise.reject(error)
    );

    // Response interceptor for handling token refresh
    this.client.interceptors.response.use(
      (response) => response,
      async (error) => {
        const originalRequest = error.config;

        if (error.response?.status === 401 && !originalRequest._retry) {
          originalRequest._retry = true;
          
          try {
            const refreshToken = localStorage.getItem('refresh_token');
            const response = await axios.post(
              `${API_BASE_URL}/api/v1/auth/refresh`,
              { refresh_token: refreshToken }
            );
            
            const { access_token } = response.data;
            localStorage.setItem('access_token', access_token);
            
            originalRequest.headers.Authorization = `Bearer ${access_token}`;
            return this.client(originalRequest);
          } catch (refreshError) {
            // Redirect to login
            window.location.href = '/login';
            return Promise.reject(refreshError);
          }
        }

        return Promise.reject(error);
      }
    );
  }

  // Patient endpoints
  async getPatients(params?: Record<string, any>) {
    const response = await this.client.get('/patients', { params });
    return response.data;
  }

  async getPatient(id: number) {
    const response = await this.client.get(`/patients/${id}`);
    return response.data;
  }

  async createPatient(data: any) {
    const response = await this.client.post('/patients', data);
    return response.data;
  }

  // Search endpoints
  async searchByCoordinate(x: number, y: number, z: number) {
    const response = await this.client.post('/search/coordinates', { x, y, z });
    return response.data;
  }
}

export const apiClient = new ApiClient();
```

### React Query Hooks

```typescript
// src/hooks/usePatients.ts
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { apiClient } from '../services/api';
import type { Patient, PatientCreate } from '../types';

export function usePatients(filters?: Record<string, any>) {
  return useQuery({
    queryKey: ['patients', filters],
    queryFn: () => apiClient.getPatients(filters),
  });
}

export function usePatient(id: number) {
  return useQuery({
    queryKey: ['patients', id],
    queryFn: () => apiClient.getPatient(id),
    enabled: !!id,
  });
}

export function useCreatePatient() {
  const queryClient = useQueryClient();
  
  return useMutation({
    mutationFn: (data: PatientCreate) => apiClient.createPatient(data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['patients'] });
    },
  });
}
```

### Niivue Viewer Component

```typescript
// src/components/viewer/NiivueViewer.tsx
import React, { useEffect, useRef } from 'react';
import { Niivue, NVImage } from '@niivue/niivue';

interface NiivueViewerProps {
  imageUrls: string[];
  onCoordinateChange?: (x: number, y: number, z: number) => void;
}

export const NiivueViewer: React.FC<NiivueViewerProps> = ({
  imageUrls,
  onCoordinateChange,
}) => {
  const canvasRef = useRef<HTMLCanvasElement>(null);
  const nvRef = useRef<Niivue | null>(null);

  useEffect(() => {
    if (!canvasRef.current) return;

    // Initialize Niivue
    const nv = new Niivue({
      show3Dcrosshair: true,
      backColor: [0, 0, 0, 1],
      crosshairColor: [1, 0, 0, 1],
    });

    nv.attachToCanvas(canvasRef.current);
    nvRef.current = nv;

    // Load images
    const volumes = imageUrls.map((url, idx) => {
      const vol = NVImage.loadFromUrl({ url });
      if (idx > 0) {
        vol.opacity = 0.5;
        vol.colormap = 'red';
      }
      return vol;
    });

    nv.loadVolumes(volumes);

    // Set up crosshair listener
    if (onCoordinateChange) {
      nv.onLocationChange = (location) => {
        const { mm } = location;
        onCoordinateChange(mm[0], mm[1], mm[2]);
      };
    }

    return () => {
      nv.destroy();
    };
  }, [imageUrls]);

  return (
    <div style={{ width: '100%', height: '600px' }}>
      <canvas ref={canvasRef} style={{ width: '100%', height: '100%' }} />
    </div>
  );
};
```

### Patient Detail Page

```typescript
// src/pages/PatientDetailPage.tsx
import React from 'react';
import { useParams } from 'react-router-dom';
import { Box, Typography, Grid, Card, CardContent } from '@mui/material';
import { usePatient } from '../hooks/usePatients';
import { NiivueViewer } from '../components/viewer/NiivueViewer';

export const PatientDetailPage: React.FC = () => {
  const { id } = useParams<{ id: string }>();
  const { data: patient, isLoading, error } = usePatient(Number(id));

  if (isLoading) return <div>Loading...</div>;
  if (error) return <div>Error loading patient</div>;
  if (!patient) return <div>Patient not found</div>;

  return (
    <Box sx={{ p: 3 }}>
      <Typography variant="h4" gutterBottom>
        Patient: {patient.patient_label}
      </Typography>

      <Grid container spacing={3}>
        <Grid item xs={12} md={6}>
          <Card>
            <CardContent>
              <Typography variant="h6">Demographics</Typography>
              <Typography>Sex: {patient.sex}</Typography>
              <Typography>DOB: {patient.dob || 'Not specified'}</Typography>
              <Typography>Handedness: {patient.handedness}</Typography>
            </CardContent>
          </Card>
        </Grid>

        <Grid item xs={12} md={6}>
          <Card>
            <CardContent>
              <Typography variant="h6">Brain Damage</Typography>
              <Typography>Areas: {patient.damaged_areas?.join(', ')}</Typography>
              <Typography>Laterality: {patient.laterality}</Typography>
              <Typography>Etiology: {patient.etiology}</Typography>
            </CardContent>
          </Card>
        </Grid>

        <Grid item xs={12}>
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                Lesion Mask Viewer
              </Typography>
              <NiivueViewer
                imageUrls={[
                  '/api/v1/viewer/template',
                  `/api/v1/patients/${id}/mask`,
                ]}
              />
            </CardContent>
          </Card>
        </Grid>
      </Grid>
    </Box>
  );
};
```

## Testing Examples

### Backend Unit Test

```python
# tests/test_services/test_patient.py
import pytest
from app.services import patient as patient_service
from app.schemas.patient import PatientCreate

@pytest.mark.asyncio
async def test_create_patient(db_session, test_user):
    """Test creating a new patient."""
    patient_data = PatientCreate(
        patient_label="TEST001",
        sex_id=1,
        handedness="Right"
    )
    
    patient = await patient_service.create_patient(
        db_session, patient_data, test_user.id
    )
    
    assert patient.patient_label == "TEST001"
    assert patient.sex_id == 1
    assert patient.created_by_id == test_user.id

@pytest.mark.asyncio
async def test_get_patients_with_filter(db_session, test_patients):
    """Test filtering patients by sex."""
    patients = await patient_service.get_patients(
        db_session, filters={'sex_id': 1}
    )
    
    assert all(p.sex_id == 1 for p in patients)
```

### Frontend Component Test

```typescript
// src/components/patients/__tests__/PatientList.test.tsx
import { render, screen, waitFor } from '@testing-library/react';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { PatientList } from '../PatientList';
import { apiClient } from '../../../services/api';

jest.mock('../../../services/api');

describe('PatientList', () => {
  it('renders patient list', async () => {
    const mockPatients = [
      { id: 1, patient_label: 'PT001', sex: 'Male' },
      { id: 2, patient_label: 'PT002', sex: 'Female' },
    ];

    (apiClient.getPatients as jest.Mock).mockResolvedValue(mockPatients);

    const queryClient = new QueryClient();
    
    render(
      <QueryClientProvider client={queryClient}>
        <PatientList />
      </QueryClientProvider>
    );

    await waitFor(() => {
      expect(screen.getByText('PT001')).toBeInTheDocument();
      expect(screen.getByText('PT002')).toBeInTheDocument();
    });
  });
});
```

## Deployment

### Docker Compose for Development

```yaml
# docker-compose.yml
version: '3.8'

services:
  postgres:
    image: postgres:15
    environment:
      POSTGRES_DB: bdpdb
      POSTGRES_USER: bdpdb
      POSTGRES_PASSWORD: bdpdb_dev
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data

  minio:
    image: minio/minio
    command: server /data --console-address ":9001"
    environment:
      MINIO_ROOT_USER: minioadmin
      MINIO_ROOT_PASSWORD: minioadmin
    ports:
      - "9000:9000"
      - "9001:9001"
    volumes:
      - minio_data:/data

  redis:
    image: redis:7
    ports:
      - "6379:6379"

  backend:
    build: ./backend
    command: uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
    volumes:
      - ./backend:/app
    ports:
      - "8000:8000"
    environment:
      DATABASE_URL: postgresql+asyncpg://bdpdb:bdpdb_dev@postgres:5432/bdpdb
      S3_ENDPOINT: http://minio:9000
      REDIS_URL: redis://redis:6379
    depends_on:
      - postgres
      - minio
      - redis

  frontend:
    build: ./frontend
    command: npm run dev
    volumes:
      - ./frontend:/app
      - /app/node_modules
    ports:
      - "3000:3000"
    environment:
      VITE_API_BASE_URL: http://localhost:8000
    depends_on:
      - backend

volumes:
  postgres_data:
  minio_data:
```

### Kubernetes Deployment (Production)

```yaml
# k8s/deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: bdpdb-backend
spec:
  replicas: 3
  selector:
    matchLabels:
      app: bdpdb-backend
  template:
    metadata:
      labels:
        app: bdpdb-backend
    spec:
      containers:
      - name: backend
        image: bdpdb/backend:latest
        ports:
        - containerPort: 8000
        env:
        - name: DATABASE_URL
          valueFrom:
            secretKeyRef:
              name: bdpdb-secrets
              key: database-url
        - name: SECRET_KEY
          valueFrom:
            secretKeyRef:
              name: bdpdb-secrets
              key: secret-key
        resources:
          requests:
            memory: "256Mi"
            cpu: "250m"
          limits:
            memory: "512Mi"
            cpu: "500m"
        livenessProbe:
          httpGet:
            path: /health
            port: 8000
          initialDelaySeconds: 30
          periodSeconds: 10
        readinessProbe:
          httpGet:
            path: /health
            port: 8000
          initialDelaySeconds: 5
          periodSeconds: 5
```

## Performance Optimization Tips

1. **Database Indexing**
   - Add indexes on frequently queried columns (patient_label, sex_id, etc.)
   - Use composite indexes for common filter combinations
   - Use partial indexes for specific query patterns

2. **Caching Strategy**
   - Cache patient lists with Redis
   - Cache computed overlap maps
   - Use ETags for image resources
   - Implement browser caching headers

3. **Image Serving**
   - Use CDN for static template images
   - Implement range requests for large NIfTI files
   - Consider converting to chunked formats (Zarr, N5)
   - Pre-generate common views/slices

4. **Frontend Optimization**
   - Code splitting for route-based loading
   - Lazy load heavy components (viewer)
   - Memoize expensive computations
   - Use virtual scrolling for long lists

## Security Checklist

- [ ] Implement rate limiting on all endpoints
- [ ] Enable CORS with explicit origin whitelist
- [ ] Use parameterized queries (SQLAlchemy ORM handles this)
- [ ] Sanitize file uploads
- [ ] Implement CSP headers
- [ ] Enable HTTPS only in production
- [ ] Use secure cookie flags
- [ ] Implement audit logging
- [ ] Regular dependency updates
- [ ] Penetration testing before production

## Monitoring Setup

### Prometheus Metrics

```python
# app/core/metrics.py
from prometheus_client import Counter, Histogram, generate_latest
from fastapi import Response

http_requests_total = Counter(
    'http_requests_total',
    'Total HTTP requests',
    ['method', 'endpoint', 'status']
)

http_request_duration_seconds = Histogram(
    'http_request_duration_seconds',
    'HTTP request duration',
    ['method', 'endpoint']
)

@app.get('/metrics')
async def metrics():
    return Response(
        content=generate_latest(),
        media_type='text/plain'
    )
```

## Next Steps

1. Review and approve this implementation guide
2. Set up development environment
3. Create initial project scaffolding
4. Implement core models and migrations
5. Build MVP backend API
6. Develop frontend prototype
7. Iterate based on feedback

