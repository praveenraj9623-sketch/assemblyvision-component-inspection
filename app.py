import io
import warnings

import cv2
import numpy as np
import streamlit as st
from PIL import Image, ImageOps

st.set_page_config(
    page_title="AssemblyVision",
    page_icon="🔍",
    layout="wide",
)

st.title("AssemblyVision")
st.caption("Component Inspection & Quality Analytics | Prototype — in progress")

st.info(
    "Implemented: image validation, brightness and sharpness measurements, "
    "and OpenCV edge visualisation. "
    "Planned: fitted PatchCore anomaly scoring and localisation using Anomalib."
)

st.write(
    "An independent industrial-inspection prototype. "
    "No Renault or Nissan production images or systems are connected."
)

source = st.radio(
    "Choose an input",
    ["Synthetic test pattern", "Upload an image"],
    horizontal=True,
)

rgb = None

if source == "Synthetic test pattern":
    canvas = np.full((480, 640, 3), 220, dtype=np.uint8)
    cv2.rectangle(canvas, (100, 100), (300, 350), (70, 70, 70), -1)
    cv2.circle(canvas, (450, 240), 95, (100, 100, 100), -1)
    cv2.circle(canvas, (450, 240), 40, (220, 220, 220), -1)
    rgb = canvas
    st.caption(
        "Generated image-processing test pattern. "
        "It is not a real component image or defect benchmark."
    )
else:
    uploaded = st.file_uploader(
        "Upload a component image",
        type=["png", "jpg", "jpeg"],
    )

    if uploaded is not None:
        if uploaded.size > 10 * 1024 * 1024:
            st.error("Please use an image smaller than 10 MB.")
            st.stop()

        try:
            with warnings.catch_warnings():
                warnings.simplefilter("error", Image.DecompressionBombWarning)
                with Image.open(io.BytesIO(uploaded.getvalue())) as image:
                    if image.width * image.height > 20_000_000:
                        raise ValueError("Image dimensions exceed the limit.")
                    image.load()
                    image = ImageOps.exif_transpose(image).convert("RGB")
                    image.thumbnail((1600, 1600))
                    rgb = np.asarray(image).copy()
        except Exception:
            st.error(
                "Could not process the image. "
                "Use a valid PNG or JPEG of at most 20 megapixels."
            )
            st.stop()

if rgb is not None:
    gray = cv2.cvtColor(rgb, cv2.COLOR_RGB2GRAY)

    brightness = float(np.mean(gray))
    sharpness = float(cv2.Laplacian(gray, cv2.CV_64F).var())
    edges = cv2.Canny(gray, 100, 200)

    first, second, third = st.columns(3)
    first.metric("Processed dimensions", f"{rgb.shape[1]} × {rgb.shape[0]}")
    second.metric("Mean brightness", f"{brightness:.1f} / 255")
    third.metric("Laplacian variance", f"{sharpness:.1f}")

    left, right = st.columns(2)
    with left:
        st.image(rgb, caption="Input image", use_container_width=True)
    with right:
        st.image(
            edges,
            caption="OpenCV edge map — not a defect prediction",
            use_container_width=True,
            clamp=True,
        )

    st.caption(
        "Brightness and Laplacian variance describe this processed image. "
        "They are not calibrated inspection thresholds or defect probabilities. "
        "Sharpness values depend on image content and resolution."
    )

    success, encoded = cv2.imencode(".png", edges)
    if success:
        st.download_button(
            "Download edge map",
            data=encoded.tobytes(),
            file_name="assemblyvision_edges.png",
            mime="image/png",
        )

with st.expander("Development roadmap and limitations"):
    st.markdown(
        """
        **Next model-development phase**
        - Select one licensed industrial benchmark category.
        - Establish training, calibration, and final evaluation partitions.
        - Fit a PatchCore model using Anomalib on normal training images.
        - Evaluate anomaly scores and localisation on held-out images.
        - Publish measured results and failure examples.

        **Current limitations**
        - No anomaly model is fitted or loaded.
        - No defect classification, pass/fail decision, or factory monitoring.
        - No automotive manufacturer affiliation.
        """
    )

st.divider()
st.markdown(
    "Planned anomaly-model foundation: "
    "[Anomalib](https://github.com/open-edge-platform/anomalib), "
    "licensed under Apache-2.0. "
    "The current starter performs OpenCV image processing only."
)
