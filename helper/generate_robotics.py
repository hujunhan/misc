import os


def create_folder_structure(base_folder, structure):
    for folder, subfolders in structure.items():
        folder_name = folder  # No need to replace underscores this time
        new_folder = os.path.join(base_folder, folder_name)
        os.makedirs(new_folder, exist_ok=True)

        if isinstance(subfolders, dict):
            create_folder_structure(new_folder, subfolders)


if __name__ == "__main__":
    base_folder = "/Users/hu/Downloads/new_markdown/Technology/Robotics"  # Current working directory

    structure = {
        "Introduction": {},
        "Core Concepts": {
            "Mathematics": {"Kinematics": {}, "Planning Algorithms": {}},
            "Control Systems": {},
            "Data Fusion and Localization": {},
        },
        "Sensing and Perception": {"Computer Vision": {}, "Sensors": {}},
        "Hardware and Embedded Systems": {
            "Actuators": {},
            "Sensors and Interfaces": {},
            "Embedded Controllers": {},
        },
        "Software and Frameworks": {"ROS": {}, "Simulation": {}},
        "Specialized Topics": {"Mobile Robots": {}, "Manipulators": {}, "SLAM": {}},
        "Projects and Case Studies": {},
        "Tutorials and Courses": {"Seminar": {}, "Udemy": {}},
        "Additional Resources": {},
    }

    create_folder_structure(base_folder, structure)
