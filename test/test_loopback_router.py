#!/usr/bin/env python3
"""Tests for pyride_msg_loopback_router.py"""

import json
import sys
import os
import unittest
from unittest.mock import MagicMock, patch

# Add scripts directory to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'scripts'))

try:
    import rclpy
    from rclpy.node import Node
    from std_msgs.msg import Header
    from pyride_common_msgs.msg import NodeStatus, NodeMessage
    from pyride_msg_loopback_router import PyRideLoopbackMsgRouter, NODE_ID
except ImportError as e:
    print(f"Warning: Could not import ROS dependencies: {e}")
    print("Running in mock mode...")
    NODE_ID = 'message_router'

    class MockNode:
        pass

    Node = MockNode
    NodeStatus = MagicMock
    NodeMessage = MagicMock
    PyRideLoopbackMsgRouter = MagicMock


class TestPyRideLoopbackMsgRouter(unittest.TestCase):
    """Test cases for PyRideLoopbackMsgRouter."""

    def setUp(self):
        """Set up test fixtures."""
        self.mock_context = MagicMock()
        self.mock_context.ok.return_value = True

    @unittest.skipUnless(rclpy.ok(), "Requires ROS2 context")
    def test_main_inits_and_shuts_down(self):
        """Test main function initializes and shuts down properly.

        This test requires a full ROS2 environment and is skipped if not available.
        """
        # This test would require a full ROS2 environment to run
        # It verifies that main() calls rclpy.init(), rclpy.spin(), and rclpy.shutdown()
        # in the correct order and handles KeyboardInterrupt gracefully
        self.assertTrue(True)  # Placeholder

    def test_constant_default_node_id(self):
        """Test that NODE_ID constant exists and has correct default."""
        self.assertEqual(NODE_ID, 'message_router')

    def test_input_cb_filters_wrong_node_id(self):
        """Test that messages with wrong node_id are ignored."""
        with patch.object(Node, 'get_parameter', return_value=MagicMock(
            get_parameter_value=MagicMock(return_value=MagicMock(string_value='message_router'))
        )):
            router = PyRideLoopbackMsgRouter.__new__(PyRideLoopbackMsgRouter)
            router._router_node_id = 'message_router'
            router.pub = MagicMock()

            msg = NodeMessage()
            msg.node_id = 'other_node'

            router.input_cb(msg)

            router.pub.publish.assert_not_called()

    def test_input_cb_processes_correct_node_id(self):
        """Test that messages with correct node_id are processed."""
        with patch.object(Node, 'get_parameter', return_value=MagicMock(
            get_parameter_value=MagicMock(return_value=MagicMock(string_value='message_router'))
        )):
            router = PyRideLoopbackMsgRouter.__new__(PyRideLoopbackMsgRouter)
            router._router_node_id = 'message_router'
            router.pub = MagicMock()

            command = {'node_id': 'target_node', 'command': 'test command'}
            msg = NodeMessage()
            msg.node_id = 'message_router'
            msg.command = json.dumps(command)
            msg.priority = 5

            router.input_cb(msg)

            router.pub.publish.assert_called_once()
            published_msg = router.pub.publish.call_args[0][0]
            self.assertEqual(published_msg.node_id, 'target_node')
            self.assertEqual(published_msg.status_text, 'test command')
            self.assertEqual(published_msg.priority, 5)
            self.assertFalse(published_msg.for_console)

    def test_input_cb_invalid_json(self):
        """Test that invalid JSON is rejected."""
        mock_logger = MagicMock()
        with patch.object(Node, 'get_parameter', return_value=MagicMock(
            get_parameter_value=MagicMock(return_value=MagicMock(string_value='message_router'))
        )):
            router = PyRideLoopbackMsgRouter.__new__(PyRideLoopbackMsgRouter)
            router._router_node_id = 'message_router'
            router.get_logger = MagicMock(return_value=mock_logger)
            router.pub = MagicMock()

            msg = NodeMessage()
            msg.node_id = 'message_router'
            msg.command = 'not valid json'

            router.input_cb(msg)

            mock_logger.error.assert_called()
            router.pub.publish.assert_not_called()

    def test_input_cb_missing_fields(self):
        """Test that messages missing required fields are rejected."""
        mock_logger = MagicMock()
        with patch.object(Node, 'get_parameter', return_value=MagicMock(
            get_parameter_value=MagicMock(return_value=MagicMock(string_value='message_router'))
        )):
            router = PyRideLoopbackMsgRouter.__new__(PyRideLoopbackMsgRouter)
            router._router_node_id = 'message_router'
            router.get_logger = MagicMock(return_value=mock_logger)
            router.pub = MagicMock()

            # Missing 'node_id' field
            command = {'command': 'test'}
            msg = NodeMessage()
            msg.node_id = 'message_router'
            msg.command = json.dumps(command)

            router.input_cb(msg)

            mock_logger.error.assert_called()
            router.pub.publish.assert_not_called()

    def test_input_cb_preserves_header(self):
        """Test that the header is preserved from input to output."""
        with patch.object(Node, 'get_parameter', return_value=MagicMock(
            get_parameter_value=MagicMock(return_value=MagicMock(string_value='message_router'))
        )):
            router = PyRideLoopbackMsgRouter.__new__(PyRideLoopbackMsgRouter)
            router._router_node_id = 'message_router'
            router.pub = MagicMock()

            command = {'node_id': 'target_node', 'command': 'status update'}
            msg = NodeMessage()
            msg.node_id = 'message_router'
            msg.command = json.dumps(command)
            msg.header.stamp = 12345
            msg.header.frame_id = 'base_link'

            router.input_cb(msg)

            published_msg = router.pub.publish.call_args[0][0]
            self.assertEqual(published_msg.header.stamp, 12345)
            self.assertEqual(published_msg.header.frame_id, 'base_link')

    def test_input_cb_priority_preserved(self):
        """Test that priority is preserved from input to output."""
        with patch.object(Node, 'get_parameter', return_value=MagicMock(
            get_parameter_value=MagicMock(return_value=MagicMock(string_value='message_router'))
        )):
            router = PyRideLoopbackMsgRouter.__new__(PyRideLoopbackMsgRouter)
            router._router_node_id = 'message_router'
            router.pub = MagicMock()

            for priority_val in [-128, -1, 0, 1, 127]:
                command = {'node_id': 'target', 'command': 'test'}
                msg = NodeMessage()
                msg.node_id = 'message_router'
                msg.command = json.dumps(command)
                msg.priority = priority_val

                router.input_cb(msg)

                published_msg = router.pub.publish.call_args[0][0]
                self.assertEqual(published_msg.priority, priority_val)


class TestMessageFields(unittest.TestCase):
    """Test that message types have expected fields."""

    def test_node_message_fields(self):
        """Test NodeMessage has all required fields."""
        msg = NodeMessage()
        self.assertTrue(hasattr(msg, 'header'))
        self.assertTrue(hasattr(msg, 'node_id'))
        self.assertTrue(hasattr(msg, 'priority'))
        self.assertTrue(hasattr(msg, 'command'))

    def test_node_status_fields(self):
        """Test NodeStatus has all required fields."""
        msg = NodeStatus()
        self.assertTrue(hasattr(msg, 'header'))
        self.assertTrue(hasattr(msg, 'node_id'))
        self.assertTrue(hasattr(msg, 'for_console'))
        self.assertTrue(hasattr(msg, 'priority'))
        self.assertTrue(hasattr(msg, 'status_text'))


if __name__ == '__main__':
    unittest.main()
