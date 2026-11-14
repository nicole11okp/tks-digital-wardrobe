
import streamlit as st
import json
import random
import uuid
from pathlib import Path

st.set_page_config(page_title="My Digital Wardrobe", page_icon="👗")

DATA_FILE = Path("wardrobe.json")
IMAGE_FOLDER = Path("wardrobe_images")
IMAGE_FOLDER.mkdir(exist_ok=True)


def load_wardrobe():
    if DATA_FILE.exists():
        return json.loads(DATA_FILE.read_text())
    return []


def save_wardrobe():
    DATA_FILE.write_text(
        json.dumps(st.session_state.wardrobe, indent=2)
    )


if "wardrobe" not in st.session_state:
    st.session_state.wardrobe = load_wardrobe()


st.title("My Digital Wardrobe")
st.write("Organize your clothes and create outfits from what you own.")

st.header("Add Clothing")

clothing_name = st.text_input("Name your clothing item")

category = st.selectbox(
    "Clothing category",
    ["Tops", "Bottoms", "Shoes", "Outerwear", "Accessories"]
)


style = st.selectbox(
    "Clothing style",
    ["Casual", "School", "Going Out", "Dressy", "Versatile"]
)


clothing_image = st.file_uploader(
    "Upload a photo of your clothing item",
    type=["jpg", "jpeg", "png"]
)

if clothing_image is not None:
    st.image(clothing_image, width=250)

if st.button("Add to Wardrobe"):
    if clothing_name.strip() and clothing_image is not None:
        extension = Path(clothing_image.name).suffix.lower()
        image_path = IMAGE_FOLDER / f"{uuid.uuid4().hex}{extension}"
        image_path.write_bytes(clothing_image.getvalue())

        item = {
            "name": clothing_name.strip(),
            "category": category,
            "style": style,
            "image": str(image_path)
        }

        st.session_state.wardrobe.append(item)
        save_wardrobe()

        st.success(f"{clothing_name} added to your wardrobe!")
    else:
        st.warning("Please enter a name and upload a photo.")


st.divider()
st.header("My Closet")

if not st.session_state.wardrobe:
    st.info("Your wardrobe is empty. Add your first item!")
else:
    columns = st.columns(3)

    for index, item in enumerate(st.session_state.wardrobe):
        with columns[index % 3]:
            if Path(item["image"]).exists():
                st.image(item["image"], width="stretch")
            st.write(item["name"])
            st.caption(item["category"])

            if st.button("Delete", key=f"delete_{index}"):
                st.session_state.wardrobe.pop(index)
                save_wardrobe()
                st.rerun()

st.divider()
st.header("Your Personal Stylist")
st.write("Generate an outfit using clothes from your wardrobe.")


occasion = st.selectbox(
    "What are you dressing for?",
    ["Casual", "School", "Going Out", "Dressy"]
)


if st.button("Generate My Outfit"):

    style_tips = {
        "Casual": "A relaxed, everyday outfit.",
        "School": "A comfortable, school-appropriate outfit.",
        "Going Out": "A fun outfit for going out.",
        "Dressy": "A more polished, dressed-up outfit."
    }

    st.info(style_tips[occasion])
    def match_style(items):
        matching = [
            item for item in items
            if item.get("style") in [occasion, "Versatile"]
        ]
        return matching if matching else items

    tops = [
        item for item in st.session_state.wardrobe
        if item["category"] == "Tops"
    ]

    bottoms = [
        item for item in st.session_state.wardrobe
        if item["category"] == "Bottoms"
    ]

    shoes = [
        item for item in st.session_state.wardrobe
        if item["category"] == "Shoes"
    ]

    tops = match_style(tops)
    bottoms = match_style(bottoms)
    shoes = match_style(shoes)

    if tops and bottoms and shoes:
        outfit = [
            random.choice(tops),
            random.choice(bottoms),
            random.choice(shoes)
        ]

        st.subheader("Your Outfit")

        outfit_columns = st.columns(3)

        for index, item in enumerate(outfit):
            with outfit_columns[index]:
                st.image(item["image"], width="stretch")
                st.write(item["name"])
    else:
        st.warning(
            "Add at least one top, bottom, and pair of shoes!"
        )
