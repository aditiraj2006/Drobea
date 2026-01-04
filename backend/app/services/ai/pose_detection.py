import cv2
import mediapipe as mp
import numpy as np
from typing import Dict, List, Tuple, Optional
import logging

logger = logging.getLogger(__name__)

class PoseDetector:
    def __init__(self):
        self.mp_pose = mp.solutions.pose
        self.pose = self.mp_pose.Pose(
            static_image_mode=True,
            model_complexity=2,
            enable_segmentation=True,
            min_detection_confidence=0.5
        )
        self.mp_drawing = mp.solutions.drawing_utils
    
    async def analyze_pose(self, image_path: str) -> Dict[str, any]:
        """
        Analyze pose from image and return pose data
        """
        try:
            # Load image
            image = cv2.imread(image_path)
            if image is None:
                raise ValueError(f"Could not load image: {image_path}")
            
            # Convert BGR to RGB
            rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            
            # Process image
            results = self.pose.process(rgb_image)
            
            if not results.pose_landmarks:
                raise ValueError("No pose detected in image")
            
            # Extract pose landmarks
            landmarks = self._extract_landmarks(results.pose_landmarks.landmark)
            
            # Determine pose type
            pose_type = self._classify_pose(landmarks)
            
            # Calculate bounding box
            bounding_box = self._calculate_bounding_box(landmarks, image.shape)
            
            # Calculate confidence
            confidence = self._calculate_confidence(results.pose_landmarks.landmark)
            
            return {
                "landmarks": landmarks,
                "bounding_box": bounding_box,
                "confidence": confidence,
                "pose_type": pose_type,
                "image_dimensions": {
                    "width": image.shape[1],
                    "height": image.shape[0]
                }
            }
            
        except Exception as e:
            logger.error(f"Pose detection failed: {e}")
            raise
    
    def _extract_landmarks(self, landmarks) -> List[Dict[str, float]]:
        """Extract pose landmarks with normalized coordinates"""
        extracted_landmarks = []
        
        for landmark in landmarks:
            extracted_landmarks.append({
                "x": landmark.x,
                "y": landmark.y,
                "z": landmark.z,
                "visibility": landmark.visibility
            })
        
        return extracted_landmarks
    
    def _classify_pose(self, landmarks: List[Dict[str, float]]) -> str:
        """Classify the type of pose based on landmark positions"""
        # Key landmark indices for pose classification
        NOSE = 0
        LEFT_SHOULDER = 11
        RIGHT_SHOULDER = 12
        LEFT_HIP = 23
        RIGHT_HIP = 24
        LEFT_ANKLE = 27
        RIGHT_ANKLE = 28
        LEFT_WRIST = 15
        RIGHT_WRIST = 16
        
        # Get key points
        nose = landmarks[NOSE]
        left_shoulder = landmarks[LEFT_SHOULDER]
        right_shoulder = landmarks[RIGHT_SHOULDER]
        left_hip = landmarks[LEFT_HIP]
        right_hip = landmarks[RIGHT_HIP]
        left_ankle = landmarks[LEFT_ANKLE]
        right_ankle = landmarks[RIGHT_ANKLE]
        left_wrist = landmarks[LEFT_WRIST]
        right_wrist = landmarks[RIGHT_WRIST]
        
        # Calculate body orientation
        shoulder_center_x = (left_shoulder["x"] + right_shoulder["x"]) / 2
        hip_center_x = (left_hip["x"] + right_hip["x"]) / 2
        
        # Determine if person is facing front or back
        if abs(shoulder_center_x - hip_center_x) < 0.05:
            orientation = "front"
        else:
            orientation = "side"
        
        # Calculate body angle
        body_angle = self._calculate_body_angle(left_shoulder, right_shoulder, left_hip, right_hip)
        
        # Determine pose type based on body position
        if orientation == "front":
            if body_angle < 10:  # Standing straight
                return "standing_front"
            elif body_angle > 10:  # Leaning or dynamic pose
                return "dynamic_front"
        else:
            if body_angle < 10:
                return "standing_side"
            else:
                return "dynamic_side"
        
        # Check for sitting pose
        if self._is_sitting_pose(landmarks):
            return "sitting"
        
        # Check for walking pose
        if self._is_walking_pose(landmarks):
            return "walking"
        
        return "standing"
    
    def _calculate_body_angle(self, left_shoulder, right_shoulder, left_hip, right_hip) -> float:
        """Calculate the angle of the body"""
        shoulder_center = {
            "x": (left_shoulder["x"] + right_shoulder["x"]) / 2,
            "y": (left_shoulder["y"] + right_shoulder["y"]) / 2
        }
        hip_center = {
            "x": (left_hip["x"] + right_hip["x"]) / 2,
            "y": (left_hip["y"] + right_hip["y"]) / 2
        }
        
        # Calculate angle from vertical
        dx = shoulder_center["x"] - hip_center["x"]
        dy = shoulder_center["y"] - hip_center["y"]
        
        angle = np.degrees(np.arctan2(dx, dy))
        return abs(angle)
    
    def _is_sitting_pose(self, landmarks: List[Dict[str, float]]) -> bool:
        """Check if the pose is sitting"""
        LEFT_HIP = 23
        RIGHT_HIP = 24
        LEFT_KNEE = 25
        RIGHT_KNEE = 26
        LEFT_ANKLE = 27
        RIGHT_ANKLE = 28
        
        left_hip = landmarks[LEFT_HIP]
        right_hip = landmarks[RIGHT_HIP]
        left_knee = landmarks[LEFT_KNEE]
        right_knee = landmarks[RIGHT_KNEE]
        left_ankle = landmarks[LEFT_ANKLE]
        right_ankle = landmarks[RIGHT_ANKLE]
        
        # Check if knees are significantly higher than ankles (sitting position)
        left_knee_ankle_diff = left_knee["y"] - left_ankle["y"]
        right_knee_ankle_diff = right_knee["y"] - right_ankle["y"]
        
        return left_knee_ankle_diff > 0.1 and right_knee_ankle_diff > 0.1
    
    def _is_walking_pose(self, landmarks: List[Dict[str, float]]) -> bool:
        """Check if the pose is walking"""
        LEFT_ANKLE = 27
        RIGHT_ANKLE = 28
        LEFT_WRIST = 15
        RIGHT_WRIST = 16
        
        left_ankle = landmarks[LEFT_ANKLE]
        right_ankle = landmarks[RIGHT_ANKLE]
        left_wrist = landmarks[LEFT_WRIST]
        right_wrist = landmarks[RIGHT_WRIST]
        
        # Check for walking indicators (asymmetric arm/leg positions)
        arm_asymmetry = abs(left_wrist["x"] - right_wrist["x"])
        leg_asymmetry = abs(left_ankle["x"] - right_ankle["x"])
        
        return arm_asymmetry > 0.1 or leg_asymmetry > 0.1
    
    def _calculate_bounding_box(self, landmarks: List[Dict[str, float]], image_shape: Tuple[int, int, int]) -> Dict[str, float]:
        """Calculate bounding box around the person"""
        # Get all visible landmarks
        visible_landmarks = [lm for lm in landmarks if lm["visibility"] > 0.5]
        
        if not visible_landmarks:
            return {"x": 0, "y": 0, "width": 1, "height": 1}
        
        # Calculate bounding box
        x_coords = [lm["x"] for lm in visible_landmarks]
        y_coords = [lm["y"] for lm in visible_landmarks]
        
        min_x = min(x_coords)
        max_x = max(x_coords)
        min_y = min(y_coords)
        max_y = max(y_coords)
        
        # Add padding
        padding = 0.1
        width = max_x - min_x
        height = max_y - min_y
        
        min_x = max(0, min_x - padding * width)
        max_x = min(1, max_x + padding * width)
        min_y = max(0, min_y - padding * height)
        max_y = min(1, max_y + padding * height)
        
        return {
            "x": min_x,
            "y": min_y,
            "width": max_x - min_x,
            "height": max_y - min_y
        }
    
    def _calculate_confidence(self, landmarks) -> float:
        """Calculate overall confidence of pose detection"""
        confidences = [landmark.visibility for landmark in landmarks]
        return sum(confidences) / len(confidences)
    
    async def detect_multiple_poses(self, image_path: str) -> List[Dict[str, any]]:
        """Detect multiple poses in an image (if any)"""
        # For now, we'll return a single pose detection
        # In the future, this could be extended to detect multiple people
        pose_data = await self.analyze_pose(image_path)
        return [pose_data]
    
    def get_pose_landmarks_visualization(self, image_path: str, output_path: str) -> bool:
        """Create visualization of pose landmarks"""
        try:
            image = cv2.imread(image_path)
            rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            
            results = self.pose.process(rgb_image)
            
            if results.pose_landmarks:
                annotated_image = rgb_image.copy()
                self.mp_drawing.draw_landmarks(
                    annotated_image,
                    results.pose_landmarks,
                    self.mp_pose.POSE_CONNECTIONS
                )
                
                # Convert back to BGR for saving
                annotated_image = cv2.cvtColor(annotated_image, cv2.COLOR_RGB2BGR)
                cv2.imwrite(output_path, annotated_image)
                return True
            
            return False
            
        except Exception as e:
            logger.error(f"Failed to create pose visualization: {e}")
            return False
