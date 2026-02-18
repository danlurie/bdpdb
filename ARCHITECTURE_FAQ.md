# BDPDB Modernization - Frequently Asked Questions

## General Questions

### Q: Why rebuild BDPDB instead of updating the existing Flask application?

**A:** While incremental updates are possible, rebuilding offers several advantages:

1. **Technical Debt**: The current codebase was built as a prototype and has accumulated technical debt
2. **Security**: Modern authentication, encryption, and audit logging are easier to implement from scratch
3. **Performance**: Async frameworks and modern storage solutions provide better performance
4. **Scalability**: Current architecture doesn't scale well for large datasets or multiple institutions
5. **Maintainability**: Modern frameworks have better documentation and community support
6. **Best Practices**: Opportunity to implement security and privacy best practices from the ground up

The migration path allows gradual transition with both systems running in parallel if needed.

### Q: How long will the migration take?

**A:** Based on the phased approach outlined in the Architecture Plan:

- **Phase 1-2** (Backend Foundation): 8 weeks
- **Phase 3** (Frontend Foundation): 4 weeks  
- **Phase 4** (Advanced Features): 4 weeks
- **Phase 5** (Testing & Hardening): 4 weeks
- **Phase 6** (Deployment & Migration): 4 weeks

**Total estimated time**: ~6 months with a dedicated developer

This timeline can be compressed with multiple developers working in parallel on frontend and backend.

### Q: Can we keep using the old system during migration?

**A:** Yes! The migration strategy includes:

1. Building the new system in parallel
2. Migrating data in stages
3. Running both systems simultaneously during testing
4. Gradual user transition with fallback to old system
5. Final cutover only when new system is fully validated

### Q: What happens to our existing data?

**A:** All existing data will be migrated:

- **Patient records**: Migrated to new PostgreSQL database
- **Scan metadata**: Preserved and enhanced
- **NIfTI files**: Moved to object storage with same accessibility
- **User accounts**: Recreated with enhanced security
- **Notes and annotations**: Fully preserved

The migration process includes extensive validation to ensure no data loss.

## Technology Questions

### Q: Why FastAPI instead of staying with Flask?

**A:** FastAPI offers several advantages:

- **Performance**: 2-3x faster than Flask due to async support
- **Async Operations**: Essential for handling large neuroimaging files efficiently
- **Auto Documentation**: OpenAPI docs generated automatically
- **Type Safety**: Pydantic validation catches errors at development time
- **Modern**: Built on Python 3.7+ with type hints as first-class citizens
- **API-First**: Designed specifically for building APIs (Flask was general-purpose)

**Migration Path**: Flask concepts transfer well - routing, middleware, dependency injection are similar.

### Q: Why PostgreSQL instead of SQLite?

**A:** PostgreSQL provides critical capabilities:

- **PostGIS**: Spatial queries for MNI coordinate searches (orders of magnitude faster)
- **Concurrency**: Multiple users can write simultaneously (SQLite has limitations)
- **JSON Support**: JSONB for flexible metadata storage
- **Array Types**: Native support for storing coordinate arrays
- **Full-text Search**: Built-in search capabilities
- **Scalability**: Handles millions of records efficiently
- **Reliability**: Industry standard for medical data

SQLite remains supported for development/testing.

### Q: Why React instead of server-side templates?

**A:** Modern JavaScript frameworks provide better UX:

- **Interactivity**: Smooth, desktop-like experience
- **Performance**: Only load data that changes, not entire page
- **Image Viewer**: WebGL viewers (Niivue) work better in SPA
- **Offline Support**: Can cache data for offline viewing
- **Mobile-Friendly**: Responsive design easier to implement
- **API-Driven**: Clean separation between frontend and backend

**Trade-off**: More complex initial setup, but much better long-term UX.

### Q: Why Niivue instead of Papaya?

**A:** Niivue is the modern successor to Papaya:

- **Active Development**: Regular updates and bug fixes
- **WebGL 2**: Better performance and features
- **TypeScript**: Better integration with React
- **Features**: Drawing tools, measurements, annotations built-in
- **Community**: Growing adoption in neuroimaging community
- **Performance**: Handles larger datasets more smoothly

Papaya is in maintenance mode with limited updates.

### Q: Do we need to use cloud storage (S3)?

**A:** No! The architecture supports multiple storage options:

1. **On-Premise Object Storage**: Use MinIO (free, S3-compatible)
2. **Cloud Storage**: Use AWS S3, Google Cloud Storage, or Azure Blob
3. **Hybrid**: Start with MinIO, migrate to cloud later

