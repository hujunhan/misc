import os


def create_folder_structure(base_folder, structure):
    for folder, subfolders in structure.items():
        folder_name = folder.replace("_", " ")
        new_folder = os.path.join(base_folder, folder_name)
        os.makedirs(new_folder, exist_ok=True)

        if isinstance(subfolders, dict):
            create_folder_structure(new_folder, subfolders)


if __name__ == "__main__":
    base_folder = "/Users/hu/Downloads/new_markdown"  # Current working directory

    structure = {
        "Technology": {
            "Computer Science": {
                "Algorithms": {},
                "Programming Languages": {"Python": {}, "C++": {}},
                "Web Development": {},
                "AI Machine Learning": {"Papers": {}, "Projects": {}},
                "Computational Photography": {},
                "Miscellaneous": {},
            },
            "Robotics": {
                "Computer Vision": {},
                "Hardware EmbeddedSystems": {},
                "Planning Localization": {},
                "Projects Seminars": {},
            },
        },
        "Sciences": {
            "Mathematics": {"Algebra": {}, "Statistics": {}, "Modeling": {}},
            "Control Theory": {"Digital_Signal_Processing": {}, "Process_Control": {}},
            "Philosophy_Neuroscience": {
                "Cognitive_Science": {},
                "Philosophy_of_Mind": {},
                "Psychology": {},
            },
        },
        "Business Entrepreneurship": {
            "Strategy": {},
            "Investment Finance": {},
            "Industry Analysis": {},
        },
        "Life Skills": {
            "Personal_Development": {
                "Learning": {},
                "Career_Planning": {},
                "Life_Plans": {},
            },
            "Hobbies_Interests": {"Music": {}, "Photography": {}, "Travel": {}},
            "Health_Wellness": {"Nutrition": {}, "Mental_Health": {}},
        },
        "Social Sciences Humanities": {
            "Economics": {},
            "Sociology": {},
            "Geography": {},
            "Comparative_Religion": {},
            "Literature": {},
        },
        "Miscellaneous": {
            "First_Aid": {},
            "Legal_Knowledge": {},
            "Spiritual_Mysticism": {},
        },
    }

    create_folder_structure(base_folder, structure)
