import React, { useRef } from "react";
import { Canvas, useFrame } from "@react-three/fiber";
import { Box } from "@react-three/drei";
import "./styles.css";

function RotatingCube() {
  // Define a reference to the cube mesh
  const mesh = useRef();

  // Use the useFrame hook to animate the cube
  useFrame(() => {
    // Rotate the cube on its x and y axes
    mesh.current.rotation.x += 0.01;
    mesh.current.rotation.y += 0.01;
  });

  return (
    <Box ref={mesh} scale={[1, 1, 1]}>
      {/* Set any additional properties for the Box component */}
      <meshStandardMaterial color="orange" />
    </Box>
  );
}

export default function App() {
  return (
    <Canvas>
      <ambientLight />
      <pointLight position={[10, 10, 10]} />
      <RotatingCube />
    </Canvas>
  );
}