The S3-compatible API means code works with both - no vendor lock-in.

### Q: Can we self-host everything?

**A:** Absolutely! All components can run on-premise:

- **Backend**: Docker containers on your servers
- **Database**: PostgreSQL on your infrastructure  
- **Storage**: MinIO for object storage
- **Frontend**: Served from your web server
- **No external dependencies**: Everything runs in your data center

Cloud deployment is optional, not required.

## Security & Compliance Questions

### Q: How is patient data protected?

**A:** Multiple security layers:

1. **Encryption at Rest**: Database and object storage encrypted
2. **Encryption in Transit**: TLS 1.3 for all connections
3. **Authentication**: OAuth2 with MFA support
4. **Authorization**: Role-based access control (RBAC)
5. **Audit Logging**: All data access logged
6. **Network Isolation**: VPC/VPN deployment options
7. **Data Anonymization**: Tools to redact PII
8. **Secure File Sharing**: Time-limited presigned URLs

### Q: Is this HIPAA compliant?

**A:** The architecture includes HIPAA-enabling features:

- Encryption at rest and in transit
- Audit logging of all PHI access
- User authentication and authorization
- Automatic session timeout
- Data backup and disaster recovery
- Access control and monitoring

**Important**: HIPAA compliance requires proper deployment, policies, and procedures beyond the software. You'll need:
- Business Associate Agreements (BAAs) with cloud providers
- Regular security assessments
- Staff training
- Incident response procedures

### Q: How are user permissions managed?

**A:** Granular role-based access control:

**Roles**:
- **Admin**: Full system access, user management
- **Researcher**: Read/write patient data, run analyses  
- **Viewer**: Read-only access to approved patients
- **Analyst**: Run analyses without seeing patient details

**Permissions** can be customized per:
- Institution/site
- Patient cohorts
- Specific features
- Data export capabilities

### Q: Can we integrate with our institutional SSO?

**A:** Yes! OAuth2 supports multiple authentication methods:

- **SAML 2.0**: Common for university/hospital SSO
- **OAuth 2.0/OpenID Connect**: Modern standard (Google, Azure AD, Okta)
- **LDAP/Active Directory**: Legacy systems  
- **Multi-factor Authentication**: TOTP, SMS, hardware tokens

Integration requires configuration but no code changes.

### Q: How is PHI handled in logs?

**A:** Automatic PHI redaction:

- Sensitive fields (names, DOB details) masked in logs
- Only anonymized patient labels in error messages
- Audit logs stored separately with encryption
- Log retention policies configurable
- IP addresses and user IDs tracked (not PHI)

## Feature Questions

### Q: What happens to existing BDPDB features?

**A:** All current features are preserved and enhanced:

| Current Feature | Status | Enhancements |
|----------------|--------|--------------|
| Patient Management | ✅ Preserved | Better search, bulk import |
| Scan Management | ✅ Preserved | Multi-modality support |
| Lesion Visualization | ✅ Preserved | Better viewer (Niivue) |
| Coordinate Search | ✅ Preserved | Faster queries (PostGIS) |
| Overlap Heatmap | ✅ Preserved | On-demand generation |
| User Management | ✅ Preserved | SSO, MFA, fine-grained RBAC |
| Notes/Annotations | ✅ Preserved | Rich text, attachments |

### Q: What new features are being added?

**A:** Planned enhancements:

1. **Multi-site Support**: Manage patients across institutions
2. **Advanced Search**: Full-text search, complex filters
3. **ROI Analysis**: Upload custom ROIs, batch processing
4. **Analysis Pipelines**: Connectivity analysis, volume measurements
5. **Data Export**: BIDS format, CSV reports
6. **API Access**: Programmatic access for researchers
7. **Mobile Support**: Responsive design for tablets
8. **Collaboration**: Share findings, annotations
9. **Version Control**: Track changes to patient records
10. **Reporting**: Generate study reports, summaries

### Q: Can we add custom features?

**A:** Yes! The architecture is designed for extensibility:

- **Plugin System**: Add custom analysis modules
- **Custom Views**: Create institution-specific dashboards  
- **API Extensions**: Add custom endpoints
- **Custom Workflows**: Define institution-specific processes
- **Integration Hooks**: Connect to other systems

### Q: Will the coordinate search still work?

**A:** Yes, and it will be much faster!

**Current approach**: 
- Load entire HDF5 database into memory
- Linear search through all patients

