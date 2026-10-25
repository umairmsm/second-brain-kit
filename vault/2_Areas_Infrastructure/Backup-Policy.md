---
title: "Infrastructure: 3-2-1 Backup & Disaster Recovery Policy"
area: infrastructure
status: active
tags:
  - backup
  - disaster-recovery
  - storage
---

# 3-2-1 Backup & Disaster Recovery Policy

## 1. Principles
* **3 Copies**: 1 live primary copy on server NVMe, 1 local backup on NAS/ZFS array, 1 offsite encrypted snapshot.
* **2 Media Types**: High-speed NVMe storage and hard drive array.
* **1 Offsite Target**: Encrypted object storage (S3-compatible, Cloudflare R2, or remote server).

## 2. Retention Schedule
* Hourly snapshots retained for 24 hours.
* Daily snapshots retained for 30 days.
* Weekly snapshots retained for 8 weeks.
* Monthly snapshots retained for 12 months.
