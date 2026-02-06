# rby1_inha_nav2

This repository contains a minimal subset of the rby1_nav2 package for navigation and HRI (Human-Robot Interaction) in restaurant environments.

## Included Directories and Files

- `src/bt/` : Behavior Tree XML files for navigation and HRI
- `config/param_hri.yaml` : Parameters for HRI navigation
- `config/param_restaurant.yaml` : Parameters for restaurant navigation
- `launch/navigation_hri.launch.py` : Launch file for HRI navigation
- `launch/navigation_restaurant.launch.py` : Launch file for restaurant navigation

## Usage

Clone this repository and use the included launch files to start navigation for HRI or restaurant scenarios. Make sure to have ROS 2 and required dependencies installed.

## Example Launch

```bash
ros2 launch rby1_inha_nav2 navigation_hri.launch.py
ros2 launch rby1_inha_nav2 navigation_restaurant.launch.py
```

## Notes
- Only essential files for HRI and restaurant navigation are included.
- For full functionality, refer to the original rby1_nav2 package.

## License
MIT License
