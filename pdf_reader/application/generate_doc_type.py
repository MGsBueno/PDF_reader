import json


PROFILE_LIBRARY = {
    "generic_example": {
        "context_name": "structures",
        "block_names": ["Title", "Subtitle", "Summary", "Details"],
        "rules": {
            "Title": [r"^title"],
            "Subtitle": [r"^subtitle"],
            "Summary": [r"^summary"],
            "Details": [r"^details"],
        },
        "ignore": ["Page", "Header", "Footer"],
        "minimum_font_size": 12,
        "minimum_description_font_size": 10,
    },
    "structured_report_example": {
        "context_name": "structures",
        "block_names": [
            "Main Section",
            "Objective",
            "Contextualization",
            "Indicators",
            "Challenges",
            "Classification",
            "Results and Opportunities",
            "Action Plan",
            "Actions and Thematic Axes",
            "Goals",
            "Initiatives",
            "Responsible Parties",
            "Additional Information",
            "Context",
            "Regionalization",
        ],
        "rules": {
            "Main Section": [r"^main section"],
            "Objective": [r"^objective"],
            "Contextualization": [r"^contextualization"],
            "Indicators": [r"^indicators", r"^prioritized indicators"],
            "Challenges": [r"^challenges"],
            "Classification": [r"^classification"],
            "Results and Opportunities": [r"^results and opportunities"],
            "Action Plan": [r"^action plan"],
            "Actions and Thematic Axes": [r"^actions", r"^thematic axes"],
            "Goals": [r"^goals$"],
            "Initiatives": [r"^initiatives"],
            "Responsible Parties": [r"^responsible parties?"],
            "Additional Information": [r"^additional information"],
            "Context": [r"^context"],
            "Regionalization": [r"^regionalization"],
        },
        "ignore": [
            "Page",
            "Contextualization",
            "Footer",
        ],
        "minimum_font_size": 12,
        "minimum_description_font_size": 10,
    },
}


def create_block(
    name,
    match=None,
    end_on_match=None,
    minimum_font_size=None,
    minimum_description_font_size=None,
    starts_structure=None,
    uses_description=None,
):
    block = {}
    if match is not None:
        block["match"] = match
    if end_on_match is not None:
        block["end_on_match"] = end_on_match
    if minimum_font_size is not None:
        block["minimum_font_size"] = minimum_font_size
    if minimum_description_font_size is not None:
        block["minimum_description_font_size"] = minimum_description_font_size
    if starts_structure is not None:
        block["starts_structure"] = starts_structure
    if uses_description is not None:
        block["uses_description"] = uses_description
    return name, block


def create_doc_type(blocks, ignore=None, block_names=None, context_name="structures"):
    if ignore is None:
        ignore = []

    if block_names is None:
        block_names = []

    return {
        context_name: {
            "blocks": dict(blocks),
            "ignore": ignore,
            "block_names": block_names,
        }
    }


def save_json(data, file_name="doc_type.json"):
    with open(file_name, "w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=2)
    print(f"File {file_name} created successfully.")


def build_doc_type_from_profile(profile: dict):
    context_name = profile.get("context_name", "structures")
    block_names = profile.get("block_names", [])
    rules = profile.get("rules", {})
    minimum_font_size = profile.get("minimum_font_size", 12)
    minimum_description_font_size = profile.get("minimum_description_font_size", 10)

    blocks = []
    for name in block_names:
        blocks.append(
            create_block(
                name,
                match=rules.get(name, [f"^{name.lower()}"]),
                minimum_font_size=minimum_font_size,
                minimum_description_font_size=minimum_description_font_size,
            )
        )

    return create_doc_type(
        blocks,
        ignore=profile.get("ignore", []),
        block_names=block_names,
        context_name=context_name,
    )


def build_doc_type(profile_name="generic_example"):
    if profile_name not in PROFILE_LIBRARY:
        raise ValueError(f"Unknown doc type profile: {profile_name}")

    return build_doc_type_from_profile(PROFILE_LIBRARY[profile_name])