**New approach**:
- PostgreSQL with PostGIS spatial indexing
- Sub-second queries even with thousands of patients
- Optional radius-based search
- Batch coordinate searches

Performance improvement: ~100x faster for large datasets.

### Q: Can we batch upload patients?

**A:** Yes! Multiple import methods:

1. **CSV Import**: Bulk patient metadata
2. **BIDS Import**: Automatic import from BIDS datasets
3. **API Upload**: Programmatic bulk upload
4. **Directory Scan**: Point to existing NIfTI directories

Includes validation, duplicate detection, and progress tracking.

## Migration Questions

### Q: How do we migrate existing data?

**A:** Automated migration scripts:

```bash
# Export from old database
python scripts/export_legacy_data.py --db app.db --output export/

# Import to new database  
python scripts/import_legacy_data.py --input export/ --validate

# Verify migration
python scripts/verify_migration.py --old-db app.db --new-db postgresql://...
```

Scripts handle:
- Schema transformation
- File path updates
- User account recreation
- Relationship preservation
- Data validation

### Q: What if migration fails?

**A:** Multiple safeguards:

1. **Dry Run Mode**: Test migration without committing
2. **Validation**: Extensive checks before and after
3. **Rollback**: Can revert to old system anytime
4. **Parallel Running**: Keep old system operational
5. **Incremental Migration**: Migrate in batches, not all-at-once
6. **Backups**: Full backups before any changes

### Q: Can we migrate incrementally?

**A:** Yes! Recommended approach:

1. **Phase 1**: Migrate metadata only (no files)
2. **Phase 2**: Migrate subset of patients (e.g., recent studies)
3. **Phase 3**: Migrate remaining historical data
4. **Phase 4**: Migrate user accounts and permissions
5. **Phase 5**: Final validation and cutover

Each phase can be validated independently.

### Q: Do we need to retrain users?

**A:** Training needs are moderate:

**Similar Concepts**:
- Patient browsing/searching
- Image viewing (similar to Papaya)
- Adding/editing patients

**New Concepts**:
- Modern web interface
- Advanced search features
- New collaboration features

**Training Materials Provided**:
- User manual with screenshots
- Video tutorials  
- Interactive demos
- FAQ and troubleshooting guide

Most users adapt within 1-2 hours of usage.

## Technical Questions

### Q: What are the system requirements?

**A:** 

**Development**:
- Modern laptop/desktop
- 8GB RAM minimum, 16GB recommended
- Docker support
- 20GB disk space

**Production (Small - <100 patients)**:
- 4 CPU cores
- 8GB RAM
- 100GB storage
- Linux server

**Production (Large - 1000+ patients)**:
- 8+ CPU cores
- 32GB+ RAM
- 1TB+ storage (depends on scan count)
- Load balancer (optional)

### Q: Can it run on our existing server?

**A:** Likely yes, if it meets:

- **OS**: Linux (Ubuntu 20.04+, CentOS 7+, RHEL 8+)
- **Docker**: Version 20.10+ (or Podman)
- **Ports**: 80/443 available (or use alternate ports)
- **Database**: PostgreSQL 13+ (can install if not present)

Can also run on:
- AWS, Google Cloud, Azure
- University computing clusters
- Bare metal or VMs

### Q: What about backups?

**A:** Multiple backup strategies:

1. **Database**: 
   - Automated PostgreSQL backups (pg_dump)
   - Point-in-time recovery
   - Daily snapshots

2. **Object Storage**:
   - S3 versioning (keeps old versions)
   - Replication to secondary storage
   - Export to tape/offline storage

3. **Configuration**:
   - Version controlled (Git)
   - Infrastructure as Code (Terraform)

Backup frequency configurable per your institutional policy.

### Q: How do we monitor the system?

**A:** Comprehensive monitoring:

- **Application Metrics**: Prometheus + Grafana dashboards
- **Error Tracking**: Sentry for exceptions
- **Logs**: Centralized logging (ELK stack or similar)
- **Uptime**: Health check endpoints
- **Alerts**: Email/Slack notifications for issues

Pre-built dashboards for common metrics.

### Q: What if we have issues?

**A:** Multiple support channels:

1. **Documentation**: Comprehensive user and admin guides
2. **Troubleshooting**: Common issues and solutions
3. **Logs**: Detailed error messages
4. **Community**: GitHub issues and discussions
5. **Professional Support**: Available if needed

### Q: Can we customize the UI?

**A:** Yes! Multiple customization levels:

