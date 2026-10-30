# AssemblyVision

Component Inspection & Quality Analytics

**Status: Prototype — in progress**

## Implemented

- Streamlit image-upload interface
- Image size and format validation
- OpenCV brightness and sharpness measurements
- Edge-map visualisation and download
- Explicitly labelled synthetic test pattern

These measurements are not defect predictions or inspection decisions.

## Planned

- Anomalib-based PatchCore fitting
- One industrial benchmark component category
- Validation-selected decision threshold
- Held-out evaluation and failure analysis
- Versioned inference artifacts

## Foundation

Anomalib: https://github.com/open-edge-platform/anomalib

Reference revision: 0cc8e6331a2a667fdb286b981d335393dc846383

Anomalib is a third-party Apache-2.0 library. Its authors retain credit
for their work. This starter does not yet import or run Anomalib.

## Local execution

    .\.venv\Scripts\python.exe -m streamlit run app.py

## Streamlit deployment

Entrypoint: app.py

## Limitations

Independent portfolio prototype. No Renault/Nissan affiliation,
production data, factory deployment, or measured defect-detection
performance is claimed.
