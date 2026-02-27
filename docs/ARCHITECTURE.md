# ARCHITECTURE — ADVENTUREHEROAUTO

## Purpose
Auto dealer / automotive commerce platform under Resonance Energy. Handles inventory, leads, and customer experience.

## System Overview
```
[Inventory Feed] --> [Listing Engine] --> [Web Storefront]
[Lead Capture]   --> [CRM]           --> [Follow-up Automation]
```

## Components
- **Inventory Feed**: VIN decoder, DMS integration, photo pipeline
- **Listing Engine**: Auto-generates descriptions, pricing, SEO content
- **Web Storefront**: Vehicle search, filtering, detail pages
- **CRM**: Lead management, customer timeline, follow-up sequences
- **Follow-up Automation**: Email/SMS drips, AI-assisted responses

## Data Flow
DMS/Feed → Inventory Processor → Storefront → Lead → CRM → Automation

## Integration Points
- CAPITALCITYIMPORTS (sister dealership)
- NCL analytics dashboard
- Matrix Monitor (live sales metrics)

## Key Decisions
- AI-generated listings reduce manual work
- Lead scoring prioritizes hot buyers
