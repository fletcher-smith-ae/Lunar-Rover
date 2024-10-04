cmake_minimum_required(VERSION 2.8.3)

project(rover)

find_package(catkin REQUIRED)

catkin_package()

find_package(roslaunch)

foreach(dir . sdf rover resource launch test urdf meshes meshes/dae rviz config)
	install(DIRECTORY ${dir}/
		DESTINATION ${CATKIN_PACKAGE_SHARE_DESTINATION}/${dir})
endforeach(dir)

install(
  DIRECTORY
    launch
    config
  DESTINATION
    share/${PROJECT_NAME}/
)