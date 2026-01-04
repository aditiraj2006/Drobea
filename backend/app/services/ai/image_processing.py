import cv2
import numpy as np
from PIL import Image, ImageEnhance, ImageFilter
import rembg
import io
import base64
from typing import Tuple, List, Dict, Any, Optional
import logging

logger = logging.getLogger(__name__)

class ImageProcessor:
    def __init__(self):
        self.rembg_session = rembg.new_session('u2net')
    
    async def enhance_photo(self, image_path: str) -> str:
        """
        Enhance user photo for better virtual try-on results
        """
        try:
            # Load image
            image = Image.open(image_path)
            
            # Convert to RGB if necessary
            if image.mode != 'RGB':
                image = image.convert('RGB')
            
            # Enhance image quality
            enhanced_image = await self._enhance_image_quality(image)
            
            # Save enhanced image
            enhanced_path = image_path.replace('.', '_enhanced.')
            enhanced_image.save(enhanced_path, quality=95)
            
            return enhanced_path
            
        except Exception as e:
            logger.error(f"Photo enhancement failed: {e}")
            return image_path
    
    async def remove_background(self, image_path: str) -> str:
        """
        Remove background from image using rembg
        """
        try:
            with open(image_path, 'rb') as input_file:
                input_data = input_file.read()
            
            # Remove background
            output_data = rembg.remove(input_data, session=self.rembg_session)
            
            # Save result
            output_path = image_path.replace('.', '_nobg.')
            with open(output_path, 'wb') as output_file:
                output_file.write(output_data)
            
            return output_path
            
        except Exception as e:
            logger.error(f"Background removal failed: {e}")
            return image_path
    
    async def resize_image(self, image_path: str, target_size: Tuple[int, int]) -> str:
        """
        Resize image to target dimensions while maintaining aspect ratio
        """
        try:
            image = Image.open(image_path)
            
            # Calculate new size maintaining aspect ratio
            image.thumbnail(target_size, Image.Resampling.LANCZOS)
            
            # Create new image with target size and paste resized image
            new_image = Image.new('RGB', target_size, (255, 255, 255))
            new_image.paste(image, ((target_size[0] - image.size[0]) // 2, 
                                   (target_size[1] - image.size[1]) // 2))
            
            # Save resized image
            resized_path = image_path.replace('.', f'_resized_{target_size[0]}x{target_size[1]}.')
            new_image.save(resized_path, quality=95)
            
            return resized_path
            
        except Exception as e:
            logger.error(f"Image resizing failed: {e}")
            return image_path
    
    async def normalize_lighting(self, image_path: str) -> str:
        """
        Normalize lighting and contrast in the image
        """
        try:
            image = Image.open(image_path)
            
            # Convert to numpy array for processing
            img_array = np.array(image)
            
            # Apply CLAHE (Contrast Limited Adaptive Histogram Equalization)
            lab = cv2.cvtColor(img_array, cv2.COLOR_RGB2LAB)
            l, a, b = cv2.split(lab)
            
            clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
            l = clahe.apply(l)
            
            lab = cv2.merge([l, a, b])
            normalized = cv2.cvtColor(lab, cv2.COLOR_LAB2RGB)
            
            # Convert back to PIL Image
            normalized_image = Image.fromarray(normalized)
            
            # Save normalized image
            normalized_path = image_path.replace('.', '_normalized.')
            normalized_image.save(normalized_path, quality=95)
            
            return normalized_path
            
        except Exception as e:
            logger.error(f"Lighting normalization failed: {e}")
            return image_path
    
    async def detect_face(self, image_path: str) -> Optional[Dict[str, Any]]:
        """
        Detect face in the image and return face coordinates
        """
        try:
            # Load image
            image = cv2.imread(image_path)
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            
            # Load face cascade
            face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
            
            # Detect faces
            faces = face_cascade.detectMultiScale(gray, 1.1, 4)
            
            if len(faces) > 0:
                # Get the largest face
                face = max(faces, key=lambda x: x[2] * x[3])
                x, y, w, h = face
                
                return {
                    "x": int(x),
                    "y": int(y),
                    "width": int(w),
                    "height": int(h),
                    "confidence": 1.0
                }
            
            return None
            
        except Exception as e:
            logger.error(f"Face detection failed: {e}")
            return None
    
    async def extract_dominant_colors(self, image_path: str, num_colors: int = 5) -> List[Dict[str, Any]]:
        """
        Extract dominant colors from the image
        """
        try:
            image = Image.open(image_path)
            
            # Resize image for faster processing
            image = image.resize((150, 150))
            
            # Convert to numpy array
            img_array = np.array(image)
            img_array = img_array.reshape((-1, 3))
            
            # Use K-means clustering to find dominant colors
            from sklearn.cluster import KMeans
            
            kmeans = KMeans(n_clusters=num_colors, random_state=42)
            kmeans.fit(img_array)
            
            colors = kmeans.cluster_centers_.astype(int)
            labels = kmeans.labels_
            
            # Calculate color frequencies
            color_counts = np.bincount(labels)
            color_frequencies = color_counts / len(labels)
            
            # Create color list with frequencies
            dominant_colors = []
            for i, color in enumerate(colors):
                dominant_colors.append({
                    "rgb": color.tolist(),
                    "hex": f"#{color[0]:02x}{color[1]:02x}{color[2]:02x}",
                    "frequency": float(color_frequencies[i])
                })
            
            # Sort by frequency
            dominant_colors.sort(key=lambda x: x["frequency"], reverse=True)
            
            return dominant_colors
            
        except Exception as e:
            logger.error(f"Color extraction failed: {e}")
            return []
    
    async def create_thumbnail(self, image_path: str, size: Tuple[int, int] = (300, 300)) -> str:
        """
        Create thumbnail of the image
        """
        try:
            image = Image.open(image_path)
            image.thumbnail(size, Image.Resampling.LANCZOS)
            
            # Save thumbnail
            thumbnail_path = image_path.replace('.', f'_thumb_{size[0]}x{size[1]}.')
            image.save(thumbnail_path, quality=85)
            
            return thumbnail_path
            
        except Exception as e:
            logger.error(f"Thumbnail creation failed: {e}")
            return image_path
    
    async def validate_image(self, image_path: str) -> Dict[str, Any]:
        """
        Validate image for virtual try-on requirements
        """
        try:
            image = Image.open(image_path)
            
            # Check image dimensions
            width, height = image.size
            min_dimension = 512
            max_dimension = 4096
            
            # Check file size (assuming it's already loaded)
            file_size = len(open(image_path, 'rb').read())
            max_file_size = 10 * 1024 * 1024  # 10MB
            
            validation_result = {
                "is_valid": True,
                "errors": [],
                "warnings": [],
                "dimensions": {"width": width, "height": height},
                "file_size": file_size,
                "format": image.format
            }
            
            # Validate dimensions
            if width < min_dimension or height < min_dimension:
                validation_result["is_valid"] = False
                validation_result["errors"].append(f"Image too small. Minimum size: {min_dimension}x{min_dimension}")
            
            if width > max_dimension or height > max_dimension:
                validation_result["warnings"].append(f"Image very large. Maximum recommended: {max_dimension}x{max_dimension}")
            
            # Validate file size
            if file_size > max_file_size:
                validation_result["is_valid"] = False
                validation_result["errors"].append(f"File too large. Maximum size: {max_file_size / (1024*1024):.1f}MB")
            
            # Validate format
            if image.format not in ['JPEG', 'PNG', 'WEBP']:
                validation_result["is_valid"] = False
                validation_result["errors"].append("Unsupported format. Use JPEG, PNG, or WEBP")
            
            return validation_result
            
        except Exception as e:
            logger.error(f"Image validation failed: {e}")
            return {
                "is_valid": False,
                "errors": [f"Image validation failed: {str(e)}"],
                "warnings": [],
                "dimensions": {"width": 0, "height": 0},
                "file_size": 0,
                "format": None
            }
    
    async def _enhance_image_quality(self, image: Image.Image) -> Image.Image:
        """
        Enhance image quality using various techniques
        """
        try:
            # Enhance contrast
            enhancer = ImageEnhance.Contrast(image)
            image = enhancer.enhance(1.1)
            
            # Enhance sharpness
            enhancer = ImageEnhance.Sharpness(image)
            image = enhancer.enhance(1.1)
            
            # Enhance color
            enhancer = ImageEnhance.Color(image)
            image = enhancer.enhance(1.05)
            
            return image
            
        except Exception as e:
            logger.error(f"Image quality enhancement failed: {e}")
            return image
