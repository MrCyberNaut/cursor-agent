# AR Business Card Assets

This folder contains all the assets required for the AR business card experience.

## Required Files

### 1. Business Card Marker
- **File**: `business-card-marker.mind`
- **Description**: MindAR marker file generated from your business card image
- **How to create**: 
  1. Take a high-resolution photo of your business card (at least 1200x800px)
  2. Go to [MindAR Image Target Compiler](https://hiukim.github.io/mind-ar-js-doc/tools/compile)
  3. Upload your business card image
  4. Download the generated `.mind` file
  5. Rename it to `business-card-marker.mind`

### 2. 3D Caricature Model
- **File**: `caricature.glb`
- **Description**: 3D model of yourself/the person on the business card
- **Requirements**:
  - Format: `.glb` (optimized for web)
  - Polygon count: < 10,000 triangles
  - File size: < 2MB
  - Include textures baked into the model
- **Tools to create**:
  - [Ready Player Me](https://readyplayer.me/) - Easy avatar creation
  - Blender - Custom modeling
  - [VRoid Studio](https://vroid.com/en/studio) - Anime-style characters

### 3. Isometric Room Model
- **File**: `isometric-room.glb`
- **Description**: 3D isometric room scene for background
- **Requirements**:
  - Format: `.glb`
  - Polygon count: < 15,000 triangles
  - File size: < 3MB
  - Isometric perspective optimized
- **Tools to create**:
  - Blender with isometric camera setup
  - [Sketchfab](https://sketchfab.com/) - Download free models
  - [Poly Pizza](https://poly.pizza/) - Low-poly assets

## Asset Optimization Tips

### For Blender Users:
1. **Decimation**: Use the Decimate modifier to reduce polygon count
2. **Texture Baking**: Bake complex materials into simple diffuse textures
3. **LOD (Level of Detail)**: Create simplified versions for mobile devices
4. **Export Settings**:
   - Format: glTF 2.0 (.glb)
   - Include: Selected Objects
   - Transform: +Y Up
   - Geometry: Apply Modifiers
   - Materials: Export

### Compression Tools:
- [glTF-Pipeline](https://github.com/CesiumGS/gltf-pipeline)
- [gltf-transform](https://gltf-transform.donmccurdy.com/)
- [Basis Universal](https://github.com/BinomialLLC/basis_universal) for texture compression

## Current Asset Status

- ❌ `business-card-marker.mind` - **Required**: Create from your business card
- ❌ `caricature.glb` - **Required**: Your 3D avatar
- ❌ `isometric-room.glb` - **Optional**: 3D room scene (will be hidden on low-performance devices)

## Testing Your Assets

1. Place all files in this `assets/` folder
2. Test the AR experience on multiple devices
3. Check performance with the FPS counter
4. Optimize if frame rate drops below 20 FPS

## Asset Licensing

Ensure all 3D models and textures you use have appropriate licenses for your intended use (personal/commercial).