# PyRIDE Common Messages

Common message definitions for PyRIDE robot interface framework.

## Overview

This package provides ROS2 message, service, and action definitions used by PyRIDE nodes for:
- Node communication (status and command messages)
- Object tracking (detection, updates, status changes)
- Object enrollment workflows

## Topics

### Node Communication

| Topic | Message Type | Direction | Purpose |
|-------|--------------|-----------|---------|
| `/pyride/node_message` | NodeMessage | In | Commands sent to nodes |
| `/pyride/node_status` | NodeStatus | Out | Status updates from nodes |

### Object Tracking

| Topic | Message Type | Direction | Purpose |
|-------|--------------|-----------|---------|
| (varies) | TrackedObjectUpdate | Out | Array of tracked objects |
| (varies) | TrackedObjectStatusChange | Out | Status change notifications |
| (varies) | AnnotatedView | Out | Image with annotated objects |

## Message Definitions

### NodeMessage
Command message sent to nodes.
- `header`: Standard ROS header with timestamp/frame
- `node_id`: Target node identifier
- `priority`: Message priority level (int8)
- `command`: JSON-encoded command payload

### NodeStatus
Status message published by nodes.
- `header`: Standard ROS header
- `node_id`: Publishing node identifier
- `for_console`: True if message is for console display
- `priority`: Message priority level (int8)
- `status_text`: Status message text

### ObjectBound
2D bounding box for object detection.
- `tl_x`: Top-left X coordinate
- `tl_y`: Top-left Y coordinate
- `width`: Bounding box width
- `height`: Bounding box height

### TrackedObjectInfo
Information about a tracked object.
- `objtype`: Object type identifier (uint8)
- `id`: Object instance ID (uint8)
- `bound`: 2D bounding box (ObjectBound)
- `est_pos`: Estimated position (geometry_msgs/Point32)
- `confidence`: Detection confidence (0.0-1.0)

### TrackedObjectStatusChange
Notification when a tracked object's status changes.
- `header`: Standard ROS header
- `objtype`: Object type identifier (uint8)
- `trackid`: Track ID (uint8)
- `name`: Object name
- `status`: New status (uint8)
- `confidence`: Confidence score

### TrackedObjectUpdate
Batch update containing multiple tracked objects.
- `header`: Standard ROS header
- `objects`: Array of TrackedObjectInfo

### AnnotatedView
Image with annotated object detections.
- `image`: Camera image (sensor_msgs/Image)
- `objects`: Array of detected objects (TrackedObjectInfo)

## Services

### RenameObject
Rename an enrolled object.

**Request:**
- `old_name`: Current object name
- `new_name`: New object name

**Response:**
- `success`: True if rename succeeded

## Actions

### ObjectEnrolment
Action for enrolling new objects into the system.

**Goal:**
- `name`: Name to assign to the object
- `instances`: Number of instances to enroll
- `timeout`: Maximum time for enrollment (seconds)

**Result:**
- `success`: True if enrollment succeeded
- `reason`: Failure reason if unsuccessful

**Feedback:**
- `step`: Current enrollment step

## Scripts

### pyride_msg_loopback_router.py
Route messages from `/pyride/node_message` to `/pyride/node_status`.

Listens for messages where `node_id` matches the configured router ID (default: `message_router`), parses the JSON command, and republishes as a status message.

**Parameters:**
- `router_node_id`: Node ID to match (default: `message_router`)

## Launch Files

### loopback_router.launch.py
Launch the loopback router node with optional configuration.

```bash
# Default launch
ros2 launch pyride_common_msgs loopback_router.launch.py

# Custom router ID
ros2 launch pyride_common_msgs loopback_router.launch.py router_node_id:=custom_router
```

**Parameters:**
- `router_node_id`: Node ID to match (default: `message_router`)

## Testing

Unit tests for the loopback router are available in `test/test_loopback_router.py`.

```bash
# Run tests
cd /home/xun/ros2_ws
colcon test --packages-select pyride_common_msgs

# Or run directly
python3 -m pytest src/pyride_common_msgs/test/test_loopback_router.py -v
```

**Test Coverage:**
- Message filtering by node ID
- JSON parsing and validation
- Priority preservation
- Header preservation
- Message field validation

## Dependencies

- `std_msgs`: Standard ROS message types
- `sensor_msgs`: Sensor message types (for Image)
- `geometry_msgs`: Geometry message types (for Point32)
- `action_msgs`: ROS2 action types

## Building

```bash
colcon build --packages-up-to pyride_common_msgs
```

## License

BSD
