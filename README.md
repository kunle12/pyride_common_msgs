# PyRIDE Common Messages

Common message definitions for PyRIDE robot interface framework.

## Overview

This package provides ROS2 message, service, and action definitions used by PyRIDE nodes for:
- Node communication (status and command messages)
- Object tracking (detection, updates, status changes)
- Object enrollment workflows
- Audio streaming and recording
- Speech-to-text transcription
- Text-to-speech synthesis
- Face recognition and comparison

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

### AudioData
Raw audio data buffer.

- `data`: Audio sample bytes (uint8 array). PCM format described by accompanying AudioFormat message.

### AudioFormat
Audio stream metadata, typically published with `transient_local` durability for late-joining subscribers.

- `sample_rate`: Sample rate in Hz (e.g., 16000, 24000, 96000)
- `channels`: Number of audio channels
- `depth`: Bits per sample (8, 16, 24, 32)

### AudioTranscription
Speech-to-text transcription result.

- `text`: Transcribed text string
- `language`: Language code (e.g., `"en"`, `"zh"`, `"zh-CN"`)

### FaceId
Face identity information.

- `confidence`: Matching confidence (float)
- `id`: Person identifier (uint8)

### FaceIdWithImg
Face identity with associated image data.

- `confidence`: Matching confidence (float)
- `id`: Person identifier (uint8)
- `img`: Image data (sensor_msgs/Image)

## Services

### CompareFace
Compare a face descriptor against enrolled faces.

**Request:** FaceId
**Response:** FaceId (best match), success (bool), reason (string)

### CompareFaceWithImg
Compare a face image against enrolled faces.

**Request:** sensor_msgs/Image
**Response:** FaceId (best match), success (bool), reason (string)

### ImgToFace
Extract face descriptor from an image.

**Request:** sensor_msgs/Image
**Response:** FaceId, success (bool), reason (string)

### KnownFaces
List all known/enrolled faces.

**Request:** (empty)
**Response:** names (string[]), ids (uint8[]), success (bool)

### RegisterFace
Register a new face.

**Request:** FaceId, name (string)
**Response:** success (bool), reason (string)

### RenameObject
Rename an enrolled object.

**Request:**
- `old_name`: Current object name
- `new_name`: New object name

**Response:**
- `success`: True if rename succeeded

### UnregisterFace
Remove a face from the enrollment database.

**Request:** name (string)
**Response:** success (bool), reason (string)

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
- `elapsed_played_time`: Elapsed playback time (builtin_interfaces/Time)

### TextToSpeech
Action for synthesizing text to speech. Used by `omnivoice_tts`.

**Goal:**
- `text`: Text to synthesize and speak (string)
- `voice`: Voice name identifier (string)
- `language`: Language code (string)
- `save_to_file`: If true, save audio to file instead of playback/ROS topic (bool)
- `seed`: Random seed for synthesis; <=0 uses random seed, >0 uses fixed seed (int32)

**Result:**
- `success`: True if synthesis succeeded (bool)
- `reason`: Failure or cancel reason (string)

**Feedback:**
- `progress`: Optional progress indicator 0-100 (int32)

### RecordAudio
Action for recording audio to a file.

**Goal:**
- `period`: Recording duration (builtin_interfaces/Time)
- `format`: Audio format (e.g., "wav", "mp3")
- `filename`: Output file path

**Result:**
- `success`: True if recording succeeded
- `reason`: Failure reason if unsuccessful

**Feedback:**
- `bytes`: Bytes recorded so far

### AudioFilePlay
Action for playing an audio file.

**Goal:**
- `filepath`: Path to the audio file

**Result:**
- `success`: True if playback succeeded
- `reason`: Failure reason if unsuccessful
- `total_time`: Total playback duration (builtin_interfaces/Time)

**Feedback:**
- `elapsed_played_time`: Elapsed playback time (builtin_interfaces/Time)

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

## Building

```bash
colcon build --packages-up-to pyride_common_msgs
```

## License

MIT License
