#!/usr/bin/env python

import rclpy
from rclpy.node import Node
import json
from pyride_common_msgs.msg import NodeStatus, NodeMessage

# Default node ID for this router (can be overridden via parameter)
NODE_ID = 'message_router'


class PyRideLoopbackMsgRouter(Node):
    def __init__(self):
        super().__init__('pyride_msg_loopback_router')
        self.declare_parameter('router_node_id', NODE_ID)
        self._router_node_id = self.get_parameter('router_node_id').get_parameter_value().string_value
        self.sub = self.create_subscription(
            NodeMessage,
            "/pyride/node_message",
            self.input_cb,
            10
        )
        self.pub = self.create_publisher(NodeStatus, "/pyride/node_status", 10)

    def input_cb( self, input_msg ):
        if input_msg.node_id != self._router_node_id:
            return
        try:
            message = json.loads(input_msg.command)
        except Exception:
            self.get_logger().error("invalid message format for PyRIDE message router")
            return
        if not isinstance(message, dict) or 'node_id' not in message or 'command' not in message:
            self.get_logger().error("invalid message format for PyRIDE message router")
            return

        msg = NodeStatus()
        msg.node_id = message['node_id']
        msg.header = input_msg.header
        msg.status_text = message['command']
        msg.priority = input_msg.priority
        msg.for_console = False
        self.pub.publish(msg)


def main():
    rclpy.init()
    node = PyRideLoopbackMsgRouter()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
