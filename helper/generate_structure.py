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
            "Computer_Science": {
                "Algorithms": {},
                "Programming_Languages": {"Python": {}, "C++": {}},
                "Web_Development": {},
                "AI_MachineLearning": {"Papers": {}, "Projects": {}},
                "Computational_Photography": {},
                "Miscellaneous": {},
            },
            "Robotics": {
                "Computer_Vision": {},
                "Hardware_EmbeddedSystems": {},
                "Planning_Localization": {},
                "Projects_Seminars": {},
            },
        },
        "Sciences": {
            "Mathematics": {"Algebra": {}, "Statistics": {}, "Modeling": {}},
            "Control_Theory": {"Digital_Signal_Processing": {}, "Process_Control": {}},
            "Philosophy_Neuroscience": {
                "Cognitive_Science": {},
                "Philosophy_of_Mind": {},
                "Psychology": {},
            },
        },
        "Business_Entrepreneurship": {
            "Strategy": {},
            "Investment_Finance": {},
            "Industry_Analysis": {},
        },
        "Life_Skills": {
            "Personal_Development": {
                "Learning": {},
                "Career_Planning": {},
                "Life_Plans": {},
            },
            "Hobbies_Interests": {"Music": {}, "Photography": {}, "Travel": {}},
            "Health_Wellness": {"Nutrition": {}, "Mental_Health": {}},
        },
        "Social_Sciences_Humanities": {
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
