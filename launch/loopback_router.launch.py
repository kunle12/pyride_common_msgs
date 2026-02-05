"""Launch file for pyride_msg_loopback_router node."""

from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node


def generate_launch_description() -> LaunchDescription:
    """Generate launch description for the loopback router."""
    declare_arguments = []

    declare_router_node_id = DeclareLaunchArgument(
        'router_node_id',
        default_value='message_router',
        description='Node ID to match in incoming messages',
    )

    declare_arguments.append(declare_router_node_id)

    loopback_router_node = Node(
        package='pyride_common_msgs',
        executable='pyride_msg_loopback_router',
        name='pyride_msg_loopback_router',
        namespace='pyride',
        parameters=[
            {'router_node_id': LaunchConfiguration('router_node_id')},
        ],
        remappings=[
            ('/pyride/node_message', '/pyride/node_message'),
            ('/pyride/node_status', '/pyride/node_status'),
        ],
        output='screen',
        emulate_tty=True,
    )

    return LaunchDescription(declare_arguments + [loopback_router_node])