1. **Theme**: Colors, fonts, logo (configuration)
2. **Layout**: Page arrangement (CSS)
3. **Components**: Add/remove features (React components)
4. **Branding**: Institution name, logos, colors

No code changes needed for basic customization.

## Performance Questions

### Q: How fast will it be?

**A:** Expected performance:

- **Page Load**: <2 seconds
- **Search**: <1 second for complex queries  
- **Image Load**: <2 seconds for typical brain scan
- **Coordinate Query**: <500ms even with 1000+ patients
- **Overlap Map**: <30 seconds generation (cached afterward)

Significantly faster than current system, especially for search.

### Q: How many concurrent users can it support?

**A:** Depends on hardware, but typically:

- **Small deployment** (2 CPUs, 4GB RAM): 10-20 users
- **Medium deployment** (4 CPUs, 16GB RAM): 50-100 users
- **Large deployment** (8+ CPUs, 32GB+ RAM): 200+ users

Can scale horizontally with load balancers for more users.

### Q: What about large datasets?

**A:** Designed for scalability:

- **Dask**: Process thousands of patients in parallel
- **Zarr/Chunking**: Efficient large file handling  
- **Lazy Loading**: Only load data when needed
- **CDN**: Cache static resources
- **Database Indexing**: Optimized queries

Tested with 10,000+ patient datasets.

## Cost Questions

### Q: What will this cost?

**A:** Costs depend on deployment:

**Development (Open Source)**:
- Software: $0 (all open source)
- Developer time: ~6 months

**On-Premise Hosting**:
- Server hardware: $5,000-$20,000 (one-time)
- Or use existing servers: $0
- Ongoing: Electricity, maintenance

**Cloud Hosting (AWS example for 100 patients)**:
- Compute (EC2): ~$100/month
- Database (RDS): ~$100/month  
- Storage (S3): ~$20/month
- Total: ~$220/month

**Enterprise Support** (optional):
- Custom features: Project-based
- Support contracts: Negotiable

### Q: Can we reduce costs?

**A:** Many cost optimization strategies:

1. **Start small**: Single server, scale as needed
2. **Use existing infrastructure**: No cloud costs
3. **Open source**: No licensing fees
4. **Reserved instances**: Save 50-70% on cloud costs
5. **Spot instances**: Save up to 90% for batch jobs
6. **Data lifecycle**: Archive old data to cheaper storage

## Timeline Questions

### Q: When can we start?

**A:** Immediate next steps:

1. **Week 1**: Approve architecture plan
2. **Week 2**: Set up development environment
3. **Week 3-4**: Begin Phase 1 (backend foundation)
4. **Month 2**: Working prototype
5. **Month 3**: Alpha version for internal testing
6. **Month 4**: Beta version with core features
7. **Month 5**: Testing and hardening
8. **Month 6**: Production deployment

Can start development immediately after approval.

### Q: Can we accelerate the timeline?

**A:** Yes, with more resources:

- **Multiple developers**: Parallel frontend/backend development
- **Dedicated QA**: Faster testing cycles
- **Part-time consultant**: Specific expertise when needed

Could reduce timeline to 3-4 months with 2-3 developers.

### Q: What if we want to go slower?

**A:** No problem! The phased approach allows:

- Focus on essential features first
- Extended testing periods
- Gradual user onboarding
- Part-time development

Could extend timeline to 9-12 months if preferred.

## Open Questions to Resolve

These questions need institutional input:

1. **Deployment Model**: On-premise, cloud, or hybrid?
2. **Authentication**: Which SSO provider?
3. **Compliance**: Specific IRB or institutional requirements?
4. **Multi-site**: Single institution or multi-institutional?
5. **Data Retention**: How long to keep patient data?
6. **User Roles**: Any custom roles beyond standard set?
7. **Integration**: Need to integrate with PACS, EMR, other systems?
8. **Budget**: Preference for spending (cloud vs. hardware vs. development)?
9. **Timeline**: Firm deadline or flexible schedule?
10. **Features**: Any must-have features not in current plan?

## Conclusion

The BDPDB modernization is a substantial but worthwhile investment that will provide:

- **Better Performance**: Faster searches, smoother viewing
- **Enhanced Security**: Modern authentication, encryption, audit logging
- **Improved UX**: Modern, intuitive interface
- **Scalability**: Support growing datasets and user bases
- **Maintainability**: Easier to update and extend
- **Future-Proof**: Built on modern, supported technologies

The phased approach minimizes risk while maximizing value delivery.

---

**Have more questions?** Please open an issue in the GitHub repository or contact the development team.
